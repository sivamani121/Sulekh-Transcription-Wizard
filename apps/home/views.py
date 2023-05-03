# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Sentence, Answered, sent_req, Confirmed, DataSets, Annotated, Verified
from apps.authentication.models import User
from django.shortcuts import render, redirect
from .forms import AskForm, Anno, ExcelUploadForm
from ai4bharat.transliteration import XlitEngine
from datetime import datetime, timezone
import pandas as pd
from django.db.models import Q
from django.db.models import Max
from .forms import TaskChangeForm
import threading
from django.urls import reverse


import time
e = XlitEngine("hi", beam_width=10, rescore=True)


def savesent(request):
    # from ai4bharat.transliteration import XlitEngine
    f = open('apps/static/file.txt', 'r', encoding='utf-8')
    s = f.read()
    s = c = list(s.strip().split("\n\n"))
    for i in range(len(s)):
        s[i] = list(s[i].strip().split('\n'))
    for i in range(len(s)):
        for j in range(len(s[i])):
            s[i][j] = list(s[i][j].strip().split('\t'))
            s[i][j][2] = list(s[i][j][2].strip().split(','))
    for i in s:
        s = ""
        t = ""
        for j in i:
            s += " "+j[0]
            t += j[1]
        y = Sentence(words=s.strip(), tags=t.strip())
        y.save()
    return render(request, 'home/index.html')


@login_required(login_url="/login/")
def index(request):
    uid = request.session['user_id']
    user = User.objects.all().filter(id=uid).first()
    n = Answered.objects.all().filter(userid=user)
    ann = 0
    con = 0
    ver = 0
    for i in n:
       
        if i.sentno.status == 1:
            ann += 1
        elif i.sentno.status == 2:
            ver += 1
            ann += 1
        elif i.sentno.status == 3:
            con += 1
            ann += 1
            ver += 1
    scr = ann+2*ver+3*con
    
    
    sents = Answered.objects.order_by('-updatedate')
    if len(sents) > 6:
        sents = sents[0:6]

    context = {'segment': 'index',
               'sents': sents,
               }
    context['ann'] = ann
    context['ver'] = ver
    context['con'] = con

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

    print(user.tag, load_template,
          '---------------------------------------', 'verify' in load_template)
    if ('tables' in load_template) or ('annotate' in load_template) or ('verify' in load_template) or ('confirm' in load_template):

        if(user.tag > 1 and 'confirm' in load_template):
            sent = Sentence.objects.all().filter(status=2)

        elif(user.tag >= 0 and 'annotate' in load_template):
            sent = Sentence.objects.all().filter(status=0)
        else:
            sent = Sentence.objects.all().filter(status=1)

        if len(sent) > 0:
            sent = sent[0]

            words = list(sent.words.strip().split(" "))
            n = len(words)
            print(words, sent.tags, range)
            context['sentence'] = sent
            context['words'] = words
            context['tags'] = sent.tags
            context['n'] = range(n)
            context['utag'] = user.tag
            wordsh = []

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
    if request.method == 'POST':
        response = request.POST
        print("you somehow did --------------------")
        sent = Sentence.objects.all().filter(id=request.session['qid']).first()

        if response.get('skipped') == '1':
            user.score = sent.id
            user.save()
        else:
            words = sent.words
            words = list(words.strip().split())
            print(words)
            tags = sent.tags
            tags = tags.strip()
            ans = ""
            for i in range(len(tags)):
                if i != 0:
                    ans += " "
                if tags[i].upper() != 'H':
                    print(tags[i])
                    ans += words[i]
                    print(words[i])
                elif response.get(f"flexRadioDefault{i}") == '11':
                    # print(response.get(f"id_{i}"))
                    ans += response.get(f"id_{i}")
                else:
                    ans += response.get(f"flexRadioDefault{i}")
            print(ans)
            sent.meaning = ans
            sent.status = 1
            sent.save()
            uid = request.session['user_id']
            user = User.objects.filter(id=uid)[0]
            newans = Answered(sentno=sent, userid=user)
            newans.save()
            annoted = Annotated(asent=sent, auser=user)
            annoted.save()
        sent.lock = False
        sent.save()

    load_template = request.path.split('/')[-1]

    context['segment'] = load_template

    if(user.tag >= 0):
        sent = Sentence.objects.all().filter(status=0, id__gt=user.score, lock=False)
        # print(sent)
        if len(sent) == 0:
            user.score = 0
            user.save
            sent = Sentence.objects.all().filter(status=0, id__gt=user.score, lock=False)

        if len(sent) == 0:
            n = 0
            # print(words,sent.tags,range)
            context['sentence'] = None
            context['words'] = None
            context['tags'] = None
            context['n'] = range(n)
            context['utag'] = None
            context['form'] = None
            request.session['qid'] = None
            html_template = loader.get_template('home/' + load_template)
            # print(html_template)
            return HttpResponse(html_template.render(context, request))
        sent = sent.first()
        sent.lock = True
        sent.save()
        timer = threading.Timer(5000, sent.unlock)
        timer.start()
        words = list(sent.words.strip().split(" "))
        n = len(words)
        request.session['qid'] = sent.id

        # print(words,sent.tags,range)
        context['sentence'] = sent
        context['words'] = words
        context['tags'] = sent.tags.strip()
        context['n'] = range(n)
        # print(range(n))
        context['utag'] = user.tag
        # user.score=sent.id
        # user.save()

        context['ten'] = range(10)
        wordsh = []
        for i in words:
            out = e.translit_word(i, topk=10)
            wordsh.append(list(out.values())[0])

        context['wordsh'] = wordsh

    html_template = loader.get_template('home/' + load_template)
    print(html_template)
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ask_us(request):
    msg = ""

    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        # return HttpResponse.''.render(context, request))
        print('hi')
        if form.is_valid():
            d = request.POST['datasetname']
            d = str(d)
            d = d.strip()
            # read the uploaded Excel file using pandas
            t = DataSets.objects.all().filter(datasetname=d)
            if len(t) != 0:
                msg = "dataset name alredy used "

            else:
                df = pd.read_excel(request.FILES['excel_file'])
                print(request.POST['datasetname'])
                uid = request.session['user_id']
                user = User.objects.filter(id=uid)[0]
                t = DataSets(datasetname=d, duser=user)
                for index, row in df.iterrows():
                    sent = Sentence(words=row['sentence'], tags=row['tags'])
                    sent.save()
                msg="dataset added successfully"
                t.save()
    form = ExcelUploadForm()
    context = {}

    print('FORM ASKED ---------------')

    context['form'] = form
    context['msg'] = msg
    uid = request.session['user_id']
    dt=DataSets.objects.filter(duser=User.objects.filter(id=uid)[0])
    context['datasets']=dt
    print(dt)
    queries = None
    user = User.objects.filter(id=request.session['user_id'])[0]
    queries = sent_req.objects.filter(user=user)

    return render(request, 'home/askus.html', context)


def Proview(request):

    context = {

    }
    if request.method == 'POST':
        inp_mail = request.POST.get('input-email')
        inp_username = request.POST.get('input-username')
        inp_about = request.POST.get('input-about')
        print(inp_mail, inp_username, inp_about)
        user = User.objects.filter(id=request.session['user_id'])[0]

        if len(inp_mail) > 0:
            user.email = inp_mail
            user.save()
        if len(inp_username) > 0:
            user.username = inp_username
            user.save()

        if len(inp_about) > 0:
            user.about = inp_about
            user.save()
    return HttpResponse(render(request, 'home/profile.html', context))


@login_required(login_url="/login/")
def confirm(request):

    print(request)
    context = {}
    uid = request.session['user_id']
    user = User.objects.all().filter(id=uid).first()
    if user.tag < 2:
        return redirect(reverse('home'))

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    # try:
    if request.method == 'POST':
        response = request.POST
        print("you somehow did --------------------")
        sent = Sentence.objects.all().filter(id=request.session['qid']).first()
        if response.get('skipped') == '1':
            user.score = sent.id
            user.save()
        else:
            print(request.session['qid'])
            print(sent.id)
            words = list(sent.words.strip().split(' '))
            tags = sent.tags
            ans = ""
            for i in range(len(tags)):
                if i != 0:
                    ans += " "
                if tags[i] == 'E':
                    ans += words[i]
                elif response.get(f"flexRadioDefault{i}") == '11':
                    print(response.get(f"id_{i}"))
                    ans += response.get(f"id_{i}")
                else:
                    ans += response.get(f"flexRadioDefault{i}")
            print(ans)
            sent.meaning = ans
            sent.status = 3
            sent.save()

            uid = request.session['user_id']
            user = User.objects.filter(id=uid)[0]
            newans = Answered.objects.filter(sentno=sent).first()
            newans.updatedate = datetime.now()
            newans.save()
            conf = Confirmed(csent=sent, cuser=newans.userid)
            conf.save()
    load_template = request.path.split('/')[-1]

    context['segment'] = load_template
    uid = request.session['user_id']
    user = User.objects.all().filter(id=uid).first()

    if(user.tag >= 0):
        sent = Sentence.objects.all().filter(status=2, id__gt=user.score)
        print(sent)
        if len(sent) == 0:
            user.score = 0
            user.save
            sent = Sentence.objects.all().filter(status=2, id__gt=user.score)
        if len(sent) == 0:
            n = 0
            # print(words,sent.tags,range)
            context['sentence'] = None
            context['words'] = None
            context['tags'] = None
            context['n'] = range(n)
            context['utag'] = None
            context['form'] = None
            context['marks'] = None
            request.session['qid'] = None
            html_template = loader.get_template('home/' + load_template)
            print(html_template)
            return HttpResponse(html_template.render(context, request))
        sent = sent.first()
        words = list(sent.words.strip().split(" "))
        n = len(words)
        request.session['qid'] = sent.id

        print(words, sent.tags, range)
        context['sentence'] = sent
        context['words'] = words
        context['tags'] = sent.tags.strip()
        context['n'] = range(n)
        print(range(n))
        context['utag'] = user.tag
        ans = sent.meaning
        ans = ans.strip().split()
        context['ans'] = ans
        print(ans)

        context['ten'] = range(10)
        wordsh = []
        for i in words:
            out = e.translit_word(i, topk=10)
            wordsh.append(list(out.values())[0])

        context['wordsh'] = wordsh
        marks = []
        print(wordsh,"-------------------------------------------------",ans)
        for i in range(len(wordsh)):
            t = 11
            for j in range(10):
                if wordsh[i][j] == ans[i]:
                    t = j
            marks.append(t)
        context['marks'] = marks

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
    if user.tag < 1:
        return redirect(reverse('home'))
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    # try:
    if request.method == 'POST':
        response = request.POST
        print("you somehow did --------------------")
        sent = Sentence.objects.all().filter(id=request.session['qid']).first()
        if response.get('skipped') == '1':
            user.score = sent.id
            user.save()
        else:
            print(request.session['qid'])
            print(sent.id)

            words = list(sent.words.strip().split())
            tags = sent.tags
            ans = ""
            for i in range(len(tags)):
                if i != 0:
                    ans += " "
                if tags[i] == 'E':
                    ans += words[i]
                elif response.get(f"flexRadioDefault{i}") == '11':
                    print(response.get(f"id_{i}"))
                    ans += response.get(f"id_{i}")
                else:
                    ans += response.get(f"flexRadioDefault{i}")
            print(ans)
            sent.meaning = ans
            sent.status = 2
            sent.save()
            ver = Verified(vsent=sent, vuser=user)
            ver.save()

    load_template = request.path.split('/')[-1]

    context['segment'] = load_template

    if(user.tag >= 0):
        sent = Sentence.objects.all().filter(status=1, id__gt=user.score)
        print(sent)
        if len(sent) == 0:
            user.score = 0
            user.save
            sent = Sentence.objects.all().filter(status=1, id__gt=user.score)
        if len(sent) == 0:
            n = 0
            # print(words,sent.tags,range)
            context['sentence'] = None
            context['words'] = None
            context['tags'] = None
            context['n'] = range(n)
            context['utag'] = None
            context['form'] = None
            context['marks'] = None
            request.session['qid'] = None
            html_template = loader.get_template('home/' + load_template)
            print(html_template)
            return HttpResponse(html_template.render(context, request))
        sent = sent.first()
        words = list(sent.words.strip().split(" "))
        n = len(words)
        request.session['qid'] = sent.id

        print(words, sent.tags, range)
        context['sentence'] = sent
        context['words'] = words
        context['tags'] = sent.tags.strip()
        context['n'] = range(n)
        print(range(n))
        ans = sent.meaning
        print(ans)
        ans = list(ans.strip().split())
        context['ans'] = ans
        print(ans)

        context['ten'] = range(10)
        wordsh = []
        for i in words:
            out = e.translit_word(i, topk=10)
            wordsh.append(list(out.values())[0])
            
        context['wordsh'] = wordsh
        marks = []
        for i in range(len(wordsh)):
            t = 11
            for j in range(10):
                if wordsh[i][j] == ans[i]:
                    t = j
            marks.append(t)
        context['marks'] = marks
        # print(wordsh)

    html_template = loader.get_template('home/' + load_template)
    print(html_template)
    return HttpResponse(html_template.render(context, request))

    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('home/page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('home/page-500.html')
    #     return HttpResponse(html_template.render(context, request))

# def user_list(request):
#     users = User.objects.all()
#     if request.method == 'POST':
#         form = TaskChangeForm(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data['user_id']
#             task = form.cleaned_data['task']
#             user = User.objects.get(pk=user_id)
#             user.task = task
#             user.save()
#             return redirect('user_list')
#     else:
#         form = TaskChangeForm()
#     return HttpResponse(render(request,'home/user_list.html',{'users': users, 'form': form}))


def search(request):
    sent_list = Sentence.objects.order_by('id').filter(status=3)
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        print(keywords)
        if keywords:
            sent_list = sent_list.filter(words__icontains=keywords)
    context = {
        'sents': sent_list,
    }
    return render(request, 'home/search.html', context)


def user_modify(request):
    uid = request.session['user_id']
    user = User.objects.all().filter(id=uid).first()
    if user.tag < 3:
        return redirect(reverse('home'))
    usrs_list = User.objects.exclude(tag=3).order_by('id')
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        print(keywords)
        if keywords:
            usrs_list = usrs_list.filter(id__icontains=keywords)
    context = {
        'usrs': usrs_list,
    }
    return render(request, 'home/user_modify.html', context)


def change_user(request, user_id):
    if request.method == 'POST':
        response = request.POST
        q=response.get('quantity')
        print(q+"-------------------")
        ch_user = User.objects.all().filter(id=user_id).first()
        print(ch_user)
        ch_user.tag=q
        ch_user.save()

    ch_user = User.objects.all().filter(id=user_id).first()
    print(ch_user)
    n = Answered.objects.all().filter(userid=ch_user)
    ann = 0
    con = 0
    ver = 0
    for i in n:
       
        if i.sentno.status == 1:
            ann += 1
        elif i.sentno.status == 3:
            con += 1
        elif i.sentno.status == 2:
            ver += 1
    scr = ann+2*ver+3*con
    context = {}
    context['ann'] = ann
    context['ver'] = ver
    context['con'] = con
    context['scr'] = scr
    context['user'] = ch_user
    print(ch_user.tag)
    # print(ann, ver, con, scr)
    return render(request, 'home/user_change.html', context)
