# from django.db import models


# # Create your models here.

# class ToolCategory(models.Model):
#     name = models.CharField('Website category name', max_length=20)
#     order_num = models.IntegerField('Serial Number', default=99,
#                                     help_text='Serial number can be used to adjust the order, the smaller the higher the front')

#     class Meta:
#         verbose_name = 'Tool category'
#         verbose_name_plural = verbose_name
#         ordering = ['order_num', 'id']

#     def __str__(self):
#         return self.name


# class ToolLink(models.Model):
#     name = models.CharField('site name', max_length=20)
#     description = models.CharField('Site Description', max_length=100)
#     link = models.URLField('Website Link')
#     order_num = models.IntegerField('Serial Number', default=99,
#                                     help_text='Serial number can be used to adjust the order, the smaller the higher the front')
#     category = models.ForeignKey(ToolCategory, verbose_name='Website Category', blank=True, null=True,
#                                  on_delete=models.SET_NULL)

#     class Meta:
#         verbose_name = 'Recommended tool'
#         verbose_name_plural = verbose_name
#         ordering = ['order_num', 'id']

#     def __str__(self):
#         return self.name
