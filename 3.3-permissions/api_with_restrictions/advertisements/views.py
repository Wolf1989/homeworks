from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework import response


from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.permissions import IsAuthenticatedUser, IsOwner


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.filter(draft=False)
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AdvertisementFilter
    search_fields = ['creator__username', 'draft']
    ordering_fields = ['id', 'title']

    def get_queryset(self):
        """Отображает """
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Объединяем стандартный queryset с queryset содержащий все черновые
            # объявления пользователя
            queryset |= Advertisement.objects.filter(creator=self.request.user, draft=True)
        return queryset

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser() or IsOwner()]
        return []

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticatedUser])
    def add_to_favourites(self, request, pk=None):
        """Добавление объявления в список избранных"""
        obj = self.get_object()
        user = request.user
        if obj.creator != user:
            user.featured_ads.add(obj)
            result = 'Объявления было добавлено в Избранное'
        else:
            result = 'Нельзя добавить собственно объявление в Избранное'
        return response.Response({'detail': result})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedUser])
    def show_favorites(self, request):
        """Получение списка избранных объявлений пользователя"""
        advs = request.user.featured_ads.all()
        page = self.paginate_queryset(advs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(advs, many=True)
        return response.Response({"favorites_ads": serializer.data})
        
