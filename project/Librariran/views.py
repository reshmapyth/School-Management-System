from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from accounts.models import *
from .serializers import LibraryHistorySerializer, FeesHistorySerializer

class LibraryHistoryView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        library_history = LibraryHistory.objects.all()
        serializer = LibraryHistorySerializer(library_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = LibraryHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required to update the details."}, status=status.HTTP_400_BAD_REQUEST)

        library_history = get_object_or_404(LibraryHistory, id=id)
        serializer = LibraryHistorySerializer(library_history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        library_history = get_object_or_404(LibraryHistory, id=id)
        library_history.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class FeesHistoryView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        fees_history = FeesRemarks.objects.all()
        serializer = FeesHistorySerializer(fees_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FeesHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required to update the details."}, status=status.HTTP_400_BAD_REQUEST)

        fees_history = get_object_or_404(FeesRemarks, id=id)
        serializer = FeesHistorySerializer(fees_history, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response({"error": "'id' is required in the body."}, status=status.HTTP_400_BAD_REQUEST)

        fees_history = get_object_or_404(FeesRemarks, id=id)
        fees_history.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
