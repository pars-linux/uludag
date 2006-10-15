from django.shortcuts import render_to_response
from pardus.web.models import Pages
from django.http import HttpResponse

def index(request):
    return HttpResponse("Yes it will be web page of Pardus")

def detail(request, nice_title):
    page = Pages.objects.filter(NiceTitle=nice_title[:-1])
    if len(page.values()) > 0 :
        _page= page.values()
        _content = _page[0]['Content']
    else:
        _content = "<p> %s Not found.</p>" % nice_title

    return render_to_response('web/index.html',{'content':_content})
