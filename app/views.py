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


import os

from django.templatetags.static import static

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geopy.distance

def Overview(request):
    all = len(Store.objects.all())
    value1 = round((len(Store.objects.filter(category='Estates'))/all)*100,1)
    value2 = round((len(Store.objects.filter(category='Vehicles'))/all)*100,1)
    value3 = round((len(Store.objects.filter(category='Fashion & Beauty'))/all)*100,1)
    value4 = round((len(Store.objects.filter(category='Mobiles'))/all)*100,1)
    value5 = round((len(Store.objects.filter(category='Furniturs'))/all)*100,1)
    value6 = round((len(Store.objects.filter(category='Computers'))/all)*100,1)
    value7 = round((len(Store.objects.filter(category='Gifts'))/all)*100,1)
    value8 = round((len(Store.objects.filter(category='Babies stuff'))/all)*100,1)
    value9 = round((len(Store.objects.filter(category='Motorcycles'))/all)*100,1)
    value10 = round((len(Store.objects.filter(category='Sport'))/all)*100,1)
    value11 = round((len(Store.objects.filter(category='Pharmacies'))/all)*100,1)
    value12 = round((len(Store.objects.filter(category='Services'))/all)*100,1)
    value13 = round((len(Store.objects.filter(category='Variants'))/all)*100,1)
    value14 = round((len(Store.objects.filter(category='Malls'))/all)*100,1)
    # print((value3*245)/100)


    context = {
        'ownersNumber': len(UserProfile.objects.filter(is_owner = True)),
        'usersNumber': len(UserProfile.objects.filter(is_owner = False)),
        'ownerPercentage' : int(len(UserProfile.objects.filter(is_owner = True)) / len(UserProfile.objects.filter())*100),
        'usersPercentage' : 100 - int(len(UserProfile.objects.filter(is_owner = True)) / len(UserProfile.objects.filter())*100),
        'PostNumber' : len(Post.objects.all()),
        # 'TALL': 245,
        'Value1': value1,
        'Percentage1': (value1*245)/100,
        'Value2': value2,
        'Percentage2': (value2*245)/100,
        'Value3': value3,
        'Percentage3': (value3*245)/100,
        'Value4': value4,
        'Percentage4': (value4*245)/100,
        'Value5': value5,
        'Percentage5': (value5*245)/100,
        'Value6': value6,
        'Percentage6': (value6*245)/100,
        'Value7': value7,
        'Percentage7': (value7*245)/100,
        'Value8': value8,
        'Percentage8': (value8*245)/100,
        'Value9': value9,
        'Percentage9': (value9*245)/100,
        'Value10': value10,
        'Percentage10': (value10*245)/100,
        'Value11': value11,
        'Percentage11': (value11*245)/100,
        'Value12': value12,
        'Percentage12': (value12*245)/100,
        'Value13': value13,
        'Percentage13': (value13*245)/100,
        'Value14': value14,
        'Percentage14': (value14*245)/100,

        'Lattakia' : len(Store.objects.filter(address='Lattakia')),
        'Tartus' : len(Store.objects.filter(address='Tartus')),
        'Raqqah' : len(Store.objects.filter(address='Raqqah')),
        'Aleppo' : len(Store.objects.filter(address='Aleppo')),
        'Hamah' : len(Store.objects.filter(address='Hamah')),
        'Homs' : len(Store.objects.filter(address='Homs')),
        'Idlib' : len(Store.objects.filter(address='Idlib')),
        'Hasaka' : len(Store.objects.filter(address='Hasaka')),
        'DayrAlZawr' : len(Store.objects.filter(address='DayrAlZawr')),
        'AsSuwaydaa' : len(Store.objects.filter(address='AsSuwaydaa')),
        'Quneitra' : len(Store.objects.filter(address='Quneitra')),
        'Daraa' : len(Store.objects.filter(address='Daraa')),
        'Damascus' : len(Store.objects.filter(address='Damascus')),
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
        longitude=None
        latitude=None

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
        if body['longitude']:
                longitude = body['longitude']
                latitude = body['latitude']
                geolocator = Nominatim(user_agent="storeOpedia")
                loc = geolocator.reverse(str(latitude)+","+str(longitude) , timeout=None)
                if str(loc).rsplit(' ', 2)[1] == 'اللاذقية,':
                    address = 'Lattakia'
                elif str(loc).rsplit(' ', 2)[1] == 'طرطوس,':
                    address = 'Tartus'
                elif str(loc).rsplit(' ', 2)[1] == 'الرقة,':
                    address = 'Raqqah'
                elif str(loc).rsplit(' ', 2)[1] == 'حلب,':
                    address = 'Aleppo'
                elif str(loc).rsplit(' ', 2)[1] == 'حماة,':
                    address = 'Hamah'
                elif str(loc).rsplit(' ', 2)[1] == 'حمص,':
                    address = 'Homs'
                elif str(loc).rsplit(' ', 2)[1] == 'إدلب,':
                    address = 'Idlib'
                elif str(loc).rsplit(' ', 2)[1] == 'الحسكة,':
                    address = 'Hasaka'
                elif str(loc).rsplit(' ', 2)[1] == 'الزور,':
                    address = 'DayrAlZawr'
                elif str(loc).rsplit(' ', 2)[1] == 'السويداء,':
                    address = 'AsSuwaydaa'
                elif str(loc).rsplit(' ', 2)[1] == 'القنيطرة,':
                    address = 'Quneitra'
                elif str(loc).rsplit(' ', 2)[1] == 'درعا,':
                    address = 'Daraa'
                elif str(loc).rsplit(' ', 2)[1] == 'دمشق,':
                    address = 'Damascus'
                else:
                    address = 'other'
       #check values
        # print(phoneNumber)
        # if opening=='':
        #     opening = '08:00:00'
        # if closing=='':
        #     closing = '20:00:00'
        # print('1')
        if userName and email and password and phoneNumber and name and address and category and opening and closing and phone:
            # print('2')
            if User.objects.filter(username=userName).exists():
                # print(body)
                # return HttpResponse('<h1>This Username is taken</h1>')
                # print('6')
                return JsonResponse({'message':"UserName Already Exists"})

            else:#CHECK IF EMAIL IS TAKEN
                # print('7')
                if User.objects.filter(email=email).exists():
                    # return HttpResponse('<h1>this email is taken</h1>')
                    return JsonResponse({'message':'Email Already Exists'})

                else:
                    # print('5')
                    patt="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                    if re.match(patt,email):
                    #add user
                        user = User.objects.create_user( username = userName , email = email , password = password )
                        user.save()
                        # print(datetime.strptime(opening))
                    #add user profile
                        userProfile = UserProfile( user = user , phone = phoneNumber , is_owner=True)
                        userProfile.save()


                        store = Store(owner = userProfile , name = name , address = address , category = category, opening = opening , closing = closing , phone = phone , rate = rate , longitude = float(longitude) , latitude = float(latitude))

                        # print('3')
                        store.profile_photo = static('Pic/profile_photo.jpg')
                        store.cover_photo = static('Pic/cover_photo.jpg')
                        # print('4')
                        store.save()
                        send_mail(
                            subject='Store Opedia Site',
                            message='Thank you for registering on our website..\n We hope you have a good time with us..',
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[email],
                            fail_silently=False
                        )
                        return JsonResponse({ 'ownerID':str(user.id), 'ownerName':user.username , 'ownerEmail':user.email , 'ownerPhoneNumber':userProfile.phone ,
                                                'shopID':str(store.id) , 'shopCategory':store.category , 'shopName':store.name , 'shopPhoneNumber':store.phone , 'location':store.address , 'startWorkTime':store.opening , 'endWorkTime':store.closing , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store.profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store.cover_photo.url)) , 'shopDescription':'desc' , 'socialUrl':[] , 'rate':0.0 , 'is_active':True,
                                                'longitude' : store.longitude, "latitude":store.latitude,
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
    print('START')
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)

    id = body['id']
    storeId = body['shopID']

    name = body['shopName']
    description = body['shopDescription']
    phone = body['shopPhoneNumber']
    opening = body['startWorkTime']
    closing = body['endWorkTime']
    insta = body['insta']
    facebook = body['facebook']
    address = body['location']
    category = body['shopCategory']
    if body['profile_photo']:
        profile_photo = body['profile_photo']
        typeProfile = body['storeProfileImageType']
    if body['cover_photo']:
        cover_photo = body['cover_photo']
        typeCover = body['storeCoverImageType']

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
                store.insta = insta
                store.facebook = facebook

                if body['profile_photo']:
                    profile_photo= ContentFile(base64.b64decode(profile_photo),name =str(store.id)+ '.' + typeProfile )
                    store.profile_photo=profile_photo
                if body['cover_photo']:
                    cover_photo= ContentFile(base64.b64decode(cover_photo),name =str(store.id)+ '.' + typeCover )
                    store.cover_photo=cover_photo
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
    storeId=None
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
    # photos = body['photos']
    if body['photos']:
        photos = body['photos']
        type = body['postImageType']

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

                    if body['photos']:
                        photos= ContentFile(base64.b64decode(photos),name =str(post.id)+ '.' + type )
                        post.photos = photos

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
        longitude=None
        latitude=None

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
            rate = body['rate']
            if body['profile_photo'] != 'noImage':
                profile_photo = body['profile_photo']
                typeProfile = body['storeProfileImageType']
            if body['cover_photo'] != 'noImage':
                cover_photo = body['cover_photo']
                typeCover = body['storeCoverImageType']
            if body['longitude']:
                longitude = body['longitude']
                latitude = body['latitude']
                geolocator = Nominatim(user_agent="storeOpedia")
                # from geopy.point import Point
                # loc = geolocator.reverse(Point(latitude,longitude) , timeout=None)
                loc = geolocator.reverse(str(latitude)+","+str(longitude) , timeout=None)
                print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
                print(str(loc))
                if str(loc).rsplit(' ', 2)[1] == 'اللاذقية,':
                    address = 'Lattakia'
                elif str(loc).rsplit(' ', 2)[1] == 'طرطوس,':
                    address = 'Tartus'
                elif str(loc).rsplit(' ', 2)[1] == 'الرقة,':
                    address = 'Raqqah'
                elif str(loc).rsplit(' ', 2)[1] == 'حلب,':
                    address = 'Aleppo'
                elif str(loc).rsplit(' ', 2)[1] == 'حماة,':
                    address = 'Hamah'
                elif str(loc).rsplit(' ', 2)[1] == 'حمص,':
                    address = 'Homs'
                elif str(loc).rsplit(' ', 2)[1] == 'إدلب,':
                    address = 'Idlib'
                elif str(loc).rsplit(' ', 2)[1] == 'الحسكة,':
                    address = 'Hasaka'
                elif str(loc).rsplit(' ', 2)[1] == 'الزور,':
                    address = 'DayrAlZawr'
                elif str(loc).rsplit(' ', 2)[1] == 'السويداء,':
                    address = 'AsSuwaydaa'
                elif str(loc).rsplit(' ', 2)[1] == 'القنيطرة,':
                    address = 'Quneitra'
                elif str(loc).rsplit(' ', 2)[1] == 'درعا,':
                    address = 'Daraa'
                elif str(loc).rsplit(' ', 2)[1] == 'دمشق,':
                    address = 'Damascus'
                else:
                    address = 'other'


            if Store.objects.filter(name=name).exists():
                return JsonResponse({'message':"This Name Already Exists"})
            # print(facebook)
            # print(insta)

            store = Store(owner=owner,name=name,description=description,category=category,
                        opening=opening,closing=closing,phone=phone,address=address,facebook=facebook,
                        insta=insta,
                        # profile_photo=profile_photo,cover_photo=cover_photo,
                        longitude = longitude, latitude=latitude,
                        rate=rate)
            store.save()
            # print('test')
            # print(body['profile_photo'])
            # print(body['storeProfileImageType'])
            # print('end')

            if body['profile_photo'] != 'noImage':
                # print('yes')
                profile_photo= ContentFile(base64.b64decode(profile_photo), name =str(store.id)+ '.' + typeProfile )
                store.profile_photo=profile_photo
            else:
                # print('no')
                store.profile_photo = static('Pic/profile_photo.jpg')

            if body['cover_photo'] != 'noImage':
                cover_photo= ContentFile(base64.b64decode(cover_photo),name =str(store.id)+ '.' + typeCover )
                store.cover_photo=cover_photo
            else:
                # print('no')
                store.cover_photo = static('Pic/cover_photo.jpg')
            # if body['longitude']:
            #     store.longitude = longitude
            #     store.latitude = latitude
            store.save()
            if user2.is_owner == False:
                user2.is_owner = True
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
        type=None

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        id = body['id']
        storeID = body['shopID']
        title = body['name']
        description = body['description']
        price = body['price']
        # print('Startphotos')
        # print(body['photos'])
        if body['photos']:
            photos = body['photos']
            type = body['postImageType']

            # print('photos')
            # print(photos)

        category = body['category']

        if(int(storeID)==storeId):
            user = User.objects.get(id=id)
            userPro = UserProfile.objects.get(user_id=id)
            if userPro.is_owner :
                store=Store.objects.get(id=storeId)
                if store.owner == userPro:
                    post = Post(title=title,description=description,price=price,category=category,owner=store)
                    post.save()
                    if body['photos']:
                        photos= ContentFile(base64.b64decode(photos),name =str(post.id)+ '.' + type )
                    post.photos = photos
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
                    x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude},
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
    postID = body['postID']

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
        if int(id) == 0:
            store=Store.objects.all()
        else:
            user = User.objects.get(id=userId)
            userPro = UserProfile.objects.get(user_id=user.id)
            store=Store.objects.filter(~Q(owner=userPro))

        stores = []


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
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude,
                'isFollow': Followed_Stores.objects.filter(user = UserProfile.objects.get(user_id=userId) , store = store[i]).exists() 
                },
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
    print('id' in request.POST)
    print(request.POST)
    if(int(storeID)==storeId):
        # user = User.objects.get(id=id)
        userPro = UserProfile.objects.get(user_id=id)

        if userPro.is_owner:
            store = Store.objects.get(id=storeId)
            if store.owner == userPro:
                posts = []
                post=Post.objects.filter(owner=storeId)
                for i in range(0,len(post)):
                    # with open("media/photos/posts/2023/07/26/79.jpg", "rb") as photo:
                        # photoData = base64.b64encode(photo.read())
                    # ctx["image"] = photoData
                    # photo = base64.b64encode(post[i].photos.getvalue())
                    # print(str(post[i].photos.url))
                    x = {
                        'postID':str(post[i].id),
                        'title':post[i].title,
                        'description':post[i].description,
                        'price':str(post[i].price),
                        'photos':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(post[i].photos.url))
                        # 'photos':str(base64.b64encode(post[i].photos.read())),
                        # 'postImageType': str(post[i].photos).rsplit('.', 1)[1]
                        },
                    posts += x
                # print(posts)
                return JsonResponse({"posts":sorted(posts, key=lambda a: a["postID"],reverse=True) , 'message':'Done'},status = 200)
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
            # print('1')
            # print(len(followedStore))
            if len(followedStore) == 0:
                # print('yes')
                return JsonResponse({'message':'You dont have any followed store yet'},status = 200)

            for j in range(0,len(followedStore)):
                post=Post.objects.filter(owner=followedStore[j].store)
                # store=Store.objects.filter(id=followedStore[j].store.id)
                # user =User.objects.get(id=followedStore[j].store.owner.user_id)
                # userPro =UserProfile.objects.get(id=followedStore[j].store.owner.id)
                followNum = len(Followed_Stores.objects.filter(store = followedStore[j].store))
                if followedStore[j].store.facebook or followedStore[j].store.insta:
                    socialUrl = [ followedStore[j].store.facebook , followedStore[j].store.insta ]
                else:
                    socialUrl =[]
                # print(store)
                for i in range(0,len(post)):

                    x = {
                        'postID':str(post[i].id),
                        'title':post[i].title,
                        'description':post[i].description,
                        'price':str(post[i].price),
                        'photos':str(post[i].photos),
                        'shopID':str(post[i].owner.id) ,
                        'ownerID':str(post[i].owner.owner.user_id) , 'ownerEmail':post[i].owner.owner.user.email , 'ownerName':post[i].owner.owner.user.username ,'ownerPhoneNumber':post[i].owner.owner.phone ,
                        'shopCategory':post[i].owner.category , 'shopName':post[i].owner.name , 'shopPhoneNumber':post[i].owner.phone , 'location':post[i].owner.address ,
                        'startWorkTime':str(post[i].owner.opening) , 'endWorkTime':str(post[i].owner.closing) ,
                        'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(post[i].owner.profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(post[i].owner.cover_photo.url)) ,
                        'shopDescription':post[i].owner.description , 'socialUrl': socialUrl, 'rate':post[i].owner.rate ,'followesNumber':followNum , 'is_active':post[i].owner.is_active , 'longitude' : post[i].owner.longitude, "latitude":post[i].owner.latitude
                        },
                    
                    posts += x
            # print(posts)
            if len(posts) == 0:
                # print('yes')
                return JsonResponse({'message':'You dont have any post to show yet'},status = 200)
            return JsonResponse({"posts":sorted(posts, key=lambda a: a["postID"],reverse=True) , 'message':'Done'},status = 200)
        print('no')
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
                    'id':str(follow[i].store.id),
                    'name':str(follow[i].store),
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
                    'id':str(fav[i].store.id),
                    'name':str(fav[i].store),
                    },
                favs += x

            return JsonResponse({'message':"Done" , 'favs':favs} , status = 200)
        return JsonResponse({'message':"You dont have any favourite stores yet"} , status = 400)
    return JsonResponse({'message':"Access Denied"} , status = 400)


@csrf_exempt
@api_view(['POST'])
def showMyLikedPosts(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']

    if int(id)==userId:
        userPro = UserProfile.objects.get(user_id=id)
        if Liked_Posts.objects.filter(user=userPro).exists():
            likes = []
            like = Liked_Posts.objects.filter(user=userPro)
            for i in range(0,len(like)):

                x = {
                    'id':str(like[i].post.id),
                    'title':str(like[i].post),
                    },
                likes += x

            return JsonResponse({'message':"Done" , 'PostsLikedByMe':likes} , status = 200)
        return JsonResponse({'message':"You didnt like any post yet"} , status = 400)
    return JsonResponse({'message':"Access Denied"} , status = 400)


@csrf_exempt
@api_view(['POST'])
def showStoresFromCategories(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']
    cat = body['category']

    if int(id)==userId and cat:
        if int(id) == 0:
            store=Store.objects.all()
        else:
            user = User.objects.get(id=userId)
            userPro = UserProfile.objects.get(user_id=user.id)
            store=Store.objects.filter(~Q(owner=userPro) , category=cat)

        stores = []

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
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude,
                'isFollow': Followed_Stores.objects.filter(user = UserProfile.objects.get(user_id=userId) , store = store[i]).exists()
                },
            stores += x
        return JsonResponse({"stores":stores , 'message':'Done'},status = 200)

    else:
        return JsonResponse({'message':'Access Denied'},status = 400)


@csrf_exempt
@api_view(['POST'])
def filters(request,userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']
    type = body['type']

    if(int(id)==userId):
        if int(id) == 0:
            store=Store.objects.all()
        else:
            user = User.objects.get(id=userId)
            userPro = UserProfile.objects.get(user_id=user.id)
            if userPro.is_owner:
                store=Store.objects.filter(~Q(owner=userPro))
            else:
                store=Store.objects.all()

        stores = []

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
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude,
                 'isFollow': Followed_Stores.objects.filter(user = UserProfile.objects.get(user_id=userId) , store = store[i]).exists() },
            stores += x
        if type == 'rate':
            return JsonResponse({"stores":sorted(stores, key=lambda a: a["rate"],reverse=True) , 'message':'Done'},status = 200)
        elif type == 'new':
            return JsonResponse({"stores":sorted(stores, key=lambda a: a["shopID"],reverse=True) , 'message':'Done'},status = 200)
        elif type == 'old':
            return JsonResponse({"stores":sorted(stores, key=lambda a: a["shopID"],reverse=False) , 'message':'Done'},status = 200)
        else:
            return JsonResponse({'message':'STILL WORKING ON IT'},status = 200)


    else:
        return JsonResponse({'message':'Access Denied'},status = 400)


@csrf_exempt
@api_view(['POST'])
def nearestStores(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']
    longitude = body['longitude']
    latitude = body['latitude']
    c1 = (latitude,longitude)
    if int(id)==userId:
        if int(id) == 0:
            store=Store.objects.all()
            # print(len(store))
        else:
            user = User.objects.get(id=userId)
            userPro = UserProfile.objects.get(user_id=user.id)
            store=Store.objects.filter(~Q(owner=userPro))
        stores = []
        for i in range(0,len(store)):
            # print(store[i].owner.id)
            user =User.objects.get(id=store[i].owner.user_id)
            userPro =UserProfile.objects.get(id=store[i].owner.id)
            followNum = len(Followed_Stores.objects.filter(store = store[i]))
            if store[i].facebook or store[i].insta:
                socialUrl = [ store[i].facebook , store[i].insta ]
            else:
                socialUrl =[]
            c2=(store[i].latitude,store[i].longitude)
            x = {
                'shopID':str(store[i].id) ,
                'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone ,
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude,
                'isFollow': Followed_Stores.objects.filter(user = UserProfile.objects.get(user_id=userId) , store = store[i]).exists(),
                'distance':geopy.distance.geodesic(c1,c2).km
                },
            stores += x
        print(sorted(stores, key=lambda a: a['distance'],reverse=False))
        return JsonResponse({"stores":sorted(stores, key=lambda a: a['distance'],reverse=False) , 'message':'Done'},status = 200)

    else:
        return JsonResponse({'message':'Access Denied'},status = 400)



@csrf_exempt
@api_view(['POST'])
def filterLocation(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']
    address = body['address']

    if int(id)==userId:
        if int(id) == 0:
            store=Store.objects.filter(address = address)
        else:
            user = User.objects.get(id=userId)
            userPro = UserProfile.objects.get(user_id=user.id)
            store=Store.objects.filter(~Q(owner=userPro) , address = address)
        stores = []
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
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude,
                'isFollow': Followed_Stores.objects.filter(user = UserProfile.objects.get(user_id=userId) , store = store[i]).exists()
                },
            stores += x

        return JsonResponse({"stores":sorted(stores, key=lambda a: a['rate'],reverse=True) , 'message':'Done'},status = 200)

    else:
        return JsonResponse({'message':'Access Denied'},status = 400)




@csrf_exempt
@api_view(['POST'])
def searchStore(request , userId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']
    search = body['search']


    if int(id)==userId:
        if int(id) == 0:
            store=Store.objects.filter(name__icontains=search)
            # print(len(store))
        else:
            user = User.objects.get(id=userId)
            userPro = UserProfile.objects.get(user_id=user.id)
            store=Store.objects.filter(~Q(owner=userPro) , name__icontains=search)

        stores = []

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
                'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl': socialUrl, 'rate':store[i].rate ,'followesNumber':followNum , 'is_active':store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude,
                'isFollow': Followed_Stores.objects.filter(user = UserProfile.objects.get(user_id=userId) , store = store[i]).exists()},
            stores += x
        return JsonResponse({"stores":stores , 'message':'Done'},status = 200)

    else:
        return JsonResponse({'message':'Access Denied'},status = 400)


@csrf_exempt
@api_view(['POST'])
def rate(request,userId,storeId):
    body_unicode = request.body.decode()
    body = json.loads(body_unicode)
    id = body['id']
    storeID = body['shopID']
    value = body['value']

    if(int(id)==userId and int(storeID)==storeId):
        userPro = UserProfile.objects.get(user_id=userId)
        store=Store.objects.get(id=storeId)
        if store.owner != userPro:
            if Rated_Stores.objects.filter(user=userPro , store=store).exists():
                rate = Rated_Stores.objects.get(user=userPro , store=store)
                rate.value = value
                rate.save()
            else:
                rate = Rated_Stores(user=userPro , store=store , value=value)
                rate.save()

            allRates = Rated_Stores.objects.all()
            num = len(allRates)
            rate=0.0
            for i in range(0,num):
                rate+=allRates[i].value
            rate=rate/num
            store.rate = rate
            store.save()
            return JsonResponse({'message':'Done', 'newRate':rate , 'ratingNumber':num},status = 200)
        else:
            return JsonResponse({'message':'You cannot rate your store'},status = 400)
    return JsonResponse({'message':'Access Denied'},status = 400)

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
                        x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':float(store[i].rate) ,'followesNumber':followNum , "is_active" :store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude},
                        stores += x

            elif message=='deactive':
                for i in range(0,len(store)):
                    if store[i].is_active==0:
                        followNum = len(Followed_Stores.objects.filter(store = store[i]))
                        if store[i].facebook or store[i].insta:
                            socialUrl = [ store[i].facebook , store[i].insta ]
                        else:
                            socialUrl =[]
                        x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude},
                        stores += x
            else:
                for i in range(0,len(store)):
                    followNum = len(Followed_Stores.objects.filter(store = store[i]))
                    if store[i].facebook or store[i].insta:
                        socialUrl = [ store[i].facebook , store[i].insta ]
                    else:
                        socialUrl =[]
                    x = {'shopID':str(store[i].id) , 'ownerID':str(user.id) , 'ownerEmail':user.email , 'ownerName':user.username ,'ownerPhoneNumber':userPro.phone , 'shopCategory':store[i].category , 'shopName':store[i].name , 'shopPhoneNumber':store[i].phone , 'location':store[i].address , 'startWorkTime':str(store[i].opening) , 'endWorkTime':str(store[i].closing) , 'shopProfileImage':'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].profile_photo.url)) , 'shopCoverImage': 'http://anasattoum2023.pythonanywhere.com/' + str(os.path.abspath(store[i].cover_photo.url)) , 'shopDescription':store[i].description , 'socialUrl':socialUrl , 'rate':store[i].rate ,'followesNumber':followNum , "is_active" :store[i].is_active , 'longitude' : store[i].longitude, "latitude":store[i].latitude},
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
