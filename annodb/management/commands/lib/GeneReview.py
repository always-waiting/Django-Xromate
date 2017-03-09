# encoding: utf-8

import annodb.models as dbmodels
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
import annodb.lib.parser as parser
from threading import Thread
from Queue import Queue
import json
import urllib3
urllib3.disable_warnings()

http = urllib3.PoolManager()

def importdb(cmdobj, **opt):
    """
    导入GeneReview数据库
    只导入accession，gene_symbol，description三个字段
    """
    print "开发"
    register_connection("cmd-import", opt['db'], opt['host'])
    url = "ftp.ncbi.nih.gov"
    path = "pub/GeneReviews/"
    filename = "GRshortname_NBKid_genesymbol_dzname.txt"
    queue = Queue()
    with switch_db(dbmodels.GeneReview, "cmd-import") as GeneReview:
        GeneReview.objects.delete()
        GRparser = parser.ParseGeneReview(url, path, filename, opt['debug'])
        for one in GRparser:
            update_location0(one, GeneReview, opt['debug'])
        """
            queue.put(one)

        thread = []
        for i in range(3):
            worker = Thread(target=update_location, args=(i,queue, GeneReview, opt['debug']))
            worker.setDaemon(True)
            worker.start()
            thread.append(worker)
        queue.join()
        for i in thread:
            i.join()
            #gene = GeneReview(**one)
            #gene.save()
        """
def update_location0(one, GeneReview, debug = False):
    if debug:
        print "Download %s"  % one['gene_symbol']
    url = "http://grch37.rest.ensembl.org/lookup/symbol/homo_sapiens/%s?content-type=application/json" % one['gene_symbol']
    try:
        tx = http.request('GET', url)
        if tx.status == 200:
            data = json.loads(tx.data.decode('utf-8'))
            one['chr'] = data['seq_region_name']
            one['end'] = int(data['end'])
            one['start'] = int(data['start'])
            gene = GeneReview(**one)
            gene.save()
        else:
            raise Exception("下载%s坐标失败" % one['gene_symbol'])
    except Exception,e:
        print "[Error] for get %s\n%s" % (url,e)



def update_location(worker, q, GeneReview, debug=False):
    """
    通过GeneReview数据库，更新chr, start, end字段
    """
    while True:
        if debug:
            print "Worker %s is living" % worker
        one = q.get()
        url = "http://grch37.rest.ensembl.org/lookup/symbol/homo_sapiens/%s?content-type=application/json" % one['gene_symbol']
        try:
            tx = http.request('GET', url)
            if tx.status == 200:
                data = json.loads(tx.data.decode('utf-8'))
                one['chr'] = data['seq_region_name']
                one['end'] = int(data['end'])
                one['start'] = int(data['start'])
                gene = GeneReview(**one)
                gene.save()
            else:
                raise Exception("下载%s坐标失败" % one['gene_symbol'])
        except Exception,e:
            if debug:
                print "[Error] for get %s\n%s" % (url,e)
            #q.put(one)
        finally:
            q.task_done()
        if q.qsize() == 0:
            if debug:
                print "队列为空"
            break

