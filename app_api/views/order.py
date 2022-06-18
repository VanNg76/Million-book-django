from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
import datetime

from app_api.models import Order, OrderBook, Inventory
from app_api.views.orderbook import OrderBookSerializer


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
        user = request.auth.user
        if user.is_staff == 1:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.auth.user)

        for order in orders:
            order.total_value = 0
            # order.ordered_books is having 'RelatedManager' object is not iterable
            # call all() to  retrieve the elements from the manager
            for ordered_book in order.ordered_books.all():
                value = ordered_book.quantity * ordered_book.book.price
                order.total_value += value

        serializer = OrderSerializer(orders, many=True)
        
        return Response(serializer.data)


    def create(self, request):
        """Handle POST """
        user = request.auth.user
        try:
            order = Order.objects.get(user=user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            order = Order.objects.create(
                user = user,
                date = datetime.date.today()
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk):
        """DELETE request"""
        order = Order.objects.get(pk=pk)
        orderbooks = OrderBook.objects.filter(order=order)
        for ob in orderbooks:
            inventory = Inventory.objects.get(book_id=ob.book_id)
            inventory.quantity += ob.quantity
            inventory.save()
            ob.delete()
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for order """
    ordered_books = OrderBookSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ('id', 'date', 'ordered_books', 'user', 'total_value')
        depth = 1
