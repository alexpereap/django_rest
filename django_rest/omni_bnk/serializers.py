from rest_framework import serializers
from . models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=200)
    director = serializers.CharField(max_length=200)
    year = serializers.CharField(max_length=20)
    recommended = serializers.BooleanField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.director = validated_data.get('director', instance.director)
        instance.year = validated_data.get('year', instance.year)
        instance.recommended = validated_data.get('recommended', instance.recommended)

        instance.save()
        return instance