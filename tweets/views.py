import random

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

#Checks that the URL is safe. Included in settings
from django.utils.http import is_safe_url
#Imports settings, than assign ALLOWED_HOSTS down below
from django.conf import settings

#Django Rest Framework
from tweets.serializers import(
 TweetSerializer, 
 TweetActionSerializer,
 TweetCreateSerializer
)
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated


from .models import Tweet

from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    #return HttpResponse(f"<h1>Hello World</h1>")

    #Templates, status defaults to 200 
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['POST']) # http method the client has to send == POST
@permission_classes([IsAuthenticated]) # Only gives access to user if they are authenticated
@authentication_classes([SessionAuthentication])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data= request.POST)
    print(serializer)
    # raise_exception = True, so you don't have to pass the exception in to the Reponse like w JSONRespnse
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)

    return Response(serializer.data)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated]) 
def tweet_delete_view(request, tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id) #Finds the tweet
    if not qs.exists():
        return Response({}, status=404)

    qs = qs.filter(user=request.user) #Checks that the Tweet belongs to the user trying to delete it
    if not qs.exists():
        return Response({'messgae': 'You cannot delete this Tweet'}, status=401)
    obj = qs.first()
    obj.delete()

    return Response({"message": "Tweet removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def tweet_action_view(request,*args, **kwargs):
    #print(request.POST, request.data)
    '''
    id is required
    Actions options: like, unlike, retweet
    '''
    serializer =  TweetActionSerializer(data= request.data)

    if serializer.is_valid(raise_exception=True):
        data = serializer._validated_data
        print("data ", data)
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        print("next", action, content)
        qs = Tweet.objects.filter(id=tweet_id)
        print("first", qs.first())
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()

        if action == "like":
            print(obj)
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action == "retweet":
            new_tweet = Tweet.objects.create(
                user=request.user,
                 parent=obj,
                 content=content)
            #todo
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)

    return Response({}, status=200)


# Pure Django
def tweet_create_view_pure_django(request, *args, **kwargs):
    print("reached")
    user = request.user
    # Checks if user session is active
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    # TweetForm class can be initialized with data or not 
    form = TweetForm(request.POST or None)
    # Gets the value of the input field name=next
    next_url = request.POST.get("next") or None
    print('post data is', request.POST)
    #If the form is valid it saves it, otherwise returns the form
    if form.is_valid():
        
        obj = form.save(commit=False)
        obj.user = user
        #You can do other form related logic in here
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
        #And then reinitialize a new blank form
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

#Uses the django form, rewriting for the by-hand form
#def tweet_create_view(request, *args, **kwargs):
    # TweetForm class can be initialized with data or not 
    form = TweetForm(request.POST or None)
    print('post data is', request.POST)
    #If the form is valid it saves it, otherwise returns the form
    if form.is_valid():
        obj = form.save(commit=False)
        #You can do other form related logic in here
        obj.save()
        #And then reinitialize a new blank form
        form = TweetForm()
    return render(request, 'components/form.html', context={"form": form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all() #List
    #tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 122)} for x in qs] #List
    #Serialzie DMO
    tweets_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list, #List
        
    }

    return JsonResponse(data)#List



def tweet_detail_view_pure_django(request, tweet_id):
    """
    REST API VIEW
    Consume JS, SWIFT, Java, IOS/Android
    return json data
   """
    status = 200
    data={
        "id": tweet_id,
    }
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data['message'] = "Not found"
        #raise Http404
        status = 404
   
    return JsonResponse(data, status=status) #json.dumps content_type='application/json
    #status is an arguement option JsonResponse has, hover over JsonResponse

    #return HttpResponse(f"Hello {tweet_id} - {obj.content}")
