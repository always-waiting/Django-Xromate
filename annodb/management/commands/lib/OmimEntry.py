# encoding: utf-8
import os


def test():
    print u"这时一个测试，用于判断是否成功加载"

def omim_entry_import(cmdobj, **options):
    u"""
    导入omim.txt到数据库
    """
    print "开发omim_entry_import命令"
    # 检查文件是否存在
    if not os.path.exists(options['input']):
        raise Exception(options['input'] + " not exists");
    # 开发文件解析函数
    with open(options['input']) as f:
        for chunk in myreadlines(f, '*RECORD*'):
        #debugprint(chunk)
            if chunk.find("*THEEND*"): break


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
