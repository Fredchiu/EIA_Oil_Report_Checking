# read pdf file from EIA
import requests
import time
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import StringIO
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import os
import re
import io


url = 'http://ir.eia.gov/wpsr/wpsrsummary.pdf'
index = time.strftime('%Y%m%d', time.localtime())
file_loc = './'
filepath = file_loc+index+'-wpsrsummary.pdf'


def download_file(url, index):
    local_filename = index+"-"+url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def pdfTotxt(filepath):
    try:
        fp = file(filepath, 'rb')
        # outfp=file(outpath,'w')
        rsrcmgr = PDFResourceManager(caching=False)
        laparams = LAParams()
        txt_doc = StringIO()
        device = TextConverter(
            rsrcmgr, txt_doc, codec='utf-8', laparams=laparams, imagewriter=None)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos=set(), maxpages=0,
                                      password='', caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        fp.close()
        device.close()
        # outfp.flush()
        content = txt_doc.getvalue()
        # outfp.close()
        txt_doc.close()
        return content
    except Exception, e:
        print "Exception:%s", e


def findDistillate_stock(content):
    pat1 = '(?<=Distillate\sfuel\sinventories\s)\w+'
    dir_result = re.findall(pat1, content)
    if dir_result == []:
        pat1 = '(?<=Distillate\sfuel\sinventories\s\n)\w+'
        dir_result = re.findall(pat1, content)
        pat2 = '(?<=\n'+str(dir_result[0])+'\sby\s)[0-9\.]+'
    else:
        pat2 = '(?<=Distillate\sfuel\sinventories\s' + \
            str(dir_result[0])+'\sby\s)[0-9\.]+'
        
    value_result = re.findall(pat2, content)
    
    if dir_result == ['remained']:
        value_result = 'unchanged'    
    return dir_result,value_result

if __name__ == '__main__':
    if os.path.exists(filepath) == False:
        startime = time.time()
        print 'downloading file'
        download_file(url, index)
        elapsed = time.time()-startime
        print str(elapsed)+' sec'
    
    content = pdfTotxt(filepath)
    dir_result,value_result=findDistillate_stock(content)
    print(str(index)+' : '+str(dir_result)+' '+str(value_result))
