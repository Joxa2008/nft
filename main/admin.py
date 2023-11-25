from django.contrib import admin
from .models import UserModel, NFTCollections, NFT, Block
# Register your models here.

admin.site.register(UserModel)
admin.site.register(NFTCollections)
admin.site.register(NFT)
admin.site.register(Block)
