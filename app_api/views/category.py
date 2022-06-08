from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Category


class CategoryView(ViewSet):
    """category view"""

    # def retrieve(self, request, pk):
    #     """Handle GET requests for single book """
    #     try:
    #         book = Book.objects.get(pk=pk)
    #         serializer = BookSerializer(book)
    #         return Response(serializer.data)
    #     except Book.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all categories """
      
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        
        return Response(serializer.data)

    # def create(self, request):
    #     """Handle POST operations
    #     Returns
    #         Response -- JSON serialized game instance
    #     """

    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     game_type = GameType.objects.get(pk=request.data['game_type'])
    #     game = Game.objects.create(
    #         title = request.data['title'],
    #         maker = request.data['maker'],
    #         number_of_player = request.data['number_of_player'],
    #         skill_level = request.data['skill_level'],
    #         gamer=gamer,
    #         game_type=game_type
    #     )
    #     serializer = GameSerializer(game)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

        # works to create a game, but does not pass test
        # serializer = CreateGameSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(gamer=gamer, game_type=game_type)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)


    # def destroy(self, request, pk):
    #     game = Game.objects.get(pk=pk)
    #     game.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories """
    class Meta:
        model = Category
        # Using depth to embed tables: fields need to revise to
        fields = ('id', 'name')

# class CreateGameSerializer(serializers.ModelSerializer):
#     """use for create (validation received data from client)"""
#     class Meta:
#         model = Game
#         fields = ['id', 'title', 'maker', 'number_of_player', 'skill_level', 'game_type']
#         depth = 1
