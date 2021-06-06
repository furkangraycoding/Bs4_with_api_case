import requests
import numpy as np
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

start_time = time.time()
SERVICE_ACCOUNT_FILE='keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


creds=None
creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


SAMPLE_SPREADSHEET_ID='1LxBkdpHMNjjAT0pam3ImtpI8AaBGlhzQy1F15dHZy6c'

service = build('sheets', 'v4',credentials=creds)

sheet=service.spreadsheets()

result= sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="URL!A1:A1000").execute()


values=result.get('values',[])
headers= [['URL', 'sku', 'Product Name', 'Availability', 'Normal Price', 'Offer', 'Sale Price']]

pageSize=50
page=int(len(values)/pageSize)
for j in range(0,page):
    sku=[]
    product_name=[]
    availability=[]
    BeforeDiscount_price=[]
    discount=[]
    AfterDiscountProduct_price=[]
    link=[]
    for i in range((pageSize*j),(pageSize*(j+1))):
        item_url="https://www.markastok.com"+values[i][0]
        source_code = requests.get(item_url)
        plain_text =source_code.text
        soup = BeautifulSoup(plain_text)
        passive_prod=soup.findAll('a', {'class': "col box-border passive"})
        active_prod=soup.findAll('a', {'class': "col box-border"})
        disc=soup.find('div', {'class':'detay-indirim'})
        curr_pric=soup.find('span', {'class':'currencyPrice discountedPrice'})
        prod_pric=soup.find('span', {'class':'product-price'})
        prod_name=soup.find('h1', {'class':'fl col-12 product-name'})
        skul=soup.find('div', {'class':'product-feature-content'})
        if(skul!=None and prod_pric!=None):
            for s in skul.select('div'):
                s.extract()
            if (len(active_prod)!=0 and len(passive_prod)==0):
                avail=100
            elif (len(active_prod)==0 and len(passive_prod)!=0):
                avail=0
            else:
                avail = round(((len(active_prod)/(len(active_prod)+len(passive_prod)))*100),2)

            sku.append(skul.text.strip("\n"))
            product_name.append(prod_name.text.strip("\n"))
            availability.append('%'+ str(avail))
            if(curr_pric!=None):
                BeforeDiscount_price.append(curr_pric.text.strip("\n").rstrip("TL"))
                discount.append(disc.text)  
            else:
                BeforeDiscount_price.append("-")
                discount.append("-")
            
            AfterDiscountProduct_price.append(prod_pric.text.strip("\n"))
            link.append(values[i][0])
        else:
            sku.append("-")
            product_name.append("-")
            availability.append("-")
            BeforeDiscount_price.append("-")
            discount.append("-")
            AfterDiscountProduct_price.append("-")
            link.append(values[i][0])

    finallist=[link,sku,product_name,availability,BeforeDiscount_price,discount,AfterDiscountProduct_price]
    npOfFinallist=np.array(finallist)
    transpose = npOfFinallist.T
    transpose_list = transpose.tolist()
    request=sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="URL!A"+str((pageSize*j)+2), valueInputOption="USER_ENTERED", body={"values": transpose_list}).execute()


sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range="URL!A1", valueInputOption="USER_ENTERED", body={"values": headers}).execute()


print(time.time() - start_time)
