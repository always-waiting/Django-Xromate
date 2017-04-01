# encoding:utf-8
"""
Xromate系统user表,用于记录xromate系统的用户信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring
import urllib2
import urllib
import json

class Users(mongoe.Document):
    """
    collection name: user
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }
    username = mongoe.StringField()
    name = mongoe.StringField()
    can_create_group = mongoe.BooleanField()
    created_at = mongoe.StringField()
    avatar_url = mongoe.StringField()
    email = mongoe.StringField()
    is_admin = mongoe.BooleanField()
    projects_limit = mongoe.IntField()
    linkedin = mongoe.StringField()
    theme_id = mongoe.IntField()
    state = mongoe.StringField()
    twitter = mongoe.StringField()
    private_token = mongoe.StringField()
    bio = mongoe.StringField()
    identities = mongoe.ListField()
    two_factor_enabled = mongoe.BooleanField()
    website_url = mongoe.StringField()
    can_create_project = mongoe.BooleanField()
    web_url = mongoe.StringField()
    current_sign_in_at = mongoe.StringField()
    color_scheme_id = mongoe.IntField()
    skype = mongoe.StringField()
    access_token = mongoe.StringField()
    confirmed_at = mongoe.StringField()
    last_sign_in_at = mongoe.StringField()
    external = mongoe.BooleanField()
    location = mongoe.StringField()
    organization = mongoe.StringField()
    blocked = mongoe.BooleanField()

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

    def access_level(self):
        try:
            res = urllib2.urlopen("http://192.168.4.168:10080/api/v3/projects/bioinformatics%2Fberry-xromate?access_token=" +  self.access_token)
        except urllib2.URLError,e:
            return 0
        if res:
            if res.getcode() == 200:
                data = json.loads(res.read().encode("utf8"))
                return data['permissions']['project_access']['access_level']
            else:
                return 0
        else:
            return 0

    @property
    def role(self):
        levels2role = {
            10: 'analyst',
            20: 'auditor',
            30: 'auditor',
            40: 'master',
            50: 'owner',
        }
        try:
            return levels2role[self.access_level()]
        except KeyError,e:
            return None


