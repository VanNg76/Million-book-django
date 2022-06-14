from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.db.models import Q

from app_api.models import Book, OrderBook, Order, Inventory
from app_api.views.book import BookSerializer


class OrderBookView(ViewSet):
    """orderbook view"""
    
    def list(self, request):
        """GET"""

        orderbooks = OrderBook.objects.all()
        serializer = CreateOrderBookSerializer(orderbooks, many=True)
        
        return Response(serializer.data)

    def create(self, request):
        """add a book to current user order """
        book_id = request.data['book_id']
        order_id = request.data['order_id']
        quantity = request.data['quantity']
        
        inventory = Inventory.objects.get(book_id=book_id)
        
        try:
            # if book exists in order, it allows change quantity
            orderbook = OrderBook.objects.get(
                book_id=book_id,
                order_id=order_id
            )
            # check if inventory is enough to change order
            if quantity <= inventory.quantity:
                inventory.quantity += orderbook.quantity    # return old order quantity to inventory
                orderbook.quantity=quantity
                orderbook.save()
                inventory.quantity -= quantity  # deduct inventory by new request quantity
                inventory.save()
            else:                   # never happend because front-end has prevent it to happend
                orderbook.quantity=-1
                orderbook.save()

        except OrderBook.DoesNotExist:
            # if book not exists in order, add it to order:
            orderbook = OrderBook.objects.create(
                book_id=book_id,
                order_id=order_id,
                quantity=quantity
            )
            # check if inventory is enough to add to order
            if quantity <= inventory.quantity:
                inventory.quantity -= quantity
                inventory.save()
            else:
                orderbook.quantity=-1
                orderbook.save()

        serializer = CreateOrderBookSerializer(orderbook)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk):
        """DELETE request"""
        orderbook = OrderBook.objects.get(pk=pk)
        inventory = Inventory.objects.get(book_id=orderbook.book_id)

        # return quantity to inventory
        inventory.quantity += orderbook.quantity
        inventory.save()

        # delete orderbook
        orderbook.delete()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CreateOrderBookSerializer(serializers.ModelSerializer):
    """JSON serializer for orderbook """
    class Meta:
        model = OrderBook
        fields = ('id', 'order_id', 'book_id', 'quantity')

class OrderBookSerializer(serializers.ModelSerializer):
    """JSON serializer for orderbook """
    book = BookSerializer()
    class Meta:
        model = OrderBook
        fields = ('id', 'book', 'quantity')
