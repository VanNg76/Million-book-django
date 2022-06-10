from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Order, OrderBook, Book, Inventory
from app_api.views.book import BookSerializer


class OrderView(ViewSet):
    """order view"""

    # def retrieve(self, request, pk):
    #     """Handle GET requests for single book """
    #     try:
    #         book = Book.objects.get(pk=pk)
    #         serializer = BookSerializer(book)
    #         return Response(serializer.data)
    #     except Book.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all order, related books and inventory"""
      
        orders = Order.objects.filter(user=request.auth.user)
        for order in orders:
            order.books = []
            order.total_value = 0

            orderbooks = OrderBook.objects.filter(order_id=order.id)
            for ob in orderbooks:
                book = Book.objects.get(pk=ob.book_id)
                book.order_quantity = ob.quantity
                value = book.order_quantity * book.price
                order.total_value += value
                order.books.append(book)

        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data)


    # def create(self, request):
    #     """Handle POST """

    #     category = Category.objects.create(
    #         name = request.data['name']
    #     )
    #     serializer = CategorySerializer(category)
        
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for order """
    books = BookSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ('id', 'date', 'books', 'user', 'total_value')
        depth = 1
