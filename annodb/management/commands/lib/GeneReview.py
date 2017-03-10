# encoding: utf-8
import os
import annodb.models as dbmodels
from mongoengine import register_connection
from mongoengine.context_managers import switch_db
import annodb.lib.parser as parser
import re
import urllib3
from threading import Thread
from Queue import Queue
from bs4 import BeautifulSoup
urllib3.disable_warnings()



def importdb(cmdobj, **opt):
    """
    导入GeneReview数据库
    只导入accession，gene_symbol，description三个字段
    """
    register_connection("cmd-import", opt['db'], opt['host'])
    url = "ftp.ncbi.nih.gov"
    path = "pub/GeneReviews/"
    filename = "GRshortname_NBKid_genesymbol_dzname.txt"
    GRparser = parser.ParseGeneReview(url, path, filename, opt['debug'], opt['nthread'])
    itervalue = iter(GRparser)
    if opt['test']:
        pass
    else:
        if opt['debug']: print "删除数据库原有信息"
        with switch_db(dbmodels.GeneReview, "cmd-import") as GeneReview:
            GeneReview.objects.delete()
            for one in itervalue:
                gene = GeneReview(**one)
                gene.save()

def download_html(cmdobj, **opt):
    """
    从NCBI下载需要的HTML
    """
    print "开发"
    dhtml = GeneReviewDownloadHTML(debug = opt['debug'], path = opt['outdir'], num = opt['nthread'])
    dhtml.download_entry()
    dhtml.trim_html()


class GeneReviewDownloadHTML(object):
    def __init__(self, path = "./genereviewhtml", num = 10, debug=False):
        self.urlbook = "https://www.ncbi.nlm.nih.gov/books/NBK1116/";
        self.urlbase = "http://www.ncbi.nlm.nih.gov/books/n/gene"
        self.http = urllib3.PoolManager()
        self.debug = debug
        self.path = path
        self.queue = Queue()
        self.nthread = num
        self.thread = []
        for i in range(self.nthread):
            worker = worker = Thread(target=self._handle_file)
            worker.setDaemon(True)
            self.thread.append(worker)
        self._get_items_url()

    def _get_items_url(self):
        count = 0;
        while True:
            if self.debug: print "Try to generate itmes url times %s" % count
            try:
                tx = self.http.request("GET", self.urlbook)
            except Exception,e:
                if count< 10:
                    count += 1
                    if self.debug:
                        print "[Error] for get items url\n%s, 再次尝试" % e
                else:
                    raise Exception("[Error] 多次尝试失败，退出")
                continue
            if tx.status == 200:
                if self.debug: print "Download from %s done!" % self.urlbook
                soup = BeautifulSoup(tx.data,'lxml')
                items = soup.select("ul[id=toc_tllNBK1116_toc_del1p36]")[0].select('li[class=half_rhythm]')
                geneitems = [ one['id'] for one in items]
                geneitems.pop();geneitems.pop();geneitems.pop();geneitems.pop()
                items_url = []
                for one in geneitems:
                    get = re.search("NBK1116_(?:toc_)?(.+)$",one,flags=re.IGNORECASE)
                    if get:
                        url_get = "%s/%s" % (self.urlbase,get.group(1))
                        items_url.append(url_get)
                    else:
                        if self.debug: print "Fail to get %s url" % one
                self.items_url = items_url
                if self.debug: print "Generate items_url done!"
                break
            else:
                if count < 10:
                    count += 1
                    if self.debug:
                        print "[Error] for connect %s of status %s\n再次尝试" % (self.urlbook,tx.status)
                    continue
                else:
                    raise Exception("[Error] 多次尝试失败，退出")

    def download_entry(self):
        # 测试目录存在
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if self.debug:
            #fun = [self.items_url[0]]
            fun = self.items_url
        else:
            fun = self.items_url
        for url in fun:
            count = 0
            while True:
                if self.debug: print "Begin Downloading %s - times: %s" % (url,count)
                try:
                    tx = self.http.request("GET", url)
                except Exception,e:
                    if count < 10:
                        count += 1
                        if self.debug:
                            print "[Error] for http request of %s,再次尝试" % url
                        continue
                    else:
                        if self.debug: print "多次尝试,退出"
                        break
                if tx.status == 200:
                    with open("%s/%s" % (self.path, os.path.basename(url)), "w") as f:
                        f.write(tx.data)
                    if self.debug: print "Download %s done!" % url
                    break
                else:
                    if count < 10:
                        count += 1
                        if self.debug:
                            print "[Error] for get entry of %s,再次尝试" % url
                        continue
                    else:
                        if self.debug: print "多次尝试,退出"
                        break

    def trim_html(self):
        if not os.path.exists(self.path):
            raise Exception("%s not exists. Please run download_entry first" % self.path)
        if self.debug:
            print "Trim html"
        files= os.listdir(self.path)
        for filename in files:
            if not os.path.isdir(filename):
                self.queue.put(filename)
            else:
                if self.debug: print "%s is not file" % filename
        for worker in self.thread:
            worker.start()
        for worker in self.thread:
            worker.join()
        self.queue.join()

    def _handle_file(self):
        while True:
            if self.queue.qsize() == 0:
                if self.debug: print "队列为空"
                break
            filename = self.queue.get()
            if self.debug: print "Trim file %s" % filename
            with open("%s/%s" % (self.path,filename)) as f:
                soup = BeautifulSoup(f.read(), 'lxml')
                map(lambda x: x.extract(), soup.select('div[class="post-content"]'))
                map(lambda x: x.extract(), soup.select('div[class="pre-content"]'))
                map(lambda x: x.extract(), soup.select('div[class=top]'))
                map(lambda x: x.extract(), soup.select('div[id=rightcolumn]'))
                map(lambda x: x.extract(), soup.select('div[id=footer]'))
                map(lambda x: x.extract(), soup.findAll('meta'))
                map(lambda x: x.extract(), soup.findAll('script'))
                map(lambda x: x.extract(), soup.findAll('link'))
                head = soup.find('head')
                head_add_tag1 = soup.new_tag('link', href="//static.pubmed.gov/portal/portal3rc.fcgi/4098875/css/3852956/3985586/3808861/3734262/3974050/3917732/251717/4098876/14534/45193/4113719/3849091/3984811/3751656/4033350/3840896/3577051/3852958/4008682/3881636/3579733/4062871/12930/3964959/3854974/36029/4052581/9685/3549676/3609192/3609193/3609213/3395586.css", rel="stylesheet", type="text/css")
                head_add_tag2 = soup.new_tag('link', href="//static.pubmed.gov/portal/portal3rc.fcgi/4098875/css/3411343/3882866.css", media="print", rel="stylesheet", type="text/css")
                head.append(head_add_tag1)
                head.append(head_add_tag2)
                nbk =  soup.select('.meta-content.fm-sec')[0].select("h1")[0]['id'].replace("_","")
                if self.debug: print "NBK: %s" % nbk
                for img in soup.findAll("img"):
                    img['src'] = "http://www.ncbi.nlm.nih.gov%s" % img['src']
                    if img.has_attr("src-large"):
                        img['src-large'] = "http://www.ncbi.nlm.nih.gov%s" % img['src-large']
                for a in soup.findAll('a'):
                    if not a['href'].startswith("#"):
                        a['href'] = "http://www.ncbi.nlm.nih.gov%s" % a['href']
                with open("%s/%s.html" % (self.path,nbk),"w") as f:
                    f.write(str(soup))
            os.remove("%s/%s" % (self.path,filename))
            self.queue.task_done()

