from django import forms
from django.contrib.auth.models import User
from .models import UserModel, NFT, NFTCollections
from django.core.exceptions import ValidationError


class ProfileForm(forms.ModelForm):
    class Meta:

        model = UserModel
        fields = ['card_pin']

    def clean_card_pin(self):
        int_version = 0
        try:
            int_version = int(self.cleaned_data['card_pin'])
        except Exception as err:
            raise ValidationError('Only integer acceptable')
        return self.cleaned_data['card_pin']


class CreateNFT(forms.ModelForm):
    class Meta:
        model = NFT
        fields = ['nft_img', 'price']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LogInFroms(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(max_length=30)


class CreateCollection(forms.ModelForm):
    class Meta:
        model = NFTCollections
        fields = ['collections_name', 'collections_img', 'collections_back']
