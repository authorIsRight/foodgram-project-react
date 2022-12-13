from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response

from recipes.models import IngredientRecipe


def representation(context, instance, serializer):
    request = context.get('request')
    new_context = {'request': request}
    return serializer(instance, context=new_context).data


def get_shopping_cart(user):
    """Ипользуется в RecipeViewSet

    Создает "сводную таблицу" по сумме
    из списка ингридиентов в покупках
    Используем панду для красивого вывода
    """
    ingredients = IngredientRecipe.objects.filter(
        recipe__shop_list__user=user.user).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).order_by('ingredient__name').annotate(ingredient_total=Sum('amount'))

    content = ''
    for ingredient in ingredients:
        content += (
            f'∙ {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]}) '
            f'- {ingredient["ingredient_total"]}\n'
        )
    return content


def favorite_or_shop_check(self, request, pk, model, serializer):
    user = request.user
    if (request.method == 'POST'
            and model.objects.filter(user=user, recipe_id=pk).exists()):
        return Response({
            'errors': 'Рецепт уже добавлен в список'
        }, status=status.HTTP_400_BAD_REQUEST)
    if (request.method == 'DELETE'
            and not model.objects.filter(user=user,
                                         recipe_id=pk).exists()):
        return Response({
            'errors': 'Рецепт уже удален из списка'
        }, status=status.HTTP_400_BAD_REQUEST)
    return self._create_or_destroy(
        request.method, request, pk, model, serializer
    )
