import json
from collections import OrderedDict

from django import forms
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from jsonfield import JSONCharField, JSONField


class JsonModel(models.Model):
    json = JSONField()
    default_json = JSONField(default={"check": 12})
    complex_default_json = JSONField(default=[{"checkcheck": 1212}])
    empty_default = JSONField(default={})


class GenericForeignKeyObj(models.Model):
    name = models.CharField('Foreign Obj', max_length=255, null=True)


class JSONModelWithForeignKey(models.Model):
    json = JSONField(null=True)
    foreign_obj = GenericForeignKey()
    object_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                     on_delete=models.CASCADE)


class JsonCharModel(models.Model):
    json = JSONCharField(max_length=100)
    default_json = JSONCharField(max_length=100, default={"check": 34})


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, complex):
            return {
                '__complex__': True,
                'real': obj.real,
                'imag': obj.imag,
            }

        return json.JSONEncoder.default(self, obj)


def as_complex(dct):
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    return dct


class JSONModelCustomEncoders(models.Model):
    # A JSON field that can store complex numbers
    json = JSONField(
        dump_kwargs={'cls': ComplexEncoder, "indent": 4},
        load_kwargs={'object_hook': as_complex},
    )


class OrderedJsonModel(models.Model):
    json = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})


class JsonNotRequiredModel(models.Model):
    json = JSONField(blank=True, null=True)


class JsonNotRequiredForm(forms.ModelForm):
    class Meta:
        model = JsonNotRequiredModel
        fields = '__all__'
