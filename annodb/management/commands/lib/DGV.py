# encoding: utf-8
import os


def dgv_import(self,**options):
    u"""
    DGV数据库的导入命令
    self是annodb.management.commands.annodbase.Command
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
