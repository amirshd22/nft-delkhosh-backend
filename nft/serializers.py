from rest_framework import serializers
from .models import NftPlan,Order


class NftPlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = NftPlan
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    plan = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

    def get_plan(self,obj):
        plan = obj.plan
        serializer = NftPlansSerializer(plan,many=False)
        return serializer.data