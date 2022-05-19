from django.core import serializers
from django.http.response import HttpResponse
from django.utils import timezone

from django.shortcuts import get_object_or_404

from django.db.models import Q

from .models import Category, rssNews


# 10 items paginator
def paginate(request):
    page = int(request.GET['page'])
    From = 10*(page-1)
    to = 10*page
    return (From, to)


def paginator_index(request):
    page = int(request.GET['page'])
    From = (5*(page-1)) - 2
    to = (5*page) - 2
    list = serializers.serialize('json', rssNews.objects.filter(~Q(media=None)).filter(is_important=True).order_by('-view').order_by('-pub_dt')[From:to])
    return HttpResponse(list, content_type="application/json")


def paginator_important(request):
    From, to = paginate(request)
    list = serializers.serialize('json', rssNews.objects.order_by('-pub_dt').filter(is_important=True)[From:to])
    return HttpResponse(list, content_type="application/json")


def paginator_viewed(request):
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    From, to = paginate(request)
    list = serializers.serialize('json', rssNews.objects.filter(pub_dt__gte=three_days_ago).order_by('-view')[From:to])
    return HttpResponse(list, content_type="application/json")


def paginator_latest(request):
    From, to = paginate(request)
    list = serializers.serialize('json', rssNews.objects.order_by('-pub_dt')[From:to])
    return HttpResponse(list, content_type="application/json")


def paginator_search(request):
    From, to = paginate(request)
    list = serializers.serialize('json', rssNews.objects.filter(title__icontains=request.GET['q']).order_by('-pub_dt')[From:to])
    return HttpResponse(list, content_type="application/json")


def paginator_category(request):
    From, to = paginate(request)
    category = get_object_or_404(Category, pk=request.GET['pk'])
    list = serializers.serialize('json', category.rssnews_set.all().order_by('-pub_dt')[From:to])
    return HttpResponse(list, content_type="application/json")