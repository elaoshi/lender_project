from ..models import Lender


class BaseDAO:
    MODEL_CLASS = Lender
    SAVE_BATCH_SIZE = 1000

    def createByObj(self, dict):
        return self.MODEL_CLASS(**dict)

    def save(self, obj):
        """insert one

        :param obj:
        :return:
        """
        if not obj:
            return False

        obj.save()

        return True

    def save_batch(self, objs, *, batch_size=SAVE_BATCH_SIZE):
        """insert batch

        :param batch_size: ex. 1000
        :type objs: list[BaseModel]
        :param objs:
        :return:
        """
        if not objs:
            return False

        self.MODEL_CLASS.objects.bulk_create(objs, batch_size=batch_size)

        return True

    def delete(self, obj):
        if not obj:
            return False

        obj.delete()

        return True

    def delete_batch(self, objs):
        if not objs:
            return False

        for obj in objs:
            self.delete(obj)

        return True

    def delete_batch_by_query(self, filter_kw: dict, exclude_kw: dict):
        """
        """
        self.MODEL_CLASS.objects.filter(**filter_kw).exclude(**exclude_kw).delete()

        return True

    def soft_delete(self, obj):
        """
            Soft delete
        """
        if obj is None:
            return False

        obj.is_deleted = True

        obj.save()

        return True

    def update(self, obj):
        if not obj:
            return False

        obj.save()

        return True

    def update_batch(self, objs):
        if not objs:
            return False

        for obj in objs:
            self.update(obj)

        return True

    def update_batch_by_query(self, query_kwargs: dict, exclude_kw: dict, newattrs_kwargs: dict):
        self.MODEL_CLASS.objects.filter(**query_kwargs).exclude(**exclude_kw).update(**newattrs_kwargs)

    def get_and_update(self, id, newattrs_kwargs: dict):
        self.MODEL_CLASS.objects.filter(id=id).update(**newattrs_kwargs)

    def find_one(self, filter_kw: dict, order_bys: list = None):
        """
        :param filter_kw: filter kw
        :param order_bys: order by list
        :rtype: BaseModel | None
        :return:
        """
        qs = self.MODEL_CLASS.objects.filter(**filter_kw)
        if order_bys:
            qs = qs.order_by(*order_bys)

        return qs.first()

    def __find_queryset(self, filter_kw: dict, exclude_kw: dict, order_bys: list = None):
        """
        :param filter_kw:
        :return:
        """
        qs = self.MODEL_CLASS.objects.filter(**filter_kw).exclude(**exclude_kw)
        if order_bys:
            qs = qs.order_by(*order_bys)
        return qs

    def find_all_model_objs(self, filter_kw: dict, exclude_kw: dict, order_bys: list = None) -> list:
        return self.__find_queryset(filter_kw, exclude_kw, order_bys).all()

    def is_exists(self, filter_kw: dict, exclude_kw: dict = None) -> bool:
        return self.MODEL_CLASS.objects.filter(**filter_kw).exclude(**exclude_kw).exists()

    def get_count(self, filter_kw: dict, exclude_kw: dict = None) -> int:
        return self.MODEL_CLASS.objects.filter(**filter_kw).exclude(**exclude_kw).count()

    def list_all(self):
        return self.MODEL_CLASS.objects.all()
