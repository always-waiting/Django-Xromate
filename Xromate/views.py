from django.shortcuts import render
from mysite.decorator import login_required
import logging

logger = logging.getLogger('django')

# Create your views here.

@login_required(login_url="login/")
def index(request):
    return render(request, 'Xromate/index.html')
