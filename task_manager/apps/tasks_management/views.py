from django.shortcuts import render
from .serializers import TaskManagerSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response
from apps.tasks_management.models import TaskManager
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'page_size'
    max_page_size = 100

class TaskManagerView(viewsets.ModelViewSet):
    queryset = TaskManager.objects.all()
    serializer_class = TaskManagerSerializer
    lookup_field = 'task_unique_id'
    pagination_class = CustomPagination  # Add this line

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "success",
                "message": "Tasks retrieved successfully",
                "data": serializer.data
            })

        # Fallback for non-paginated response
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Tasks retrieved successfully",
            "data": serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "status": "success",
                "message": "Task created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": serializer.errors,
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        
        # The get_object() will now use project_unique_id automatically
        task = self.get_object()  
    
        serializer = self.get_serializer(task, data=request.data, partial=None)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    
        custom_response = {
            "status": "success",
            "message": "Project updated successfully",
            "data": serializer.data
        }
        return Response(custom_response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # The get_object() will now use project_unique_id automatically
        task = self.get_object()  
        task.is_deleted = True
        task.save()
    
        custom_response = {
            "status": "success",
            "message": "Project deleted successfully",
            "data": {
                "task_unique_id": task.task_unique_id,
                "task_name": task.task_name
            }
        }
        return Response(custom_response, status=status.HTTP_200_OK)