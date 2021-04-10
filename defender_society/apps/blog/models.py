from django.db import models
from django.conf import settings
from django.shortcuts import reverse
import markdown

import re


# Create your models here.

# Article keywords, used as keywords in SEO
class Keyword(models.Model):
    name = models.CharField('article keywords', max_length=20)

    class Meta:
        verbose_name = 'Keywords'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# Article tags
class Tag(models.Model):
    name = models.CharField('article tag', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('Description', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='Used as description in SEO, length refers to SEO standard')

    class Meta:
        verbose_name = 'label'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

    def get_article_list(self):
        '''Return to the list of all published articles under the current label'''
        return Article.objects.filter(tags=self)


# Article classification
class Category(models.Model):
    name = models.CharField('Article Category', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('Description', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='Used as description in SEO, length refers to SEO standard')

    class Meta:
        verbose_name = 'Classification'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)

class newsArticle(models.Model):
    title = models.CharField(max_length = 150, verbose_name = 'Shared Article Title')
    summary = models.CharField(max_length= 150, verbose_name = 'Shared Article Summary' )
    hyperlink_address = models.CharField('Hyperlink', max_length=200, default='#',
                           help_text='Hyperlink for the articles listed, default # means no jump')

    class Meta:
        verbose_name = 'Shared Articles'
        verbose_name_plural = verbose_name
        ordering = ['title']

    def __str__(self):
        return self.title
# Article
class Article(models.Model):
    IMG_LINK = '/ static/blog/img/summary.png '
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Author', on_delete=models.PROTECT)
    title = models.CharField(max_length=150, verbose_name='Article title')
    summary = models.TextField('Article summary', max_length=230,
                               default='The article summary is equivalent to the content of the web page description, please be sure to fill in...')
    body = models.TextField(verbose_name='Article content')
    img_link = models.CharField('picture address', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='modification time', auto_now=True)
    views = models.IntegerField('Views', default=0)
    slug = models.SlugField(unique=True)
    is_top = models.BooleanField('top', default=False)

    category = models.ForeignKey(Category, verbose_name='Article Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, verbose_name='tag')
    keywords = models.ManyToManyField(Keyword, verbose_name='Article keywords',
                                      help_text='Article keywords, used as keywords in SEO, it is best to use long tail words, 3-4 are enough')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[: 20]

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):
        return Article.objects.filter(id__gt=self.id).order_by('id').first()




# Slide
class Carousel(models.Model):
    number = models.IntegerField('Number',
                                 help_text='Number determines the order in which pictures are played, no more than 5 pictures')
    title = models.CharField('title', max_length=20, blank=True, null=True, help_text='title can be empty')
    content = models.CharField('Description', max_length=80)
    img_url = models.CharField('picture address', max_length=200)
    url = models.CharField('Jump link', max_length=200, default='#',
                           help_text='Hyperlink to the picture jump, default # means no jump')

    class Meta:
        verbose_name = 'Picture Carousel'
        verbose_name_plural = verbose_name
        # The smaller the number, the earlier it is, and the adding time is about late
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[: 25]



class AboutBlog(models.Model):
    body = models.TextField(verbose_name='About content')
    create_date = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='modification time', auto_now=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'About  '

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

class RequirementsBlog(models.Model):
    body = models.TextField(verbose_name='Requirements')
    create_date = models.DateTimeField(verbose_name='Create Time', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='modification time', auto_now=True)

    class Meta:
        verbose_name = 'Requirements'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Requirements  '

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('blog:event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class EventMember(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['event', 'user']

    def __str__(self):
        return str(self.user)

        