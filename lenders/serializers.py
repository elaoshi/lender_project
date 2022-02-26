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
#
# class PaginatedLenderSerializer(PaginationSerializer):
#     class Meta:
#         object_serializer_class = LenderSerializer


class PagerSerialiser(serializers.ModelSerializer):
  class Meta:
    model = Lender
    fields = "__all__"