from django.urls import path

from blog import views
from blog.views import PostListView

urlpatterns = [
    path("", views.index, name="home"),
    path("show_all_categories/", views.show_all_categories, name="show_all_categories"),
    path("show_category/<int:id>/", views.show_category, name="show_category"),
    path("update_category/", views.update_category, name="update_category"),
    path("delete_category/<int:id>/", views.delete_category, name="delete_category"),
    path("create_category/", views.create_category, name="create_category"),
    path("show_all_posts/", PostListView.as_view(), name="show_all_posts"),
    path("update_post/<int:pk>/", views.PostUpdateView.as_view(), name="update_post"),
    path("register_user/", views.register_user, name="register_user"),
    path('like_post/<int:id>/', views.like_dislike_post, name='like_post'),
]
