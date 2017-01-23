from __future__ import unicode_literals

from django.db import models
import mongoengine as mongoe
from mysite.settings import DATABASES
# Create your models here.

mongoe.connect(DATABASES['annodb']['NAME'])

class Employee(mongoe.Document):
    email = mongoe.StringField(required=True)
    first_name = mongoe.StringField(max_length=50)
    last_name = mongoe.StringField(max_length=50)

"""DGV_field_str = [
    "method","platform","reference","variantSubtype", "variantType", "mergedVariants",
    "supportingVariants", "mergedOrSample", "cohortDescription", "genes", "samples", "chr",
    "variantAccession"
]
DGV_field_int = [
    "start", "end", "pubmedid", "observedLosses",
    "observedGains", "sampleSize", "frequency"
]
"""
class DgvVarient(mongoe.Document):
    """
    collection name: dgv_varient
    """
    variantAccession = mongoe.StringField(required=True)
    chr = mongoe.StringField()
    method = mongoe.StringField()
    platform = mongoe.StringField()
    reference = mongoe.StringField()
    variantSubtype = mongoe.StringField()
    variantType = mongoe.StringField()
    mergedVariants = mongoe.StringField()
    supportingVariants = mongoe.StringField()
    mergedOrSample = mongoe.StringField()
    cohortDescription = mongoe.StringField()
    genes = mongoe.StringField()
    samples = mongoe.StringField()

    start = mongoe.IntField()
    end = mongoe.IntField()
    pubmedid = mongoe.IntField()
    observedLosses = mongoe.IntField()
    observedGains = mongoe.IntField()
    sampleSize = mongoe.IntField()
    frequency = mongoe.IntField()




