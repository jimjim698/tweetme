from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Tweet

def home_view(request, *args, **kwargs):
    #return HttpResponse(f"<h1>Hello World</h1>")

    #Templates, status defaults to 200 
    return render(request, "pages/home.html", context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all() #List
    tweets_list = [{"id": x.id, "content": x.content} for x in qs] #List
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
