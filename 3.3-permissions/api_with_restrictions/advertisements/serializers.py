from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import DateTimeField
from django.conf import settings

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'creator',
                  'status', 'created_at', 'draft']

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        method = self.context["request"].method
        user = self.context["request"].user
        opened_advs = user.advertisement_set.filter(status='OPEN').count()
        if opened_advs == settings.MAX_OPEN_ADS:
            status = data.get('status', None)
            if method == 'POST' and status != 'CLOSED':
                raise serializers.ValidationError(
                    "Вы не можете создать больше 10 открытых объявлений"
                )
            else:
                if status == 'OPEN' and self.instance.status == 'CLOSED':
                    raise serializers.ValidationError(
                        "Нельзя изменить статус на OPEN. У вас уже 10 открытых объявлений"
                    )

        return data
