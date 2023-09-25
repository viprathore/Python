from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from gyms.api.serializers import GymSerializer
from gyms.models import Gym


class GymModelViewSet(ModelViewSet):
    """
    GymModelViewSet
        Returns the Gym name
        http_methods : GET, POST, PUT, DELETE (allowed for admin) only GET is allowed for others.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def get_permissions(self):
        """Allow admin to Modify Gym detail"""

        if self.action == "list":
            return [IsAuthenticated()]

        return [IsAdminUser()]
