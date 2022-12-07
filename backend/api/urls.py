from django.urls import include, path
from rest_framework import routers
from api.views import (
    CustomUserViewSet,
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
