class ProfileCollectionView(APIView):
    def post(self, request):
        # Validate input
        if "name" not in request.data:
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(request.data.get("name"), str):
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = ProfileCreateSerializer(data=request.data)
        if not serializer.is_valid():
            message = serializer.errors["name"][0]

            status_code = (
                status.HTTP_422_UNPROCESSABLE_ENTITY
                if str(message) == "Invalid type"
                else status.HTTP_400_BAD_REQUEST
            )
            return Response(
                {"status": "error", "message": str(message)},
                status=status_code,
            )

        name = serializer.validated_data["name"].strip().lower()

        # Idempotency check
        existing = Profile.objects.filter(name__iexact=name).first()
        if existing:
            return Response(
                {
                    "status": "success",
                    "message": "Profile already exists",
                    "data": ProfileSerializer(existing).data,
                },
                status=status.HTTP_200_OK,
            )

        # External API processing
        try:
            data = build_profile_data(name)
            profile = Profile.objects.create(**data)

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