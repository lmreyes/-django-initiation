from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),

    url(r'^v1/news-item/$', views.get_list_news_items, name='news_item_list'),
    url(r'^v1/news-item/(?P<pk>[0-9]+)/$', views.get_news_item_detail, name='news_item_detail'),
    url(r'^v1/news-item/new/$', views.new_news_item, name='new_news_item'),
    url(r'^v1/news-item/(?P<pk>[0-9]+)/edit/$', views.news_item_edit, name='news_item_edit'),
    url(r'^v1/news-item/(?P<pk>[0-9]+)/delete/$', views.news_item_delete, name='news_item_delete'),

    url(r'^v2/event/$', views.EventList.as_view(), name='event_list'),
    url(r'^v2/event/(?P<pk>[0-9]+)/$', views.EventDetail.as_view(), name='event_detail'),
    url(r'^v2/event/new/$', views.EventCreate.as_view(), name='create_event'),
    url(r'^v2/event/(?P<pk>[0-9]+)/edit/$', views.EventUpdate.as_view(), name='edit_event'),
    url(r'^v2/news-item/(?P<pk>[0-9]+)/delete/$', views.EventDelete.as_view(), name='delete_event'),

    url(r'^all/$', views.AllNews.as_view(), name='all'),
]
