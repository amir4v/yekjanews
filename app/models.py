from django.db import models
from django.utils import timezone

from .Utility import j_pub_dt


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True, db_index=True)
    def slug(self):
        return self.title.replace(' ', '-')

    is_important = models.BooleanField(default=False, db_index=True)
    parent = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class rssNews(models.Model):
    news_publisher_name = models.CharField(max_length=128)
    news_publisher_address = models.CharField(max_length=2048)

    description = models.CharField(max_length=4096, null=True, blank=True, db_index=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, db_index=True)

    media = models.CharField(max_length=2048, null=True, blank=True, unique=True, db_index=True)

    guid = models.CharField(max_length=2048, unique=True, db_index=True) # Link and ID
    title = models.CharField(max_length=128, db_index=True)
    def slug(self):
        return self.title.replace(' ', '-')

    pub_dt = models.DateTimeField(default=timezone.now, db_index=True)

    view = models.IntegerField(default=0, db_index=True) # and clicked

    is_important = models.BooleanField(default=False, db_index=True)

    jalali_pub_dt = models.CharField(default=j_pub_dt, max_length=32)

    check = models.BooleanField(default=False) # for when crawling rss and increase view and if i see this news, dont increase it again


    def __str__(self):
        return self.title