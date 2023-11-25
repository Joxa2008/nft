from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm, LogInFroms, CreateNFT, CreateCollection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UserModel, NFT, NFTCollections, Block
from django.contrib.auth.views import login_required
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def main_view(request):
    if request.path != '/create_nft/':
        try:
            owner_user = UserModel.objects.select_related().get(username=request.user)
            is_auth = request.user.is_authenticated
            return {
                'user': owner_user,
                'is_auth': is_auth
            }
        except:
            return {
                'hello': 'hello'
            }
    return {'hello': 'hello'}


def home(request):
    return render(request, 'main.html')


def log_in(request):
    message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = 'Password or Username is incorrect'

    return render(request, 'log_in.html',
                  {'message': message})


def sign_up(request):
    profile_form = ProfileForm()
    form = UserForm()
    message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.username = user
            profile.save()
            return redirect('log_in')

    return render(request, 'sing_up.html', {'profile': profile_form, 'message': message})


def log_out(request):
    logout(request)
    return redirect('log_in')


@login_required(login_url='/log_in/')
def profile(request):
    user = UserModel.objects.get(username=request.user)
    if request.method == 'POST':
        if 'back-users' in request.FILES:
            user.back_img = request.FILES['back-users']
            user.save()
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            user.save()
        return redirect('profile')

    nft = reversed(NFT.objects.select_related().filter(owner=user))
    return render(request, 'profile.html', context={
        'nft': nft,
    })


def create_NFT(request):
    collection = NFTCollections.objects.filter(owner__username=request.user)
    form = CreateNFT()
    message = ''
    if request.method == 'POST':
        form = CreateNFT(request.POST, request.FILES)
        if form.is_valid():
            nft = form.save(commit=False)
            owner = UserModel.objects.get(username=request.user)
            nft.owner = owner
            nft_coll = NFTCollections.objects.get(collections_name=request.POST['collection'])
            nft.collection = nft_coll
            num = nft_coll.items + 1
            nft.nft_name = num
            nft.save()
            nft_coll.items = num
            nft_coll.save()
            block = Block(block_id=1, owner=owner, nft=nft, price=nft.price, previous_owner=owner)
            block.save()
            return redirect('profile')
        else:
            message = 'Img doesn\'t accept .avif format'

    return render(request, 'add_nft.html', context={
        'collections': collection,
        'message': message
    })


def create_collection(request):
    form = CreateCollection()
    if request.method == 'POST':
        form = CreateCollection(request.POST, request.FILES)
        if form.is_valid():
            coll = form.save(commit=False)
            coll.owner = UserModel.objects.get(username=request.user)
            coll.save()
            return redirect('nft')

    return render(request, 'create_collection.html')


def ditail(request, pk):
    nft = NFT.objects.select_related().get(id=pk)
    curs = float(nft.price) * 1000
    money_tr = reversed(Block.objects.select_related().filter(nft=nft))
    return render(request, 'ditail_page.html', context={
        'nft': nft,
        'curs': curs,
        'money_tr': money_tr
    })


@login_required(login_url='log_in')
def explore(request):
    nfts = request.GET.get('collection', '')
    nft_coll = ''
    nft = ''
    if nfts:
        nft_coll = NFTCollections.objects.select_related().filter(~Q(owner__username=request.user)).order_by('?')
    else:
        nft = NFT.objects.select_related().filter(~Q(owner__username=request.user)).order_by('?')

    return render(request, 'exlore.html', context={
        'nft': nft,
        'nft_coll': nft_coll
    })


def collection(request, pk):
    nft = NFT.objects.select_related().filter(collection_id=pk)
    collection = NFTCollections.objects.get(id=pk)
    return render(request, 'collection.html', context={
        'nft': nft,
        'collection': collection
    })


def buy_nft(request, pk):
    message = ''
    nft = NFT.objects.select_related().get(id=pk)
    buyer = UserModel.objects.get(username=request.user)
    owner = UserModel.objects.get(username__username=nft.owner)
    if request.method == 'POST':
        if buyer.current_balance >= nft.price:
            if int(request.POST['pin_code']) == int(buyer.card_pin):
                buyer.current_balance -= nft.price
                buyer.save()
                owner.current_balance += nft.price
                owner.save()
                nft.owner = buyer
                nft.save()
                block1 = Block.objects.filter(nft=nft).last()
                block = Block(block_id=int(block1.block_id) + 1, previous_owner=owner, owner=buyer, nft=nft,
                              price=nft.price)
                block.save()
                return redirect('profile')
            else:
                message = 'Password is incorrect!'
        else:
            message = 'You don\'t have anought money!'

    return render(request, 'buy_now.html', context={
        'i': nft,
        'message': message
    })


def error_404(request, exception):
    return render(request, '404.html')
