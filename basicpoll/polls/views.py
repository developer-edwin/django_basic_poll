from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Polls main oage")

def detail(request, question_id):
    return HttpResponse(f'You are seeing the question number {question_id}')

def results(request, question_id):
    return HttpResponse(f'You are seeing the results of the question number {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You are voting the question number {question_id}')