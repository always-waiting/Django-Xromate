# encoding: utf-8

import annodb.models as dbmodels
import urllib3
import re
from bs4 import BeautifulSoup
import json
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
from threading import Thread
from Queue import Queue
"""
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
"""
positions = (
    { 'chr': 1, 'start': 1, 'end': 24},
    { 'chr': 2, 'start': 1, 'end': 24313 },
    { 'chr': 3, 'start': 1, 'end': 19800 },
    { 'chr': 4, 'start': 1, 'end': 19116 },
    { 'chr': 5, 'start': 1, 'end': 18090 },
    { 'chr': 6, 'start': 1, 'end': 17117 },
    { 'chr': 7, 'start': 1, 'end': 15913 },
    { 'chr': 8, 'start': 1, 'end': 14632 },
    { 'chr': 9, 'start': 1, 'end': 14121 },
    { 'chr': 10, 'start': 1, 'end': 13547 },
    { 'chr': 11, 'start': 1, 'end': 13516 },
    { 'chr': 12, 'start': 1, 'end': 13395 },
    { 'chr': 13, 'start': 1790, 'end': 11516 },
    { 'chr': 14, 'start': 1760, 'end': 10734 },
    { 'chr': 15, 'start': 1900, 'end': 10253 },
    { 'chr': 16, 'start': 1, 'end': 9035 },
    { 'chr': 17, 'start': 1, 'end': 8119 },
    { 'chr': 18, 'start': 1, 'end': 7807 },
    { 'chr': 19, 'start': 1, 'end': 5912 },
    { 'chr': 20, 'start': 1, 'end': 6302 },
    { 'chr': 21, 'start': 1320, 'end': 4812 },
    { 'chr': 22, 'start': 1320, 'end': 5130 },
    { 'chr': 'X', 'start': 1, 'end': 15527 },
    { 'chr': 'Y', 'start': 1, 'end': 5937 },
)

def importdb(cmdobj, **opt):
    """
    导入Decipher CNV
    """
    # 定位数据库
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
    http = urllib3.PoolManager()
    url = "https://decipher.sanger.ac.uk/browser/API/CNV/Decipher.json"
    # 先删除吧
    with switch_db(dbmodels.DecipherCnv,'cmd-import') as DecipherCNV:
        for chr_info in selectchr:
            DecipherCNV.objects(chr=str(chr_info['chr'])).delete()
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
                    deciphercnv = DecipherCNV.objects.create(**one)
                    deciphercnv.save()
                    #perl中的操作是为了去除有相同patient_id的cnv，我认为这样做不好，尝试保留所有cnv
            except urllib3.exceptions.MaxRetryError, e:
                print e
        # 删除重复的patient_id
        Delete = DecipherCNV.objects.aggregate(
            {'$group':{'_id':'$patient_id', 'count':{'$sum':1}}},
            {'$match':{'count':{'$gt' : 1 }}},
        )
        for one in Delete:
            DecipherCNV.objects(patient_id = one['_id']).delete()
        # 更新表型和性别信息
        ## 设置队列
        queue = Queue()
        ## 设置多线程
        for i in range(10):
            worker = Thread(target=update_phenotypes_sex,args=(i, queue))
            worker.setDaemon(True)
            worker.start()
        ## 设置队列信息
        for chr_info in selectchr:
            for item in DecipherCNV.objects(chr=str(chr_info['chr'])):
                queue.put(item)
        #onecnv = DecipherCNV.objects(patient_id=249937)[0];
        #queue.put(onecnv)
        ## 等待队列结束
        queue.join()


def update_phenotypes_sex(i, q):
    while True:
        cnv = q.get()
        print "Worker",i,"get no id:", cnv.id
        patientId = str(cnv.patient_id)
        http = urllib3.PoolManager()
        # 更新sex
        href_sex = "https://decipher.sanger.ac.uk/patient/"+patientId+"/overview/general"
        sex = ""
        try:
            tx = http.request('GET', href_sex)
            if tx.status == 200:
                soup = BeautifulSoup(tx.data, 'lxml')
                content = soup.find("td").text
                if content.find("Age") != -1:
                    sex = soup.find_all("tr")[1].find_all("td")[1].text.lstrip().rstrip()
                else:
                    sex = soup.find("tr").find_all("td")[1].text.lstrip().rstrip()
            else:
                raise Exception("disconnect to "+href_sex)
        except Exception, e:
            print "[Error] for updating sex type of pid and noid(",patientId, cnv.no_id,"):", e
            q.task_done()
            continue
        # 更新phenotypes
        href = "https://decipher.sanger.ac.uk/patient/"+patientId+"/phenotype"
        phenotypes = []
        try:
            tx = http.request('GET', href)
            if tx.status == 200:
                soup = BeautifulSoup(tx.data, 'lxml')
                get = soup.find("a", href="#phenotype/patient-phenotypes")
                person = str(get['data-person'])
                href_phenotypes = 'https://decipher.sanger.ac.uk/patient/'+patientId+'/person/'+person+'/phenotypes'
                tx = http.request('GET', href_phenotypes)
                if tx.status == 200:
                    soup = BeautifulSoup(tx.data, 'lxml')
                    get = soup.select('div[class~=phenotype-list-group] div[class~=phenotypes-container] div div span')
                    for one in get:
                        phenotypes.append(re.sub("\n|\s{2,}","",one.text).rstrip().lstrip())
                else:
                    raise Exception("disconnect to "+href_phenotypes)
            else:
                raise Exception("diconnect to "+href)
        except Exception,e:
            print "[Error] for updating phenotypes of pid and noid(",patientId, cnv.no_id,"):", e
        finally:
            cnv.update(chr_sex=sex, phenotypes=";".join(phenotypes))
            q.task_done()

