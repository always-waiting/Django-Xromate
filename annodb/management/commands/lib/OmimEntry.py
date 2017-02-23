# encoding: utf-8
import os
import StringIO
import re
import annodb.models as dbmodels
import mongoengine

#print "2"*60
#dbmodels.dbconnection('test', 'mongodb://192.168.4.13:27017')
def test():
    print u"这时一个测试，用于判断是否成功加载"

def omim_entry_import(cmdobj, **options):
    u"""
    导入omim.txt到数据库
    """
    #print "开发omim_entry_import命令"
    # 检查文件是否存在
    if not os.path.exists(options['input']):
        raise Exception(options['input'] + " not exists");
    # 检查能否链接数据库
    try:
        #print "0"*60
        mongoengine.register_connection("cmd-omimentry-import", options['db'], options['host'])
    except:
        raise Exception(u"链接数据库" + options['host'] + "/" + options['db']+ u"失败")
    # 开发文件解析函数
    with open(options['input']) as f:
        for chunk in myreadlines(f, '*RECORD*'):
            if not chunk: continue;
            if chunk.find("*THEEND*") != -1: break
            """
            开发文件解析函数完成
            """
            #if chunk.find('104760') != -1:
            record = parser_omim_item(chunk);
            try:
                pass
                #debugprint(record['referenceList'][0])
            except:
                pass
            """
            开发解析后导入数据库的代码
            """
            import_omim_entry(record)
            #break; #目前只导入一个


def import_omim_entry(record):
    with mongoengine.context_managers.switch_db(dbmodels.OmimEntry, "cmd-omimentry-import") as dbmodels.OmimEntry:
        try:
            entry = dbmodels.OmimEntry.objects.get(mimNumber = record['mimNumber'])
        except dbmodels.OmimEntry.DoesNotExist:
            # 插入样本
            entry = dbmodels.OmimEntry(**record)
            entry.save()
        except dbmodels.OmimEntry.MultipleObjectsReturned:
            raise Exception(u"有多条记录，需要人工核查!")
        except:
            raise Exception(u"在数据库查询时出现未知错误")


def parser_omim_item(chunk):
    record = {}
    for field in chunk.split("*FIELD*"):
        if not field: continue
        if field == "\n": continue
        content = StringIO.StringIO(field)
        header = content.next().rstrip().lstrip()
        if header.upper().find("NO") != -1:
            parser_header_no(content, record);
        elif header.upper().find("TI") != -1:
            parser_header_ti(content, record)
        elif header.upper().find("TX") != -1:
            parser_header_tx(content, record)
        elif header.upper().find("SA") != -1:
            parser_header_sa(content, record)
        elif header.upper().find("RF") != -1:
            parser_header_rf(content, record)
        elif header.upper().find("CS") != -1:
            parser_header_cs(content, record)
        elif header.upper().find("CN") != -1:
            parser_header_cn(content, record)
        elif header.upper().find("CD") != -1:
            parser_header_cd(content, record)
        elif header.upper().find("ED") != -1:
            parser_header_ed(content, record)
        elif header.upper().find("AV") != -1:
            parser_header_av(content, record)
        else:
            raise Exception(header + u"没有对应的解析器!!")
        #debugprint(header)
    return record

def parser_header_cs(content, record):
    #pass
    record_cs = {}
    record_cs['mimNumber'] = record['mimNumber']
    record_cs['prefix'] = record['prefix']
    record_cs['preferredTitle'] = record['title']['preferredTitle']
    record_cs['oldFormatExists'] = False
    text = content.read().lstrip().rstrip()
    if not text: return
    items = [ re.sub("\s+", " ", n.replace(":","")).lstrip().rstrip() for n in re.split("([A-z, ]+\:\n)",text)]
    #debugprint(text)
    if not items[0]: items.pop(0)
    number = len(items)/2.
    if number.is_integer():
        for i in range(int(number)):
            key = items[2*i]
            cs_content = items[2*i+1]
            if re.match(\
                "INHERITANCE|GROWTH|HEAD AND NECK|CARDIOVASCULAR|RESPIRATORY|CHEST|ABDOMEN|GENITOURINARY|SKELETAL|SKIN\, NAILS\, HAIR|\
                MUSCLE.*SOFT.*TISSUE|NEUROLOGIC|VOICE|METABOLIC FEATURES|ENDOCRINE FEATURES|HEMATOLOGY|IMMUNOLOGY|NEOPLASIA|PRENATAL MANIFESTATIONS|\
                LABORATORY ABNORMALITIES|MISCELLANEOUS|MOLECULAR BASIS",\
                key):
                if not cs_content: continue
                key_attr = key.title().replace(" ","")
                key_attr = key_attr[0].lower() + key_attr[1:]
                innercontent = re.split('(\[[^;]+\]\;)', cs_content)
                if not innercontent[0]: innercontent.pop(0)
                if len(innercontent) % 2: #有键的介绍
                    key_desc = innercontent.pop(0)
                else:
                    key_desc = ""
                record_cs[key_attr+'Exists'] = True
                if key_desc: record_cs[key_attr] = key_desc
                if not len(innercontent): continue
                for i in range(int(len(innercontent)/2)):
                    #sub_key = innercontent[2*i]
                    #sub_conntent = innercontent[2*i+1]
                    sub_attr = key_attr + re.sub("\[|\];|,","",innercontent[2*i].title()).replace(" ","")
                    record_cs[sub_attr+"Exists"] = True
                    record_cs[sub_attr] = innercontent[2*i+1].lstrip().rstrip()
            else:
                record_cs['oldFormatExists'] = True
                try:
                    record_cs['oldFormat'][key] = cs_content
                except:
                    record_cs['oldFormat'] = {key:cs_content}
        record['clinicalSynopsis'] = record_cs
        record['clinicalSynopsisExists'] = True
    else:
        #debugprint(items)
        #raise Exception(u"CS域的值非偶数")
        print u"CS域的值非偶数,因此不导入数据库".encode('utf-8').strip()



def parser_header_av(content, record):
    record['allelicVariantExists'] = True
    rawList = re.split("\n\.(\d{4})\n","\n" + content.read().lstrip().rstrip())
    if not rawList[0]: rawList.pop(0)
    number = int(len(rawList)/2)
    allelicVariantList = []
    for i in range(number):
        allele = rawList[2*i]
        text = rawList[2*i+1].lstrip().rstrip()
        hashlist = {'number': int(allele)}
        try:
            index = text.index("\n")
            name = text[0:index]
            splittext = re.split("\n\n",text[index+1:])
            allelenamestr = splittext.pop(0)
            allelenamelist = re.split(";;", allelenamestr)
            if len(allelenamelist) > 1:
                hashlist['alternativeNames'] = ";;".join(allelenamelist[:-1])
                hashlist['mutations'] = allelenamelist[-1]
            else:
                hashlist['mutations'] = allelenamelist[-1]
            hashlist['text'] = "\n".join([ n.lstrip().rstrip().replace("\n"," ") for n in splittext])
        except:
            """
            只有一行，应该是moved或者removed
            """
            name = text
        if name.lower().find("removed") != -1:
            status = 'removed'
        elif name.lower().find("moved") != -1:
            status = "moved"
        else:
            status = 'live'
        hashlist['name'] = name
        hashlist['status'] = status
        #print hashlist
        allelicVariantList.append(hashlist)
    record['allelicVariantList'] = allelicVariantList

def parser_header_ed(content, record):
    record['editHistory'] = content.read().lstrip().rstrip()

def parser_header_cd(content, record):
    record['createDate'] = content.read().lstrip().rstrip()

def parser_header_cn(content, record):
    record['contributors'] = content.read().lstrip().rstrip()

def parser_header_rf(content, record):
    rfrecords = []
    rflist = [n.replace("\n"," ") for n in re.split("\r?\n\r?\n", content.read())]
    for rf in rflist:
        if not rf:
            continue
        #get = re.match("(\d+)\.\s+([^:]+)\:\s+([^\.]+)[\.\?]+[\s']+(.*)", rf)
        # 不再添加source
        get = re.match("(\d+)\.\s+([^:]+)\:\s+(.+)", rf)
        try:
            refnumber = int(get.group(1))
            authors = get.group(2)
            title = get.group(3)
            source = ""
        except:
            print "$$$$ ->", rf
            #get = re.match("(\d+)\.\s+([^:]+)\:\s+([^\.]+(\.[^\.]+)*)[\.\?]+[\s']+(\D.*)",rf)
            continue
        rfrecords.append({
            'reference' : {
                'referenceNumber' : refnumber,
                'authors'         : authors,
                'title'           : title,
                'source'          : source
            }
        })
        #if int(get.group(1)) == 1: print rf
    record['referenceList'] = rfrecords

def parser_header_sa(content, record):
    record['seeAlso'] = content.read().lstrip().rstrip().replace("\n"," ")

def parser_header_tx(content, record):
    record['textSectionList'] = []
    all = content.read()
    values = [ n.lstrip().rstrip().replace("\n", " ") for n in re.split("\n[A-Z\s]+\n", all)]
    # 第一个总是""
    if not values[0]:
        values.pop(0)
    keys = [ n.lstrip().rstrip().replace("\n", "") for n in re.findall("\n[A-Z\s]+\n", all)]
    if not len(keys):
        record['textSectionList'].append({
            'textSectionName'    : 'text',
            'textSectionTitle'   : 'Text',
            'textSectionContent' : values[0]
        })
        return
    for i in range(len(keys)):
        textsectionname = keys[i].title().replace(" ","")
        textsectionname = textsectionname[0].lower() + textsectionname[1:]
        record['textSectionList'].append({
            'textSectionName'    : textsectionname,
            'textSectionTitle'   : keys[i].title(),
            'textSectionContent' : values[i]
        })



def parser_header_ti(content, record):
    th = content.next().rstrip().lstrip()
    fieldcontent = {}
    get = re.match("(\S?)\d+\s(.*)",th)
    record['prefix'] = get.group(1)
    record['title'] = { 'preferredTitle': get.group(2) }
    move = re.match("MOVED TO (\d+)", get.group(2))
    remove = re.match("REMOVED", get.group(2))
    if remove:
        record['status'] = "removed"
    elif move:
        record['status'] = "moved"
        record['movedTo'] = int(move.group(1))
    else:
        record['status'] = 'live'
    remind = content.read().replace("\n"," ")
    if remind:
        record['title']['alternativeTitles'] = remind

def parser_header_no(content, record):
    mimnumber = content.next().rstrip().lstrip()
    record['mimNumber'] = int(mimnumber)
    print "Go throught mim", record['mimNumber']

def myreadlines(f, newline):
  buf = ""
  while True:
    while newline in buf:
      pos = buf.index(newline)
      yield buf[:pos]
      buf = buf[pos + len(newline):]
    chunk = f.read(4096)
    if not chunk:
      yield buf
      break
    buf += chunk

# inline-tools for development
def debugprint(text):
    print "*"*60
    print text;
    print "#"*60
