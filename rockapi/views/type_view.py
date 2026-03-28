"""View module for handling requests for type data"""

from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rockapi.models import Type


class TypeView(ViewSet):
    """Rock API types view"""

    def list(self, request):
        """Handle GET requests to get all types

        Returns:
            Response -- JSON serialized list of types
        """

        try:
            # Type.objects.all() uses Django's ORM to run SELECT * FROM rockapi_type
            types = Type.objects.all()
            # Serialize the list of types and return the JSON
            serialized = TypeSerializer(types, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Status 200 OK if type found, 404 Not Found if not found, 500 Server Error if anything else goes wrong
            Response -- JSON serialized type record
        """
        try:
            rock_type = Type.objects.get(pk=pk)
            serialized = TypeSerializer(rock_type)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Type.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TypeSerializer(serializers.ModelSerializer):
    """JSON serializer for types"""

    class Meta:
        model = Type
        fields = (
            "id",
            "label",
        )
