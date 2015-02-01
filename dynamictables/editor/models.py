# coding=utf-8
from django.db import models
import yaml, os

class FieldDefinition(object):
    __field_mappings = {
        "int": models.IntegerField,
        "char": models.CharField,
        "date": models.DateField
    }
    def __init__(self, id, title, type):
        self.id = id
        self.title = title
        self.type = type

    def __str__(self):
        return "\n" + str(self.__dict__)

    def __repr__(self):
        return str(self)

    def get_model_field(self):
        if (self.type == "char"):
            return models.CharField(verbose_name=self.title, max_length=255)
        if (self.type == "int"):
            return models.IntegerField(verbose_name=self.title)
        if (self.type == "date"):
            return models.DateField(verbose_name=self.title)
        raise Exception("Not supported field type: " + self.type)

class TableDefinition(object):
    def __init__(self, name, title, fields):
        self.name = name
        self.title = title
        self.fields = fields

    def __str__(self):
        return "\n" + str(self.__dict__)

    def __repr__(self):
        return str(self)

    def get_model_type(self):
        # assuming names are both pythonic and tablename-compatible
        attributes = { x.id : x.get_model_field() for x in self.fields }
        attributes['__module__'] = __name__
        attributes['Meta'] = type('Meta', (), { 'verbose_name' : self.title, 'verbose_name_plural' : self.title })
        return type(self.name, (models.Model,), attributes)

print str(os.path.abspath(os.curdir))

def load_models():
    models = []
    with open("modeltypes.yaml") as definitions:
        table_definitions = yaml.load(definitions).items()
        for table_name, table_data in table_definitions:
            table = TableDefinition(table_name, table_data['title'], map(lambda f: FieldDefinition(**f), table_data['fields']))
            models.append(table.get_model_type())
    return models

all_models = load_models()