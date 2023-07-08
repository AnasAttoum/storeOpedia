from django.urls import path
from . import views

urlpatterns=[
    path( 'admin/Overview' , views.Overview , name='overview' ),   #NOT DONE IN FLUTTER


    path( 'users/signup' , views.signUpUsers , name='signUpUsers' ),
    path( 'owners/signup' , views.signUpOwners , name='signUpOwners' ),


    path( 'login' , views.login , name='logIn' ),


    path( 'delete/<int:userId>' , views.delete , name='delete' ),  
    path( 'delete/store/<int:userId>' , views.deleteStore , name='deleteStore' ),  
    path( 'delete/post/<int:postId>' , views.deletePost , name='deletePost' ),   


    path( 'profile/<int:userId>' , views.edit , name='edit' ),
    path( 'profile/store/<int:userId>' , views.editStore , name='editStore' ),
    path( 'profile/post/<int:postId>' , views.editPost , name='editPost' ),
    path( 'verifyPassword/<int:userId>' , views.editPassword , name='editPassword' ),


    path( 'AddStore/<int:userId>' , views.addStore , name='addStore' ),  
    path( 'AddPost/<int:storeId>' , views.addPost , name='addPost' ),   


    path( 'like/<int:userId>/<int:postId>' , views.likePost , name='likePost' ),   

    path( 'fav/<int:userId>/<int:storeId>' , views.favStore , name='favStore' ),    
    path( 'follow/<int:userId>/<int:storeId>' , views.followedStore , name='followedStore' ),  
    
    path( 'shops/<int:userId>' , views.lookupStores , name='lookupStores' ),
    

    path( 'show/stores/<int:userId>' , views.showStores , name='showStores' ), 

    




    # path( 'admin2' , views.admin2 , name='admin2' ),
]