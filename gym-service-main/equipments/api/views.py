from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from equipments.api.serializers import EquipmentSerializer
from equipments.models import Equipment


class EquipmentModelViewSet(ModelViewSet):
    """
    EquipmentModelViewSet
        Returns the Equipment name
        http_methods : GET, POST, PUT, DELETE (allowed for admin) only GET is allowed for others.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get_permissions(self):
        """Allow admin to Modify Equipment detail"""

        if self.action == "list":
            return [IsAuthenticated()]

        return [IsAdminUser()]
