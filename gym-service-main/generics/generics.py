from uuid import uuid4

from django.db.models import DateTimeField, Model, UUIDField
from django.utils import timezone


class CreatedUpdatedMixin(Model):
    """
    CreatedUpdatedMixin
        - set created_at time of creation
        - set updated_at time of updation
    """

    created_at = DateTimeField(default=timezone.now, editable=False)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(Model):
    """
    UUIDMixin
        Replace id (primary_key) with uuid
    """

    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    class Fields:
        ID = "id"

    class Meta:
        abstract = True
