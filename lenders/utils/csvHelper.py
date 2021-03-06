import csv
import io
import os

import pandas as pd
from django.utils.text import slugify

from demo import settings


class CsvHepler:

    def get_model_field_names(self, model, ignore_fields=None):
        """
        ::param model is a Django model class
        ::param ignore_fields is a list of field names to ignore by default
        This method gets all model field names (as strings) and returns a list
        of them ignoring the ones we know don't work (like the 'content_object' field)
        """
        if ignore_fields is None:
            ignore_fields = ['content_object']
        model_fields = model._meta.get_fields()
        model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
        return model_field_names

    def get_lookup_fields(self, model, fields=None):
        """
        ::param model is a Django model class
        ::param fields is a list of field name strings.
        This method compares the lookups we want vs the lookups
        that are available. It ignores the unavailable fields we passed.
        """
        model_field_names = self.get_model_field_names(model)
        if fields is not None:
            '''
            we'll iterate through all the passed field_names
            and verify they are valid by only including the valid ones
            '''
            lookup_fields = []
            for x in fields:
                if "__" in x:
                    # the __ is for ForeignKey lookups
                    lookup_fields.append(x)
                elif x in model_field_names:
                    lookup_fields.append(x)
        else:
            '''
            No field names were passed, use the default model fields
            '''
            lookup_fields = model_field_names
        return lookup_fields

    def qs_to_dataset(self, qs, fields=None):
        """
        ::param qs is any Django queryset
        ::param fields is a list of field name strings, ignoring non-model field names
        This method is the final step, simply calling the fields we formed on the queryset
        and turning it into a list of dictionaries with key/value pairs.
        """

        lookup_fields = self.get_lookup_fields(qs.model, fields=fields)
        return list(qs.values(*lookup_fields))

    def convert_to_dataframe(self, qs, fields=None, index=None):
        """
        ::param qs is an QuerySet from Django
        ::fields is a list of field names from the Model of the QuerySet
        ::index is the preferred index column we want our dataframe to be set to

        Using the methods from above, we can easily build a dataframe
        from this data.
        """
        lookup_fields = self.get_lookup_fields(qs.model, fields=fields)
        index_col = None
        if index in lookup_fields:
            index_col = index
        elif "id" in lookup_fields:
            index_col = 'id'
        values = self.qs_to_dataset(qs, fields=fields)
        df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
        return df

    def qs_to_local_csv(self, qs, fields=None, path=None, filename=None):

        media_dir = settings.MEDIA_ROOT
        media_url = settings.MEDIA_URL

        if path is None:
            if not os.path.exists(media_dir):
                '''
                media folder doesn't exist, make it!
                '''
                os.mkdir(media_dir)
            path = os.path.join(media_dir, 'csvstorage')
            if not os.path.exists(path):
                '''
                CSV storage folder doesn't exist, make it!
                '''
                os.mkdir(path)

        if filename is None:
            model_name = slugify(qs.model.__name__)
            filename = "{}.csv".format(model_name)

        filepath = os.path.join(path, filename)

        media_filepath = os.path.join(media_url, 'csvstorage', filename)

        lookups = self.get_lookup_fields(qs.model, fields=fields)
        dataset = self.qs_to_dataset(qs, fields)
        rows_done = 0
        with open(filepath, 'w') as my_file:
            writer = csv.DictWriter(my_file, fieldnames=lookups)
            writer.writeheader()
            for data_item in dataset:
                writer.writerow(data_item)
                rows_done += 1
        return media_filepath

    def parse_csv_to_list(self, file):
        """

        :param file:
        :return:
        """
        param_file = io.TextIOWrapper(file)
        data = csv.DictReader(param_file)

        items = self.drop_duplicate_row(data)

        return items

    def drop_duplicate_row(self, data):

        df = pd.DataFrame(data)
        df = df.drop_duplicates()
        return df.T.to_dict().values()
