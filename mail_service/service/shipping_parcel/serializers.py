import datetime

from rest_framework import serializers

from core.serializers import UserSerializer
from .models import Parcel, ShippedParcel, Train, TrainTrack


class ParcelSerializer(serializers.ModelSerializer):
    parcel_owner = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Parcel
        fields = ("id", "parcel_owner", "parcel_name", "parcel_weight", "parcel_volume", "withdraw_bids")


class PostTrainOfferSerializer(serializers.ModelSerializer):
    train_operator = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Train
        fields = ("id", "train_operator", "train_name", "capacity", "cost", "is_available", "withdraw_bids", "lines_they_operate")


class TrainTrackSerializer(serializers.ModelSerializer):
    is_busy = serializers.SerializerMethodField()

    class Meta:
        model = TrainTrack
        fields = ("id", "source", "destination", "is_busy")

    def get_is_busy(self, obj):
        return (obj.shipped_track.first()
            and obj.shipped_track.first().created + datetime.timedelta(hours=3)
            > datetime.datetime.now())


class BookedTrainListSerializer(serializers.Serializer):
    train = PostTrainOfferSerializer(source="train_qs")
    parcel = ParcelSerializer(source='parcel_qs')
    assigned_lines = TrainTrackSerializer()


class BookTrainAndShippedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippedParcel
        fields = ("train", "parcel", "assigned_lines")

    def create(self, validated_data):
        train = validated_data.get("train")
        parcel = validated_data.get("parcel")
        assigned_lines = validated_data.get("assigned_lines")
        current_time = datetime.datetime.now()
        before_three_hours = datetime.datetime.now()

        # Check the train can go on the assigned lines or not.
        if not train.lines_they_operate.filter(id=assigned_lines.id):
            raise serializers.ValidationError(
                {
                    "message": f"You can not assigned this track to the train because the train {train.train_name} can not go on the given track"
                }
            )

        # Check the current status of the track.
        if ShippedParcel.objects.filter(
            assigned_lines=assigned_lines,
            created__gte=before_three_hours,
            created__lte=current_time,
        ).exists():
            raise serializers.ValidationError(
                {
                    "message": "You can not shipped the train on this track a train is already running on this track."
                }
            )

        # Check the remaining capacity of train.
        if parcel.parcel_weight * parcel.parcel_volume > train.capacity:
            raise serializers.ValidationError(
                {
                    "message": "You can not send the parcel from this train because the size of the parcel is above the train remaining capacity"
                }
            )

        return ShippedParcel.objects.create(**validated_data)
