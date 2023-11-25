from django.urls import path
from .views import home, log_in, sign_up, profile, log_out, create_NFT, create_collection, ditail, explore, collection, \
    buy_nft

urlpatterns = [
    path('', home, name='home'),
    path('ditail/<int:pk>', ditail, name='ditail'),
    path('log_in/', log_in, name='log_in'),
    path('sign_up/', sign_up, name='sign_up'),
    path('profile/', profile, name='profile'),
    path('log_out/', log_out, name='log_out'),
    path('create_nft/', create_NFT, name='nft'),
    path('create_collection/', create_collection, name='create_collection'),
    path('explore/', explore, name='explore'),
    path('collection/<int:pk>', collection, name='collection'),
    path('buy_nft/<int:pk>', buy_nft, name='buy_nft')
]
