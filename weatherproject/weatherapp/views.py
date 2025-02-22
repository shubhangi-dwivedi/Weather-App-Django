from django.shortcuts import render, HttpResponse

#takes http request & return http response

def home(request):
    return HttpResponse('Hey this is my django server')