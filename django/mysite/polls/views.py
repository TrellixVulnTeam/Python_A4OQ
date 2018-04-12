from django.http import HttpResponse

def inde(request):
    return HttpResponse("Hello, world. You are at the polls index.")
