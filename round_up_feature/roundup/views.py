from django.shortcuts import render
from django.http import HttpResponse
from . import round_up
import datetime
# Create your views here.

def home(request):
    if(request.GET.get('mybtn')):
        yyyy_ww = request.GET.get('week')
        min_, max_ = helper(yyyy_ww)
        round_up.main(min_, max_)
    return render(request, 'main.html')

def formtimestamp(dt):
    timestamp = str(dt).split(' ')
    # Added seperators (T and Z in for timestamp)
    timestamp.insert(1, "T")
    timestamp.insert(3, ".000Z")
    return ''.join(timestamp)

def helper(yyyy_ww):
    # The -1 and -%w pattern tells the parser to pick the Monday in that week
    # https://stackoverflow.com/questions/17087314/get-date-from-week-number
    minTransactionDT = datetime.datetime.strptime(yyyy_ww + '-1', "%Y-W%W-%w")
    maxTransactionDT = minTransactionDT + datetime.timedelta(days=7)
    
    minTransactionTimestamp = formtimestamp(minTransactionDT)
    maxTransactionTimestamp = formtimestamp(maxTransactionDT)
    
    return minTransactionTimestamp, maxTransactionTimestamp