# taskmanager/serializers.py
from rest_framework import serializers

class StartScrapingSerializer(serializers.Serializer):
    coins = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
