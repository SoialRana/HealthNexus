from rest_framework import serializers 
from. models import Apointment

class AppointmentSerializer(serializers.ModelSerializer):
    # time=serializers.StringRelatedField(many=False)
    # patient=serializers.StringRelatedField(many=False)
    # doctor=serializers.StringRelatedField(many=False)
    class Meta:
        model=Apointment
        fields='__all__'
        