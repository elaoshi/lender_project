from lenders.dao.BaseDao import BaseDAO
from lenders.models import Lender


class LenderRepository(BaseDAO):
    MODEL_CLASS = Lender