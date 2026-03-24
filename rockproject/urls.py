"""Rock of Ages URL Configuration"""

# Django's built-in admin module - provides a web-based interface at /admin
# for managing database records without writing any code
from django.contrib import admin

# path() defines a single URL route
# include() lets us pull in URL patterns from other places (like the router)
# and nest them into this main urls.py file
from django.urls import include, path

# DefaultRouter is a DRF (Django REST Framework) class that automatically
# generates standard CRUD URL patterns for a viewset (list, create, retrieve,
# update, destroy) so we don't have to define each one manually
from rest_framework import routers

# Import the view functions and class that will handle HTTP requests:
# register_user - handles POST /register to create a new user
# login_user    - handles POST /login to authenticate a user
# TypeView      - handles all CRUD operations for the Type model
# RockView      - handles all CRUD operations for the Rock model
from rockapi.views import register_user, login_user, TypeView, RockView

# trailing_slash=False means URLs like /types work instead of requiring /types/
router = routers.DefaultRouter(trailing_slash=False)

# Registers TypeView at the /types endpoint, automatically creating routes for
# GET /types, POST /types, GET /types/<id>, PUT /types/<id>, DELETE /types/<id>
router.register(r"types", TypeView, basename="type")

# Registers RockView at the /rocks endpoint, automatically creating routes for
# GET /rocks, POST /rocks, GET /rocks/<id>, PUT /rocks/<id>, DELETE /rocks/<id>
router.register(r"rocks", RockView, basename="rock")

# Initial URL patterns for the project. The router.urls includes all the automatically generated routes for the TypeView, and we also add explicit routes for user registration and login, as well as the admin interface. When a request comes in, Django will check these patterns in order to determine which view should handle the request based on the URL and HTTP method.
urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
]
