from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from snippets.views import api_root, SnippetViewSet, UserViewSet

""" router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')
router.register(r'users', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
] """

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})


urlpatterns = [
    path('', api_root),
    path('users/', user_list, name='users-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('snippets/', snippet_list, name='snippets-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight', snippet_highlight, name='snippet-highlight')
]

""" urlpatterns = [
    path('', api_root),
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-detail'),
    path('snippets/', SnippetsList.as_view(), name='snippets-list'),
    path('snippets/<int:pk>/', SnippetDetails.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight', SnippetHighlight.as_view(), name='snippet-highlight')
] """

""" from snippets.views import snippet_details, snippets_list

urlpatterns = [
    path('snippets/', snippets_list),
    path('snippets/<int:pk>/', snippet_details)
] """

urlpatterns = format_suffix_patterns(urlpatterns)