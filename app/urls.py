from django.urls import path
from .views import Homeview,\
    detail_post,\
    write_a_post,\
    counting_post,\
    find_in_site,\
    get_client_ip,\
    last_hour_published_post\

urlpatterns = [
    path('homepage/', Homeview.as_view(), name='homepage'),
    path('detail_post/<int:pk>', detail_post, name='detail_post'),
    path('write_a_post/', write_a_post, name='write_a_post'),
    path('counting_post/', counting_post, name='counting_post'),
    path('find_in_site/', find_in_site, name='find_in_site'),
    path('get_client_ip/', get_client_ip, name='get_client_ip'),
    path('last_hour_published_post/', last_hour_published_post, name='last_hour_published_post'),

]