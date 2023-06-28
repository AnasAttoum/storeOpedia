from django.urls import path
from . import views

urlpatterns=[
    path( 'admin/Overview' , views.Overview , name='overview' ),

    path( 'users/signup' , views.signUpUsers , name='signUpUsers' ),
    path( 'owners/signup' , views.signUpOwners , name='signUpOwners' ),

    path( 'login' , views.login , name='logIn' ),

    path( '<int:userId>' , views.delete , name='delete' ),

    path( 'profile/<int:userId>' , views.edit , name='edit' ),


    path( 'AddStore/<int:userId>' , views.addStore , name='addStore' ),

    path( 'AddPost/<int:storeId>' , views.addPost , name='addPost' ),

    path( 'like/<int:userId>/<int:postId>' , views.likePost , name='likePost' ),

    path( 'fav/<int:userId>/<int:storeId>' , views.favStore , name='favStore' ),

    path( 'follow/<int:userId>/<int:storeId>' , views.followedStore , name='followedStore' ),

    path( 'follow/<int:userId>/<int:storeId>' , views.followedStore , name='followedStore' ),
    
    # path( 'shops' , views.lookupStores , name='lookupStores' ),
    path( 'shops/<int:userId>' , views.lookupStores , name='lookupStores' ),



    # path( 'admin2' , views.admin2 , name='admin2' ),
]