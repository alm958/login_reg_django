from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index' ),
    url(r'^login$', views.login, name='login' ),
    url(r'^register$', views.register, name='register' ),
    url(r'^logout$', views.logout, name='logout' ),
    url(r'^showusers/(?P<id>\d*)$', views.showusers, name='showusers' ),
    url(r'^edituser/(?P<id>\d+)$', views.edituser, name='edituser' ),
    url(r'^updateuser/(?P<id>\d+)$', views.updateuser, name='updateuser' ),
    url(r'^deleteuser/(?P<id>\d+)$', views.deleteuser, name='deleteuser' ),
    url(r'^del_user_prompt/(?P<id>\d+)$', views.del_user_prompt, name='del_user_prompt' ),
    url(r'^keep_user/(?P<id>\d+)$', views.keep_user, name='keep_user' ),
]
