from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    Follow,
    Favorite,
    IngredientRecipe,
    ShoppingList,
)

admin.site.empty_value_display = 'Empty Value Display'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Управление тэгами в админке"""

    list_display = ('pk', 'name', 'slug')


@admin.register(Ingredient)
class IngridientAdmin(admin.ModelAdmin):
    """Управление тэгами в админке"""

    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)


class RecipeIngridientInline(admin.StackedInline):
    """Вспомогательный, связывающий класс для админки"""

    model = IngredientRecipe
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Управление рецептами в админке"""

    list_display = ('pk', 'name', 'author', 'get_favorites')
    search_fields = ('name', 'author', 'tags',)
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngridientInline,)

    def get_favorites(self, obj):
        return obj.favorites.count()

    get_favorites.short_description = (
        'Число добавлений этого рецепта в избранное'
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Управление подписками в админке"""

    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Управление избранным в админке"""

    list_display = ('pk', 'user', 'recipe')


@admin.register(IngredientRecipe)
class IngridientRecipeAdmin(admin.ModelAdmin):
    """Управление ингридиентами в админке"""

    list_display = ('pk', 'ingredient', 'recipe', 'amount')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Управление списком покупок в админке"""

    list_display = ('id', 'user', 'recipe')
