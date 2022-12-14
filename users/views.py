from django.shortcuts import render, redirect
from .serializers import *
from .forms import *
from rest_framework import generics, status
from rest_framework .response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy



class UserRegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('home')


       