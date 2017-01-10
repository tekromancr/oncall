from rest_framework import serializers
from models import Light

class LightSerializer(serializers.ModelSerializer):

    assigned_user = serializers.StringRelatedField()
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = Light
        fields = ('pk', 'assigned_user', 'position', 'color',)