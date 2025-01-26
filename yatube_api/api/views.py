from rest_framework import generics, permissions
from rest_framework.response import Response
from posts.models import Post, Comment, Group, Follow
from django.contrib.auth import get_user_model
from .pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)
from rest_framework import serializers

User = get_user_model()


class PostHandlerView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        group_id = self.request.data.get("group")
        if group_id:
            group = Group.objects.filter(pk=group_id).first()
            if not group:
                raise serializers.ValidationError({"group": "Specified group does not exist."})
        else:
            group = None
        serializer.save(author=self.request.user, group=group)


class SinglePostManagerView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"detail": "You are not authorized to update this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {"detail": "You are not authorized to delete this post."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class CommentHandlerView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    pagination_class = None

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"])

    def perform_create(self, serializer):
        post = Post.objects.filter(pk=self.kwargs["post_id"]).first()
        if not post:
            raise serializers.ValidationError({"detail": "The specified post does not exist."})
        serializer.save(author=self.request.user, post=post)


class SingleCommentManagerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_id"], pk=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "You are not authorized to update this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user:
            return Response(
                {"detail": "You are not authorized to delete this comment."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)


class GroupOverviewView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
    ordering = ['title']


class GroupDetailsView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowHandlerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        follows = Follow.objects.filter(user=request.user)
        search_query = request.query_params.get("search")
        if search_query:
            follows = follows.filter(following__username__icontains=search_query)
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        following_username = serializer.validated_data.get("following")
        following_user = User.objects.filter(username=following_username).first()

        if not following_user:
            return Response(
                {"detail": f"User '{following_username}' not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user == following_user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(user=request.user, following=following_user).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        follow_instance = Follow.objects.create(user=request.user, following=following_user)
        return Response(
            FollowSerializer(follow_instance).data,
            status=status.HTTP_201_CREATED,
        )
