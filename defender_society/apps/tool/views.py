# from django.shortcuts import render
# from django.http import JsonResponse
# from django.utils.html import mark_safe
# from django.core.cache import cache
# from .apis.bd_push import push_urls, get_urls
# from .apis.useragent import get_user_agent
# #from .apis.docker_search import DockerSearch
# #from .utils import IMAGE_LIST


# import re
# import markdown


# # Create your views here.

# def Toolview(request):
#     return render(request,'tool/tool.html')


# # Baidu Active Push
# def BD_pushview(request):
#     if request.is_ajax() and request.method == "POST":
#         data = request.POST
#         url = data.get('url')
#         urls = data.get('url_list')
#         info = push_urls(url, urls)
#         return JsonResponse({'msg': info})
#     return render(request,'tool/bd_push.html')

# # Baidu actively pushes the upgraded version, extracts the sitemap link and pushes
# def BD_pushview_site(request):
#     if request.is_ajax() and request.method == "POST":
#         data = request.POST
#         url = data.get('url')
#         map_url = data.get('map_url')
#         urls = get_urls(map_url)
#         if urls =='miss':
#             info = "{'error':404,'message':'sitemap address request timed out, please check the link address!'}"
#         elif urls =='':
#             info = "{'error':400,'message':'The sitemap page did not extract a valid link, the sitemap format is not standardized.'}"
#         else:
#             info = push_urls(url, urls)
#         return JsonResponse({'msg': info})
#     return render(request,'tool/bd_push_site.html')

# # Online regular expression
# def regexview(request):
#     if request.is_ajax() and request.method == "POST":
#         data = request.POST
#         texts = data.get('texts')
#         regex = data.get('r')
#         key = data.get('key')
#         try:
#             lis = re.findall(r'{}'.format(regex), texts)
#         except:
#             lis = []
#         num = len(lis)
#         if key =='url' and num:
#             script_tag ='''<script>$(".re-result p").children("a").attr({target:"_blank",rel:"noopener noreferrer"});</script>'''
#             result ='<br>'.join(['[{}]({})'.format(i,i) for i in lis])
#         else:
#             script_tag =''
#             info ='\n'.join(lis)
#             result = "Matched&nbsp;{}&nbsp;results:\n".format(num) + "```\n" + info + "\n```"
#         result = markdown.markdown(result, extensions=[
#             'markdown.extensions.extra',
#             'markdown.extensions.codehilite',
#         ])
#         return JsonResponse({'result': mark_safe(result+script_tag),'num': num})
#     return render(request,'tool/regex.html')

# # Generate request header
# def useragent_view(request):
#     if request.is_ajax() and request.method == "POST":
#         data = request.POST
#         d_lis = data.get('d_lis')
#         os_lis = data.get('os_lis')
#         n_lis = data.get('n_lis')
#         d = d_lis.split(',') if len(d_lis)> 0 else None
#         os = os_lis.split(',') if len(os_lis)> 0 else None
#         n = n_lis.split(',') if len(n_lis)> 0 else None
#         result = get_user_agent(os=os, navigator=n, device_type=d)
#         return JsonResponse({'result': result})
#     return render(request,'tool/useragent.html')

# # HTML special character comparison table
# def html_characters(request):
#     return render(request,'tool/characters.html')

# # docker mirror query
# def docker_search_view(request):
#     if request.is_ajax() and request.method == "POST":
#         data = request.POST
#         name = data.get('name')
#         # Only the name search in the common mirror list uses the cache, which can avoid name filtering
#         if name in IMAGE_LIST:
#             cache_key ='tool_docker_search_' + name
#             cache_value = cache.get(cache_key)
#             if cache_value:
#                 res = cache_value
#             else:
#                 ds = DockerSearch(name)
#                 res = ds.main()
#                 total = res.get('total')
#                 if total and total >= 20:
#                     # Cache resources with more than 20 mirror information for one day
#                     cache.set(cache_key, res, 60*60*24)
#         else:
#             ds = DockerSearch(name)
#             res = ds.main()
#         return JsonResponse(res, status=res['status'])
#     return render(request,'tool/docker_search.html')

# def editor_view(request):
#     return render(request,'tool/editor.html')
