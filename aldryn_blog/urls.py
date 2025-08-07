# -*- coding: utf-8 -*-
from django.urls import re_path

from aldryn_blog.feeds import CategoryFeed, LatestEntriesFeed, TagFeed
from aldryn_blog.views import (ArchiveView, AuthorEntriesView, AuthorsListView, CategoryListView, CategoryPostListView,
                               PostDetailView, TaggedListView, TagsListView)

app_name = 'aldryn_blog'

urlpatterns = [
    re_path(r'^$', ArchiveView.as_view(), name='latest-posts'),
    re_path(r'^author/$', AuthorsListView.as_view(), name='author-list'),
    re_path(r'^author/(?P<slug>[\w.@+-]+)/$', AuthorEntriesView.as_view(), name='author-posts'),
    re_path(r'^feed/$', LatestEntriesFeed(), name='latest-posts-feed'),
    re_path(r'^(?P<year>\d{4})/$', ArchiveView.as_view(), name='archive-year'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', ArchiveView.as_view(), name='archive-month'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', ArchiveView.as_view(), name='archive-day'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',
        PostDetailView.as_view(), name='post-detail'),
    re_path(r'^category/$', CategoryListView.as_view(), name='category-list'),
    re_path(r'^category/(?P<category>[-\w]+)/$', CategoryPostListView.as_view(), name='category-posts'),
    re_path(r'^category/(?P<category>[-\w]+)/feed/$', CategoryFeed(), name='category-posts-feed'),
    re_path(r'^tag/$', TagsListView.as_view(), name='tag-list'),
    re_path(r'^tag/(?P<tag>[-\w]+)/$', TaggedListView.as_view(), name='tagged-posts'),
    re_path(r'^tag/(?P<tag>[-\w]+)/feed/$', TagFeed(), name='tagged-posts-feed'),
]
