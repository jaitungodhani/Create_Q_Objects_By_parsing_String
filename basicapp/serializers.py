from rest_framework import serializers
from .models import SchoolModel

class Schoolserializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolModel
        fields = '__all__'