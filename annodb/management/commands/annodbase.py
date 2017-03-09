# coding: utf8
from django.core.management.base import BaseCommand, CommandError
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import os
import textwrap
import lib.OmimEntry
import lib.DGV
import lib.OmimGenemap
import lib.OmimMorbidmap
import lib.DecipherCNV
import lib.DecipherSyndrome
import lib.ClinVar
import lib.GeneReview
class Command(BaseCommand):

    help = u"""
Annodbase commands group. There are below database:
    1. OMIM
    2. DGV
    3. Decipher
"""

    def cmds_add(self, parser, cmds, hinfo="Help info", des="Description", phinfo="Help info"):
        cmds = parser.add_parser(
            cmds, formatter_class=RawDescriptionHelpFormatter,
            help=hinfo, description = textwrap.dedent(des)
        )
        return cmds.add_subparsers(help=phinfo)

    def print_args(self, **options):
        print "Args info:"
        for (key, value) in options.iteritems():
            print "\t%20s\t------->\t%-20s" % (key, value)

    def add_arguments(self, parser):
        parser.formatter_class = RawDescriptionHelpFormatter
        #　子命令组
        subparsers = parser.add_subparsers(help='sub-command help', parser_class=type(ArgumentParser()))
        # DGV命令组
        dgv_parser = self.cmds_add(
            subparsers, 'dgv',
            u"处理DGV数据库",
            u"处理DGV数据库,目前只有import功能", "DGV commands"
        )
        # DGV import action
        self.dgv_import(dgv_parser)
        # OMIM数据库命令组
        omim_parser = self.cmds_add(
            subparsers, "omim",
            u"处理关于OMIM数据库的所有表。一共有n个表和OMIM有关",
            u"""
            OMIM数据库的命令组,处理如下表
            1.omim_entry
            2.omim_genemap
            3.omim_morbidmap
            """, u"OMIM subtables"
        )
        # OMIM -> ENTRY命令组
        omim_entry_parser = self.cmds_add(
            omim_parser, "entry",
            u"omim数据库entry表的命令组",
            u"""
            处理omim_entry表的各种动作
            1. import
            2. download
            """, u"OMIM Entry table actions"
        )
        # OMIM ENTRY import action
        self.omim_entry_import(omim_entry_parser)
        # OMIM ENTRY download action
        self.omim_entry_download(omim_entry_parser)

        # OMIM -> genemap命令组
        omim_genemap_parser = self.cmds_add(
            omim_parser, "genemap",
            u"omim数据库genemap表的命令组",
            u"""
            处理omim_genemap表的各种动作
            1. import
            2. update_entry
            3. mim2gene_update
            """, u"OMIM Genemap table actions"
        )
        # OMIM Genemap import action
        self.omim_genemap_import(omim_genemap_parser)
        # OMIM Genemap update OMIM Entry action
        self.omim_genemap_update_entry(omim_genemap_parser)
        # OMIM Genemap mim2gene_update action
        self.omim_genemap_mim2gene_update(omim_genemap_parser)
        # OMIM -> morbidmap命令组
        omim_morbidmap_parser = self.cmds_add(
            omim_parser, "morbidmap",
            u"omim数据库morbidmap表的命令组",
            u"""
            处理omim_morbidmap表的各种动作
            1. import
            2. update_genemap
            3. update_entry
            """, u"Omim Morbidmap table actions"
        )
        ## Omim Morbidmap import action
        self.omim_morbidmap_import(omim_morbidmap_parser)
        ## OMIM Morbidmap update OMIM Genemap action
        self.omim_morbidmap_update_genemap(omim_morbidmap_parser)
        ## OMIM Morbidmap update OMIM Entry action
        self.omim_morbidmap_update_entry(omim_morbidmap_parser)

        # Decipher数据库命令组
        decipher_parser = self.cmds_add(
            subparsers, 'decipher', u"处理Decipher数据库",
            u"""
            Decipher数据库命令组, 处理如下表:
            1.decipher_cnv
            2.decipher_syndrome
            """, u"Decipher subtables"
        )
        # Decipher -> cnv命令组
        decipher_cnv_parser = self.cmds_add(decipher_parser,'cnv',
            u"decipher数据库cnv表命令组",
            u"""
            处理decipher_cnv表的各种动作
            1. import
            2. update_sex
            3. update_phenotypes
            """, u"decipher_cnv action cmds"
        )
        ## Decipher CNV import action
        self.decipher_cnv_import(decipher_cnv_parser)
        self.decipher_cnv_update_sex(decipher_cnv_parser)
        self.decipher_cnv_update_phenotypes(decipher_cnv_parser)
        # Decipher -> syndrome命令组
        decipher_syndrome_parser = self.cmds_add(decipher_parser, 'syndrome',
            u"decipher数据库syndrome表命令组",
            u"""
            处理decipher_syndrome表的各种动作
            1. import
            """,u"decipher_syndrome action cmds"
        )
        ## Decipher Syndrome actions
        self.decipher_syndrome_import(decipher_syndrome_parser)

        # ClinVar命令组
        clinvar_parser = self.cmds_add(subparsers,'clinvar', u"处理ClinVar数据库",
            u"""
            ClinVar数据库命令组，处理如下表:
            1. clin_var
            """,u"ClinVar subtables"
        )
        ## ClinVar actions
        self.clinvar_import(clinvar_parser)

        # GeneReview命令组
        geneview_parser = self.cmds_add(subparsers,'genereview',u"处理GeneReview数据库",
            u"""
            GeneReview数据库命令组，处理如下表:
            1. gene_review
            """, u"GeneReview subtables"
        )
        # GeneReview actions
        self.genereview_import(geneview_parser)

    """
    以下是调用的方法
    """
    def genereview_import(self, parser):
        genereview_import = parser.add_parser("import", help=u"导入GeneReview信息",
            description = u"""
            导入GeneReview信息
            """
        )
        genereview_import.add_argument("--host","-H", type=str, help="Host for mongodb such as mongodb://localhost:27017", default="mongodb://localhost:27017")
        genereview_import.add_argument("--db",'-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        genereview_import.add_argument("--debug",action="store_true", help=u"是否打印更多信息，默认为False")
        genereview_import.set_defaults(func=lib.GeneReview.importdb)

    def clinvar_import(self, parser):
        clinvar_import = parser.add_parser("import", help=u"导入ClinVar信息",
            description = textwrap.dedent(u"""
            导入ClinVar信息,导入的信息有如下要求:
            1. 是CNV记录，即type为Deletion,Duplication,copy number gain,copy number loss;
            2. clinsign field is 'pathogenic' or 'likely pathogenic'
            """)
        )
        clinvar_import.add_argument("--host","-H", type=str, help="Host for mongodb such as mongodb://localhost:27017", default="mongodb://localhost:27017")
        clinvar_import.add_argument("--db",'-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        clinvar_import.add_argument("--input","-i", type=str, help="path of xml file, downloaded from 'ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/'", required=True)
        clinvar_import.add_argument("--debug",action="store_true", help=u"是否打印更多信息，默认为False")
        clinvar_import.set_defaults(func=lib.ClinVar.importdb)

    def decipher_syndrome_import(self, parser):
        syndrome_import = parser.add_parser("import", help=u"导入decipher syndrome信息",
            description = textwrap.dedent(u"""
            导入Decipher Syndrome信息
            """)
        )
        syndrome_import.add_argument("--host","-H", type=str, help="Host for mongodb such as mongodb://localhost:27017", default="mongodb://localhost:27017")
        syndrome_import.add_argument("--db",'-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        syndrome_import.add_argument("--chr","-c", type=int, nargs='*',help=u"想要更新的染色体，空是全部更新")
        syndrome_import.set_defaults(func=lib.DecipherSyndrome.importdb)

    def decipher_cnv_update_phenotypes(self, parser):
        update_phenotypes = parser.add_parser("update_phenotypes", help=u"更新phenotypes信息",
            description = textwrap.dedent(u"""
            通过输入patient_id更新phenotypes信息，一般用于import出错需要特别更新某些记录时
            """)
        )
        update_phenotypes.add_argument("--host","-H", type=str, help="Host for mongodb such as mongodb://localhost:27017", default="mongodb://localhost:27017")
        update_phenotypes.add_argument("--db",'-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        update_phenotypes.add_argument("--patient_id","-p", type=int, nargs='*', help=u"patient id,没有全部更新")
        update_phenotypes.set_defaults(func=lib.DecipherCNV.update_phenotypes)

    def decipher_cnv_update_sex(self, parser):
        update_sex = parser.add_parser("update_sex", help=u"更新性别信息",
            description = textwrap.dedent(u"""
            通过输入patient_id更新性别信息。一般用于import出错时，需要更新某些记录
            """)
        )
        update_sex.add_argument("--host","-H", type=str, help="Host for mongodb such as mongodb://localhost:27017", default="mongodb://localhost:27017")
        update_sex.add_argument("--db",'-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        update_sex.add_argument("--patient_id","-p", type=int, nargs='*', help=u"patient id,没有全部更新")
        update_sex.set_defaults(func=lib.DecipherCNV.update_sex)

    def decipher_cnv_import(self, parser):
        cnv_import = parser.add_parser("import", help=u"导入decipher cnv的信息",
            description = textwrap.dedent(u"""
            导入Decipher CNV信息
            """)
        )
        cnv_import.add_argument("--host", "-H", type=str, help="Host for mongodb such as mongodb://localhost:27017", default="mongodb://localhost:27017")
        cnv_import.add_argument("--db", '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        cnv_import.add_argument("--chr","-c", type=int, nargs='*',help=u"想要更新的染色体，空是全部更新")
        cnv_import.set_defaults(func=lib.DecipherCNV.importdb)

    def omim_entry_download(self, parser):
        entry_download = parser.add_parser("download", help=u"从网上下载必要的信息到entry表中",
            description = textwrap.dedent(u"""
                通过给出mim或mim列表,从http://api.omim.org/api/entry 下载必要的信息到entry表
            """)
        )
        mim_group = entry_download.add_mutually_exclusive_group(required=True)
        mim_group.add_argument("--input","-i", help=u"用于下载的mim列表，只需要第一列为mimNumber即可")
        mim_group.add_argument("--mimNumber","-mim", type=int, nargs='*', help=u"输入特定的mim下载，可以输入多个")
        entry_download.add_argument("--clean","-c", action="store_true", help=u"True时删除表中相应数据后再下载跟新，False时直接下载，只更新相应内容")
        entry_download.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        entry_download.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        entry_download.add_argument('--apikey','-a', type=str, help=u"OMIM网站的apikey,有默认值，但是需要定期更新", default="BK2V39hOQKibVY_Gud_bVQ")
        entry_download.set_defaults(func=lib.OmimEntry.download)

    def omim_genemap_mim2gene_update(self, parser):
        mim2gene_update_genemap = parser.add_parser("mim2gene_update", help=u"从输入文件中获得信息，导入到genemap表中",
            description = textwrap.dedent(u"""
            从mim2gene.txt和refFlat.txt文件获得信息，更新表genemap的染色体坐标信息。字段有:
            approvedGeneSymbol，chromosome，chromosomeSymbol，
            chromosomeLocationStart，chromosomeLocationEnd，chromosomeLocationStrand，
            """)
        )
        mim2gene_update_genemap.add_argument("--input", "-i", type=str, help="mim2gene.txt file", required = True)
        mim2gene_update_genemap.add_argument("--refflat", "-r", type=str, help="refFlat.txt file", required = True)
        mim2gene_update_genemap.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        mim2gene_update_genemap.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        mim2gene_update_genemap.set_defaults(func=lib.OmimGenemap.mim2gene_update)

    def omim_morbidmap_update_entry(self, parser):
        morbidmap_update_entry = parser.add_parser("update_entry", help=u"从omim_morbidmap中获取信息，更新到omim_entry",
            description = textwrap.dedent(u"""
            通过mimNumber，从omim_morbidmap中获得信息更新到omim_entry的phenotypeMapList字段。如果没给出mimNumber,则全部更新。mimNumber用空格分开
            """)
        )
        morbidmap_update_entry.add_argument("--mimNumber", "-mim", type=str, nargs='*', help="mimNumber need to update. If not given, all mimNumber will be updated. Different mimNumber split with blackspace")
        morbidmap_update_entry.add_argument("--entryhost","-eh", type=str, help="Host for omim_entry", default="mongodb://localhost:27017")
        morbidmap_update_entry.add_argument("--entrydb", "-edb", type=str, help="db name for omim_entry", default="dbtest")
        morbidmap_update_entry.add_argument("--morbidmaphost", "-mh", type=str, help="Host for omim_morbidmap", default="mongodb://localhost:27017")
        morbidmap_update_entry.add_argument("--morbidmapdb", "-mdb", type=str, help="db name for omim_morbidmap", default="dbtest")
        morbidmap_update_entry.set_defaults(func=lib.OmimMorbidmap.update_entry)

    def omim_morbidmap_import(self, parser):
        morbidmap_import = parser.add_parser("import", help=u"OMIM Morbidmap表的导入",
            description = textwrap.dedent(u"""
            导入Morbidmap表。处理morbidmap.txt文件，导入文件内容
            """)
        )
        morbidmap_import.add_argument("--input","-i", type=str, help="Input file ususally is morbidmap.txt", required=True)
        morbidmap_import.add_argument("--host",'-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        morbidmap_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        morbidmap_import.set_defaults(func=lib.OmimMorbidmap.importdb)


    def omim_morbidmap_update_genemap(self, parser):
        morbidmap_update_genemap = parser.add_parser("update_genemap", help=u"从omim_morbidmap中获取信息，更新到omim_genemap",
            description = textwrap.dedent(u"""
            通过mimNumber，从omim_morbidmap中获得信息更新到omim_genemap的phenotypeMapList字段。如果没给出mimNumber,则全部更新。mimNumber用空格分开
            """)
        )
        morbidmap_update_genemap.add_argument("--mimNumber", "-mim", type=str, nargs='*', help="mimNumber need to update. If not given, all mimNumber will be updated. Different mimNumber split with blackspace")
        morbidmap_update_genemap.add_argument("--genemaphost","-gh", type=str, help="Host for omim_genemap", default="mongodb://localhost:27017")
        morbidmap_update_genemap.add_argument("--genemapdb", "-gdb", type=str, help="db name for omim_genemap", default="dbtest")
        morbidmap_update_genemap.add_argument("--morbidmaphost", "-mh", type=str, help="Host for omim_morbidmap", default="mongodb://localhost:27017")
        morbidmap_update_genemap.add_argument("--morbidmapdb", "-mdb", type=str, help="db name for omim_morbidmap", default="dbtest")
        morbidmap_update_genemap.set_defaults(func=lib.OmimMorbidmap.update_genemap)

    def omim_genemap_update_entry(self, parser):
        genemap_update_entry = parser.add_parser("update_entry", help=u"""从omim_genemap中获得信息更新到omim_entry""",
            description = textwrap.dedent(u"""
            通过mimNumber，从omim_genemap中获得信息更新到omim_entry的geneMap字段。如果没给出mimNumber,则全部更新。mimNumber用空格分开
            """)
        )
        genemap_update_entry.add_argument("--mimNumber", "-mim", type=str, nargs='*', help="mimNumber need to update. If not given, all mimNumber will be updated. Different mimNumber split with blackspace")
        genemap_update_entry.add_argument("--genemaphost", "-gh", type=str, help="Host for omim_genemap", default="mongodb://localhost:27017")
        genemap_update_entry.add_argument("--genemapdb", "-gdb", type=str, help="db name for omim_genemap", default="dbtest")
        genemap_update_entry.add_argument("--entryhost", '-eh', type=str, help="Host for omim_entry", default="mongodb://localhost:27017")
        genemap_update_entry.add_argument("--entrydb", '-edb', type=str, help="db name for omim_entry", default="dbtest")
        genemap_update_entry.set_defaults(func=lib.OmimGenemap.update_entry)

    def omim_genemap_import(self, parser):
        genemap_import = parser.add_parser('import', help=u"""OMIM Genemap表的导入""",
            description = textwrap.dedent(u"""
            导入Genemap表。处理genemap.txt文件，导入文件内容
            """)
        )
        genemap_import.add_argument("--input",'-i', type=str, help="Input file ususally is genemap.txt", required=True)
        genemap_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="localhost:27017")
        genemap_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        genemap_import.set_defaults(func=lib.OmimGenemap.importdb)

    def dgv_import(self, parser):
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
        dgv_import.set_defaults(func=lib.DGV.importdb)

    def omim_entry_import(self, parser):
        entry_import = parser.add_parser('import',
            help=u"""OMIM Entry表的导入""",
            description = textwrap.dedent(u"""
            导入Entry表。处理omim.txt文件，导入文件内容
            """)
        )
        entry_import.add_argument('--input', '-i', type=str, help="Input file usually is omim.txt", required=True)
        entry_import.add_argument('--host', '-H', type=str, help="Host for mongodb such as localhost:27017", default="mongodb://localhost:27017")
        entry_import.add_argument('--db', '-d', type=str, help="Database used for mongo such as dbtest", default="dbtest")
        entry_import.set_defaults(func=lib.OmimEntry.importdb)

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
