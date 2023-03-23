# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Sentence,Answered
from apps.authentication.models import User
from django.shortcuts import render, redirect


@login_required(login_url="/login/")
def index(request):

    sents=Answered.objects.order_by('-updatedate')
    if len(sents)>6:
        sents=sents[0:6]
   

    context = {'segment': 'index',
               'sents':sents,
               }


    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    
    # try:
        
    load_template = request.path.split('/')[-1]

    if load_template == 'admin':
        return HttpResponseRedirect(reverse('admin:index'))
    context['segment'] = load_template
    uid = request.session['user_id'] 
    user = User.objects.all().filter(id=uid).first()
    
    if 'tables' in load_template or 'annotate' in load_template or 'Verify' in load_template or 'confirm' in load_template:
        
        print(user.tag,load_template,'---------------------------------------')
        if(user.tag>1 and 'confirm' in load_template):
            sent = Sentence.objects.all().filter(status=2)
            
        elif(user.tag>0 and 'Verfiy' in load_template):
            sent = Sentence.objects.all().filter(status=1)   
        elif(user.tag >=0 and 'annotate' in load_template):
            sent = Sentence.objects.all().filter(status=0)       
        else:
            return redirect('/')
       
        if len(sent)>0:
            sent=sent[0]
            
            words = list(sent.words.split(" "))
            n=len(words)
            print(words,sent.tags,range)
            context['sentence']=sent
            context['words']=words
            context['tags']=sent.tags
            context['n']=range(n)
            context['utag']=user.tag



                


        

    html_template = loader.get_template('home/' + load_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))
