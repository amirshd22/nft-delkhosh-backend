from rest_framework import serializers 
from .models import AdvertisingPlan,OrderAdvertising


class AdvertisingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdvertisingPlan
        fields="__all__"


class OrderAdvertisingSerializer(serializers.ModelSerializer):
    plan= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=OrderAdvertising
        fields="__all__"

    def get_plan(self,obj):
        plan= obj.advertisingplan
        serializer= AdvertisingPlanSerializer(plan, many=False)
        return serializer.data