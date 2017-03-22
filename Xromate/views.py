from django.shortcuts import render
import logging
logger = logging.getLogger('django')

# Create your views here.

def index(request):
    return render(request, 'Xromate/index.html')
