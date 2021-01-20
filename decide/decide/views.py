import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from django.core import serializers
from django.shortcuts import render, redirect

from voting.serializers import MinimalVotingSerializer
from authentication.models import UserProfile

from base import mods
from django.http import HttpResponse
from django.utils.translation import ugettext as _

def index(request):
    output = _('StatusMsg')
    return HttpResponse(output)

def check_session(request):
    if((request.session.get('user_token') != None and request.COOKIES.get('decide') == None) or
        (request.session.get('user_token') == None and request.COOKIES.get('decide') != None)):
        return logout(request)
    return True

class IndexView(TemplateView):
    template_name = 'decide/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user_styles'] = UserProfile.styles;
        return context

    def dispatch(self, request, *args, **kwargs):
        check_sess = check_session(request)
        if check_sess != True:
            return check_sess

        return super(IndexView, self).dispatch(request, *args, **kwargs)

class HelpVoiceAssistantView(TemplateView):
    template_name = 'decide/helpvoiceassistant.html'

    def get_context_data(self, **kwargs):
        check_session(self.request)
        context = super().get_context_data(**kwargs)

        context['user_styles'] = UserProfile.styles;
        return context

    def dispatch(self, request, *args, **kwargs):
        check_sess = check_session(request)
        if not check_sess:
            return check_sess

        return super(HelpVoiceAssistantView, self).dispatch(request, *args, **kwargs)

class ModifyProfileDateView(TemplateView):
    template_name = 'decide/modify.html'

    def get_context_data(self, **kwargs):
        check_session(self.request)
        context = super().get_context_data(**kwargs)

        context['user_styles'] = UserProfile.styles;
        context['user_sex'] = UserProfile.sex_types;
        return context

    def dispatch(self, request, *args, **kwargs):
        check_sess = check_session(request)
        if not check_sess:
            return check_sess

        return super(ModifyProfileDateView, self).dispatch(request, *args, **kwargs)
      
class SignInView(TemplateView):
    template_name='decide/sign_in.html'

    def get_context_data(self, **kwargs):
        check_session(self.request)
        context = super().get_context_data(**kwargs)

        context['user_styles'] = UserProfile.styles;
        context['user_sex'] = UserProfile.sex_types;
        return context

    def dispatch(self, request, *args, **kwargs):
        check_sess = check_session(request)
        if not check_sess:
            return check_sess

        return super(SignInView, self).dispatch(request, *args, **kwargs)

def login(request):
    response = redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        token = mods.post('authentication', entry_point='/login/',json={'username': username, 'password': password})
        user = mods.post('authentication', entry_point='/getuser/', json=token)

        user_id = user.get('id', None)
        if user_id == None:
            response['Location'] += '?failedlogin'
            return response

        request.session['user_token'] = token
        request.session['voter_id'] = user_id
        request.session['username'] = user.get('username', '')
        request.session.modified = True
        
        response.set_cookie('decide', token.get('token', ''), path='/', max_age=1800)

    return response

def logout(request):
    response = redirect('index')
    response.delete_cookie('decide')

    token = request.session.get('user_token')

    if token:
        mods.post('authentication', entry_point='/logout/', json={'token': token})

        del request.session['user_token']
        del request.session['voter_id']
        del request.session['username']
        request.session.modified = True

    return response