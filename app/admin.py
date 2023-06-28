from django.contrib import admin
from .models import UserProfile , Store , Post ,Followed_Stores, Rated_Stores , Fav_Stores , Liked_Posts , User

admin.site.unregister(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    # readonly_fields = ('id',)
    search_fields = ['username']
    list_filter = ('is_staff', 'is_superuser')
admin.site.register(User, CustomUserAdmin)

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'description' , 'category' , 'opening' , 'closing', 'phone' , 'address' , 'facebook' , 'insta' , 'rate' , 'creation_date' , 'owner')
    search_fields = ['name']
    search_fields = ['user']
    list_filter = ('category', 'address', 'rate')

    # def get_ordering(self, request):
    #     return ['description']  # sort case insensitive
admin.site.register(Store , StoreAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id' , 'title' , 'description' , 'creation_date' , 'price' , 'owner')
    search_fields = ['title' , 'description']
admin.site.register(Post , PostAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id' , 'user' , 'phone' , 'address' , 'is_owner')
    search_fields = ['user']
    list_filter = ( 'is_owner', 'address')
admin.site.register(UserProfile , UserProfileAdmin)


class Liked_PostsAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user' , 'post')
admin.site.register(Liked_Posts , Liked_PostsAdmin)


class Fav_StoresAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user' , 'store')
admin.site.register(Fav_Stores , Fav_StoresAdmin)


class Followed_StoresAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user' , 'store')
admin.site.register(Followed_Stores , Followed_StoresAdmin)


class Rated_StoresAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user' , 'store')
admin.site.register(Rated_Stores , Rated_StoresAdmin)