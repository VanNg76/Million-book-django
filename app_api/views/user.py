"""View module for handling requests about post"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserView(ViewSet):
    """ User view """

    def retrieve(self, request, pk):
        """ single user """
        try:
            if pk == '0':
                user = request.auth.user
            else:
                user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)

            return Response(serializer.data)

        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for User """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_staff', 'username')
