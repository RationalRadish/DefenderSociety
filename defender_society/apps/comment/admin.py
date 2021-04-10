# from django.contrib import admin
# from .models import ArticleComment, Notification


# # @admin.register(ArticleComment)
# # class CommentAdmin(admin.ModelAdmin):
# #     date_hierarchy = 'create_date'
# #     list_display = ('id', 'author', 'belong', 'create_date', 'show_content')
# #     list_filter = ('author', 'belong',)
# #     ordering = ('-id',)
# #     # Set the fields that need to add a tag
# #     list_display_links = ('id', 'show_content')
# #     search_fields = ('author__username', 'belong__title')

# #     # Use method to customize a field, and set a name for this field
# #     def show_content(self, obj):
# #         return obj.content[:30]

# #     show_content.short_description = 'Comment content'


# # @admin.register(Notification)
# # class NotificationAdmin(admin.ModelAdmin):
# #     date_hierarchy = 'create_date'
# #     list_display = ('id', 'create_p', 'create_date', 'is_read')
# #     list_filter = ('create_p', 'is_read',)
# #     search_fields = ('create_p__username', 'comment__content')
