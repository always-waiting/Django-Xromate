# encoding: utf-8
"""
在这里定义参考数据库的dgv_varient表
"""
from __future__ import unicode_literals
from django.db import models
import mongoengine as mongoe


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

