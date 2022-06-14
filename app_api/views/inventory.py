from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Inventory


class InventoryView(ViewSet):
    """inventory view"""

    def list(self, request):
        """Handle GET requests to get all inventories """

        inventories = Inventory.objects.all()

        # filter books by category
        book = request.query_params.get('book', None)
        
        if book is not None:
            inventories = inventories.filter(book=book)

        serializer = InventorySerializer(inventories, many=True)
        return Response(serializer.data)


    def create(self, request):
        """Handle POST """
        book_id = request.data['book_id']
        quantity = request.data['quantity']
        try:
            inventory = Inventory.objects.get(book_id=book_id)
            inventory.quantity = quantity
            inventory.save()
            serializer = InventorySerializer(inventory)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Inventory.DoesNotExist:
            inventory = Inventory.objects.create(
                book_id = book_id,
                quantity = quantity
            )
            serializer = CreateInventorySerializer(inventory)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventorySerializer(serializers.ModelSerializer):
    """JSON serializer for inventories """
    class Meta:
        model = Inventory
        fields = ('id', 'quantity', 'book')
        depth = 1

class CreateInventorySerializer(serializers.ModelSerializer):
    """JSON serializer for inventories """
    class Meta:
        model = Inventory
        fields = ('id', 'quantity', 'book_id')
