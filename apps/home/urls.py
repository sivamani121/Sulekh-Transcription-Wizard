# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views 

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path('annotate', views.anno, name='annotate'),
    re_path('verify', views.verify, name='verify'),
    re_path('confirm', views.confirm, name='confirm'),
    re_path('askus', views.ask_us, name='askus'),
    re_path('profile', views.Proview, name='profile'),
    re_path('search',views.search,name="search"),
    re_path('user_modify',views.user_modify,name="user_modify"),
    # re_path('<int:user_id>/',views.change_user,name='change_user'),
    path('<int:user_id>/', views.change_user, name='change_user'),
    # re_path('users',views. user_list, name='user_list'),
    # re_path('annotat', views.savesent, name='savesent'),
]
