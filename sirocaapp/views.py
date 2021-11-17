from django.shortcuts import render
import requests
from .models import *
from .forms import IndexForm
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp


git_api = 'https://api.github.com/repos/'
data = []


def get_index(request):
    return render(request, 'sirocaapp/index.html')


def get_pull_count(url):
    try:
        r = requests.get(url)
        soup = bs(r.text, 'lxml')
        count = int(soup.find('div', class_='pt-3 hide-full-screen mb-5').find('a', id='pull-requests-tab').find('span',
                                                                                                  class_='Counter').text)
        if count > 30:
            return count // 30
        else:
            return 1
    except:
        return 0


async def get_data(session, url, page):

    split_url = url.split('/')
    user_project = split_url[3] + '/' + split_url[4] + f'/pulls?page={page}'

    async with session.post(url=git_api+user_project) as response:
        print(f'get_data({git_api+user_project})')
        r_json = await response.json()
        data.append(r_json)


async def create_tasks(url, count):
    print('create_tasks()')
    tasks = []

    async with aiohttp.ClientSession() as session:
        for page in range(1, count+1):
            task = asyncio.create_task(get_data(session, url, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def make_request(request):
    form = IndexForm(request.POST)
    try:
        user_request = UserRequest.objects.get(url=request.POST.get("url", ""))
        pulls = UserRequestResult.objects.filter(url=user_request)
        return render(request, 'sirocaapp/index.html', context={'pulls': pulls})

    except:

        if form.is_valid():
            url = form.cleaned_data['url']
            count = get_pull_count(url)
            print(count)

            # asyncio.run(create_tasks(url, count))

            if type(data) is dict:
                return render(request, 'sirocaapp/index.html', context={'empty': data["message"]})

            if not data:
                empty = 'There are not pull requests'
                return render(request, 'sirocaapp/index.html', context={'empty': empty})

            else:
                form.save()
                user_request = UserRequest.objects.get(url=url)
                for data_list in data:
                    for i in data_list:
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
