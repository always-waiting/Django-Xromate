# encoding: utf-8

import annodb.models as dbmodels
import urllib3
urllib3.disable_warnings()
import json
from mongoengine import register_connection
from mongoengine.context_managers import switch_db


positions = (
    { 'chr': 1, 'start': 1, 'end': 249250621 },
    { 'chr': 2, 'start': 1, 'end': 243199373 },
    { 'chr': 3, 'start': 1, 'end': 198022430 },
    { 'chr': 4, 'start': 1, 'end': 191154276 },
    { 'chr': 5, 'start': 1, 'end': 180915260 },
    { 'chr': 6, 'start': 1, 'end': 171115067 },
    { 'chr': 7, 'start': 1, 'end': 159138663 },
    { 'chr': 8, 'start': 1, 'end': 146364022 },
    { 'chr': 9, 'start': 1, 'end': 141213431 },
    { 'chr': 10, 'start': 1, 'end': 135534747 },
    { 'chr': 11, 'start': 1, 'end': 135006516 },
    { 'chr': 12, 'start': 1, 'end': 133851895 },
    { 'chr': 13, 'start': 17900000, 'end': 115169878 },
    { 'chr': 14, 'start': 17600000, 'end': 107349540 },
    { 'chr': 15, 'start': 19000000, 'end': 102531392 },
    { 'chr': 16, 'start': 1, 'end': 90354753 },
    { 'chr': 17, 'start': 1, 'end': 81195210 },
    { 'chr': 18, 'start': 1, 'end': 78077248 },
    { 'chr': 19, 'start': 1, 'end': 59128983 },
    { 'chr': 20, 'start': 1, 'end': 63025520 },
    { 'chr': 21, 'start': 13200000, 'end': 48129895 },
    { 'chr': 22, 'start': 13200000, 'end': 51304566 },
    { 'chr': 'X', 'start': 1, 'end': 155270560 },
    { 'chr': 'Y', 'start': 1, 'end': 59373566 },
)

http = urllib3.PoolManager()

def importdb(cmdobj, **opt):
    """
    导入Decipher Syndrome
    """
    register_connection("cmd-import", opt['db'], opt['host'])
    selectchr = []
    try:
        for i in opt['chr']:
            selectchr.append(positions[i-1])
    except TypeError,e:
        selectchr = positions
    except Exception,e:
        print '[Error] for select chr use all:',e
        selectchr = positions
    url = 'https://decipher.sanger.ac.uk/browser/API/CNV/Syndrome.json'
    with switch_db(dbmodels.DecipherSyndrome,'cmd-import') as DecipherSyndrome:
        for chr_info in selectchr:
            DecipherSyndrome.objects(chr=str(chr_info['chr'])).delete()
        for item in selectchr:
            try:
                r = http.request('GET', url, fields=item)
                if not r.status == 200:
                    print "访问失败"
                    continue
                datas = json.loads(r.data.decode('utf-8'))
                for one in datas:
                    one['no_id'] = one['id']
                    one.pop('id')
                    deciphersyndrome = DecipherSyndrome.objects.create(**one)
                    deciphersyndrome.save()
            except urllib3.exceptions.MaxRetryError, e:
                print e

