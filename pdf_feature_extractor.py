import csv
import sys
import fitz
import os
import subprocess
import pandas as pd
import time
import os
import signal
from fitz import TextPage

import utils

def e():
        sys.exit(-1)

def usage():
      print("[-] Usage: python pdf_feature_extractor.py <path_containing_pdfs>")
      e()


if len(sys.argv) != 2: 
      usage()


dir = os.getcwd()
path = sys.argv[1]
if(not os.path.isabs(path)):      #if the given path is not absolute, we should convert it to one
         #print("the path is path is "+str(path))
         #print("dir is "+str(dir))
         path = os.path.join(dir,path)
         print("the path is not absolute and the new path is "+str(path))
if(os.path.isdir(path)):
        res = pd.DataFrame(columns=('pdfsize','metadata size', 'pages','xref length','title characters','isEncrypted','embedded files','images','contains text',''))
else:
        print("specify a valid pdf folder path as an argument")
        sys.exit()
i = 0

def sig_handler(signum, frame):
    print("segfault")


for j in os.listdir(path):
        f = path + "/" + j
        print(f)
        #pdfFileObj = open(f,'rb')
        try:
                doc = fitz.open(f)
                #print("fitz "+str(doc.xrefLength))
                #file = open(f, 'rb')
        except:
                continue
        #metadata
        metadata = doc.metadata
        print("metadata is "+str(metadata))

        #title
        if metadata:
                title = metadata['title']
        else:
                title = ""
        if not title:
                title = ""
        print("title is "+str(title))

        #whether file is encrypted
        isEncrypted = -1
        if metadata:
                isEncrypted = metadata['encryption']
                if(not isEncrypted):
                        isEncrypted = 0
                else:
                        isEncrypted = 1
        #number of objects
        objects = doc.xref_length()
                # print("object is "+str(object))

        # printing number of pages in pdf file
        numPages = doc.page_count
        print("numpages is "+str(numPages))

        #extracted text
        pdfsize = int(os.path.getsize(f)/1000)
        print("pdfsize is "+str(pdfsize))

        #extracted text
        found = "No"
        text = ""
        try:
                for page in doc:
                        text += page.get_text()
                        if (len(text) > 100):
                                found = "Yes"
                                break
        except:
         #       break
                 found = "unclear"
                 res.loc[i] = [pdfsize, len(str(metadata).encode('utf-8'))] + [numPages] + [objects] + [len(title)] + [isEncrypted] + [embedcount] + [-1] + [found] +['']
                 i +=1
                 continue
                 
        #print("file contains text " + str(found))
        # number of embedded files
        embedcount = doc.embfile_count()
        print("embedcount is "+str(embedcount))

        
        #number of images
        imgcount = 0
        try:
         for k in range(len(doc)):
               try:
                print(doc.getPageImageList(k))
                imgcount = len(doc.getPageImageList(k)) + imgcount
               except:  
                 imgcount = -1
                 break
                 

        except:
         continue
        #print("image no is "+str(imgcount))




        #writing the features in a csv file
        res.loc[i] = [pdfsize, len(str(metadata).encode('utf-8'))] + [numPages] + [objects] + [len(title)] + [isEncrypted] + [embedcount] + [imgcount] + [found] +['']
        i +=1
res.to_csv(os.path.relpath("result.csv",start=os.curdir))
print("general features extracted successfully...")


print("extracting structural features...")        #extracting structural features using pdfid
var =  str(r"tr '\n' ','")
command = ""
header =  ['header', 'obj', 'endobj', 'stream', 'endstream', 'xref', 'trailer', 'startxref', 'pageno', 'Encrypt', 'ObjStm', 'JS', 'JavaScript', 'AA', 'OpenAction', 'AcroForm', 'JBIG2Decode', 'RichMedia', 'Launch', 'EmbeddedFile', 'XFA', 'URI', 'Colors']
with open(os.path.relpath("pdfid/output.csv"),'w',encoding='UTF8') as output:
        output.write(','.join(header))
        # os.chdir('pdfid')
        t0 = time.time()
        for j in os.listdir(path):
                f = path + "/" + j
                out = utils.pdfid(f)
                out = list(out.values())
                out = ','.join(str(o) for o in out)
                output.write("\n" + out)
                d = time.time() - t0
        print("duration: %.2f s." % d)

print("finished features")
os.system("paste result.csv pdfid/output.csv > output1.csv")
os.remove("pdfid/output.csv")
os.remove("result.csv")









