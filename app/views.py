from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile , Store , Post ,Liked_Posts ,Fav_Stores,Followed_Stores, Inbox , Saved_Posts , Rated_Stores
import re
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import *
from django.contrib import auth
from datetime import datetime
from django.db.models import Q

from django.core.mail import send_mail
from django.conf import settings

import base64
from django.core.files.base import ContentFile


def Overview(request):

    context = {
        'ownersNumber': len(UserProfile.objects.filter(is_owner = True)),
        'usersNumber': len(UserProfile.objects.filter(is_owner = False)),
        'ownerPercentage' : int(len(UserProfile.objects.filter(is_owner = True)) / len(UserProfile.objects.filter())*100),
        'usersPercentage' : 100 - int(len(UserProfile.objects.filter(is_owner = True)) / len(UserProfile.objects.filter())*100),
        'PostNumber' : len(Post.objects.all()),
        # 'TALL': 245,
        'Value1': 53,
        'Percentage1': (53*245)/100,
    }
    return render( request , 'Pages/Bar.html' , context)

def InboxesPage(request):
    inboxes = Inbox.objects.all()
    context={
        'inboxes': inboxes.order_by('-id')
    }
    return render( request , 'Pages/In.html',context)

def deleteInbox(request,inboxId):
    if request.user.is_superuser:
        Inbox.objects.get(id=inboxId).delete() 
        inboxes = Inbox.objects.all()
        context={
            'inboxes': inboxes.order_by('-id')
        }
        return render( request , 'Pages/In.html',context)
    
    else:
        return JsonResponse({'message':'Access Denied'}, status = 400)

def doneInbox(request,inboxId):
    if request.user.is_superuser:
        inbox = Inbox.objects.get(id=inboxId) 
        inbox.is_done=True
        inbox.save()
        inboxes = Inbox.objects.all()
        context={
            'inboxes': inboxes.order_by('-id')
        }
        return render( request , 'Pages/In.html',context)

    else:
        return JsonResponse({'message':'Access Denied'}, status = 400)
    

def replyInbox(request,inboxId):
    if request.user.is_superuser:
        inbox = Inbox.objects.get(id=inboxId) 
        recieve = inbox.owner.user.email
        send_mail(
            subject='About your message on Store Opedia Site',
            message=request.GET['message'],
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recieve],
            fail_silently=False
        )
        inbox.is_done=True
        inbox.reply=request.GET['message']
        inbox.reply_date = datetime.now()
        inbox.save()
        inboxes = Inbox.objects.all()
        context={
            'inboxes': inboxes.order_by('-id')
        }
        return render( request , 'Pages/In.html',context)

    else:
        return JsonResponse({'message':'Access Denied'}, status = 400)


@csrf_exempt
@api_view(['POST'])
def showInbox(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
        
    id = None

    id = body['id']

    if int(id) == userId:

        UserPro =UserProfile.objects.get(user_id = userId)
        inbox = Inbox.objects.filter(owner=UserPro)

        inb = []
        for i in range(0,len(inbox)):
            if inbox[i].reply:
                x = {
                'type':inbox[i].type , 
                'description': inbox[i].description , 
                'photo' : '' , 'creation_date':inbox[i].creation_date , 
                'reply':inbox[i].reply,
                'reply_date':inbox[i].reply_date
                },
            else:
                x = {
                    'type':inbox[i].type , 
                    'description': inbox[i].description , 
                    'photo' : '' , 'creation_date':inbox[i].creation_date 
                    },
            inb += x

        return JsonResponse({'message':'Done',
                             'inbox':inb
                             }, status = 200)
    
    return JsonResponse({'message':'Access Denied'}, status = 400)


@csrf_exempt
@api_view(['POST'])
def Inboxes(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
        
    id = None
    type = None
    description = None
    photo = None

    id = body['id']
    type = body['type']
    description = body['description']
    if photo:
        photo = body['photo']
    
    if int(id)==userId:
        userPro = UserProfile.objects.get(user_id = userId)
        inbox = Inbox( owner = userPro , type = type , description = description , photo = photo)
        inbox.save()
        return JsonResponse({'message':'Message sent successfuly. we will reply as soon as possible'}, status = 200)
    
    return JsonResponse({'message':'Access Denied'}, status = 400)


@csrf_exempt
@api_view(['POST'])
def signUpUsers(request):
    # print('request.method :')
    # request.method="POST"
    # print(request.method)
    
    # return JsonResponse({'result':'invalid'})
    # if request.method == 'POST':
    if request.method == 'POST':
       #VARIABLES FOR FIELDS
        
        userName= None
        email = None
        password= None
        phoneNumber = None
        
        # print('request :')
        # print(request)

        # print('request.body :')
        # print(request.body)
        
       #get values from form
        body_unicode = request.body.decode()
        # print('body_unicode :')
        # print(body_unicode)
        
        body = json.loads(body_unicode)  
        # print('request.body :')
        # print(request.body)
        
        userName = body['name'].lower()
        email = body['emil'].lower()
        password = body['password']
        phoneNumber = body['phoneNumber']

       #check values
        # print(phoneNumber)

        if userName and email and password and phoneNumber:
            if User.objects.filter(username=userName).exists():
                # print(body)
                # return HttpResponse('<h1>This Username is taken</h1>')
                return JsonResponse({'message':"UserName Already Exists"})

            else:#CHECK IF EMAIL IS TAKEN
                
                if User.objects.filter(email=email).exists():
                    # return HttpResponse('<h1>this email is taken</h1>')
                    return JsonResponse({'message':'Email Already Exists'})

                else:
                    patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                    if re.match(patt,email):
                    #add user
                        user = User.objects.create_user( username = userName , email = email , password = password )
                        user.save()
        
                    #add user profile
                        userProfile = UserProfile( user = user , phone = phoneNumber )
                        userProfile.save()
                        send_mail(
                            subject='Store Opedia Site',
                            message='Thank you for registering on our website..\n We hope you have a good time with us..',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[email],
                            fail_silently=False
                        )
                        return JsonResponse({'id':str(user.id) , 'userName':userName,'email':email,'password':password,'phoneNumber':phoneNumber,'message':'User was Created'}, status = 200)
                    else:
                        # return HttpResponse('<h1>invalid email</h1>')
                        return JsonResponse({'message':'Invalid email'})
    else :
        return JsonResponse({'message':'ERROR NOT POST'})
    # return HttpResponse('<h1>Done</h1>')


@csrf_exempt
@api_view(['POST'])
def signUpOwners(request):
    # print('request.method :')
    # request.method="POST"
    # print(request.method)
    
    # return JsonResponse({'result':'invalid'})
    # if request.method == 'POST':
    if request.method == 'POST':
       #VARIABLES FOR FIELDS
        
        userName= None
        email = None
        password= None
        phoneNumber = None

        name = None
        address = None
        category = None
        opening = None
        closing = None
        phone = None
        rate = 0
        
       #get values from form
        body_unicode = request.body.decode()
        
        body = json.loads(body_unicode)  

        userName = body['name'].lower()
        email = body['emil'].lower()
        password = body['password']
        phoneNumber = body['phoneNumber']

        name = body['storeName']
        address = body['storeLocation']
        category = body['storeCategory']
        opening = body['startWorkTime']
        closing = body['endWorkTime']
        phone = body['shopPhoneNumber']

       #check values
        # print(phoneNumber)
        # if opening=='':
        #     opening = '08:00:00'
        # if closing=='':
        #     closing = '20:00:00'
        if userName and email and password and phoneNumber and name and address and category and opening and closing and phone:
            if User.objects.filter(username=userName).exists():
                # print(body)
                # return HttpResponse('<h1>This Username is taken</h1>')
                return JsonResponse({'message':"UserName Already Exists"})

            else:#CHECK IF EMAIL IS TAKEN
                
                if User.objects.filter(email=email).exists():
                    # return HttpResponse('<h1>this email is taken</h1>')
                    return JsonResponse({'message':'Email Already Exists'})

                else:
                    patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                    if re.match(patt,email):
                    #add user
                        user = User.objects.create_user( username = userName , email = email , password = password )
                        user.save()
                        # print(datetime.strptime(opening))
                    #add user profile
                        userProfile = UserProfile( user = user , phone = phoneNumber , is_owner=True)
                        userProfile.save()
                        

                        store = Store(owner = userProfile , name = name , address = address , category = category, opening = opening , closing = closing , phone = phone , rate = rate)
                        store.save()
                        send_mail(
                            subject='Store Opedia Site',
                            message='Thank you for registering on our website..\n We hope you have a good time with us..',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[email],
                            fail_silently=False
                        )
                        # print('Store:')
                        # print(store.id)
                        # print(store.category)
                        # print(store.name)
                        # print(store.address)
                        # print(store.opening)
                        # print(store.closing)

                        # print('user')
                        # print(user.id)
                        # print(user.username)
                        # print(user.password)
                        # print(user.email)
                        # print(userProfile.phone)

                        # print('store')
                        # print(store.id)
                        # print(store.category)
                        # print(store.name)
                        # print(store.phone)
                        # print(store.address)
                        # print(store.opening)
                        # print(store.closing)
                        # print({ 'ownerID':str(user.id), 'ownerName':user.username , 'password': user.password , 'ownerEmail':user.email , 'ownerPhoneNumber':userProfile.phone ,
                        #                      'shopID':str(store.id) , 'shopCategory':store.category , 'shopName':store.name , 'shopPhoneNumber':store.phone , 'location':store.address , 'startWorkTime':store.opening , 'endWorkTime':store.closing , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 ,
                        #                       'message':'Owner was Created' })
                        return JsonResponse({ 'ownerID':str(user.id), 'ownerName':user.username , 'ownerEmail':user.email , 'ownerPhoneNumber':userProfile.phone ,
                                                'shopID':str(store.id) , 'shopCategory':store.category , 'shopName':store.name , 'shopPhoneNumber':store.phone , 'location':store.address , 'startWorkTime':store.opening , 'endWorkTime':store.closing , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 ,
                                                'message':'Owner was Created' },
                                                status = 201)
                        
                    else:
                        # return HttpResponse('<h1>invalid email</h1>')
                        return JsonResponse({'message':'Invalid email'})
        else:
            return JsonResponse({'message':'Invalid Values'})

    else :
        return JsonResponse({'message':'ERROR NOT POST'})
    # return HttpResponse('<h1>Done</h1>')


@csrf_exempt
@api_view(['POST'])
def login(request):

    if request.method == 'POST':

        body_unicode = request.body.decode()
        body = json.loads(body_unicode)  

        email = body['email'].lower()
        password = body['password']

        try:
            # print('try')
            if(User.objects.get(email = email) != None):
                # print('try')
                # s = User.objects.get(email=email , password=password)
                # print('try')
                user = User.objects.get(email=email)
                userPro = UserProfile.objects.get(user_id=user.id)
                userAuth = auth.authenticate(username=user.username , password=password)
                # print('test')
                if userAuth is not None :
                    auth.login(request,user)
                    # print('1')
                    if( userPro.is_owner ):
                        # print(userPro)
                        # store=Store.objects.filter(owner=userPro)
                        # store=list(Store.objects.filter(owner=userPro).values('name', 'description'))
                        # print('3')

                        # for (i=0 ; i<len(store) , i++):
                        #     print('hhh')
                        
                        # stores=[
                            
                        #         {'shopID':str(store[0].id) , 'ownerID':str(user.id) , 'email':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[0].category , 'shopName':store[0].name , 'shopPhoneNumber':store[0].phone , 'location':store[0].address , 'startWorkTime':str(store[0].opening) , 'endWorkTime':str(store[0].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 ,'followesNumber':0 },
                        #         {'shopID':str(store[1].id) , 'ownerID':str(user.id) , 'email':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone ,'shopCategory':store[1].category , 'shopName':store[1].name , 'shopPhoneNumber':store[1].phone , 'location':store[1].address , 'startWorkTime':str(store[1].opening) , 'endWorkTime':str(store[1].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 , 'followesNumber':0 },
                        #     ]
                        
                        # store = Store.objects.get(owner = userPro)
                        # return JsonResponse({
                        #     'ownerID':str(user.id), 'ownerName':user.username , 'ownerEmail':user.email , 'ownerPhoneNumber':userPro.phone ,
                        #     'shopID':str(store.id) , 'shopCategory':store.category , 'shopName':store.name , 'shopPhoneNumber':store.phone , 'location':store.address , 'startWorkTime':store.opening , 'endWorkTime':store.closing , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 ,
                        #     'message':'owner auth succeded'})
                        # print('yes')
                        # print('store')
                        # print(stores)
                        # print(store[0].id)
                        return JsonResponse({
                            'ownerID':str(user.id),
                            # 'followesNumber':0,
                            # 'shops': stores,
                            'message':'owner auth succeded',
                        },status = 200)
                    
                    else:
                        # print('else')
                        return JsonResponse({
                            'id' : str(user.id),
                            'userName': user.username,
                            'email':user.email,
                            'phoneNumber' : str(userPro.phone),
                            'message':'user auth succeded'}
                            ,status = 200)
                else:
                    return JsonResponse({'message':'Invalid Email Or Password'})
        except:
            # print('catch')
            return JsonResponse({'message':'Invalid Email Or Password'})


@csrf_exempt
@api_view(['DELETE'])
def delete(request , userId):
    # print('hhh')
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    # print(id)
    # print(userId)
    if(int(id)==userId):
        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=userId)
        # print('user:')
        # print(user)
        # print(request.user)
        
        user.delete()
        return JsonResponse({'message':" User has been deleted successfully"},status = 200)
    else:
        return JsonResponse({'message':"Access Denied"},status = 400)
    
@csrf_exempt
@api_view(['DELETE'])
def deleteStore(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    storeId = body['shopID']

    if(int(id)==userId):
        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=userId)
        if userPro.is_owner :
            if len(Store.objects.filter(owner=userPro))==1 :
                userPro.is_owner=False
                userPro.save()

            store = Store.objects.get(id=storeId)
            store.delete()
            return JsonResponse({'message':"Deleted Successfully"},status = 200)
        else:
            return JsonResponse({'message':"Access Denied"},status = 400) 
    else:
        return JsonResponse({'message':"Access Denied"},status = 400) 


@csrf_exempt
@api_view(['DELETE'])
def deletePost(request , postId):
    print('hi')
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    storeId = body['shopID']
    postID = body['postID']
    print('e')

    if(int(postID)==postId):
        # user = User.objects.get(id=id)
        userPro = UserProfile.objects.get(user_id=id)
        print('d')

        if userPro.is_owner:
            print('a')
            store = Store.objects.get(id = storeId)
            print('b')
            post = Post.objects.get(id = postId)
            print('c')
            
            if post.owner == store:
                post.delete()
                return JsonResponse({'message':"Deleted Successfully"},status = 200)
        else:
            return JsonResponse({'message':"Access Denied"},status = 400) 
    else:
        return JsonResponse({'message':"Access Denied"},status = 400) 




@api_view(['PUT'])
def edit(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    print('request.body :')
    print(request.body)
    
    id = body['id']
    userName = body['userName']
    # email = body['email']
    password = body['password']
    phoneNumber = body['phoneNumber']

    if(int(id)==userId):
        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=userId)
        
        if userName != user.username:
            if User.objects.filter(username=userName).exists():
                return JsonResponse({'message':"UserName Already Exists"})
            else:
                user.username = userName
                userPro.phone = phoneNumber
                if password:
                    user.set_password(password)
                # print(user.username)
                user.save()
                userPro.save()
                # print(user.username)
                auth.login(request, user)

                return JsonResponse({'message':"Done"},status = 200)
        else:
            userPro.phone = phoneNumber
            if password:
                user.set_password(password)
            # print(user.username)
            user.save()
            userPro.save()
            # print(user.username)
            auth.login(request, user)

            return JsonResponse({'message':"Done"},status = 200)
            
        # user.username = userName
        # userPro.phone = phoneNumber
        # # print(user.username)
        # user.save()
        # userPro.save()
        # # print(user.username)

        # auth.login(request, user)
        # print('end')
        # return JsonResponse({'message' : 'User has been Updated successfully','user': {
        #                 'id' : str(user.id),
        #                 'userName': userName,
        #                 'email':user.email,
        #                 'phoneNumber' : str(userPro.phone),
        #                 'password':user.password
        #             }})

    return JsonResponse({'message':"Access Denied"})


@api_view(['PUT'])
def editStore(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    
    id = body['id']
    storeId = body['shopID']

    profile_photo = body['shopProfileImage']
    cover_photo = body['shopCoverImage']
    name = body['shopName']
    description = body['shopDescription']
    phone = body['shopPhoneNumber']
    opening = body['startWorkTime']
    closing = body['endWorkTime']
    insta = body['insta']
    facebook = body['facebook']
    address = body['location']
    category = body['shopCategory']

    if int(id)==userId :
        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=userId)

        if userPro.is_owner:  
            store = Store.objects.get(id=storeId)

            if store.owner == userPro:
                store.name =name
                store.description = description
                store.address = address
                store.category = category
                store.opening = opening
                store.closing = closing
                store.phone = phone
                store.profile_photo = profile_photo
                store.cover_photo = cover_photo
                store.insta = insta
                store.facebook = facebook
                store.save()
                return JsonResponse({'message' : 'Done'} , status = 200)
            else:
                return JsonResponse({'message' : 'you cant edit this store'} , status = 400)
        else:
            return JsonResponse({'message' : 'You dont have any store yet'} , status = 400)
    else:
        return JsonResponse({'message' : 'Access Denied'} , status = 400)


@api_view(['PUT'])
def editPost(request , postId):
    id = None
    title=None
    storeID=None
    postID=None
    description = None
    price=None
    photos=None

    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    
    id = body['id']
    storeId = body['shopID']
    postID = body['postID']
    title = body['name']
    description = body['description']
    price = body['price']
    photos = body['photos']

    if(int(postID)==postId):
        user = User.objects.get(id=id)
        userPro = UserProfile.objects.get(user_id=id)

        if userPro.is_owner :
            store=Store.objects.get(id=storeId)

            if store.owner == userPro:
                post = Post.objects.get(id=postId)

                if post.owner == store:
                    if title: post.title = title

                    if description: post.description = description

                    if price: post.price = price

                    if photos: post.photos = photos

                    post.save()
                    return JsonResponse({'message':"Your Post Have Been Edit Successfully"},status = 200) 
                
                else:
                    return JsonResponse({'message':"You are not the owner of this post"},status = 400) 
            else:
                return JsonResponse({'message':"You can not edit the post because you do not owner the store that the post belong to it"},status = 400)
        else:
            return JsonResponse({'message':"Access Denied"},status = 400)
    else:
        return JsonResponse({'message':"Access Denied"},status = 400)
    

@csrf_exempt
@api_view(['POST'])
def editPassword(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    password = body['password']

    if(int(id)==userId):

        user = User.objects.get(id=userId)
        # if(password == user.password):
        if(user.check_password(password)):
            # print('Matched')
            return JsonResponse({'message':'Matched'},status = 200)
        else:
            # print('MisMatched')
            return JsonResponse({'message':'MisMatched'},status = 400)

    else:
        return JsonResponse({'message':'Access Denied'},status = 400)



@csrf_exempt
@api_view(['POST'])
def addStore(request , userId):
    if request.method == 'POST':
        owner=None
        name = None
        description = None
        category= None
        opening=None
        closing=None
        phone = None
        address=None
        facebook=None
        insta=None
        profile_photo=None
        cover_photo=None
        rate=None

        body_unicode = request.body.decode()
        body = json.loads(body_unicode)  
        id = body['id']
        if(int(id)==userId):
            user2=UserProfile.objects.get(user_id=userId)
            
            owner = user2
            name = body['name']
            description = body['description']
            category = body['category']
            opening = body['opening']
            closing = body['closing']
            phone = body['phone']
            address = body['address']
            facebook = body['facebook']
            insta = body['insta']
            profile_photo = body['profile_photo']
            cover_photo = body['cover_photo']
            rate = body['rate']
            

            if Store.objects.filter(name=name).exists():
                return JsonResponse({'message':"This Name Already Exists"})
            print(facebook)
            print(insta)

            store = Store(owner=owner,name=name,description=description,category=category,
                        opening=opening,closing=closing,phone=phone,address=address,facebook=facebook,
                        insta=insta,profile_photo=profile_photo,cover_photo=cover_photo,
                        rate=rate)
            store.save()
            if user2.is_owner==False:
                user2.is_owner=True
                user2.save()
            return JsonResponse({'message':"Your Store Have Been Added Successfully"},status = 200)
        return JsonResponse({'message':"Access Denied"}) 
    


@csrf_exempt
@api_view(['POST'])
def addPost(request,storeId):
    if request.method == 'POST':
        id = None
        title=None
        description = None
        price=None
        photos=None
        category=None

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)  
        
        id = body['id']
        storeID = body['shopID']
        title = body['name']
        description = body['description']
        price = body['price']
        if photos:
            photos = body['photos']
            photos= ContentFile(base64.b64decode(photos),'name')
        category = body['category']

        if(int(storeID)==storeId):
            user = User.objects.get(id=id)
            userPro = UserProfile.objects.get(user_id=id)
            if userPro.is_owner :
                store=Store.objects.get(id=storeId)
                if store.owner == userPro:
                    post = Post(title=title,description=description,price=price,category=category,photos=photos,owner=store)
                    post.save()
                    # form = PostForm(request.POST, request.FILES)
                    # print('1')
                    # if form.is_valid():
                    #     print('2')
                    #     form.save()
                    return JsonResponse({'message':"Your Post Have Been Added Successfully"},status = 200) 
                
                else:
                    return JsonResponse({'message':"Access Denied1"},status = 400)
            else:
                return JsonResponse({'message':"Access Denied2"},status = 400)
        else:
            return JsonResponse({'message':"Access Denied3"},status = 400) 
        
        

@csrf_exempt
@api_view(['POST'])
def lookupStores(request , userId):
    # print('start')
    # print(userId)
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['ownerID']
    # print('bb')
    # print('1')
    if(int(id)==userId):
        # print('2')

        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=user.id)
        if(userPro.is_owner):
            store=Store.objects.filter(owner=userPro)

            # print('3')
            # stores1=[
            #         {'shopID':str(store[0].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[0].category , 'shopName':store[0].name , 'shopPhoneNumber':store[0].phone , 'location':store[0].address , 'startWorkTime':str(store[0].opening) , 'endWorkTime':str(store[0].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 ,'followesNumber':0 },
            #         {'shopID':str(store[1].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone ,'shopCategory':store[1].category , 'shopName':store[1].name , 'shopPhoneNumber':store[1].phone , 'location':store[1].address , 'startWorkTime':str(store[1].opening) , 'endWorkTime':str(store[1].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 , 'followesNumber':0 },
            #     ]
            # print(len(store))
            stores = []
            for i in range(0,len(store)):
                if store[i].is_active:
                    followNum = len(Followed_Stores.objects.filter(store = store[i]))
                    if store[i].facebook or store[i].insta:
                        socialUrl = [ store[i].facebook , store[i].insta ]
                    else:
                        socialUrl =[]
                    x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active},
                    stores += x
                # stores.append(x)
            # print(
            #     {
            #     'shops':stores,
            #     'message':"Succeed"}
            # )
            return JsonResponse({
                'shops':stores,
                'message':"Succeed"},status =200)
                
        else:
            # print('5')
            return JsonResponse({'message':"Access Denied"})
    else:
        # print('6')
        return JsonResponse({'message':"Access Denied"})


@csrf_exempt
@api_view(['POST'])
def followedStore(request,userId,storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    storeID = body['shopId']

    if(int(id)==userId and int(storeID)==storeId):
        userPro = UserProfile.objects.get(user_id=userId)
        store=Store.objects.get(id=storeId)
        if(Followed_Stores.objects.filter(user=userPro,store=store).exists()):
            followed_store=Followed_Stores.objects.get(user=userPro,store=store)
            followed_store.delete()
            return JsonResponse({'message':"You are unfollowing this store"}, status = 200) 
        else:
            followed_store=Followed_Stores(user=userPro,store=store)
            followed_store.save()
            return JsonResponse({'message':"You are following this store"}, status = 200) 
    
    return JsonResponse({'message':"Access Denied"}, status = 400)     
    
@csrf_exempt
@api_view(['POST'])
def favStore(request,userId,storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    storeID = body['shopId']

    if(int(id)==userId and int(storeID)==storeId):
        userPro = UserProfile.objects.get(user_id=userId)
        store=Store.objects.get(id=storeId)
        if(Fav_Stores.objects.filter(user=userPro,store=store).exists()):
            fav_store=Fav_Stores.objects.get(user=userPro,store=store)
            fav_store.delete()
            return JsonResponse({'message':"This store removed from your favourites"}, status = 200)
        else:
            fav_store=Fav_Stores(user=userPro,store=store)
            fav_store.save()
            return JsonResponse({'message':"This store added to your favourites"}, status = 200) 
    
    return JsonResponse({'message':"Access Denied"}, status = 400)


@csrf_exempt
@api_view(['POST'])
def likePost(request,userId,postId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    postID = body['postId']

    if(int(id)==userId and int(postID)==postId):
        userPro = UserProfile.objects.get(user_id=userId)
        post=Post.objects.get(id=postId)

        if(Liked_Posts.objects.filter(user=userPro,post=post).exists()):
            liked_post=Liked_Posts.objects.get(user=userPro,post=post)
            liked_post.delete()
            return JsonResponse({'message':"You unliked the post"}, status = 200)
        else:
            liked_post=Liked_Posts(user=userPro,post=post)
            liked_post.save()
            return JsonResponse({'message':"You liked the post"}, status = 200) 
    
    return JsonResponse({'message':"Access Denied"}, status = 400) 



@csrf_exempt
@api_view(['POST'])
def savePost(request,userId,postId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    postID = body['postID']

    if(int(id)==userId and int(postID)==postId):
        userPro = UserProfile.objects.get(user_id=userId)
        post=Post.objects.get(id=postId)
        if(Saved_Posts.objects.filter(user=userPro,post=post).exists()):
            savePost=Saved_Posts.objects.get(user=userPro,post=post)
            savePost.delete()
            return JsonResponse({'message':"This post removed from your favourites"}, status = 200)
        else:
            savePost=Saved_Posts(user=userPro,post=post)
            savePost.save()
            return JsonResponse({'message':"This post added to your favourites"}, status = 200) 
    
    return JsonResponse({'message':"Access Denied"}, status = 400)


@csrf_exempt
@api_view(['POST'])
def showStores(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']

    if(int(id)==userId):
        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=user.id)

        stores = []
        store=Store.objects.filter(~Q(owner=userPro))
        
        
        for i in range(0,len(store)):
            # print(store[i].owner.id)
            user =User.objects.get(id=store[i].owner.user_id)
            userPro =UserProfile.objects.get(id=store[i].owner.id)
            followNum = len(Followed_Stores.objects.filter(store = store[i]))
            if store[i].facebook or store[i].insta:
                socialUrl = [ store[i].facebook , store[i].insta ]
            else:
                socialUrl =[]
            x = {
                'shopID':str(store[i].id) ,
                'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone ,
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active },
            stores += x
        return JsonResponse({"stores":stores , 'message':'Done'},status = 200)


    else:
        return JsonResponse({'message':'Access Denied'},status = 400)
    
@csrf_exempt
@api_view(['POST'])
def showPostsOwner(request , storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode) 

    id = body['id']
    storeID = body['shopID']

    if(int(storeID)==storeId):
        # user = User.objects.get(id=id)
        userPro = UserProfile.objects.get(user_id=id)

        if userPro.is_owner:
            store = Store.objects.get(id=storeId)
            if store.owner == userPro:
                posts = []
                post=Post.objects.filter(owner=storeId)
                for i in range(0,len(post)):
                    
                    x = {
                        'postID':str(post[i].id),
                        'title':post[i].title,
                        'description':post[i].description,
                        'price':str(post[i].price),
                        'photos':str(post[i].photos)
                        },
                    posts += x
                return JsonResponse({"posts":posts , 'message':'Done'},status = 200)
            return JsonResponse({'message':'Access Denied'},status = 400)
        return JsonResponse({'message':'Access Denied'},status = 400)
            


    else:
        return JsonResponse({'message':'Access Denied'},status = 400)
    

@csrf_exempt
@api_view(['POST'])
def postsofFollowedStore(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode) 

    id = body['id']

    if(int(id)==userId):
        userPro = UserProfile.objects.get(user_id=id)

        if Followed_Stores.objects.filter(user = userPro):
            followedStore = Followed_Stores.objects.filter(user = userPro)
            posts = []

            for j in range(0,len(followedStore)):
                post=Post.objects.filter(owner=followedStore[j].store)
                for i in range(0,len(post)):
                    
                    x = {
                        'postID':str(post[i].id),
                        'title':post[i].title,
                        'description':post[i].description,
                        'price':str(post[i].price),
                        'photos':str(post[i].photos)
                        },
                    posts += x
            return JsonResponse({"posts":sorted(posts, key=lambda a: a["postID"],reverse=True) , 'message':'Done'},status = 200)
            
        return JsonResponse({'message':'You dont have any followed store yet'},status = 200)


    else:
        return JsonResponse({'message':'Access Denied'},status = 400)


@csrf_exempt
@api_view(['POST'])
def showMyFollowedStore(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']

    if int(id)==userId:
        userPro = UserProfile.objects.get(user_id=id)
        if Followed_Stores.objects.filter(user=userPro).exists():
            follows = []
            follow = Followed_Stores.objects.filter(user=userPro)
            for i in range(0,len(follow)):
                
                x = {
                    'store':str(follow[i].store),
                    },
                follows += x

            return JsonResponse({'message':"Done" , 'follow':follows} , status = 200) 
        return JsonResponse({'message':"You dont have any followed stores yet"} , status = 400) 
    return JsonResponse({'message':"Access Denied"} , status = 400) 


@csrf_exempt
@api_view(['POST'])
def showMyFavStore(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']

    if int(id)==userId:
        userPro = UserProfile.objects.get(user_id=id)
        if Fav_Stores.objects.filter(user=userPro).exists():
            favs = []
            fav = Fav_Stores.objects.filter(user=userPro)
            for i in range(0,len(fav)):
                
                x = {
                    'store':str(fav[i].store),
                    },
                favs += x

            return JsonResponse({'message':"Done" , 'favs':favs} , status = 200) 
        return JsonResponse({'message':"You dont have any favourite stores yet"} , status = 400) 
    return JsonResponse({'message':"Access Denied"} , status = 400) 


@csrf_exempt
@api_view(['POST'])
def toggleActivation(request,storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    storeID = body['shopId']
    if(int(storeID)==storeId):
        userPro = UserProfile.objects.get(user_id=id)
        store=Store.objects.get(id=storeId)
        if userPro.is_owner:
            if store.owner == userPro:
                if store.is_active:
                    if len(Store.objects.filter(owner=userPro,is_active=True))==1:
                        return JsonResponse({'message':"You cannot deactive because you MUST have at least one active store"} , status = 200)
                    store.is_active=False
                    store.save()
                    return JsonResponse({'message':"DeActivated Successfully"} , status = 200) 
                else:
                    store.is_active=True
                    store.save()
                    return JsonResponse({'message':"Activated Successfully"} , status = 200) 
        
            return JsonResponse({'message':"Access Denied"} , status = 400) 
        return JsonResponse({'message':"Access Denied"} , status = 400) 
    return JsonResponse({'message':"Access Denied"} , status = 400) 

@csrf_exempt
@api_view(['POST'])
def activation(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    message = body['message']

    if(int(id)==userId):
        userPro = UserProfile.objects.get(user_id=id)
        if userPro.is_owner:
            user = User.objects.get(id=id)
            store=Store.objects.filter(owner=userPro)
            stores = [] 

            if message=='active':
                for i in range(0,len(store)):
                    if store[i].is_active:
                        followNum = len(Followed_Stores.objects.filter(store = store[i]))
                        if store[i].facebook or store[i].insta:
                            socialUrl = [ store[i].facebook , store[i].insta ]
                        else:
                            socialUrl =[]
                        x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active},
                        stores += x

            elif message=='deactive':
                for i in range(0,len(store)):
                    if store[i].is_active==0:
                        followNum = len(Followed_Stores.objects.filter(store = store[i]))
                        if store[i].facebook or store[i].insta:
                            socialUrl = [ store[i].facebook , store[i].insta ]
                        else:
                            socialUrl =[]
                        x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active},
                        stores += x
            else:
                for i in range(0,len(store)):
                    followNum = len(Followed_Stores.objects.filter(store = store[i]))
                    if store[i].facebook or store[i].insta:
                        socialUrl = [ store[i].facebook , store[i].insta ]
                    else:
                        socialUrl =[]
                    x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active},
                    stores += x
            
                # stores.append(x)
            # print(
            #     {
            #     'shops':stores,
            #     'message':"Succeed"}
            # )
            return JsonResponse({
                'shops':stores,
                'message':"Succeed"},status =200)
            
        return JsonResponse({'message':"Access Denied"} , status = 400) 
    return JsonResponse({'message':"Access Denied"} , status = 400) 
