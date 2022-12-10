from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag
from users.models import User

favorite_shop_filter = {'favorites': 'favorites__user',
                        'shop_list': 'shop_list__user'}


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


class RecipeFilter(filters.FilterSet):
    """Фильтр для рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def _get_queryset(self, queryset, name, value, model):
        if value:
            return queryset.filter(**{favorite_shop_filter[model]:
                                      self.request.user})
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        return self._get_queryset(queryset, name, value, 'favorites')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return self._get_queryset(queryset, name, value, 'shop_list')
