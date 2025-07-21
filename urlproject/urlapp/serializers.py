from rest_framework import serializers
from .models import *

class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = '__all__'
