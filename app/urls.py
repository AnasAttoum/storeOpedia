from django.urls import path
from . import views


urlpatterns=[

    path( 'admin/overview' , views.Overview , name='overview' ),   
    path( 'admin/inbox' , views.InboxesPage , name='inboxesPage' ),   
    path( 'delete/inbox/<int:inboxId>' , views.deleteInbox , name='deleteInbox' ),   
    path( 'done/inbox/<int:inboxId>' , views.doneInbox , name='doneInbox' ),   
    path( 'sendReply/inbox/<int:inboxId>' , views.replyInbox , name='replyInbox' ),   
    path( 'inbox/<int:userId>' , views.Inboxes , name='inboxes' ),   


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
    

    path( 'shops/<int:userId>' , views.lookupStores , name='lookupStores' ),
    

    path( 'show/stores/<int:userId>' , views.showStores , name='showStores' ), 
    path( 'show/posts/owner/<int:storeId>' , views.showPostsOwner , name='showPostsOwner' ), 
    path( 'show/posts/followedStores/<int:userId>' , views.postsofFollowedStore , name='postsofFollowedStore' ), 

    
    path( 'like/<int:userId>/<int:postId>' , views.likePost , name='likePost' ),   
    path( 'fav/<int:userId>/<int:storeId>' , views.favStore , name='favStore' ),    
    path( 'follow/<int:userId>/<int:storeId>' , views.followedStore , name='followedStore' ),



    # path( 'admin2' , views.admin2 , name='admin2' ),
]