# from django.db import models
# from django.conf import settings
# from blog.models import Article
# import re

# import markdown

# emoji_info = [
#     [('aini_org', 'love you'), ('baibai_thumb', 'bye bye'),
#      ('baobao_thumb', 'hold hug'), ('beishang_org', 'sadness'),
#      ('bingbujiandan_thumb', 'not simple'), ('bishi_org', 'contempt'),
#      ('bizui_org', 'Shut up'), ('chanzui_org', 'Gluttonous')],
# [('chigua_thumb', 'eat melon'), ('chongjing_org', 'look forward to'),
#  ('dahaqian_org', 'yawn'), ('dalian_org', 'slap face'),
#  ('ding_org', '顶'), ('doge02_org', 'doge'),
#  ('Erha_org', 'two ha'), ('gui_org', 'kneeling')],
# [('guzhang_thumb', 'applause'), ('haha_thumb', 'haha'),
#  ('heng_thumb', 'hum'), ('huaixiao_org', 'bad smile'),
#  ('huaxin_org', '色'), ('jiyan_org', 'squeeze eyes'),
#  ('kelian_org', 'pathetic'), ('kuxiao_org', '允传')],
# [('ku_org', 'cool'), ('leimu_org', 'tear'),
#  ('Miaomiao_thumb', 'meow'), ('ningwen_org', 'in doubt'),
#  ('nu_thumb', 'anger'), ('qian_thumb', 'money'),
#  ('sikao_org', 'thinking'), ('taikaixin_org', 'so happy')],
# [('Tanshou_org', 'Tanshou'), ('tianping_thumb', 'licking screen'),
#  ('Touxiao_org', 'laughing'), ('tu_org', 'spit'),
#  ('wabi_thumb', 'pig nose'), ('weiqu_thumb', 'grief'),
#  ('wenhao_thumb', 'unintelligible'), ('wosuanle_thumb', 'acid')],
# [('wu_thumb', 'dirty'), ('xiaoerbuyu_org', 'laugh without speaking'),
#  ('xiaoku_thumb', '笑 cry'), ('xixi_thumb', 'hee hee'),
#  ('yinxian_org', 'Insidious'), ('yun_thumb', 'Halo'),
#                                  ('Zhouma_thumb', 'curse'), ('zhuakuang_org', 'crazy')]
# ]

# def get_emoji_imgs(body):
#     '''
#     Replace the title emoticon in the comment, and replace the emoticon with the picture address
#     :param body:
#     :return:
#     '''
#     img_url = '<img class="comment-emoji-img" src="/static/comment/weibo/{}.png" title="{}" alt="{}">'
#     for i in emoji_info:
#         for ii in i:
#             emoji_url = img_url.format(ii[0], ii[1], ii[0])
#             body = re.sub(':{}:'.format(ii[0]), emoji_url, body)
#     tag_info = {
#         '<h\d>': '',
#         '</h\d>': '<br>',
#         '<script.*</script>': '',
#         '<meta.*?>': '',
#         '<link.*?>': ''
#     }
#     for k, v in tag_info.items():
#         body = re.sub(k, v, body)
#     return body


# class Comment(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_related',
#                                verbose_name='commenter', on_delete=models.CASCADE)
#     create_date = models.DateTimeField('Creation Time', auto_now_add=True)
#     content = models.TextField('Comment content')
#     parent = models.ForeignKey('self', verbose_name='parent comment', related_name='%(class)s_child_comments',
#                                blank=True,
#                                null=True, on_delete=models.CASCADE)
#     rep_to = models.ForeignKey('self', verbose_name='reply', related_name='%(class)s_rep_comments',
#                                blank=True, null=True, on_delete=models.CASCADE)

#     class Meta:
#         '''This is a metaclass for inheritance'''
#         abstract = True

#     def __str__(self):
#         return self.content[:20]

#     def content_to_markdown(self):
#         to_md = markdown.markdown(self.content,
#                                   safe_mode='escape',
#                                   extensions=[
#                                       'markdown.extensions.extra',
#                                       'markdown.extensions.codehilite',
#                                   ])
#         return get_emoji_imgs(to_md)


# class ArticleComment(Comment):
#     belong = models.ForeignKey(Article, related_name='article_comments', verbose_name='belonging to article',
#                                on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = 'Article comment'
#         verbose_name_plural = verbose_name
#         ordering = ['create_date']


# class Notification(models.Model):
#     create_p = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='notification creator',
#                                  related_name='notification_create',
#                                  on_delete=models.CASCADE)
#     get_p = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='notification recipient',
#                               related_name='notification_get',
#                               on_delete=models.CASCADE)
#     Comment = models.ForeignKey(ArticleComment, verbose_name = 'belongs review', related_name = 'the_comment',
#                    on_delete = models.CASCADE)
#     create_date = models.DateTimeField('reminder time', auto_now_add=True)
#     is_read = models.BooleanField('Is it read?', default=False)

#     def mark_to_read(self):
#         self.is_read = True
#         self.save(update_fields=['is_read'])

#     class Meta:
#         verbose_name = 'Prompt information'
#         verbose_name_plural = verbose_name
#         ordering = ['-create_date']

#     def __str__(self):
#         return '{}@了{}'.format(self.create_p, self.get_p)
