# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
import models
from django.http import JsonResponse
import logging
import json
import re

logger = logging.getLogger('django')


# Create your views here.
def index(request):
    return render(request, 'annodb/home.html');

def table_locs(request, table, locs):
    query = QueryRuleGeneration(table, locs, request.GET)
    return JsonResponse(
        [ json.loads(item.to_json()) for item in query.answer() ],
        safe=False
    )

class QueryRuleGeneration(object):
    def __init__(self, table, locs, spec):
        self.table = table;
        (chrom, rlocs) = locs.split(":")
        self.chrom = chrom
        (self.start, self.end) = map(int, rlocs.split("-"))
        self.spec = spec
        self.rule = self.queryrule()
        if table == 'dgv':
            self.coll = models.DgvVarient
        elif table == 'ucscrefgene':
            self.coll = models.UcscRefflat
        elif table == 'omimgenemap':
            self.coll = models.OmimGenemap
        elif table == 'omimmorbidmap':
            self.coll = models.OmimMorbidmap
        elif table == 'deciphercnv':
            self.coll = models.DecipherCnv
        elif table == 'clinvar':
            self.coll = models.ClinVar
        elif table == 'genereview':
            self.coll = models.GeneReview
        elif table == 'deciphersyndrome':
            self.coll = models.DecipherSyndrome
        elif table == 'pubmed':
            self.coll = models.Pubmed
        else:
            raise Exception("[Error] Table %s has not collection in database" % table)

    def answer(self):
        if self.table == 'dgv':
            return self.coll.objects(**self.rule).limit(20)
        else:
            return self.coll.objects(**self.rule)

    def queryrule(self):
        query = {}
        if self.table == 'dgv':
            query['chr'] = int(self.chrom) if self.chrom.isdigit() else self.chrom
            query['start__lte'] = self.end
            query['end__gte'] = self.start
            query['mergedOrSample'] = 'S'
            if self.spec.has_key('type'):
                cnvtype = self.spec['type']
                if cnvtype.find("loss") != -1:
                    query['observedLosses__gt'] = 0
                elif cnvtype.find("gain") != -1:
                    query['observedGains__gt'] = 0
        elif self.table == 'ucscrefgene':
            query['chrom'] = self.chrom
            query['txStart__lte'] = self.end
            query['txEnd__gte'] = self.start
        elif self.table == 'omimgenemap':
            query['chromosomeSymbol'] = self.chrom
            query['chromosomeLocationStart__lte'] = self.end
            query['chromosomeLocationEnd__gte'] = self.start
            query['phenotypeMapList__ne'] = None
        elif self.table == 'omimmorbidmap' :
            query['chr'] = self.chrom
            query['start__lte'] = self.end
            query['end__gte'] = self.start
            query['phenotypeMappingKey__gt'] = 2
        elif re.match("^deciphercnv|clinvar|genereview|deciphersyndrome|pubmed$", self.table):
            query['chr'] = self.chrom
            query['start__lte'] = self.end
            query['end__gte'] = self.start
        return query
