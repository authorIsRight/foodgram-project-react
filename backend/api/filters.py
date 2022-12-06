from django_filters import rest_framework as filters
from recipes.models import Tag, Ingredient, Recipe
from users.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        exclude = ['password']


class IngredientFilter(filters.FilterSet):
    """Фильтры для произведений."""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)


