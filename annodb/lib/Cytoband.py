#encoding: utf-8
"""
注释数据库的cytoband表
"""
import mongoengine as mongoe
from annodb.apps import AnnodbConfig, dumpstring
import re

class Cytoband(mongoe.Document):
    """
    collection name: cytoband
    """
    meta = {
        'db_alias': AnnodbConfig.alias,
    }

    description  = mongoe.StringField()
    name = mongoe.StringField()
    chr = mongoe.StringField()
    chrom = mongoe.StringField()
    start = mongoe.IntField()
    end = mongoe.IntField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

    @classmethod
    def cytoband_region_to_coordinates(cls, region):
        #print region
        res = re.search('(1?[1-9]|10|2[0-2]|X|Y)([pqc]\S*)$', region)
        if res:
            #print region
            chrom = res.group(1)
            locs = res.group(2).split('-')
            #print locs
            match = re.compile("|".join(locs))
            cytos = cls.objects(chr=chrom, name=match).only('start','end').order_by('start')
            #if len(cytos) > 3:
                #print "Chr: %s" % chrom
                #print len(cytos)
                #print "Match: %s" % "|".join(locs)
                #print cytos[0].chr, cytos[0].start, cytos[0].end
                #print cytos[-1].chr, cytos[-1].start, cytos[-1].end
            coord = {'chr': chrom}
            if not len(cytos):
                print "%s is not cytoband locus" % region
                return
            if locs[0] == 'pter':
                coord['start'] = 0
            elif locs[0] == 'cen':
                p_or_q = 'p' if locs[1].find("p") != -1 else 'q'
                coord['start'] = cls.objects(chr=chrom, description='acen', name=re.compile(p_or_q)).first().start
            else:
                coord['start'] = cytos.order_by('start')[0].start
            if len(locs) > 1 and locs[1] == 'qter':
                coord['end'] = cls.objects.aggregate(
                    {'$match':{'chr':chrom}},
                    {'$group':{'_id':None, 'end':{'$max':'$end'}}}
                ).next()['end']
            else:
                coord['end'] = cytos.order_by('-end')[0].end
            return coord
        else:
            print "%s is not cytoband locus" % region
            return
