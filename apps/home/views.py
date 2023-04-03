# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Sentence,Answered,sent_req
from apps.authentication.models import User
from django.shortcuts import render, redirect
from .forms import AskForm,Anno
from ai4bharat.transliteration import XlitEngine
from datetime import datetime
e = XlitEngine("hi", beam_width=10, rescore=True)

# def savesent(request):
#     # # from ai4bharat.transliteration import XlitEngine
#     # f=open('apps/static/file.txt','r',encoding='utf-8')
#     # s=f.read()
#     # s=c=list(s.strip().split("\n\n"))
#     # for i in range(len(s)):
#     #     s[i]=list(s[i].strip().split('\n'))
#     # for i in range(len(s)):
#     #     for j in range(len(s[i])):
#     #         s[i][j]=list(s[i][j].strip().split('\t'))
#     #         s[i][j][2]=list(s[i][j][2].strip().split(','))
#     # for i in s:
#     #     s=""
#     #     t=""
#     #     for j in i:
#     #         s+=" "+j[0]
#     #         t+=j[1]
#     #     y=Sentence(words=s.strip(),tags=t.strip())
#     #     y.save()
#     return render(request,'home/index.html')

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
    print(request)
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
    

    
    print(user.tag,load_template,'---------------------------------------','verify' in load_template)
    if ('tables' in load_template) or ('annotate' in load_template) or ('verify' in load_template) or ('confirm' in load_template):
        
        if(user.tag>1 and 'confirm' in load_template):
            sent = Sentence.objects.all().filter(status=2)
            
        
             
        elif(user.tag >=0 and 'annotate' in load_template):
            sent = Sentence.objects.all().filter(status=0)       
        else:
            sent = Sentence.objects.all().filter(status=1) 
       
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
            wordsh=[]
           
               



                


        

    html_template = loader.get_template('home/' + load_template)
    print(html_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def anno(request):
    print(request)
    context = {}
    uid = request.session['user_id'] 
    user = User.objects.all().filter(id=uid).first()
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    
    # try:
    if request.method =='POST':
        response = request.POST
        print("you somehow did --------------------")
        sent = Sentence.objects.all().filter(id=request.session['qid']).first()
        
        if response.get('skipped')=='1':
            user.score=sent.id
            user.save()
        else:
            words= list(sent.words.split(' '))
            tags= sent.tags
            ans=""
            for i in range(len(tags)):
                if i!=0:
                    ans+=" "
                if tags[i] == 'E':
                    ans+=words[i]
                elif response.get(f"flexRadioDefault{i}")=='11':
                    print(response.get(f"id_{i}"))
                    ans+=response.get(f"id_{i}")
                else:
                    ans+=response.get(f"flexRadioDefault{i}")
            print(ans)
            sent.meaning=ans
            sent.status=1
            sent.save()
            uid= request.session['user_id']
            user = User.objects.filter(id=uid)[0]
            newans= Answered(sentno=sent,userid=user)
            newans.save()
           
        
    load_template = request.path.split('/')[-1]

   
    context['segment'] = load_template
    
    
        
    if(user.tag>=0 ):
        sent = Sentence.objects.all().filter(status=0,id__gt=user.score)
        print(sent)
        if len(sent)==0:
            user.score=0
            user.save
            sent = Sentence.objects.all().filter(status=0,id__gt=user.score)

        if len(sent)==0 :
            n=0
            # print(words,sent.tags,range)
            context['sentence']=None
            context['words']=None
            context['tags']=None
            context['n']=range(n)
            context['utag']=None
            context['form']=None
            request.session['qid']=None
            html_template = loader.get_template('home/' + load_template)
            print(html_template)
            return HttpResponse(html_template.render(context, request))
        sent=sent.first()
        words = list(sent.words.strip().split(" "))
        n=len(words)
        request.session['qid']=sent.id

        print(words,sent.tags,range)
        context['sentence']=sent
        context['words']=words
        context['tags']=sent.tags.strip()
        context['n']=range(n)
        print(range(n))
        context['utag']=user.tag
        # user.score=sent.id
        # user.save()


        context['ten']=range(10)
        wordsh=[]
        for i in words:
            out = e.translit_word(i, topk=10)
            wordsh.append(list(out.values())[0])
            
        context['wordsh']=wordsh


        

    html_template = loader.get_template('home/' + load_template)
    print(html_template)
    return HttpResponse(html_template.render(context, request))

    
@login_required(login_url="/login/")
def ask_us(request):
    msg=""
    form = AskForm()
    if request.method =='POST':
        response = AskForm(request.POST)
        print("you somehow did --------------------")
        print(response)
        
        quest = Sentence(words=request.POST.get('sentence'),tags=request.POST.get('tags'))
        quest.save()
        print(quest.id)
        msg="question sbmited successfully check frequently for answer "
        uid= request.session['user_id']
        user = User.objects.filter(id=uid)[0]
        sentr = sent_req(sentence=quest,user=user)
        sentr.save()
        # return HttpResponse.''.render(context, request))



    context = {}
    
    print('FORM ASKED ---------------')
    
    context['form']=form
    context['msg']=msg
    queries =None
    user=User.objects.filter(id=request.session['user_id'])[0]
    queries = sent_req.objects.filter(user = user)
    
    


    return render(request,'home/askus.html',context)

def Proview(request):

    context = {
    
    }
    if request.method == 'POST':
        inp_mail=request.POST.get('input-email')
        inp_username=request.POST.get('input-username')
        inp_about= request.POST.get('input-about')
        print(inp_mail,inp_username,inp_about)
        user=User.objects.filter(id=request.session['user_id'])[0]

        if len(inp_mail)>0:
            user.email=inp_mail
            user.save()
        if len(inp_username)>0:
            user.username = inp_username
            user.save()
        
        if len(inp_about)>0:
            user.about= inp_about
            user.save()
    return HttpResponse(render(request,'home/profile.html',context))


# def annotate(request):


@login_required(login_url="/login/")
def confirm(request):
    print(request)
    context = {}
    uid = request.session['user_id'] 
    user = User.objects.all().filter(id=uid).first()
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    
    # try:
    if request.method =='POST':
        response = request.POST
        print("you somehow did --------------------")
        sent = Sentence.objects.all().filter(id=request.session['qid']).first()
        if response.get('skipped')=='1':
            user.score=sent.id
            user.save()
        else:
            print(request.session['qid'])
            print(sent.id)
            words= list(sent.words.split(' '))
            tags= sent.tags
            ans=""
            for i in range(len(tags)):
                if i!=0:
                    ans+=" "
                if tags[i] == 'E':
                    ans+=words[i]
                elif response.get(f"flexRadioDefault{i}")=='11':
                    print(response.get(f"id_{i}"))
                    ans+=response.get(f"id_{i}")
                else:
                    ans+=response.get(f"flexRadioDefault{i}")
            print(ans)
            sent.meaning=ans
            sent.status=3
            sent.save()
        
            uid= request.session['user_id']
            user = User.objects.filter(id=uid)[0]
            newans= Answered.objects.filter(sentno=sent).first()
            newans.updatedate=datetime.now
            newans.save()
        
    load_template = request.path.split('/')[-1]

   
    context['segment'] = load_template
    uid = request.session['user_id'] 
    user = User.objects.all().filter(id=uid).first()
    
        
    if(user.tag>=0 ):
        sent = Sentence.objects.all().filter(status=2,id__gt=user.score)
        print(sent)
        if len(sent)==0:
            user.score=0
            user.save
            sent = Sentence.objects.all().filter(status=2,id__gt=user.score)
        if len(sent)==0 :
            n=0
            # print(words,sent.tags,range)
            context['sentence']=None
            context['words']=None
            context['tags']=None
            context['n']=range(n)
            context['utag']=None
            context['form']=None
            request.session['qid']=None
            html_template = loader.get_template('home/' + load_template)
            print(html_template)
            return HttpResponse(html_template.render(context, request))
        sent=sent.first()
        words = list(sent.words.strip().split(" "))
        n=len(words)
        request.session['qid']=sent.id

        print(words,sent.tags,range)
        context['sentence']=sent
        context['words']=words
        context['tags']=sent.tags.strip()
        context['n']=range(n)
        print(range(n))
        context['utag']=user.tag
        ans=sent.meaning
        ans = ans.strip().split()
        context['ans']=ans
        print(ans)
        
        context['ten']=range(10)
        wordsh=[]
        for i in words:
            out = e.translit_word(i, topk=10)
            wordsh.append(list(out.values())[0])
            
        context['wordsh']=wordsh


        

    html_template = loader.get_template('home/' + load_template)
    print(html_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))














@login_required(login_url="/login/")
def verify(request):
    print(request)
    context = {}
    uid = request.session['user_id'] 
    user = User.objects.all().filter(id=uid).first()
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    
    # try:
    if request.method =='POST':
        response = request.POST
        print("you somehow did --------------------")
        sent = Sentence.objects.all().filter(id=request.session['qid']).first()
        if response.get('skipped')=='1':
            user.score=sent.id
            user.save()
        else:
            print(request.session['qid'])
            print(sent.id)
            
            words= list(sent.words.split(' '))
            tags= sent.tags
            ans=""
            for i in range(len(tags)):
                if i!=0:
                    ans+=" "
                if tags[i] == 'E':
                    ans+=words[i]
                elif response.get(f"flexRadioDefault{i}")=='11':
                    print(response.get(f"id_{i}"))
                    ans+=response.get(f"id_{i}")
                else:
                    ans+=response.get(f"flexRadioDefault{i}")
            print(ans)
            sent.meaning=ans
            sent.status=2
            sent.save()
           
        
    load_template = request.path.split('/')[-1]

   
    context['segment'] = load_template
    
    
        
    if(user.tag>=0 ):
        sent = Sentence.objects.all().filter(status=1,id__gt=user.score)
        print(sent)
        if len(sent)==0:
            user.score=0
            user.save
            sent = Sentence.objects.all().filter(status=1,id__gt=user.score)
        if len(sent)==0 :
            n=0
            # print(words,sent.tags,range)
            context['sentence']=None
            context['words']=None
            context['tags']=None
            context['n']=range(n)
            context['utag']=None
            context['form']=None
            request.session['qid']=None
            html_template = loader.get_template('home/' + load_template)
            print(html_template)
            return HttpResponse(html_template.render(context, request))
        sent=sent.first()
        words = list(sent.words.strip().split(" "))
        n=len(words)
        request.session['qid']=sent.id

        print(words,sent.tags,range)
        context['sentence']=sent
        context['words']=words
        context['tags']=sent.tags.strip()
        context['n']=range(n)
        print(range(n))
        ans=sent.meaning
        print(ans)
        ans=list(ans.strip().split())
        context['ans']=ans

        context['ten']=range(10)
        wordsh=[]
        for i in words:
            out = e.translit_word(i, topk=10)
            wordsh.append(list(out.values())[0])
            
        context['wordsh']=wordsh


        

    html_template = loader.get_template('home/' + load_template)
    print(html_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))













