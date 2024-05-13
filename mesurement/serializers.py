from rest_framework import serializers
from . models import Mesurement
class MesurementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mesurement
        fields = '__all__'