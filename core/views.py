from django.shortcuts import render
from rest_framework import views
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from django.core.files.storage import FileSystemStorage
from core.serializers import ProfileSerializer
from core.models import Profile
import json


class ProfileView(views.APIView):
    parser_classes = [FileUploadParser]

    def get(self, request, filename, format=None):

        if 'file' not in request.data:
            return Response({'detail': 'None JSON file sended'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']
        with file_obj.open() as file:
            data = json.load(file)
            print(data)

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, filename, format=None):
        file_obj = request.data['file']
        # print(file_obj)
        with file_obj.open() as file:
            data = json.load(file)
            print(data)
        # print(dir(file_obj))
        print('############\n\n')
        # fs = FileSystemStorage()
        # filename = fs.save(file_obj.name, file_obj)

        return Response(status=204)


class ProfileDetailView(views.APIView):
    parser_classes = [FileUploadParser]

    def get(self, request, pk, format=None):

        user = get_object_or_404(Profile, pk=pk)
        data = ProfileSerializer(data=user)

        return Response(data=data, status=status.HTTP_201_CREATED)

    def put(self, request, filename, pk, format=None):
        if 'file' not in request.data:
            return Response({'detail': 'None JSON file sended'}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']
        # print(file_obj)
        with file_obj.open() as file:
            data = json.load(file)
            print(data)
        # print(dir(file_obj))
        print('############\n\n')
        # fs = FileSystemStorage()
        # filename = fs.save(file_obj.name, file_obj)
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(data, status=200)

    def delete(self, request, pk, format=None):

        user = get_object_or_404(Profile, pk=pk)
        user.delete()

        return Response(data={'detail': 'User deleted with success'}, status=status.HTTP_200_OK)
