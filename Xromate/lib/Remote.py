# encoding:utf-8
"""
Xromate系统remote表,用于记录远程信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
import urllib2
import urllib
import json

class Remotes(mongoe.Document):
    """
    collection name: remote
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }

    caseid = mongoe.StringField()
    name = mongoe.StringField()
    age = mongoe.StringField()
    sex = mongoe.StringField(choices=['1','2'])
    clientsex = mongoe.StringField()
    yangpintype = mongoe.StringField()
    datatype = mongoe.StringField()
    antenatalmaterial = mongoe.StringField()
    casesize = mongoe.BooleanField()
    hospital = mongoe.StringField()
    sourcedoctor = mongoe.StringField()
    pollutiontext = mongoe.StringField()
    sendpersontext = mongoe.StringField()

    # Pregnacy History
    historybir = mongoe.StringField()
    birthnum = mongoe.StringField()
    historybirtext = mongoe.StringField()
    pregnantnum = mongoe.StringField()
    geneticdispre = mongoe.StringField()
    geneticdispretext = mongoe.StringField()
    chromtype = mongoe.StringField()
    chromtypetext = mongoe.StringField()
    karyomemo = mongoe.StringField()

    # Prenatal Diagnosis
    pregweek = mongoe.StringField()
    pregday = mongoe.StringField()
    mensesperiod = mongoe.StringField()
    ultrasound = mongoe.StringField()
    bloodcheck = mongoe.StringField()
    diagnoses = mongoe.StringField()
    lastmenses = mongoe.StringField()
    ultrasoundtext = mongoe.StringField()
    ultrasoundtext1 = mongoe.StringField()
    ultrasoundtext2 = mongoe.StringField()
    ultrasoundtext3 = mongoe.StringField()
    ultrasoundtext4 = mongoe.StringField()
    diagnosesitem = mongoe.StringField()
    diagnosestext = mongoe.StringField()
    threesyd = mongoe.StringField()
    eighteensyd = mongoe.StringField()
    otherexplain = mongoe.StringField()
    otherdia = mongoe.StringField()

    # Relative Information
    sibcheck = mongoe.StringField()
    sibnumber = mongoe.StringField()
    sibname = mongoe.StringField()
    sibrelation = mongoe.StringField()
    casetype = mongoe.StringField()

    # Clinical Information
    sickphenop = mongoe.StringField()
    othersickphenop = mongoe.StringField()
    geneticdispro = mongoe.StringField()
    geneticdisprotext = mongoe.StringField()
    diagnosesresult = mongoe.StringField()
    clinicinfor = mongoe.StringField()

    #
    status = mongoe.StringField()
    samplestatus = mongoe.StringField(choices=['1','2','3','4','5','6','7','8'])
    interalresult = mongoe.StringField()
    karyotype = mongoe.StringField()
    sampledate = mongoe.StringField()
    reportdate = mongoe.StringField()
    resultexp = mongoe.StringField()
    location = mongoe.StringField()
    mcc = mongoe.StringField()

    #
    sample = mongoe.DictField()

    def get_remote(self):
        data = json.dumps({'caseid': self.caseid})
        url = XromateConfig.remote_get_url
        headers = {'Content-Type': 'application/json'}
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        result = json.loads(response.read())
        result['datatype'] = result['data']
        if result['casesize'] == 'false':
            result['casesize'] = False
        else:
            result['casesize'] = True
        del result['data']
        return result

    def pull(self):
        new = self.get_remote()
        self.update(**new)
        self.reload()


    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)
