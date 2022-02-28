from rest_framework.pagination import PageNumberPagination
from ..dao.LenderRepository import LenderRepository
from ..serializers import LenderSerializer, PagerSerialiser
from ..utils.csvHelper import CsvHepler


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 10
    page_query_param = "page"


class LenderService:
    """
    business service layer ( user story )
    """

    def fetch(self, request):
        lender_repository = LenderRepository()

        qs = lender_repository.list_all()
        active = request.query_params.get('active')
        if active is not None and active == 1:
            qs = qs.filter(active=active)

        pg = MyPageNumberPagination()

        page_lenders = pg.paginate_queryset(queryset=qs, request=request)
        ser = PagerSerialiser(instance=page_lenders, many=True)

        return pg.get_paginated_response(ser.data)

    def show(self, id):

        lender_repository = LenderRepository()
        item = lender_repository.find_one({"id": id})
        if item is None:
            return False
        return LenderSerializer(item).data

    def save(self, data):
        data = LenderSerializer(data=data)
        if data.is_valid():
            data.save()
            return data.data

        return False

    def update(self, id, data):

        lender_repository = LenderRepository()

        item = lender_repository.find_one({"id": id})
        if item is None:
            return False

        item = lender_repository.update_batch_by_query({"id": id},exclude_kw={}, newattrs_kwargs=data)

        return item

    def delete(self, id):

        lender_repository = LenderRepository()
        item = lender_repository.find_one({"id": id})
        if item is None:
            return False
        item.delete()
        return True

    def dumps(self):
        lender_repository = LenderRepository()
        return lender_repository.dump()

    def bulk_upload(self, file):

        lender_repository = LenderRepository()
        csv_helper = CsvHepler()
        data = csv_helper.parse_csv_to_list(file)

        list_of_dict = list(data)

        objs = [
            lender_repository.createByObj(row)
            for row in list_of_dict
        ]
        return lender_repository.save_batch(objs)
