from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^registration$', views.registration), 
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^addtrip$', views.addtrip),
    url(r'^addtrip_page$', views.addtrip_page),
    url(r'^jointrip/(?P<id>\w+)$', views.jointrip),
    url(r'^viewtrip/(?P<id>\w+)$', views.viewtrip), 
]