# coding: utf8
from django.core.management.base import BaseCommand, CommandError
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os
import textwrap

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

    def print_args(self, **options):
        print "Args info:"
        for (key, value) in options.iteritems():
            print "\t%20s\t------->\t%-20s" % (key, value)

    def add_arguments(self, parser):
        #　子命令组
        subparsers = parser.add_subparsers(help='sub-command help', parser_class=type(ArgumentParser()))

        # dgv-import
        parser_dgv = subparsers.add_parser('dgv-import',
            formatter_class=RawDescriptionHelpFormatter,
            help='Import GRCh37_hg19_supportingvariants_version.txt into mongodb',
            description = textwrap.dedent(u"""
            把DGV数据库的信息导入到Mongo.导入时有如下规则:
            1. 导入的信息是GRCh37_hg19_supportingvariants_version.txt文件中内容
            2. 导入的变异要求长度大于min_length(default: 100000)
            """
            )
        )
        parser_dgv.add_argument('--input', '-i', type=str, help='Input file such as GRCh37_hg19_supportingvariants_2016-05-15.txt', required=True)
        parser_dgv.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        parser_dgv.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        parser_dgv.add_argument('--collection', '-c', type=str, help="Collection used for mongo suce as dgv_test", default='dgv_test')
        parser_dgv.add_argument('--workers', '-w', type=int, help="Number of concurrent workers to insert", default=4)
        parser_dgv.add_argument('--min_length', '-m', type=int, help="Min length of variants", default=100000)
        parser_dgv.add_argument('--drop', dest='drop', action='store_true')
        parser_dgv.add_argument('--no-drop', dest='drop', action='store_false')
        parser_dgv.set_defaults(drop=False)
        parser_dgv.add_argument('--upsert', dest='upsert', action='store_true')
        parser_dgv.add_argument('--no-upsert', dest='upsert', action='store_false')
        parser_dgv.set_defaults(upsert=False)
        parser_dgv.set_defaults(func=Command.dgv_import)

    def handle(self, *args, **options):
        self.print_args(**options)
        options['func'](self, **options)

    def dgv_import(self,**options):
        u"""
        DGV数据库的导入命令
        """
        cmd = "awk '{if (($4 - $3) >= %d) {print $0}}'" % options['min_length']

        dgv_fields = './dgv_fields'
        fields = [
            "variantAccession", "chr", "start", "end",
            "variantType", "variantSubtype", "reference", "pubmedid",
            "method", "platform", "mergedVariants", "supportingVariants",
            "mergedOrSample", "frequency", "sampleSize", "observedGains",
            "observedLosses", "cohortDescription", "genes", "samples"
        ]
        with open(dgv_fields, 'w') as f:
            f.write("\n".join(fields))
        tmp = "./supporting_variants_20k"
        while os.path.exists(tmp) and os.path.getsize(tmp):
            tmp = tmp + '1'
        cmd = " ".join([cmd, options['input'], ">", tmp])
        os.system(cmd)
        cmd = "mongoimport --fieldFile=%s -h %s -d %s -c %s --type=tsv -j %s" %\
            (dgv_fields, options['host'], options['db'], options['collection'], options['workers'])
        if options['upsert']:
            cmd = " ".join([cmd,"--upsert --upsertFields=variantAccession"])
        if options['drop']:
            cmd = " ".join([cmd,'--drop'])
        cmd = " ".join([cmd, tmp])
        print cmd
        os.system(cmd)
        os.system("rm -rf %s %s" % (dgv_fields, tmp))


