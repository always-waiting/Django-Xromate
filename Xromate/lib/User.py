# encoding:utf-8
"""
Xromate系统user表,用于记录xromate系统的用户信息
"""
import mongoengine as mongoe
from Xromate.apps import XromateConfig, dumpstring

class Users(mongoe.Document):
    """
    collection name: user
    """
    meta = {
        'db_alias': XromateConfig.alias,
    }
    username = mongoe.StringField()
    name = mongoe.StringField()
    can_create_group = mongoe.StringField()
    created_at = mongoe.StringField()
    avatar_url = mongoe.StringField()
    email = mongoe.StringField()
    is_admin = mongoe.StringField()
    projects_limit = mongoe.IntField()
    linkedin = mongoe.StringField()
    theme_id = mongoe.IntField()
    state = mongoe.StringField()
    twitter = mongoe.StringField()
    private_token = mongoe.StringField()
    bio = mongoe.StringField()
    identities = mongoe.StringField()
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

    def __str__(self):
        string = ["{\n"]
        for k, v in self._data.iteritems():
            string.append("\t%s => \n" % k)
            string.append(dumpstring(v, level=2))
        string.append("}\n")
        return "".join(string)

