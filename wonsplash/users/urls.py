from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("mylikes/", view=views.MyLikes.as_view(), name="user_likes"),
    path("<str:username>/", view=views.Profile.as_view(), name="user_profile"),
    path("<str:username>/followings/images/", view=views.MyFollowCollects.as_view(), name="following_images"),
    path("follow/<int:user_id>/", view=views.Following.as_view(), name="follow"),
    path("unfollow/<int:user_id>/", view=views.UnFollowing.as_view(), name="unfollow"),
    path("login/facebook/", views.FacebookLogin.as_view(), name="fb_login"),
]
