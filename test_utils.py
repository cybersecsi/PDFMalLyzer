import os
from utils import *

def get_test_pdf():
    return os.path.join(os.getcwd(), "tests", "test.pdf")



def test_md5():
    assert md5sum(get_test_pdf()) == "77f3e768f0c3a240f052c711ac021a1b"



def test_pdfid():
    expected_val = {
    'header' : "%PDF-1.2",
    'obj': 211,
    'endobj': 211,
    'stream': 59,
    'endstream': 59,
    'xref': 1,
    'trailer': 1,
    'startxref': 1,
    'pageno': 59,
    'Encrypt': 0,
    'ObjStm': 0,
    'JS': 0,
    'JavaScript': 0,
    'AA': 0,
    'OpenAction': 0,
    'AcroForm': 0,
    'JBIG2Decode': 0,
    'RichMedia': 0,
    'Launch': 0,
    'EmbeddedFile': 0,
    'XFA': 0,
    'URI': 0,
    'Colors': 0
}

    print(list(expected_val.keys()))

    ret = pdfid(get_test_pdf())
    assert ret == expected_val
