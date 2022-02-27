from io import StringIO

from django.core.files import File
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from lenders.utils.dumps import convert_to_dataframe


class DatasetManager(models.Manager):
    def create_new(self, qs, fields=None):
        df = convert_to_dataframe(qs, fields=fields)
        fp = StringIO()
        fp.write(df.to_csv())
        date = timezone.now().strftime("%m-%d-%y")
        model_name = slugify(qs.model.__name__)
        filename = "{}-{}.csv".format(model_name, date)
        obj = self.model(
            name=filename.replace('.csv', ''),
            app=slugify(qs.model._meta.app_label),
            model=qs.model.__name__,
            lables=fields,
            object_count=qs.count()
        )
        obj.save()
        obj.csvfile.save(filename, File(fp))  # saves file to the file field
        return obj