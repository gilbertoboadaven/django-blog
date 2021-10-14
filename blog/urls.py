from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    #Auth
    path('blog/register',views.register,name="user_register"),
    path('blog/login',views.ingreso,name="user_login"),
    path('blog/logout',views.salir,name="user_logout"),
    #Blog
    path('blog/',views.post_list,name="post_list"),
    path('blog/add',views.post_add,name="post_add"),
    path('blog/<slug:post>/',views.post_detail,name="post_detail"),
    path('blog/tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
]