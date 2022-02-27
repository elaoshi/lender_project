from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..dao.LenderRepository import LenderRepository
from ..serializers import LenderSerializer, PagerSerialiser



class MyPageNumberPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"

class LenderService():
    def fetch(self, request):
        lenderRepository = LenderRepository()

        qs = lenderRepository.list_all()
        active = request.query_params.get('active')
        if active is not None and active == 1:
            qs = qs.filter(active=active)

        pg = MyPageNumberPagination()

        page_lenders = pg.paginate_queryset(queryset=qs, request=request)
        ser = PagerSerialiser(instance=page_lenders, many=True)

        return pg.get_paginated_response(ser.data)


    def show(self,id):

        lenderRepository = LenderRepository()
        item = lenderRepository.find_one({"id":id})
        return Response(LenderSerializer(item).data)


    def save(self,data):
        data = LenderSerializer(data=data)
        if data.is_valid():
            data.save()
            return data.data

        return False


    def update(self,id,data):

        lenderRepository = LenderRepository()
        item = lenderRepository.update_batch_by_query({"id":id},newattrs_kwargs=data)

        return item

