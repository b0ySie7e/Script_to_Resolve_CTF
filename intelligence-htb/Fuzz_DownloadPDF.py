#/usr/bin/python3
import requests
import datetime
import threading
from pathlib import Path


def grequetsPDF():
    start_date=datetime.datetime(2019,1,1)
    end_date=datetime.datetime(2024,1,1)
    one_day = datetime.timedelta(days=1)
    
    while start_date<end_date:
        namePDF = start_date.strftime("%Y-%m-%d-upload.pdf")
        start_date=start_date+one_day
        threading.Thread(target=downloadPDF, args=(namePDF,)).start()


def downloadPDF(namePdf):
    url='http://10.10.10.248/documents/'
    urlFile=url+namePdf
    try:
        r=requests.get(str(urlFile))
        if(r.status_code==200):
            print(namePdf)
            filename=Path(namePdf)
            filename.write_bytes(r.content)

    except:
        print('[+] Error') 
 
if __name__=='__main__':
    grequetsPDF()       
    
    