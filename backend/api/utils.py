import pandas as pd
from django.db.models import Sum

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
    df = pd.DataFrame(list(ingredients))
    df = df.iloc[:, [0, 2, 1]]
    df.columns = ['ингредиент', 'количество', 'ед измерения']

    return (
        [df.to_string(index=False)]
        )
