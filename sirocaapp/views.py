from django.shortcuts import render
import requests

git_api = 'https://api.github.com/repos/'


def get_index(request):
    return render(request, 'sirocaapp/index.html')


def get_data(url):
    split_url = url.split('/')
    user_project = split_url[3] + '/' + split_url[4] + '/pulls'
    r = requests.get(git_api+user_project)
    return r.json()
