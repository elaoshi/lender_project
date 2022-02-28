from lenders.dao.BaseDao import BaseDAO
from lenders.models import Lender
from lenders.utils.csvHelper import CsvHepler


class LenderRepository(BaseDAO):
    MODEL_CLASS = Lender

    def dump(self):
        qs = self.list_all()
        csv_helper = CsvHepler()
        return csv_helper.qs_to_local_csv(qs)
