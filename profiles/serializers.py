from rest_framework import serializers
from .models import Profile


class ProfileCreateSerializer(serializers.Serializer):
    name = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        error_messages={
            "required": "Missing name",
            "blank": "Missing or empty name",
        },
    )

    def validate_name(self, value):
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
            "created_at",
        ]