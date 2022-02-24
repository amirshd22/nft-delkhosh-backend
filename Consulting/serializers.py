from rest_framework import serializers
from .models import OrderConsulting,ConsultingPlan


class ConsultingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model= ConsultingPlan
        fields= "__all__"


class OrderConsultingSerializer(serializers.ModelSerializer):
    plan= serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderConsulting
        fields= "__all__"
    
    def get_plan(self,obj):
        plan = obj.consultingplan
        serializer = ConsultingPlanSerializer(plan,many=False)
        return serializer.data
