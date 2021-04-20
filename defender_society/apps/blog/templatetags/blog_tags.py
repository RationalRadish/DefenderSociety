from django import template
from ..models import Article, Category, Tag, Carousel, newsArticle
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

register = template.Library()


# Article related tag function
@register.simple_tag
def get_article_list(sort=None, num=None):
    '''Get the specified sorting method and the specified number of articles'''
    if sort:
        if num:
            return Article.objects.order_by(sort)[:num]
        return Article.objects.order_by(sort)
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()


@register.simple_tag
def keywords_to_str(art):
    '''Turn article keywords into strings'''
    keys = art.keywords.all()
    return','.join([key.name for key in keys])


@register.simple_tag
def get_tag_list():
    '''Return to tag list'''
    return Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)


@register.simple_tag
def get_category_list():
    '''Return to category list'''
    return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)


@register.inclusion_tag('blog/tags/article_list.html')
def load_article_summary(articles):
    '''Return to article list template'''
    return {'articles': articles}


@register.inclusion_tag('blog/tags/pagecut.html', takes_context=True)
def load_pages(context):
    '''Pagination label template, no need to pass parameters, directly inherit parameters'''
    return context


# Other functions
@register.simple_tag
def get_carousel_list():
    '''Get carousel picture list'''
    return Carousel.objects.all()

@register.simple_tag
def get_shared_article_list():
    '''Get the shared articles list'''
    return newsArticle.objects.all()

@register.simple_tag
def my_highlight(text, q):
    '''Custom title search term highlighting function, ignoring case'''
    if len(q)> 1:
        try:
            text = re.sub(q, lambda a:'<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text


@register.simple_tag
def get_request_param(request, param, default=None):
    '''Get the requested parameters'''
    return request.POST.get(param) or request.GET.get(param, default)


@register.simple_tag
def tweet_list(context, *args, **kwargs):
    recent_media = get_tweets()

    return {
        'profile': 'bbbskentuckiana',
        'tweets': recent_media
    }


@register.filter(name='split')
def split(str, key):
    return str.split(key)

@register.filter
def get_by_index(a, i):
    return a[i]