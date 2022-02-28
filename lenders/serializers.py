from rest_framework import serializers
from lenders.models import Lender


class LenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lender
        fields = [
            'name', 'code',
            'upfront_commistion_rate', 'trait_commistion_rate',
            'active', 'id'
        ]


    def create(self, validated_data):
        validated_data['code'] = validated_data['code'].capitalize()
        lender = Lender.objects.create(**validated_data)
        return lender

class PagerSerialiser(serializers.ModelSerializer):


    class Meta:
        model = Lender
        fields = "__all__"
        ordering = ['-id']
