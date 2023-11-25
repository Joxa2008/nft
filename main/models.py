from django.db import models
from django.contrib.auth.models import User
import uuid
import hashlib


# Create your models here.

class UserModel(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='imgs/', default='default.jpeg')
    back_img = models.ImageField(upload_to='back/', default='default-back.png')
    card_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    card_pin = models.CharField(max_length=10)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.username}"


class NFTCollections(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    collections_img = models.ImageField(upload_to='coll_img/')
    collections_back = models.ImageField(upload_to='coll_back/')
    collections_name = models.CharField(max_length=50, unique=True)
    items = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'NFT Collection'
        verbose_name_plural = 'NFT Collections'


class NFT(models.Model):
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    collection = models.ForeignKey(NFTCollections, on_delete=models.CASCADE)
    nft_name = models.CharField(max_length=100)
    nft_img = models.ImageField(upload_to='nft/')
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'NFT'
        verbose_name_plural = 'NFT'


class Block(models.Model):
    block_id = models.PositiveIntegerField()
    previous_owner = models.ForeignKey(UserModel, on_delete=models.RESTRICT, related_name='boshqa_ega')
    owner = models.ForeignKey(UserModel, on_delete=models.RESTRICT)
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)

