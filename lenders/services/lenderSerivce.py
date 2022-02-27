import csv
import io

from rest_framework.pagination import PageNumberPagination

from ..dao.LenderRepository import LenderRepository
from ..serializers import LenderSerializer, PagerSerialiser
import pandas as pd


class MyPageNumberPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"

class LenderService():
    """
    business service layer ( user story )
    """
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
        if item == None:
            return False
        return LenderSerializer(item).data


    def save(self,data):
        data = LenderSerializer(data=data)
        if data.is_valid():
            data.save()
            return data.data

        return False


    def update(self,id,data):

        lenderRepository = LenderRepository()

        item = lenderRepository.find_one({"id": id})
        if item == None:
            return False

        item = lenderRepository.update_batch_by_query({"id":id},newattrs_kwargs=data)

        return item


    def delete(self,id):

        lenderRepository = LenderRepository()
        item = lenderRepository.find_one({"id": id})
        if item == None:
            return False
        item.delete()
        return True

    def dumps(self,output="csv"):
        lenderRepository = LenderRepository()
        return lenderRepository.dump(output=output)


    def bulk_upload(self,request):

        lenderRepository = LenderRepository()

        file = request.FILES['file'].file
        paramFile = io.TextIOWrapper(file)
        portfolio1 = csv.DictReader(paramFile)

        df = pd.DataFrame(portfolio1)
        df = df.drop_duplicates()
        portfolio1 = df.T.to_dict().values()
        
        list_of_dict = list(portfolio1)

        objs = [
            lenderRepository.createByObj(row)
            for row in list_of_dict
        ]
        return lenderRepository.save_batch(objs)
