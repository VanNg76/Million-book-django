from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Author


class AuthorView(ViewSet):
    """author view"""


    def list(self, request):
        """Handle GET requests to get all authors """
      
        authors = Author.objects.all().order_by('id')
        serializer = AuthorSerializer(authors, many=True)
        
        return Response(serializer.data)


    def create(self, request):
        """Handle POST """

        author = Author.objects.create(
            name = request.data['name']
        )
        serializer = AuthorSerializer(author)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        """DELETE request"""
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class AuthorSerializer(serializers.ModelSerializer):
    """JSON serializer for author """
    class Meta:
        model = Author
        fields = ('id', 'name')


