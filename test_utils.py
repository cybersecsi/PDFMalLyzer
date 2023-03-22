import os
from utils import *

def get_test_pdf():
    return os.path.join(os.getcwd(), "tests", "test.pdf")

def get_malicious():
    return os.path.join(os.getcwd(), "tests", "7ff7a2930d92a080ca615a8cb3f9d7d1ddec3609")



def test_md5():
    assert md5sum(get_test_pdf()) == "77f3e768f0c3a240f052c711ac021a1b"

def test_header():
    assert parse_header('header: %PDF-1.5') == '%PDF-1.5'
    assert parse_header('header: %-1.5') == 'Malformed'




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
    'JS_Obfuscated': 0,
    'JavaScript': 0,
    'JavaScript_Obfuscated': 0,
    'AA': 0,
    'AA_Obfuscated': 0,
    'OpenAction': 0,
    'OpenAction_Obfuscated': 0,
    'AcroForm': 0,
    'AcroForm_Obfuscated': 0,
    'JBIG2Decode': 0,
    'JBIG2Decode_Obfuscated': 0,
    'RichMedia': 0,
    'RichMedia_Obfuscated': 0,
    'Launch': 0,
    'Launch_Obfuscated': 0,
    'EmbeddedFile': 0,
    'EmbeddedFile_Obfuscated': 0,
    'XFA': 0,
    'XFA_Obfuscated': 0,
    'URI': 0,
    'Colors': 0
}

    print(list(expected_val.keys()))

    ret = pdfid(get_test_pdf())
    assert ret == expected_val


# With pdfs containing 1(1)
def test_encoded():
    expected = {'header': 'Malformed', 'obj': 8, 'endobj': 8, 'stream': 2, 'endstream': 2, 'xref': 1, 'trailer': 1, 'startxref': 1, 'Encrypt': 0, 'ObjStm': 0, 'JS': 1, 'JavaScript': 1, 'AA': 0, 'OpenAction': 1, 'AcroForm': 0, 'JBIG2Decode': 0, 'RichMedia': 0, 'Launch': 0, 'EmbeddedFile': 0, 'XFA': 0, 'URI': 0, 'Colors': 0, 'JS_Obfuscated': 1, 'JavaScript_Obfuscated': 0, 'AA_Obfuscated': 0, 'OpenAction_Obfuscated': 0, 'AcroForm_Obfuscated': 0, 'JBIG2Decode_Obfuscated': 0, 'RichMedia_Obfuscated': 0, 'Launch_Obfuscated': 0, 'EmbeddedFile_Obfuscated': 0, 'XFA_Obfuscated': 0, 'pageno': 1}
    v = pdfid(get_malicious())
    assert v == expected
