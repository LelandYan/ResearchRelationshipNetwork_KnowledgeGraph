from django.conf.urls import url
from . import views
from . import entity
from . import search_list

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload$', views.upload, name='upload'),
    url(r'^entity$', entity.search_entity, name='entity'),
    url(r'^searchList$', search_list.search_list, name='searchList'),

    url(r'^ajax_return_paper/$', entity.ajax_return_paper, name='ajax_return_paper'),
    url(r'^ajax_extInfo/$', entity.ajax_extInfo, name='ajax_extInfo'),
    url(r'^ajax_rec_coauthor/$', entity.ajax_rec_coauthor, name='ajax_rec_coauthor'),

    url(r'^', views.notfound, name='notfound')
]
