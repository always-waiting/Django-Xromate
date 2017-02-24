# coding: utf8
from django.core.management.base import BaseCommand, CommandError
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os
import textwrap
import lib.OmimEntry
import lib.DGV
import lib.OmimGenemap
import lib.OmimMorbidmap
"""
class Command(BaseCommand):
    help = ''
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write("这是一个测试")
"""
class Command(BaseCommand):

    help = u"Annodbase commands group"

    def cmds_add(self, parser, cmds, hinfo=u"Help info", des=u"Description"):
        cmds = parser.add_parser(
            cmds, formatter_class=RawDescriptionHelpFormatter,
            help=hinfo, description = textwrap.dedent(des)
        )
        return cmds

    def print_args(self, **options):
        print "Args info:"
        for (key, value) in options.iteritems():
            print "\t%20s\t------->\t%-20s" % (key, value)

    def add_arguments(self, parser):
        #　子命令组
        subparsers = parser.add_subparsers(help=u'sub-command help', parser_class=type(ArgumentParser()))
        # DGV命令组
        dgv_cmds = self.cmds_add(
            subparsers, 'dgv',
            u"处理DGV数据库",
            u"""处理DGV数据库,目前只有import功能"""
        )
        dgv_parser = dgv_cmds.add_subparsers(help=u"DGV commands")
        # DGV import action
        self.dgv_parser_import(dgv_parser)
        # OMIM数据库命令组
        omim_cmds = self.cmds_add(
            subparsers, "omim",
            u"处理关于OMIM数据库的所有表。一共有n个表和OMIM有关",
            u"""
            OMIM数据库的命令组
            目前正在开发阶段，过程如下
            1.完成entry表的导入功能
            2.开发genemap表的导入功能
            """
        )
        omim_parser = omim_cmds.add_subparsers(help=u"OMIM subtables")
        # OMIM -> ENTRY命令组
        omim_entry_cmds = self.cmds_add(
            omim_parser, "entry",
            u"omim数据库entry表的命令组",
            u"""
            处理omim_entry表的各种动作
            目前完成了entry表的导入命令:import
            """
        )
        omim_entry_parser = omim_entry_cmds.add_subparsers(help=u"OMIM Entry table actions")
        # OMIM ENTRY import action
        self.omim_entry_parser_import(omim_entry_parser)

        # OMIM -> genemap命令组
        omim_genemap_cmds = self.cmds_add(
            omim_parser, "genemap",
            u"omim数据库genemap表的命令组",
            u"""
            处理omim_genemap表的各种动作
            目录开发genemap表的导入命令:import
            """
        )
        omim_genemap_parser = omim_genemap_cmds.add_subparsers(help=u"OMIM Genemap table actions")
        # OMIM Genemap import action
        self.omim_genemap_parser_import(omim_genemap_parser)
        # OMIM Genemap update OMIM Entry action
        self.omim_genemap_parser_update_entry(omim_genemap_parser)

        # OMIM -> morbidmap命令组
        omim_morbidmap_cmds = self.cmds_add(
            omim_parser, "morbidmap",
            u"omim数据库morbidmap表的命令组",
            u"""
            处理omim_morbidmap表的各种动作
            目前开发morbidmap表的导入命令:import
            """
        )
        omim_morbidmap_parser = omim_morbidmap_cmds.add_subparsers(help=u"Omim Morbidmap table actions")
        ## Omim Morbidmap import action
        self.omim_morbidmap_parser_import(omim_morbidmap_parser)
        ## OMIM Morbidmap update OMIM Genemap action
        self.omim_morbidmap_parser_update_genemap(omim_morbidmap_parser)
        ## OMIM Morbidmap update OMIM Entry action
        self.omim_morbidmap_parser_update_entry(omim_morbidmap_parser)


    """
    以下是调用的方法
    """
    def omim_morbidmap_parser_update_entry(self, parser):
        morbidmap_update_entry = parser.add_parser("update_entry", help=u"从omim_morbidmap中获取信息，更新到omim_genemap",
            description = textwrap.dedent(u"""
            通过mimNumber，从omim_morbidmap中获得信息更新到omim_entry。如果没给出mimNumber,则全部更新。mimNumber用空格分开
            """)
        )
        morbidmap_update_entry.add_argument("--mimNumber", "-mim", type=str, nargs='*', help="mimNumber need to update. If not given, all mimNumber will be updated. Different mimNumber split with blackspace")
        morbidmap_update_entry.add_argument("--entryhost","-eh", type=str, help="Host for omim_entry", default="mongodb://localhost:27017")
        morbidmap_update_entry.add_argument("--entrydb", "-edb", type=str, help="db name for omim_entry", default="dbtest")
        morbidmap_update_entry.add_argument("--morbidmaphost", "-mh", type=str, help="Host for omim_morbidmap", default="mongodb://localhost:27017")
        morbidmap_update_entry.add_argument("--morbidmapdb", "-mdb", type=str, help="db name for omim_morbidmap", default="dbtest")
        morbidmap_update_entry.set_defaults(func=lib.OmimMorbidmap.update_entry)

    def omim_morbidmap_parser_import(self, parser):
        morbidmap_import = parser.add_parser("import", help=u"OMIM Morbidmap表的导入",
            description = textwrap.dedent(u"""
            导入Morbidmap表。处理morbidmap.txt文件，导入文件内容
            """)
        )
        morbidmap_import.add_argument("--input","-i", type=str, help="Input file ususally is morbidmap.txt", required=True)
        morbidmap_import.add_argument("--host",'-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        morbidmap_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        morbidmap_import.set_defaults(func=lib.OmimMorbidmap.omim_morbidmap_import)


    def omim_morbidmap_parser_update_genemap(self, parser):
        morbidmap_update_genemap = parser.add_parser("update_genemap", help=u"从omim_morbidmap中获取信息，更新到omim_genemap",
            description = textwrap.dedent(u"""
            通过mimNumber，从omim_morbidmap中获得信息更新到omim_genemap。如果没给出mimNumber,则全部更新。mimNumber用空格分开
            """)
        )
        morbidmap_update_genemap.add_argument("--mimNumber", "-mim", type=str, nargs='*', help="mimNumber need to update. If not given, all mimNumber will be updated. Different mimNumber split with blackspace")
        morbidmap_update_genemap.add_argument("--genemaphost","-gh", type=str, help="Host for omim_genemap", default="mongodb://localhost:27017")
        morbidmap_update_genemap.add_argument("--genemapdb", "-gdb", type=str, help="db name for omim_genemap", default="dbtest")
        morbidmap_update_genemap.add_argument("--morbidmaphost", "-mh", type=str, help="Host for omim_morbidmap", default="mongodb://localhost:27017")
        morbidmap_update_genemap.add_argument("--morbidmapdb", "-mdb", type=str, help="db name for omim_morbidmap", default="dbtest")
        morbidmap_update_genemap.set_defaults(func=lib.OmimMorbidmap.update_genemap)

    def omim_morbidmap_parser_import(self, parser):
        morbidmap_import = parser.add_parser("import", help=u"OMIM Morbidmap表的导入",
            description = textwrap.dedent(u"""
            导入Morbidmap表。处理morbidmap.txt文件，导入文件内容
            """)
        )
        morbidmap_import.add_argument("--input","-i", type=str, help="Input file ususally is morbidmap.txt", required=True)
        morbidmap_import.add_argument("--host",'-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        morbidmap_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        morbidmap_import.set_defaults(func=lib.OmimMorbidmap.omim_morbidmap_import)

    def omim_genemap_parser_update_entry(self, parser):
        genemap_update_entry = parser.add_parser("update_entry", help=u"""从omim_genemap中获得信息更新到omim_entry""",
            description = textwrap.dedent(u"""
            通过mimNumber，从omim_genemap中获得信息更新到omim_entry。如果没给出mimNumber,则全部更新。mimNumber用空格分开
            """)
        )
        genemap_update_entry.add_argument("--mimNumber", "-mim", type=str, nargs='*', help="mimNumber need to update. If not given, all mimNumber will be updated. Different mimNumber split with blackspace")
        genemap_update_entry.add_argument("--genemaphost", "-gh", type=str, help="Host for omim_genemap", default="mongodb://localhost:27017")
        genemap_update_entry.add_argument("--genemapdb", "-gdb", type=str, help="db name for omim_genemap", default="dbtest")
        genemap_update_entry.add_argument("--entryhost", '-eh', type=str, help="Host for omim_entry", default="mongodb://localhost:27017")
        genemap_update_entry.add_argument("--entrydb", '-edb', type=str, help="db name for omim_entry", default="dbtest")
        genemap_update_entry.set_defaults(func=lib.OmimGenemap.omim_genemap_update_entry)

    def omim_genemap_parser_import(self, parser):
        genemap_import = parser.add_parser('import', help=u"""OMIM Genemap表的导入""",
            description = textwrap.dedent(u"""
            导入Genemap表。处理genemap.txt文件，导入文件内容
            """)
        )
        genemap_import.add_argument("--input",'-i', type=str, help="Input file ususally is genemap.txt", required=True)
        genemap_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        genemap_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        genemap_import.set_defaults(func=lib.OmimGenemap.omim_genemap_import)

    def dgv_parser_import(self, parser):
        dgv_import = parser.add_parser('import',
            formatter_class=RawDescriptionHelpFormatter,
            help='Import GRCh37_hg19_supportingvariants_version.txt into mongodb',
            description = textwrap.dedent(u"""
            把DGV数据库的信息导入到Mongo.导入时有如下规则:
            1. 导入的信息是GRCh37_hg19_supportingvariants_version.txt文件中内容
            2. 导入的变异要求长度大于min_length(default: 100000)
            """)
        )
        dgv_import.add_argument('--input', '-i', type=str, help='Input file such as GRCh37_hg19_supportingvariants_2016-05-15.txt', required=True)
        dgv_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        dgv_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        # 未来删除这个选项，把表的名字都固定下来。dgv_varient
        dgv_import.add_argument('--collection', '-c', type=str, help="Collection used for mongo suce as dgv_test", default='dgv_test')
        dgv_import.add_argument('--workers', '-w', type=int, help="Number of concurrent workers to insert", default=4)
        dgv_import.add_argument('--min_length', '-m', type=int, help="Min length of variants", default=100000)
        dgv_import.add_argument('--drop', dest='drop', action='store_true')
        dgv_import.add_argument('--no-drop', dest='drop', action='store_false')
        dgv_import.set_defaults(drop=False)
        dgv_import.add_argument('--upsert', dest='upsert', action='store_true')
        dgv_import.add_argument('--no-upsert', dest='upsert', action='store_false')
        dgv_import.set_defaults(upsert=False)
        dgv_import.set_defaults(func=lib.DGV.dgv_import)

    def omim_entry_parser_import(self, parser):
        entry_import = parser.add_parser('import',
            help=u"""OMIM Entry表的导入""",
            description = textwrap.dedent(u"""
            导入Entry表。处理omim.txt文件，导入文件内容
            """)
        )
        entry_import.add_argument('--input', '-i', type=str, help="Input file usually is omim.txt", required=True)
        entry_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="mongodb://localhost:27017")
        entry_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        entry_import.set_defaults(func=lib.OmimEntry.omim_entry_import)

    def FUN(self, **options):
        print options['text']

    def handle(self, *args, **options):
        self.print_args(**options)
        options['func'](self, **options)


# inline-tools for development
def debugprint(text):
    print "*"*60
    print text;
    print "#"*60
