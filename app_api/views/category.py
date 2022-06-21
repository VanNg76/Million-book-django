from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Category


class CategoryView(ViewSet):
    """category view"""

    def list(self, request):
        """Handle GET requests to get all categories """
      
        categories = Category.objects.all().order_by('id')
        serializer = CategorySerializer(categories, many=True)
        
        return Response(serializer.data)

    def create(self, request):
        """Handle POST """

        category = Category.objects.create(
            name = request.data['name']
        )
        serializer = CategorySerializer(category)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """DELETE request"""
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories """
    class Meta:
        model = Category
        fields = ('id', 'name')
