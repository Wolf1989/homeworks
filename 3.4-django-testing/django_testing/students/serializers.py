from django.conf import settings
from rest_framework import serializers
from rest_framework.status import HTTP_400_BAD_REQUEST

from students.models import Course, Student



class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, attrs):
        students = attrs.get('students')
        if students and len(students) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError("Превышен лимит студентов")
        return attrs