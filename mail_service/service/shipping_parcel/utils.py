import datetime

from django.db.models import F, Case, When

from .models import Parcel, TrainTrack
from .serializers import ParcelSerializer, TrainTrackSerializer


def get_parcel_shipped_data(parcel):
    return (
        {"shipping_status": True, "shipping_cost": parcel.cost}
        if parcel and parcel.cost
        else {"shipping_status": False, "shipping_cost": None}
    )


def get_train_shipped_data(train):
    response_data = {
        "shipping_status": False,
        "train_left_time": None,
        "parcel": None,
        "assigned_lines": None,
    }
    if train and train.train_left_time and train.parcel and train.assigned_lines:
        response_data = {
            "shipping_status": True,
            "train_left_time": train.train_left_time,
            "parcel": ParcelSerializer(Parcel.objects.filter(id=train.parcel).select_related('parcel_owner').first()).data,
            "assigned_lines": TrainTrackSerializer(
                TrainTrack.objects.filter(id=train.assigned_lines).first()
            ).data,
        }
    return response_data
