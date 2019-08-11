from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("mylikes/", view=views.MyLikes.as_view(), name="user_likes"),
    path("<str:username>/", view=views.Profile.as_view(), name="user_profile"),
    path("follow/<int:user_id>/", view=views.Following.as_view(), name="follow"),
    path("unfollow/<int:user_id>/", view=views.UnFollowing.as_view(), name="unfollow"),
]
