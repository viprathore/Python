from django.contrib import admin

from .models import Parcel, ShippedParcel, Train, TrainTrack

admin.site.register(Parcel)
admin.site.register(Train)
admin.site.register(TrainTrack)
admin.site.register(ShippedParcel)
