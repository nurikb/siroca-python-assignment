from django.shortcuts import render
import requests
from .models import *
from .forms import IndexForm
from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp


git_api = 'https://api.github.com/repos/'
user_agency = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 OPR/78.0.4093.147'

data = []


def get_index(request):
    return render(request, 'sirocaapp/index.html')


def get_pull_count(url):
    #   get the number of pull requests
    #   the count is divided by 30 since there are 30 pull requests in one response
    header = {'User-Agent': user_agency}
    try:
        r = requests.get(url, headers=header)
        soup = bs(r.text, 'lxml')
        count = int(soup.find('div', class_='pt-3 hide-full-screen mb-5').find('a', id='pull-requests-tab').find('span',
                                                                                                 class_='Counter').text)
        if count == 0:
            return 0
        elif count > 30 and count > 0:
            return count // 30
        else:
            return 1
    except AttributeError:
        return 0


async def get_data(session, url, page):

    split_url = url.split('/')
    user_project = split_url[3] + '/' + split_url[4] + f'/pulls?page={page}'

    async with session.get(url=git_api+user_project) as response:
        r_json = await response.json()
        if r_json != []:
            data.append(r_json)


async def create_tasks(url, count):
    tasks = []

    async with aiohttp.ClientSession() as session:
        for page in range(1, count+1):
            task = asyncio.create_task(get_data(session, url, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


def make_request(request):
    form = IndexForm(request.POST)
    try:
        url = request.POST.get("url", "")
        user_request = UserRequest.objects.get(url=url)
        pulls = UserRequestResult.objects.filter(url=user_request)
        return render(request, 'sirocaapp/index.html', context={'pulls': pulls})

    except UserRequest.DoesNotExist:

        if form.is_valid():
            url = form.cleaned_data['url']
            count = get_pull_count(url)
            print(count)
            if count == 0:
                empty = 'There are not pull requests'
                return render(request, 'sirocaapp/index.html', context={'empty': empty})

            asyncio.run(create_tasks(url, count+1))

            try:
                return render(request, 'sirocaapp/index.html', context={'empty': data[0]["message"]})
            except TypeError:
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
