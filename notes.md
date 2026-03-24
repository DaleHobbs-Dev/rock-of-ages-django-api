# Notes for Rock of Ages Project

## Django Models for Rock of Ages

A "model" in Django is a Python class that represents a database table. Each attribute of the class corresponds to a field in the database. For the Rock of Ages project, we will define the following models:

- **User**: Represents a user of the application. Fields include username, email, password, and profile information. This is automatically provided by Django's built-in User model.
- **Type**: Represents the type of rock. Fields include name and description.
- **Rock**: Represents a rock in the game. Fields include name, type (ForeignKey to Type), strength, and durability.

## Migration of Models

After creating the models, we need to run migrations to create the corresponding tables in the database. Say our models are defined in the `rockapi` app. The commands are:

```bash
python manage.py makemigrations rockapi
python manage.py migrate
```

This will create the necessary tables for the User, Type, and Rock models in the database.

## Django Views for Rock of Ages

A "view" in Django is a Python function or class that takes a web request and returns a web response. For the Rock of Ages project, we will define the following views:

- **type_view**: A view to handle requests related to rock types. It will allow users to create, read, update, and delete rock types.
- **rock_view**: A view to handle requests related to rocks. It will allow users to create, read, update, and delete rocks.

## Django URLs for Rock of Ages

In Django, we define URL patterns to route HTTPrequests to the appropriate views. For the Rock of Ages project, we will define the following URL patterns initally in the `rockproject/urls.py` file:

```python
from django.urls import path
from . import views
urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user),
    path("admin/", admin.site.urls),
]
```

Then, above the `urlpatterns` list, we will set up a router for our viewsets:

```python
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'types', views.TypeView, 'type')
router.register(r'rocks', views.RockView, 'rock')
```

This will create the necessary URL patterns for the Type and Rock views, allowing us to perform CRUD operations on these models through the API. One line of `router.register` (for instance `router.register(r'types', views.TypeView, 'type')`) will open up the following endpoints:

- `GET /types/`: List all rock types
- `POST /types/`: Create a new rock type
- `GET /types/{id}/`: Retrieve a specific rock type
- `PUT /types/{id}/`: Update a specific rock type
- `DELETE /types/{id}/`: Delete a specific rock type

preventing us from having to write out each of these endpoints manually.

## Testing Endpoints for this Django API

Each HTTP reqeust will require a token for authentication. To obtain a token, you can send a POST request to the `/login` endpoint with the user's credentials (username and password). The response will include a token that you can use for subsequent requests. You could also get a token from the db.sqlite3 authtoken_token table if you have access to the database.

After getting the token, you can include it in the Authorization header of your requests to access the protected endpoints. For example, if your token is `abc123`, you would include the following header in your requests:

```Authorization: Token abc123```

So client-side `services.js` functions for HTTP requests to the API would look like this going forward:

```javascript
export const getTypes = () => {
  return fetch("/types", {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  }).then((res) => res.json());
};
```
