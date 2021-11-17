from django.shortcuts import render


def get_index(request):
    return render(request, 'sirocaapp/index.html')

