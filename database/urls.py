from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('search/', views.search),
    path('borrow/', views.borrow),
    path('renew/', views.renew),
    path('mybooks/', views.mybooks),
    path('return/', views.returnBooks),
    path('review/', views.bookReview),
    path('searchreview/', views.SearchReview),
]
