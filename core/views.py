from django.shortcuts import render
from rest_framework import views
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import FileSystemStorage
from core.serializers import ProfileSerializer, PostSerializer, CommentSerializer
from core.models import Profile, Post, Comment
import json
from rest_framework.schemas.openapi import SchemaGenerator


class EndpointsView(views.APIView):

    def get(self, request, format=None):

        generator = SchemaGenerator(title='Social Web API')
        schema = generator.get_schema()

        data = {path: [method for method in schema['paths'][path]] for path in schema['paths']}

        return Response(data=data, status=status.HTTP_200_OK)


class ProfileView(views.APIView):
    parser_classes = [FileUploadParser]

    def get(self, request, format=None):

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, filename='request.json', format=None):
        if 'file' not in request.data:
            return Response({'detail': 'None JSON file sended'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']

        with file_obj.open() as file:
            data = json.load(file)

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # fs = FileSystemStorage()
        # filename = fs.save(file_obj.name, file_obj)


class ProfileDetailView(views.APIView):
    parser_classes = [FileUploadParser]

    def get(self, request, pk, format=None):

        user = get_object_or_404(Profile, pk=pk)
        data = ProfileSerializer(data=user)

        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request, pk, filename='request.json', format=None):
        if 'file' not in request.data:
            return Response({'detail': 'None JSON file sended'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']

        with file_obj.open() as file:
            data = json.load(file)

        # fs = FileSystemStorage()
        # filename = fs.save(file_obj.name, file_obj)

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):

        user = get_object_or_404(Profile, pk=pk)
        user.delete()

        return Response(data={'detail': 'User deleted with success'}, status=status.HTTP_200_OK)


class PostView(views.APIView):

    def get(self, request, format=None):

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProfilePostsView(views.APIView):

    def get(self, request, pk, format=None):

        posts = Post.objects.filter(user__id=pk)
        serializer = PostSerializer(posts, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostCommentView(views.APIView):

    def get(self, request, format=None):

        posts_data = []
        for post in Post.objects.all():
            comments = Comment.objects.filter(post=post)
            comments_serializer = CommentSerializer(comments, many=True)

            post_serializer = PostSerializer(post)
            post_data = post_serializer.data
            post_data['comments'] = comments_serializer.data

            posts_data.append(post_data)

        return Response(data=posts_data, status=status.HTTP_200_OK)


class PostCommentDetailView(views.APIView):

    def get(self, request, pk, format=None):

        post = get_object_or_404(Post, pk=pk)

        comments = Comment.objects.filter(post=post)
        comments_serializer = CommentSerializer(comments, many=True)

        post_serializer = PostSerializer(post)
        post_data = post_serializer.data
        post_data['comments'] = comments_serializer.data

        return Response(data=post_data, status=status.HTTP_200_OK)


class CommentView(views.APIView):

    def get(self, request, post_id, format=None):

        comments = Comment.objects.filter(post__id=post_id)
        comments_serializer = CommentSerializer(comments, many=True)

        return Response(data=comments_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, post_id, filename='request.json', format=None):
        if 'file' not in request.data:
            return Response({'detail': 'None JSON file sended'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']

        with file_obj.open() as file:
            data = json.load(file)

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            post = get_object_or_404(Post, id=post_id)
            serializer.post = post
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(views.APIView):

    def get(self, request, post_id, comment_id, format=None):

        comment = Comment.objects.filter(post__id=post_id, id=comment_id)
        if comment:
            comment_serializer = CommentSerializer(comment)

            return Response(data=comment_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request,  post_id, comment_id, filename='request.json', format=None):
        if 'file' not in request.data:
            return Response({'detail': 'None JSON file sended'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']

        with file_obj.open() as file:
            data = json.load(file)

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            post = get_object_or_404(Post, id=post_id)
            serializer.post = post
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id, format=None):

        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()

        return Response(data={'detail': 'Comment deleted with success'}, status=status.HTTP_200_OK)


class ReportView(views.APIView):

    def get(self, request, format=None):
        data = []

        for profile in Profile.objects.all():
            data.append(
                {
                    'pk': profile.pk,
                    'name': profile.name,
                    'total_posts': Post.objects.filter(user=profile).count(),
                    'total_comments': Comment.objects.filter(post__user=profile).count(),
                }
            )

        return Response(data=data, status=status.HTTP_200_OK)
