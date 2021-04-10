# # The server must be restarted after creating a new tags file

# from django import template
# from ..models import emoji_info

# register = template.Library()


# @register.simple_tag
# def get_comment_count(entry):
#     '''Get the total number of comments on an article'''
#     lis = entry.article_comments.all()
#     return lis.count()


# @register.simple_tag
# def get_parent_comments(entry):
#     '''Get the list of parent comments of an article, select only the next 20 comments in reverse order'''
#     lis = entry.article_comments.filter(parent=None).order_by("-id")[:20]
#     return lis


# @register.simple_tag
# def get_child_comments(com):
#     '''Get a list of child flat roads of a parent comment'''
#     lis = com.articlecomment_child_comments.all()
#     return lis


# @register.simple_tag
# def get_comment_user_count(entry):
#     '''Get the total number of commenters'''
#     p = []
#     lis = entry.article_comments.all()
#     for each in lis:
#         if each.author not in p:
#             p.append(each.author)
#     return len(p)


# @register.simple_tag
# def get_notifications(user, f=None):
#     '''Get the prompt information under the corresponding conditions of a user'''
#     if f == 'true':
#         lis = user.notification_get.filter(is_read=True)
#     elif f == 'false':
#         lis = user.notification_get.filter(is_read=False)
#     else:
#         lis = user.notification_get.all()
#     return lis


# @register.simple_tag
# def get_notifications_count(user, f=None):
#     '''Get the total number of prompt messages under the corresponding conditions of a user'''
#     if f == 'true':
#         lis = user.notification_get.filter(is_read=True)
#     elif f == 'false':
#         lis = user.notification_get.filter(is_read=False)
#     else:
#         lis = user.notification_get.all()
#     return lis.count()


# @register.simple_tag
# def get_emoji_imgs():
#     '''
#     Return a list containing emoticons
#     :return:
#     '''
#     return emoji_info


# @register.filter(is_safe=True)
# def emoji_to_url(value):
#     """
#     Convert the emoji name into a picture address
#     """
#     emoji_static_url = 'comment/weibo/{}.png'
#     return emoji_static_url.format(value)
