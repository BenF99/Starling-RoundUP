from django.shortcuts import render
from django.http import HttpResponse
from . import round_up
# Create your views here.

def home(request):
    if(request.GET.get('mybtn')):
        round_up.main()
    return render(request, 'main.html')