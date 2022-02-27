from rest_framework import serializers, pagination

from lenders.models import Lender


class LenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lender
        fields = [
            'name','code',
            'upfront_commistion_rate','trait_commistion_rate',
            'active'
        ]


class PagerSerialiser(serializers.ModelSerializer):
  class Meta:
    model = Lender
    fields = "__all__"
    ordering = ['-id']