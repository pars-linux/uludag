from django.shortcuts import render_to_response


def showmainpage(request):

	return render_to_response("index.html", {"title":"General Knowledge"})