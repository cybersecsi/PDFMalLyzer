# python pdfid.py /Users/gx1/git/secsi/PDFMalLyzer/tests/small_file/02solp.pdf

import hashlib
import os
import subprocess

var =  str(r"tr '\n' ','")

STRUCTURAL_HEADER = ['header','obj','endobj','stream','endstrean','xref','trailer','startxref','pageno' ,'encrypt','ObjStm','JS','Javascript','AA','OpenAction','Acroform','JBIG2Decode','RichMedia','launch','EmbeddedFile','XFA', 'URI', 'Colors']


def md5sum(f):
    md5_hash = hashlib.md5()
    with open(f, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def pfid_cmd(f):
    return "python pdfid.py " + f 

def parse_header(s):
    return s.split(":")[1].strip()

def _clean_ret(ret):
    clean_ret = {key.replace("/", "").strip() if key != 'header' else key: int(item) if key != 'header' else item.strip() for key, item in ret.items()}
    # Replace name
    clean_ret['pageno'] = clean_ret.pop('Page')

    return clean_ret

def pdfid(f):
    """Call the Steven script to obtain the structural features

    Args:
        filename (str): the full path filename
    """
    print("[+] Structural of {}".format(f))
    os.chdir('pdfid')
    ret = {}
    out = subprocess.getoutput(pfid_cmd(f))
    splitted_lines = out.split("\n")[1:]
    header = parse_header(splitted_lines[0])
    ret['header'] = header
    splitted_lines = splitted_lines[1:]
    for s in splitted_lines: 
        s_arr = s.split()
        if len(s_arr):
            if not s_arr[0].startswith('/Colors'):
                ret[s_arr[0]] = s_arr[1]
            else:
                ret[s_arr[0]] = s_arr[3]

    os.chdir('../')
    return _clean_ret(ret)