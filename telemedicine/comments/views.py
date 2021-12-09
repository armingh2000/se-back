from users.models import Patient, Doctor, User
from rest_framework.views import APIView
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Comment


# Create your views here.

class CreateCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        if not user.is_patient:
            return Response('user must be patient to comment', status=status.HTTP_403_FORBIDDEN)

        doctor_user = get_object_or_404(User, pk=request.data['doctor_pk'])
        if doctor_user.pk == user.pk:
            return Response('doctor and patient are the same', status=status.HTTP_409_CONFLICT)

        body = request.data['body']
        if len(body) == 0:
            return Response('comment is empty', status=status.HTTP_400_BAD_REQUEST)

        doctor = Doctor.objects.get(user=doctor_user)
        patient = Patient.objects.get(user=user)

        Comment.objects.create(doctor=doctor, patient=patient, body=body)

        return Response(status=status.HTTP_201_CREATED)

class CommentListView(APIView):
    def get(self, request):
        doctor_pk = request.GET['doctor_pk']
        doctor_user = get_object_or_404(User, pk=doctor_pk)
        doctor = get_object_or_404(Doctor, user=doctor_user)
        comment_list = Comment.objects.filter(doctor=doctor)
        comment_list = CommentSerializer(comment_list, many=True).data

        return Response(comment_list, status=status.HTTP_200_OK)
