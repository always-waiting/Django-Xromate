# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create api/genoverse views here
def dgv(request):
    return redirect('/genoverse/dgv')
