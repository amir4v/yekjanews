from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .models import rssNews, Category


# default fix context
def pre_context():
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    context = {
        'top10': rssNews.objects.filter(pub_dt__gte=three_days_ago).filter(is_important=True).order_by('-view')[:10],

        'latest': rssNews.objects.order_by('-pub_dt')[:10],
        'important': rssNews.objects.order_by('-pub_dt').filter(is_important=True)[:10],
        'viewed': rssNews.objects.filter(pub_dt__gte=three_days_ago).order_by('-view')[:10],

        'cats': Category.objects.filter(is_important=True),
    }
    return context


def index(request):
    top_two_list = rssNews.objects.filter(~Q(media=None)).filter(is_important=True).order_by('-view').order_by('-pub_dt')[:8]
    context = {
        'top': top_two_list[0],
        'two': top_two_list[1:3],
        'list': top_two_list[3:8],
    }
    context.update(pre_context())
    return render(request, 'page/index.html', context)


# latest -then- is_important
def important(request):
    context = {
        'list': rssNews.objects.order_by('-pub_dt').filter(is_important=True)[:10],
    }
    context.update(pre_context())
    return render(request, 'page/important.html', context)


# three_days_ago -then- most-viewed
def viewed(request):
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    context = {
        'list': rssNews.objects.filter(pub_dt__gte=three_days_ago).order_by('-view')[:10],
    }
    context.update(pre_context())
    return render(request, 'page/viewed.html', context)


# latest
def latest(request):
    context = {
        'list': rssNews.objects.order_by('-pub_dt')[:10],
    }
    context.update(pre_context())
    return render(request, 'page/latest.html', context)


# in title -then- latest
def search(request):
    context = {
        'list': rssNews.objects.filter(title__icontains=request.GET['q']).order_by('-pub_dt')[:10],
    }
    context.update(pre_context())
    return render(request, 'page/search.html', context)


# single news
def news(request, pk, title=""):
    news = get_object_or_404(rssNews, pk=pk)
    news.view += 1
    news.save()
    context = {'news': news}
    context.update(pre_context())
    return render(request, 'page/news.html', context)


# go out to original news
def go(request, pk):
    news = get_object_or_404(rssNews, pk=pk)
    news.view += 1
    news.save()
    return redirect(news.guid)


# category.rssnews_set -then- latest
def category(request, pk, title=""):
    category = get_object_or_404(Category, pk=pk)
    context = {
        'list': category.rssnews_set.all().order_by('-pub_dt')[:10],
        'category': category,
    }
    context.update(pre_context())
    return render(request, 'page/category.html', context)


from django.http import HttpResponse
def google(request):
    return HttpResponse("google-site-verification: google30072320facbb1e3.html")