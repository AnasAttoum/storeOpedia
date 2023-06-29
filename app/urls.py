from django.urls import path
from . import views

urlpatterns=[
    path( 'admin/Overview' , views.Overview , name='overview' ),   #NOT DONE IN FLUTTER

    path( 'users/signup' , views.signUpUsers , name='signUpUsers' ),
    path( 'owners/signup' , views.signUpOwners , name='signUpOwners' ),

    path( 'login' , views.login , name='logIn' ),

    path( '<int:userId>' , views.delete , name='delete' ),  #NOT DONE IN FLUTTER

    path( 'profile/<int:userId>' , views.edit , name='edit' ),  #NOT DONE IN FLUTTER


    path( 'AddStore/<int:userId>' , views.addStore , name='addStore' ),  #NOT DONE IN FLUTTER

    path( 'AddPost/<int:storeId>' , views.addPost , name='addPost' ),   #NOT DONE IN FLUTTER

    path( 'like/<int:userId>/<int:postId>' , views.likePost , name='likePost' ),    #NOT DONE IN FLUTTER

    path( 'fav/<int:userId>/<int:storeId>' , views.favStore , name='favStore' ),    #NOT DONE IN FLUTTER

    path( 'follow/<int:userId>/<int:storeId>' , views.followedStore , name='followedStore' ),   #NOT DONE IN FLUTTER
    
    path( 'shops/<int:userId>' , views.lookupStores , name='lookupStores' ),

    




    # path( 'admin2' , views.admin2 , name='admin2' ),
]