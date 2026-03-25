"""View module for handling requests about rocks"""

# HttpResponseServerError returns a 500 status code when an unexpected server-side
# error occurs (i.e. something broke in our code, not a bad request from the client)
from django.http import HttpResponseServerError

# serializers  - converts complex data types (like Django model instances) to/from
#                JSON so data can be sent over the API
# status       - contains HTTP status code constants like status.HTTP_200_OK (200),
#                status.HTTP_404_NOT_FOUND (404), etc. so we don't have to hardcode numbers
# Response     - DRF's response class that automatically handles converting data to JSON
# ViewSet      - base class that groups related HTTP method handlers (list, create,
#                retrieve, update, destroy) into a single class
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

# Import User model to expand the user foreign key on Rock
from django.contrib.auth.models import User

# The Rock model represents the rockapi_rock table in the database.
# Importing it here gives us access to Rock.objects which is Django's ORM (Object
# Relational Mapper) - it lets us query the database using Python instead of raw SQL
# e.g. Rock.objects.all() instead of SELECT * FROM rockapi_rock
from rockapi.models import Rock, Type


class RockView(ViewSet):
    """Rock view set"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """

        # You will implement this feature in a future chapter
        return Response("", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            # Rock.objects.all() uses Django's ORM to run SELECT * FROM rockapi_rock
            # and return all rows as a Python list of Rock model instances
            if request.query_params.get("mine") == "true":
                rocks = Rock.objects.filter(user=request.user)
            else:
                rocks = Rock.objects.all()

            # many=True tells the serializer we're passing a list of objects,
            # not just a single Rock instance
            # context={"request": request} passes the original HTTP request to the serializer,
            # which allows the serializer to access query parameters (like _expand) and
            # use them to conditionally expand foreign keys if needed
            serializer = RockSerializer(rocks, many=True, context={"request": request})

            # .data accesses the serialized (JSON-ready) version of the rocks list
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            # If anything unexpected goes wrong, return a 500 error with the exception message
            return HttpResponseServerError(ex)


class RockTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for expanding the Type model, which is a foreign key on Rock"""

    class Meta:
        model = Type
        fields = ("label",)


class RockUserSerializer(serializers.ModelSerializer):
    """JSON serializer for expanding the User model, which is a foreign key on Rock"""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class RockSerializer(serializers.ModelSerializer):
    """JSON serializer - converts Rock model instances to/from JSON.
    Defined below RockView but used inside it because Python reads the
    whole file before executing, so order doesn't matter here."""

    class Meta:
        # Tells the serializer which model to base itself on
        model = Rock
        # Only these fields will be included in the JSON output.
        # Any other model fields (like user/foreign keys) are excluded unless listed here
        fields = (
            "id",
            "name",
            "weight",
            "user",
            "type",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")

        if request and "type" in request.GET.getlist("_expand"):
            representation["type"] = RockTypeSerializer(instance.type).data

        if request and "user" in request.GET.getlist("_expand"):
            representation["user"] = RockUserSerializer(instance.user).data

        return representation
