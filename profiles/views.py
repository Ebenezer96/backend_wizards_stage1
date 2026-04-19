import json
from requests.exceptions import RequestException
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from .models import Profile
from .serializers import (
    ProfileCreateSerializer,
    ProfileSerializer,
    ProfileListSerializer,
)
from .services import build_profile_data, ExternalAPIError
from .pagination import ProfilePagination


class ProfileCollectionView(APIView):
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        data = request.data.copy()

        if "name" not in data and "_content" in data:
            try:
                data = json.loads(data.get("_content", "{}"))
            except json.JSONDecodeError:
                return Response(
                    {"status": "error", "message": "Invalid JSON payload"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = ProfileCreateSerializer(data=data)

        if not serializer.is_valid():
            message = serializer.errors.get("name", ["Invalid input"])[0]
            status_code = (
                status.HTTP_422_UNPROCESSABLE_ENTITY
                if str(message) == "Invalid type"
                else status.HTTP_400_BAD_REQUEST
            )
            return Response(
                {"status": "error", "message": str(message)},
                status=status_code,
            )

        normalized_name = serializer.validated_data["name"]

        existing = Profile.objects.filter(name__iexact=normalized_name).first()
        if existing:
            return Response(
                {
                    "status": "success",
                    "data": ProfileSerializer(existing).data,
                },
                status=status.HTTP_200_OK,
            )

        try:
            profile_data = build_profile_data(normalized_name)
            profile = Profile.objects.create(**profile_data)

        except ExternalAPIError as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except RequestException:
            return Response(
                {"status": "error", "message": "Upstream service failure"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        except Exception:
            return Response(
                {"status": "error", "message": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "status": "success",
                "data": ProfileSerializer(profile).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request):
        profiles = Profile.objects.all().order_by("-created_at")

        gender = request.query_params.get("gender")
        country_id = request.query_params.get("country_id")
        age_group = request.query_params.get("age_group")

        if gender:
            profiles = profiles.filter(gender__iexact=gender)
        if country_id:
            profiles = profiles.filter(country_id__iexact=country_id)
        if age_group:
            profiles = profiles.filter(age_group__iexact=age_group)

        paginator = ProfilePagination()
        paginated_profiles = paginator.paginate_queryset(profiles, request)
        serializer = ProfileListSerializer(paginated_profiles, many=True)

        return Response(
            {
                "status": "success",
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileDetailView(APIView):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        return Response(
            {"status": "success", "data": ProfileSerializer(profile).data},
            status=status.HTTP_200_OK,
        )