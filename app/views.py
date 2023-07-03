from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile , Store , Post ,Liked_Posts ,Fav_Stores,Followed_Stores
import re
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import *
from django.contrib import auth
from datetime import datetime


def Overview(request):

    context = {
        'ownersNumber': len(UserProfile.objects.filter(is_owner = True)),
        'usersNumber': len(UserProfile.objects.filter(is_owner = False)),
        'ownerPercentage' : int(len(UserProfile.objects.filter(is_owner = True)) / len(UserProfile.objects.filter())*100),
        'usersPercentage' : 100 - int(len(UserProfile.objects.filter(is_owner = True)) / len(UserProfile.objects.filter())*100),
        'PostNumber' : len(Store.objects.all()),
        # 'TALL': 245,
        'Value1': 53,
        'Percentage1': (53*245)/100,
    }
    return render( request , 'Pages/Bar.html' , context)


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
        return JsonResponse({'message':"Access Denied"})
    

@api_view(['PUT'])
def edit(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    print('request.body :')
    print(request.body)
    
    id = body['id']
    userName = body['userName']
    email = body['email']
    password = body['password']
    phoneNumber = body['phoneNumber']

    if(int(id)==userId):
        user = User.objects.get(id=userId)
        userPro = UserProfile.objects.get(user_id=userId)
        user.username = userName
        userPro.phone = phoneNumber
        # print(user.username)
        user.save()
        userPro.save()
        # print(user.username)

        # auth.login(request, user)
        # print('end')
        return JsonResponse({'message' : 'User has been Updated successfully','user': {
                        'id' : str(user.id),
                        'userName': userName,
                        'email':user.email,
                        'phoneNumber' : str(userPro.phone),
                        'password':user.password
                    }})

    return JsonResponse({'message':"ERROR"})

# def admin2(request):
#     return render( request , 'login.html' )

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
            
            store = Store(owner=owner,name=name,description=description,category=category,
                        opening=opening,closing=closing,phone=phone,address=address,facebook=facebook,
                        insta=insta,profile_photo=profile_photo,cover_photo=cover_photo,
                        rate=rate)
            store.save()
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

        body_unicode = request.body.decode()
        body = json.loads(body_unicode)  
        
        id = body['id']
        title = body['title']
        description = body['description']
        price = body['price']
        photos = body['photos']

        if(int(id)==storeId):
            store=Store.objects.get(id=storeId)
            post = Post(title=title,description=description,price=price,photos=photos,owner=store)
            post.save()
            return JsonResponse({'message':"Your Post Have Been Added Successfully"}) 
        
@csrf_exempt
@api_view(['POST'])
def likePost(request,userId,postId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    if(int(id)==userId):
        userPro = UserProfile.objects.get(user_id=userId)
        post=Post.objects.get(id=postId)
        if(Liked_Posts.objects.filter(user=userPro,post=post).exists()):
            liked_post=Liked_Posts.objects.get(user=userPro,post=post)
            liked_post.delete()
            return JsonResponse({'message':"You unliked the post"})
        else:
            liked_post=Liked_Posts(user=userPro,post=post)
            liked_post.save()
            return JsonResponse({'message':"You liked the post"}) 
    
    return JsonResponse({'message':"Access Denied"}) 
    
@csrf_exempt
@api_view(['POST'])
def favStore(request,userId,storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    if(int(id)==userId):
        userPro = UserProfile.objects.get(user_id=userId)
        store=Store.objects.get(id=storeId)
        if(Fav_Stores.objects.filter(user=userPro,store=store).exists()):
            fav_store=Fav_Stores.objects.get(user=userPro,store=store)
            fav_store.delete()
            return JsonResponse({'message':"This store removed from your favourites"})
        else:
            fav_store=Fav_Stores(user=userPro,store=store)
            fav_store.save()
            return JsonResponse({'message':"This store added to your favourites"}) 
    
    return JsonResponse({'message':"Access Denied"}) 

@csrf_exempt
@api_view(['POST'])
def followedStore(request,userId,storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    if(int(id)==userId):
        userPro = UserProfile.objects.get(user_id=userId)
        store=Store.objects.get(id=storeId)
        if(Followed_Stores.objects.filter(user=userPro,store=store).exists()):
            followed_store=Followed_Stores.objects.get(user=userPro,store=store)
            followed_store.delete()
            return JsonResponse({'message':"You are unfollowing this store"}) 
        else:
            followed_store=Followed_Stores(user=userPro,store=store)
            followed_store.save()
            return JsonResponse({'message':"You are following this store"}) 
    
    return JsonResponse({'message':"Access Denied"}) 

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
                x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'url' , 'shopCoverImage':'url' , 'shopDescription':'desc' , 'socialUrl':'test' , 'rate':0 ,'followesNumber':0 },
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
def editPassword(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)  
    id = body['id']
    password = body['password']

    if(int(id)==userId):

        user = User.objects.get(id=userId)
        # if(password == user.password):
        if(user.check_password(password)):
            return JsonResponse({'message':'Matched'},status = 200)
        else:
            return JsonResponse({'message':'MisMatched'})

    else:
        return JsonResponse({'message':'Access Denied'})

