from rest_framework import serializers

from habits.models import Place


class PlaceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'