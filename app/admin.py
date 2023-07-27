from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import UserProfile , Store , Post ,Followed_Stores, Rated_Stores , Fav_Stores , Liked_Posts , User , Saved_Posts , Inbox

admin.site.unregister(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    # readonly_fields = ('id',)
    search_fields = ['username']
    list_filter = ('is_staff', 'is_superuser')
admin.site.register(User, CustomUserAdmin)

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id' , 'name' , 'description' , 'category' , 'opening' , 'closing', 'phone' , 'address' , 'facebook' , 'insta' , 'rate' , 'is_active', 'creation_date' , 'owner')
    search_fields = ['name','user']
    list_filter = ('category', 'address', 'rate','is_active')
    # fields = ['image_tag']
    readonly_fields = ['profile_photo_preview','cover_photo_preview']
    # readonly_fields = ['cover_photo_preview']
    # def profile_photo_image(self, obj):
    #     return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
    #         url = obj.profile_photo.url,
    #         width=obj.profile_photo.width,
    #         height=obj.profile_photo.height,
    #         )
    # )
    # def has_add_permission(self, request):
    #     if request.user.username=='admin':
    #         return True
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     # if request.user.username=='admin':
    #     #     return True
    #     return True
    
    # def has_delete_permission(self, request, obj=None):
    #     if request.user.username=='admin':
    #         return True
    #     return False
    
    # def has_view_permission(self, request, obj=None):
    #     # if request.user.username=='admin':
    #     #     return True
    #     return True
    
    # def get_queryset(self, request):
    #     qs = super( StoreAdmin , self ).get_queryset(request)
    #     if request.user.username=='admin':
    #         return qs
        
    #     # return super().get_queryset(request)
    #     userPro = UserProfile.objects.get(user_id=request.user.id)
    #     return qs.filter(owner=userPro)
    
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # is_superuser = request.user.is_superuser

    #     if request.user.username!='admin':
    #         form.base_fields['owner'].disabled = True
    #         form.base_fields['rate'].disabled = True
    #     return form
    
    # def get_readonly_fields(self, request, obj=None):
    #     if request.user.username!='admin':
    #         return ['creation_date']
    #     return self.readonly_fields
    
   
    # def get_ordering(self, request):
    #     return ['description']  # sort case insensitive
admin.site.register(Store , StoreAdmin)
# StoreAdmin.add_fieldsets = (
#     (None, {
#         # 'classes': ('wide',),
#         'fields': ('profile_photo_preview',)
#     }),
# )


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id' , 'title' , 'description' , 'creation_date' , 'price' , 'category' , 'photos' , 'owner')
    search_fields = ['title' , 'description']
    readonly_fields = ['post_photo_preview']
    list_filter = ('owner',)
admin.site.register(Post , PostAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id' , 'user' , 'phone' , 'address' , 'is_owner')
    search_fields = ['user']
    list_filter = ( 'is_owner', 'address')
admin.site.register(UserProfile , UserProfileAdmin)


class Liked_PostsAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id'  , 'user', 'post_id' , 'post')
admin.site.register(Liked_Posts , Liked_PostsAdmin)


class Fav_StoresAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id'  , 'user', 'store_id' , 'store')
admin.site.register(Fav_Stores , Fav_StoresAdmin)


class Followed_StoresAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id'  , 'user', 'store_id' , 'store')
admin.site.register(Followed_Stores , Followed_StoresAdmin)


class Rated_StoresAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id'  , 'user', 'store_id' , 'store' , 'value')
admin.site.register(Rated_Stores , Rated_StoresAdmin)

class Saved_PostsAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id'  , 'user', 'post_id' , 'post')
admin.site.register(Saved_Posts , Saved_PostsAdmin)

class InboxAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id' , 'type', 'description', 'photo', 'creation_date' , 'is_done' , 'reply' , 'reply_date')
    # readonly_fields = ('id',)
    search_fields = ['type' , 'description']
    list_filter = ('type', 'is_done')
admin.site.register(Inbox, InboxAdmin)