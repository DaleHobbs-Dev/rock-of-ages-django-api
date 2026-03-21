"""Type model"""

from django.db import models


class Type(models.Model):
    """Type model for the Rock of Ages API"""

    label = models.CharField(max_length=155)
