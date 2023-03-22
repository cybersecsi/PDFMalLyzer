# python pdfid.py /Users/gx1/git/secsi/PDFMalLyzer/tests/small_file/02solp.pdf

import hashlib
import os
import subprocess

var =  str(r"tr '\n' ','")

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()




def md5sum(f):
    md5_hash = hashlib.md5()
    with open(f, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
        return md5_hash.hexdigest()


def pfid_cmd(f):
    return "python pdfid.py \"" + f + "\""

# Valid PDF versions
PDF_VALID_VERSIONS = [
    '%PDF-1.0',
    '%PDF-1.1',
    '%PDF-1.2',
    '%PDF-1.3',
    '%PDF-1.4',
    '%PDF-1.5',
    '%PDF-1.6',
    '%PDF-1.7',    
    '%PDF-2.0'
]

def parse_header(s):
    print(s.split(":"))
    ret = s.split(":")[1].strip()
    return ret if ret in PDF_VALID_VERSIONS else 'Malformed'

def _obfuscated_fields(ret):
    FIELDS = ['/Page', '/JS', '/JavaScript', '/AA', '/OpenAction', '/AcroForm', '/JBIG2Decode', '/RichMedia', '/Launch', '/EmbeddedFile', '/XFA']
    for f in FIELDS:
        # Get the value
        val = ret[f]
        # If it is integer, simply remain the value and adds the obfuscation to 0
        if is_integer(val):
            ret["{}_Obfuscated".format(f)] = 0
        # It meas that the number is in form 2(1) where 2 is the number of elements and 1 the number of obfuscations
        else: 
           splitted_val = val.split('(')
           # Take 2(1) and create a new key for the obfuscation and change that of the object
           no_objects = splitted_val[0]
           no_obfusc  = splitted_val[1].replace(")", "")
           ret[f] = no_objects
           ret["{}_Obfuscated".format(f)] = no_obfusc

    return ret

def _clean_ret(ret):
    ret = _obfuscated_fields(ret)
    clean_ret = {key.replace("/", "").strip() if key != 'header' else key: int(item) if key != 'header' else item.strip() for key, item in ret.items()}
    # Replace name
    clean_ret['pageno'] = clean_ret.pop('Page')
    clean_ret['pageno_Obfuscated'] = clean_ret.pop('Page_Obfuscated')

    return clean_ret

def pdfid(f):
    """Call the Steven script to obtain the structural features

    Args:
        filename (str): the full path filename
    """
    the_cmd = pfid_cmd(f)
    print("[+] {}".format(the_cmd))
    os.chdir('pdfid')
    ret = {}
    out = subprocess.getoutput(the_cmd)
    splitted_lines = out.split("\n")[1:]
    print(splitted_lines)
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
    clean_ret  = _clean_ret(ret)
    return clean_ret