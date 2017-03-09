# encoding: utf-8
"""
注释数据库的gene_review表
"""

import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring

class GeneReview(mongoe.Document):
    """
    collection name: gene_review
     L<GeneReviews|http://www.ncbi.nlm.nih.gov/books/NBK1116/>
     an international point-of-care resource for busy clinicians,
     provides clinically relevant and medically actionable information
     for inherited conditions in a standardized journal-style format,
     covering diagnosis, management, and genetic counseling for patients
     and their families. Each chapter in GeneReviews is written by one or
     more experts on the specific condition or disease and goes through a
     rigorous editing and peer review process before being published online.
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }
    accession = mongoe.StringField()
    chr = mongoe.StringField()
    gene_symbol = mongoe.StringField()
    description = mongoe.StringField()
    start = mongoe.IntField()
    end = mongoe.IntField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)


