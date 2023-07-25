from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.html import mark_safe



class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=10 , blank=True)
    address=models.CharField(default='',max_length=250 , blank=True)
    is_owner=models.BooleanField(default=0)
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural="User Profiles"
        verbose_name="User Profile"

    
class Store(models.Model):
    owner=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    name = models.CharField(max_length=50 , blank=True)
    description = models.CharField(max_length=150 , blank=True)
    category= models.CharField(max_length=20 , blank=True)
    opening=models.CharField(max_length=10 , blank=True)
    closing=models.CharField(max_length=10 , blank=True)
    phone = models.CharField(max_length=10 , blank=True)
    address=models.CharField(max_length=250 , blank=True)
    longitude=models.CharField(max_length=250 , blank=True)
    latitude=models.CharField(max_length=250 , blank=True)
    facebook=models.CharField(max_length=50 , blank=True)
    insta=models.CharField(max_length=50 , blank=True)
    profile_photo=models.ImageField(upload_to='photos/profiles/%Y/%m/%d/' , blank=True)
    cover_photo=models.ImageField(upload_to='photos/covers/%Y/%m/%d/' , blank=True)
    rate=models.FloatField( blank=True)
    is_active=models.BooleanField(default=1)
    creation_date=models.DateTimeField(default=datetime.now)
    fav=models.ManyToManyField(UserProfile,related_name="favourites",through="Fav_Stores")
    rated=models.ManyToManyField(UserProfile,related_name="rated",through="Rated_Stores")
    followed=models.ManyToManyField(UserProfile,related_name="followed",through="Followed_Stores")



    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Stores"
        verbose_name="Store"

    def profile_photo_preview(self):
            return mark_safe('<img src="{url}" width="150" height="150" />'.format(url=self.profile_photo.url))
    def cover_photo_preview(self):
            return mark_safe('<img src="{url}" width="150" height="150" />'.format(url=self.cover_photo.url))
    
class Post(models.Model):
    title=models.CharField(max_length=20 , blank=True)
    description = models.CharField(max_length=150 , blank=True)
    creation_date=models.DateTimeField(default=datetime.now)
    category= models.CharField(max_length=20,default='' , blank=True)
    price=models.FloatField(blank=True)
    photos=models.ImageField(null=True , blank=True ,upload_to='photos/posts/%Y/%m/%d/')
    like_posts=models.ManyToManyField(UserProfile,related_name="liked",through="Liked_Posts")
    save_posts=models.ManyToManyField(UserProfile,related_name="saved",through="Saved_Posts")
    owner = models.ForeignKey(Store, default=0 ,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural="Posts"
        verbose_name="Post"

    def post_photo_preview(self):
        return mark_safe('<img src="{url}" width="150" height="150" />'.format(url=self.photos.url))

class Followed_Stores(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    def __str__(self):
        return "Followed_Stores"
    
    class Meta:
        verbose_name_plural="Followed Stores"
        verbose_name="Followed Store"

class Rated_Stores(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    def __str__(self):
        return "Rated_Stores"
    class Meta:
        verbose_name_plural="Rated Stores"
        verbose_name="Rated Store"

class Fav_Stores(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    store=models.ForeignKey(Store,on_delete=models.CASCADE)
    def __str__(self):
        return "Fav_Stores"
    class Meta:
        verbose_name_plural="Favorite Stores"
        verbose_name="Favorite Store"
    
class Liked_Posts(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return self.post.title
    class Meta:
        verbose_name_plural="Liked Posts"
        verbose_name="Liked Post"

class Saved_Posts(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return self.post.title
    class Meta:
        verbose_name_plural="Saved Posts"
        verbose_name="Saved Post"


class Inbox(models.Model):
    owner=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    type= models.CharField(max_length=20 , blank=True)
    description = models.CharField(max_length=500 , blank=True)
    reply = models.CharField(max_length=500,default='' , blank=True)
    photo=models.ImageField(upload_to='photos/Inbox/%Y/%m/%d/' , blank=True)
    is_done=models.BooleanField(default=0)
    creation_date=models.DateTimeField(default=datetime.now)
    reply_date=models.DateTimeField(default=datetime.now)


    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural="Inboxes"
        verbose_name="inbox"
