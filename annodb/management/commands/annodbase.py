# coding: utf8
from django.core.management.base import BaseCommand, CommandError
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os
import textwrap
import lib.OmimEntry
import lib.DGV

"""
class Command(BaseCommand):
    help = ''
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(u"这是一个测试")
"""
class Command(BaseCommand):

    help = "Annodbase commands group"

    def cmds_add(self, parser, cmds, hinfo="Help info", des="Description"):
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
        subparsers = parser.add_subparsers(help='sub-command help', parser_class=type(ArgumentParser()))
        # DGV命令组
        dgv_cmds = self.cmds_add(
            subparsers, 'dgv',
            u"处理DGV数据库",
            u"""处理DGV数据库,目前只有import功能"""
        )
        dgv_parser = dgv_cmds.add_subparsers(help="DGV commands")
        # DGV import action
        self.dgv_parser_import(dgv_parser)
        # OMIM数据库命令组
        omim_cmds = self.cmds_add(
            subparsers, "omim",
            u"处理关于OMIM数据库的所有表。一共有n个表和OMIM有关",
            u"""
            OMIM数据库的命令组
            目前正在开发阶段，正在开发entry表的导入功能
            """
        )
        omim_parser = omim_cmds.add_subparsers(help="OMIM subtables")
        # OMIM -> ENTRY命令组
        omim_entry_cmds = self.cmds_add(
            omim_parser, "entry",
            u"omim数据库entry表的命令组",
            u"""
            处理omim_entrys表的各种动作
            目前开发entry表的导入命令:import
            """
        )
        omim_entry_parser = omim_entry_cmds.add_subparsers(help="OMIM Entry table actions")
        # OMIM ENTRY import action
        self.omim_entry_parser_import(omim_entry_parser)

    def dgv_parser_import(self, parser):
        dgv_import = parser.add_parser('import',
            formatter_class=RawDescriptionHelpFormatter,
            help='Import GRCh37_hg19_supportingvariants_version.txt into mongodb',
            description = textwrap.dedent(u"""
            把DGV数据库的信息导入到Mongo.导入时有如下规则:
            1. 导入的信息是GRCh37_hg19_supportingvariants_version.txt文件中内容
            2. 导入的变异要求长度大于min_length(default: 100000)
            """
            )
        )
        dgv_import.add_argument('--input', '-i', type=str, help='Input file such as GRCh37_hg19_supportingvariants_2016-05-15.txt', required=True)
        dgv_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        dgv_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
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
            """
            )
        )
        entry_import.add_argument('--input', '-i', type=str, help="Input file usually is omim.txt", required=True)
        entry_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        entry_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        entry_import.add_argument('--collection', '-c', type=str, help="Collection used for mongo suce as entry_test", default='entry_test')
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
