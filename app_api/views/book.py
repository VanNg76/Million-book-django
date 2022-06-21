from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q
# from rest_framework.decorators import action

from app_api.models import Book, Category


class BookView(ViewSet):
    """book view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single book """
        try:
            book = Book.objects.get(pk=pk)
            
            # filter by ManyToMany relationship
            categoryArray = Category.objects.filter(books__id=pk)
            # then use set() to set the result to property 'categories'
            book.categories.set(categoryArray)

            serializer = BookSerializer(book)
            return Response(serializer.data)

        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all books """

        # filter books by category
        category = request.query_params.get('category', None)
        
        # filter books before or after publication date
        pub_date = request.query_params.get('published_date', None)
        is_before = request.query_params.get('before', None)
        
        # search books by title
        search_title = request.query_params.get('title', None)
        
        # search books by author name
        search_author_name = request.query_params.get('author_name', None)

        user = request.auth.user
        if user.is_staff == 1:
            books = Book.objects.all()
        else:
            # only get books that has inventory > 0 
            books = Book.objects.filter(inventory__quantity__gt=0)
            
        if category is not None:
            books = books.filter(categories__id = int(category))

        if pub_date is not None:
            if is_before == 'true':
                books = books.filter(publication_date__lte = pub_date)
            else:
                books = books.filter(publication_date__gt = pub_date)

        if search_title is not None:
            books = books.filter(
                Q(title__contains=search_title)
            )

        if search_author_name is not None:
            books = books.filter(
                Q(author__name__contains=search_author_name)
            )

        books = books.order_by('id')
        serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data)


    def create(self, request):
        """Handle POST new book """
        
        book = Book.objects.create(
            title = request.data['title'],
            introduction = request.data['introduction'],
            publication_date = request.data['publication_date'],
            price = request.data['price'],
            author_id = request.data['author_id'],
            cover_image_url = request.data['cover_image_url']
        )
        
        serializer = CreateBookSerializer(book)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        """Handle PUT request for book"""
        
        book = Book.objects.get(pk=pk)
        book.title = request.data["title"]
        book.introduction = request.data["introduction"]
        book.publication_date = request.data["publication_date"]
        book.price = request.data["price"]
        book.author_id = request.data["author_id"]
        book.cover_image_url = request.data["cover_image_url"]
        book.save()
        
        # if categories send back from client, below 3 line will
        # remove all related records in joined table and add new records into joined table
        # book.refresh_from_db()
        # book.categories.remove(*book.categories.all())
        # book.categories.add(*request.data['categories'])
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk):
        """DELETE request"""
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books """
    class Meta:
        model = Book
        fields = ('id', 'title', 'introduction', 'price', 'publication_date', 'author', 'cover_image_url')
        depth = 1

class CreateBookSerializer(serializers.ModelSerializer):
    """JSON serializer for new book """
    class Meta:
        model = Book
        fields = ('id', 'title', 'introduction', 'price', 'publication_date', 'author_id', 'cover_image_url')
