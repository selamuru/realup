from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'remanage/templates/dashboard.html')


def portfolio(request):
    return render(request, 'remanage/templates/portfolio.html')


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        import pdb; pdb.set_trace()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/main/')
    return render_to_response('remanage/templates/login.html',
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def main(request):
    return render(request, 'remanage/templates/main.html')