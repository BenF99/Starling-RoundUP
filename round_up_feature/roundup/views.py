from django.shortcuts import render
from django.http import HttpResponse
from . import round_up
import datetime
# Create your views here.


def home(request):
    """Home view for HTML template

    Args:
        request (HTTP request): response from web server

    Returns:
        render: HTML template with values filled
    """
    context = {  # Context to be SENT to template
        'savings': 0.0  # Set to 0.0 until butten pressed
    }
    if(request.GET.get('mybtn')):
        yyyy_ww = request.GET.get('week')  # Gets week selected
        min_, max_ = helper(yyyy_ww)  # Retrieves min and max dates
        # Value overwritten once btn pressed
        context['savings'] = round_up.main(min_, max_)
    return render(request, 'main.html', context)


def formtimestamp(dt):
    """Creates timestamp from datetime

    Args:
        dt (datetime): datetime obj

    Returns:
        String: timestamp containing T and Z (required by API)
    """
    timestamp = str(dt).split(' ')
    # * Added seperators (T and Z in for timestamp)
    timestamp.insert(1, "T")
    timestamp.insert(3, ".000Z")
    return ''.join(timestamp)


def helper(yyyy_ww):
    """Formats HTML date

    Args:
        yyyy_ww (String): year_weak

    Returns:
        String, String: Min and max dates to retrieve savings
    """
    # The -1 and -%w pattern tells the parser to pick the Monday in that week
    # https://stackoverflow.com/questions/17087314/get-date-from-week-number
    minTransactionDT = datetime.datetime.strptime(yyyy_ww + '-1', "%Y-W%W-%w")
    maxTransactionDT = minTransactionDT + \
        datetime.timedelta(days=7)  # + 1 week to initial date

    # timestamp for API required format (min)
    minTransactionTimestamp = formtimestamp(minTransactionDT)
    # timestamp for API required format (max)
    maxTransactionTimestamp = formtimestamp(maxTransactionDT)

    return minTransactionTimestamp, maxTransactionTimestamp
