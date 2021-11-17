from django.shortcuts import render
import requests
from .models import *
from .forms import IndexForm


git_api = 'https://api.github.com/repos/'


def get_index(request):
    return render(request, 'sirocaapp/index.html')


def get_data(url, page):

    split_url = url.split('/')
    user_project = split_url[3] + '/' + split_url[4] + f'/pulls?page={page}'
    r = requests.get(git_api+user_project)
    return r.json()


def make_request(request):
    form = IndexForm(request.POST)
    try:
        user_request = UserRequest.objects.get(url=request.POST.get("url", ""))
        pulls = UserRequestResult.objects.filter(url=user_request)
        return render(request, 'sirocaapp/index.html', context={'pulls': pulls})

    except:

        if form.is_valid():
            url = form.cleaned_data['url']
            page = 0
            while True:
                page += 1
                data = get_data(url, page)

                if data == []:
                    break
                if type(data) is dict:
                    return render(request, 'sirocaapp/index.html', context={'empty': data["message"]})
                    break
                if not data:
                    empty = 'There are not pull requests'
                    return render(request, 'sirocaapp/index.html', context={'empty': empty})
                    break
                else:
                    form.save()
                    user_request = UserRequest.objects.get(url=url)
                    for i in data:
                        user_request_result_model = UserRequestResult()
                        user_request_result_model.url = user_request
                        user_request_result_model.pull_name = i["title"]
                        user_request_result_model.reviewers_name = i["user"]["login"]
                        user_request_result_model.assignees_name = i["base"]["user"]["login"]
                        user_request_result_model.pull_url = i["html_url"]
                        user_request_result_model.save()
                        pulls = UserRequestResult.objects.filter(url__url=url)
            return render(request, 'sirocaapp/index.html', context={'pulls': pulls})

        return render(request, 'sirocaapp/index.html', context={'form': form})

    return render(request, 'sirocaapp/index.html')
