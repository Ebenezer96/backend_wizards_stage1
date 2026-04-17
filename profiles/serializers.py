from rest_framework import serializers
from .models import Profile


class ProfileCreateSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, trim_whitespace=True)

    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Invalid type")

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Missing or empty name")

        return value.lower()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "name",
            "gender",
            "gender_probability",
            "sample_size",
            "age",
            "age_group",
            "country_id",
            "country_probability",
            "created_at",
        ]


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "name",
            "gender",
            "age",
            "age_group",
            "country_id",
        ]