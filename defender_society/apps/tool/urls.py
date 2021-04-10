# from django.urls import path
# from .views import (Toolview, BD_pushview, BD_pushview_site,
#                      regexview, useragent_view, html_characters,
#                      docker_search_view, editor_view,
#                      )

# urlpatterns = [
#      path('', Toolview, name='total'), # Tool summary page
#      path('baidu-linksubmit/', BD_pushview, name='baidu_push'), # Baidu actively push
#      path('baidu-linksubmit-sitemap/', BD_pushview_site, name='baidu_push_site'), # Baidu actively pushes sitemap
#      path('regex/', regexview, name='regex'), # regular expression online
#      path('user-agent/', useragent_view, name='useragent'), # user-agent generator
#      path('html-special-characters/', html_characters, name='html_characters'), # HTML special character query
#      path('docker-search/', docker_search_view, name='docker_search'), #docker mirror query
#      path('markdown-editor/', editor_view, name='markdown_editor'), # editor.md tool
# ]