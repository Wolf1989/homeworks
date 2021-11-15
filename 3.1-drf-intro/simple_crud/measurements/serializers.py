from rest_framework.serializers import ModelSerializer, SlugRelatedField

from measurements.models import Project, Measurement


class MeasurementSerializer(ModelSerializer):

    class Meta:
        model = Measurement
        fields = "__all__"


class ProjectSerializer(ModelSerializer):

    measurements = MeasurementSerializer(many=True)

    class Meta:
        model = Project
        fields = "__all__"