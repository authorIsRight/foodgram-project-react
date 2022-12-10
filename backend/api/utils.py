from collections import Counter

from recipes.models import IngredientRecipe


def representation(context, instance, serializer):
    request = context.get('request')
    new_context = {'request': request}
    return serializer(instance, context=new_context).data


def get_shopping_cart(user):
    """Ипользуется в RecipeViewSet

    Создает "сводную таблицу" по сумме
    из списка ингридиентов в покупках
    """
    ingredients = IngredientRecipe.objects.filter(
        recipe__shop_list__user=user.user
    )
    summed_ingredients = Counter()
    for ing in ingredients:
        summed_ingredients[
            (ing.ingredient.name, ing.ingredient.measurement_unit)
        ] += ing.amount
    return ([
        f"- {name}: {amount} {measurement_unit}\n"
        for (name, measurement_unit), amount
        in summed_ingredients.items()
    ])
