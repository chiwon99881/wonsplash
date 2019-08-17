from django.urls import path
from . import views

app_name = "collects"
urlpatterns = [
    path("", view=views.Feed.as_view(), name="feed"),
    path("like/<int:image_id>/", view=views.Like.as_view(), name="like_image"),
    path("unlike/<int:image_id>/", view=views.UnLike.as_view(), name="unlike_image"),
    path("search/", view=views.Search.as_view(), name="search"),
    path("post/", view=views.Post.as_view(), name="post"),
    path("detail/<int:image_id>/", view=views.Detail.as_view(), name="detail"),
    path("<str:username>/followings/", view=views.MyFollowCollects.as_view(), name="followings_images"),
]
