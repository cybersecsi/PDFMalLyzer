# python pdfid.py /Users/gx1/git/secsi/PDFMalLyzer/tests/small_file/02solp.pdf

import os
import subprocess


def pdfid(f):
    """Call the Steven script to obtain the structural features

    Args:
        filename (str): the full path filename
    """
    var =  str(r"tr '\n' ','")
    os.chdir('pdfid')
    out = subprocess.getoutput("python pdfid.py " + f + " | awk '{print $2}' | tail -n +2 | "+var+"")
    os.chdir('../')
    return out