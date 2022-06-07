from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status

from app_api.models import Book


class BookView(ViewSet):
    """book view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single book """
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all books """
        books = Book.objects.all()

        # game_type = request.query_params.get('type', None)
        # if game_type is not None:
        #     games = games.filter(game_type_id=game_type)

        serializer = BookSerializer(books, many=True)
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

    # def update(self, request, pk):
    #     """(is working!! update function without validation)"""
    #     # Handle PUT requests for a game

    #     game = Game.objects.get(pk=pk)
    #     game.title = request.data["title"]
    #     game.maker = request.data["maker"]
    #     game.number_of_player = request.data["number_of_player"]
    #     game.skill_level = request.data["skill_level"]

    #     game_type = GameType.objects.get(pk=request.data["game_type"])
    #     game.game_type = game_type
    #     game.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def update(self, request, pk):
    #     """Handle PUT requests for a game
    #     update function with validation
    #     """
    #     game = Game.objects.get(pk=pk)
    #     game_type = GameType.objects.get(pk=request.data['game_type'])
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     # The original game object is passed to the serializer, along with the request.data
    #     # This will make any updates on the game object
    #     serializer = CreateGameSerializer(game, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(game_type=game_type, gamer=gamer)
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk):
    #     game = Game.objects.get(pk=pk)
    #     game.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)


class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books """
    class Meta:
        model = Book
        # Using depth to embed tables: fields need to revise to
        fields = ('id', 'title', 'cover_image_url', 'introduction', 'price')

# class CreateGameSerializer(serializers.ModelSerializer):
#     """use for create (validation received data from client)"""
#     class Meta:
#         model = Game
#         fields = ['id', 'title', 'maker', 'number_of_player', 'skill_level', 'game_type']
#         depth = 1
