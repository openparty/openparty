# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

from openparty.apps.twitter.models import Tweet

def index(request):
    tweets = Tweet.objects.order_by('-tweet_id')[:100]
    ctx = {'tweets': tweets}
    return render_to_response('twitter/index.html', ctx, context_instance=RequestContext(request))
