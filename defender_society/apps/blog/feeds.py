# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from .models import Article
from django.conf import settings


class AllArticleRssFeed(Feed):
    # Title displayed on the party reader
    title = settings.SITE_END_TITLE
    # Jump URL, homepage
    link = "/"
    # Description content
    description = settings.SITE_DESCRIPTION

    # The content items that need to be displayed, you can choose some popular or latest blogs by yourself
    def items(self):
        return Article.objects.all()[:100]

    # The title of the displayed content, this is the most important thing
    def item_title(self, item):
        return "【{}】{}".format(item.category, item.title)

    # Description of displayed content
    def item_description(self, item):
        return item.body_to_markdown()
