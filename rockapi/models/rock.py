"""Rock model"""

# models gives us the base Model class and field types (CharField, ForeignKey, etc.)
# that Django uses to define database table columns
from django.db import models

# Django's built-in User model that handles authentication. Importing it here
# lets us create a relationship between a Rock and the User who owns it.
# We don't need to write a User model ourselves — Django provides it for free
from django.contrib.auth.models import User


# Inheriting from models.Model is what makes this a Django model:
# 1. Tells Django to create a rockapi_rock table in the database for this class
# 2. Automatically adds an "id" primary key column to the table
# 3. Attaches the "objects" manager, giving us Rock.objects.all(),
#    Rock.objects.filter(), Rock.objects.get(), etc. for querying the database
class Rock(models.Model):
    """Rock model for the Rock of Ages API"""

    # ForeignKey creates a many-to-one relationship — many Rocks can belong to one User
    # on_delete=models.CASCADE means if a User is deleted, all their Rocks are deleted too
    # related_name="collection" lets us access a user's rocks from the User side
    # with user.collection.all() instead of the default user.rock_set.all()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collection")

    # Another ForeignKey relationship — many Rocks can have one Type (e.g. "Igneous")
    # "Type" is a string reference instead of the class directly because Type may not
    # be imported/defined yet when Python reads this line — this avoids import order issues
    # related_name="rocks" lets us access all rocks of a type with type.rocks.all()
    type = models.ForeignKey("Type", on_delete=models.CASCADE, related_name="rocks")

    # CharField is a string column — max_length=155 sets the maximum character limit
    # in the database column (maps to VARCHAR(155) in SQL)
    name = models.CharField(max_length=155)

    # DecimalField stores precise decimal numbers — important for weights where
    # floating point rounding errors would be problematic
    # max_digits=5 means up to 5 total digits (e.g. 999.99)
    # decimal_places=2 means 2 of those digits are after the decimal point
    weight = models.DecimalField(max_digits=5, decimal_places=2)
