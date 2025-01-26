# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SingleCommentManagerView,
    SinglePostManagerView,
    GroupOverviewView,
    CommentHandlerView,
    GroupDetailsView,
    FollowHandlerView,
    PostHandlerView,
)

router = DefaultRouter()

urlpatterns = [
    path("follow/", FollowHandlerView.as_view(), name="follow-list"),
    path("jwt/", include("rest_framework.urls", namespace="rest_framework")),

    path("posts/", PostHandlerView.as_view(), name="post-list"),
    path(
        "posts/<int:pk>/",
        SinglePostManagerView.as_view(),
        name="post-detail"
    ),
    path(
        "posts/<int:post_id>/comments/",
        CommentHandlerView.as_view(),
        name="comment-list",
    ),
    path(
        "posts/<int:post_id>/comments/<int:pk>/",
        SingleCommentManagerView.as_view(),
        name="comment-detail",
    ),
    path("groups/", GroupOverviewView.as_view(), name="group-list"),
    path("groups/<int:pk>/", GroupDetailsView.as_view(), name="group-detail"),
    
]
