# # -*- coding: utf-8 -*-
# from django import template
# from django.db.models.aggregates import Count
# from ..models import ToolCategory,ToolLink

# register = template.Library()


# @register.simple_tag
# def  get_toolcates ():
#     '''Get all tool categories, only display categories with tools'''
#     return ToolCategory.objects.annotate(total_num=Count('toollink')).filter(total_num__gt=0)


# @register.simple_tag
# def get_toollinks(cate):
#     '''Get all tools under a single category'''
#     return cate.toollink_set.all()


# @register.simple_tag
# def get_toollist_by_key(key=None):
#     '''Return to tool list'''
#     tools = []
#     if not key or key not in IZONE_TOOLS:
#         for _k in IZONE_TOOLS:
#             _tag = IZONE_TOOLS[_k]['tag']
#             _tools = IZONE_TOOLS[_k]['tools']
#             for each in _tools:
#                 item = {}
#                 item [ 'tag' ] =  _tag
#                 item['name'] = each['name']
#                 item['url'] = reverse(each['url'])
#                 item['img'] = static(each['img'])
#                 item['desc'] = each['desc']
#                 tools.append(item)
#     else:
#         _tag = IZONE_TOOLS[key]['tag']
#         _tools = IZONE_TOOLS[key]['tools']
#         for each in _tools:
#             item = {}
#             item [ 'tag' ] =  _tag
#             item['name'] = each['name']
#             item['url'] = reverse(each['url'])
#             item['img'] = static(each['img'])
#             item['desc'] = each['desc']
#             tools.append(item)
#     return tools


# @register.inclusion_tag('tool/tags/tool_item.html')
# def load_tool_item(item):
#     '''Return to a single tool display bar'''
#     return {'tool_item': item}