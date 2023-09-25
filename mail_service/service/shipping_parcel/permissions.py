from rest_framework import permissions


class ParcelPermissions(permissions.BasePermission):
    __doc__ = """
    post master have a only read access and the parcel owner have all access.
    """

    def has_permission(self, request, view):
        return request.user.user_type == "PARCEL_OWNER" or (
            request.user.user_type == "POST_MASTER" and request.method == "GET"
        )


class TrainPermissions(permissions.BasePermission):
    __doc__ = """
    post master have a only read access and the Train operator have all access.
    """

    def has_permission(self, request, view):
        return request.user.user_type == "TRAIN_OPERATOR" or (
            request.user.user_type == "POST_MASTER" and request.method == "GET"
        )


class PostMasterPermissions(permissions.BasePermission):
    __doc__ = """
    Only post master have a access.
    """

    def has_permission(self, request, view):
        return request.user.user_type == "POST_MASTER"


from rest_framework_simplejwt.models import TokenUser

SERVICE_IDENTIFIER = 'MAIL_SERVICE'


class IsServiceAccessible(permissions.BasePermission):
    """
    Allow only access to user having corresponding service scope access.
    """

    def has_permission(self, request, view):
        try:
            assert request.user and request.user.is_authenticated
            if isinstance(request.user, TokenUser):
                return SERVICE_IDENTIFIER in request.auth.payload.get('aud')
            else:
                return False
        except AssertionError:
            return False