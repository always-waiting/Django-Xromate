# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
import mongoengine as mongoe
from lib.OmimEntry import OmimEntry
from lib.DgvVarient import DgvVarient
from lib.OmimGenemap import OmimGenemap
from lib.OmimMorbidmap import OmimMorbidmap
from lib.DecipherCNV import DecipherCnv
from lib.DecipherSyndrome import DecipherSyndrome
from lib.ClinVar import ClinVar
from lib.GeneReview import GeneReview
from lib.Pubmed import Pubmed
from lib.UcscRefflat import UcscRefflat
from lib.Cytoband import Cytoband
from apps import AnnodbConfig
# Create your models here.

mongoe.connect(
    AnnodbConfig.db,
    host=AnnodbConfig.host,
    alias=AnnodbConfig.alias
)
