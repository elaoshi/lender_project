from rest_framework import serializers
from rest_framework.fields import DecimalField

from lenders.models import Lender


class LenderSerializer(serializers.ModelSerializer):
    upfront_commistion_rate = DecimalField(max_digits=5, decimal_places=2,coerce_to_string=False)
    trait_commistion_rate = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=False)

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

    upfront_commistion_rate = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=False)
    trait_commistion_rate = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Lender
        fields = "__all__"
        ordering = ['-id']
