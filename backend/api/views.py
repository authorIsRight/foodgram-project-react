from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .pagination import PageLimitPagination
from recipes.models import (Favorite, Follow, Ingredient, Recipe, ShoppingList,
                            Tag)
from users.models import User
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (CustomUserSerializer, FavoriteSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShoppingListSerializer, TagSerializer)
from .utils import favorite_or_shop_check, get_shopping_cart


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с обьектами класса User и подписки на авторов"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=False,
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(follow__user=request.user)
        if queryset.exists():
            pages = self.paginate_queryset(queryset)
            serializer = FollowSerializer(pages, many=True,
                                          context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response('Подписок еще нет',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        change_subscription = Follow.objects.filter(
            user=user.id, author=author.id
        )
        serializer = FollowSerializer(author,
                                      context={'request': request})
        if request.method == 'POST':
            if user == author:
                return Response('Нельзя подписаться на себя самого',
                                status=status.HTTP_400_BAD_REQUEST)
            if change_subscription.exists():
                return Response(f'Вы уже подписаны на {author}',
                                status=status.HTTP_400_BAD_REQUEST)
            subscribe = Follow.objects.create(
                user=user,
                author=author
            )
            subscribe.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if change_subscription.exists():
            change_subscription.delete()
            return Response(f'Вы больше не подписаны на {author}',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(f'Нельзя отписаться от {author}, не подписавшись',
                        status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет работы с обьектами класса Tag"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с обьектами класса Ingridient"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    search_fields = ('^name', )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с обьектами класса Recipe"""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    @staticmethod
    def create_object(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_object(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        obj = get_object_or_404(model, user=user, recipe=recipe)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _create_or_destroy(self, http_method, recipe, key,
                           model, serializer):
        if http_method == 'POST':
            return self.create_object(request=recipe, pk=key,
                                      serializers=serializer)
        return self.delete_object(request=recipe, pk=key, model=model)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        return (favorite_or_shop_check(self, request,
                                       pk, Favorite, FavoriteSerializer)
                )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):

        return (favorite_or_shop_check(self, request, pk,
                                       ShoppingList, ShoppingListSerializer)
                )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, user):
        shopping_cart = get_shopping_cart(user)
        filename = 'shopping-list.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
