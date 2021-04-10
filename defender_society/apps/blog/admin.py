from django.conf import settings
from django.apps import apps
from django.contrib import admin
from .models import *



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # The function of this is to give a screening mechanism, which is generally better according to time
    date_hierarchy = 'create_date'

    exclude = ('views',)

    # When viewing the attributes displayed when modifying, the first field has the <a> tag, so it is better to put the title
    list_display = ('id', 'title', 'author', 'create_date', 'update_date', 'is_top')

    # Set the fields that need to add the <a> tag
    list_display_links = ('title',)

    # Activate the filter, this is useful
    list_filter = ('create_date', 'category', 'is_top')

    list_per_page = 50  # Control the number of objects displayed on each page, the default is 100

    filter_horizontal = ('tags', 'keywords')  # Add a left and right box to multiple selection

    search_fields = ('author__username', 'title')

    # Restrict user permissions, you can only see the articles you edit
    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        User = apps.get_model(settings.AUTH_USER_MODEL)
        if db_field.name == 'author':
            if request.user.is_superuser:
                kwargs['queryset'] = User.objects.filter(is_staff=True, is_active=True)
            else:
                kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super(ArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(newsArticle)
class sharedArticleAdmin(admin.ModelAdmin):
    list_display = ( 'id','title', 'summary', 'hyperlink_address')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug')


# Customize the name and URL title of the management site
admin.site.site_header = 'Website management'
admin.site.site_title = 'Blog background management'


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'content', 'img_url', 'url')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'start_time', 'end_time']

@admin.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ['event', 'user']

@admin.register(AboutBlog)
class AboutBlogAdmin(admin.ModelAdmin):
    list_display = ('short_body', 'create_date', 'update_date')

    def short_body(self, obj):
        return 'Freely  edit the content of the About page, support markdown syntax. '

    short_body.short_description = 'AboutBlog'

    # Restrict user permissions, only super-management can edit
    def get_queryset(self, request):
        qs = super(AboutBlogAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return None
