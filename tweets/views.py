import random

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Tweet

from .forms import TweetForm

def home_view(request, *args, **kwargs):
    #return HttpResponse(f"<h1>Hello World</h1>")

    #Templates, status defaults to 200 
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    # TweetForm class can be initialized with data or not 
    form = TweetForm(request.POST or None)
    # Gets the value of the input field name=next
    next_url = request.POST.get("next") or None
    print('post data is', request.POST)
    #If the form is valid it saves it, otherwise returns the form
    if form.is_valid():
        obj = form.save(commit=False)
        #You can do other form related logic in here
        obj.save()
        if next_url != None:
            return redirect(next_url)

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

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all() #List
    tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 122)} for x in qs] #List
    data = {
        "isUser": False,
        "response": tweets_list, #List
        
    }

    return JsonResponse(data)#List



def tweet_detail_view(request, tweet_id):
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
