from rest_framework.pagination import PageNumberPagination

from ..dao.LenderRepository import LenderRepository
from ..models import Lender
from ..serializers import LenderSerializer, PagerSerialiser



class MyPageNumberPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"

class LenderService():


    def list(self,request):
        lenderRepository = LenderRepository()
        qs = lenderRepository.list_all()
        # items = LenderSerializer(qs,many=True)
        pg = MyPageNumberPagination()

        page_lenders = pg.paginate_queryset(queryset=qs, request=request)
        ser = PagerSerialiser(instance=page_lenders, many=True)

        return pg.get_paginated_response(ser.data)

    def save(self,data):
        data = LenderSerializer(data=data)
        if data.is_valid():
            data.save()
            return data.data

        return False