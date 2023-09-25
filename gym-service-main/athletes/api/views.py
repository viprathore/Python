import datetime
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models import F, Sum, Value
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from athletes.api.serializers import AthleteCreateSerializer, AthleteListSerializer
from athletes.exceptions import InvalidDatesException

Athlete = get_user_model()


class AthleteModelViewSet(ModelViewSet):
    """
    AthleteModelViewSet
        - Create/Update/Delete/Retrieve athlete
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Athlete.objects.select_related("gym").prefetch_related("athlete_exercises")
    serializer_class = AthleteCreateSerializer

    def validate_dates(self, start_date, end_date):
        """
        validate_dates
            checks the date format and start_date must be less than end_date
        """
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except Exception as e:
            raise e

        if start_date > end_date:
            raise InvalidDatesException(
                "End date must be greater than start date or Invalid date format (Must be yyyy-mm-dd)"
            )

    def get_permissions(self):
        """Returns the permission based on the type of action"""

        if self.action == "create":
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        """Select serializer according to action"""

        if self.action == "create":
            return AthleteCreateSerializer

        return AthleteListSerializer

    @action(detail=False, url_path="get_calories/(?P<pk>[^/.]+)")
    def get_total_calories_between_dates(self, request, pk: UUID):
        """
        get_total_calories_between_dates
            Returns the total calories burnt by user between two dates
        """

        athlete = get_object_or_404(Athlete, pk=pk)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        self.validate_dates(start_date, end_date)

        exercise_qs = self.queryset.filter(
            id=athlete.id,
            athlete_exercises__created_at__date__range=(start_date, end_date),
        )

        if exercise_qs.exists():
            qs = exercise_qs.annotate(
                total_calories=Value(
                    float(
                        exercise_qs.aggregate(
                            Sum(F("athlete_exercises__calories_burnt"))
                        ).get("athlete_exercises__calories_burnt__sum")
                    )
                )
            ).first()
        else:
            return Response(
                {"msg": "Details not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)
