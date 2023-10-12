# Importing libraries
import json
import imaplib, email, email.policy
import html2text
from bs4 import BeautifulSoup
from schemas.donhang import Donhang
from services.email_services import list_of_emails
from services.donhang_services import save_donhang
import models

# user = 'dungngtdev@gmail.com'
# password = 'tgzysduvicnlxfjw'
imap_url = 'imap.gmail.com'
con = imaplib.IMAP4_SSL(imap_url)
# con = None

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
 
# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data
 
def email_to_html(parsed):
    all_parts = []
    for part in parsed.walk():
        if type(part.get_payload()) == list:
            for subpart in part.get_payload():
                all_parts += email_to_html(subpart)
        else:
            if encoding := part.get_content_charset():
                all_parts.append(part.get_payload(decode=True).decode(encoding))
    return ''.join(all_parts)

# Function to get the list of emails under this label
async def get_emails(con,receiver,result_bytes):
    try:
        msgs = [] # all the email data are pushed inside an array
        for num in result_bytes[0].split():
            typ, email_data = con.fetch(num, '(RFC822)')
            for response in email_data:
                if isinstance(response, tuple):
                    raw_email = response[1]
                    parsed = email.message_from_bytes(raw_email)
                    for header in [ 'subject']:
                        # print('%-8s: %s' % (header.upper(), parsed[header]))
                        subject = '%-8s: %s' % (header.upper(), parsed[header])
                        tensp = subject[subject.rfind('You made the sale for')+ len('You made the sale for')+1:len(subject)]
                    msg_data = email_to_html(parsed)
                    soup = BeautifulSoup(msg_data, 'html5lib') 
                    data_content = soup.find_all('p')
                    
                    # donhang = Donhang()
                    # Donhang.taikhoan = receiver
                    thongtin = ""
                    tongtien = ""
                    order_number = ""
                    item_number = ""
                    date_sold = ""
                    soluong = ""
                    link_sp = ""
                    for idx, content in enumerate(soup.find_all('p')):
                        # print(content)
                        if "Your buyer's shipping details:" in content.get_text():
                            # print(data_content[idx+1].get_text().split("\n"))
                            thongtin = data_content[idx+1].get_text().replace('\r', '').replace('\n', '')
                        if "Paid:" in content.get_text():
                            # print(data_content[idx+1].get_text())
                            tongtien = data_content[idx+1].get_text().replace('\r', '').replace('\n', '')
                        if "Order number:" in content.get_text():
                            # print(data_content[idx+1].get_text())
                            order_number = data_content[idx+1].get_text().replace('\r', '').replace('\n', '')
                        if "Item number:" in content.get_text():
                            # print(data_content[idx+1].get_text())
                            item_number = data_content[idx+1].get_text().replace('\r', '').replace('\n', '')
                        if "Date sold:" in content.get_text():
                            # print(data_content[idx+1].get_text())
                            date_sold = data_content[idx+1].get_text().replace('\r', '').replace('\n', '')
                        if "Quantity sold:" in content.get_text():
                            # print(data_content[idx+1].get_text())
                            soluong = data_content[idx+1].get_text().replace('\r', '').replace('\n', '')
                    for idx, content in enumerate(soup.find_all('a', href=True)):
                        print(f"https://www.ebay.com/mesh/ord/details?orderid={order_number}")
                        if f"https://www.ebay.com/mesh/ord/details?orderid={order_number}" in content['href']:
                            link_sp = content['href']
                            break
                    await models.Donhang.create(taikhoan=receiver, tensp=tensp,thongtin=thongtin,
                                    tongtien=tongtien,link_sp=link_sp,order_number=order_number
                                    ,item_number=item_number,date_sold=date_sold,soluong=soluong)
                        # await save_donhang(donhang)
                        # print(table.get_text())
                        # for row in table.find_all('p'):
                            # print(row.get_text())
                            
                            # print(row)
                    # print('raw_email',raw_email)
                    msgs.append(email_to_html(parsed))
            # raw_email = email_data[0][1].decode("UTF-8")
            # email_message = email.message_from_string(raw_email)
            # soup = BeautifulSoup(msg_data, 'html5lib') 
            # table = soup.find('table')  
            # for row in table:
            #     print(row)
            # print('raw_email',raw_email)
            # msgs.append(msg_data)
            print('finish all')
        return msgs
    except ValueError:
        print(ValueError)

async def get_don_hang():
    # this is done to make SSL connection with GMAIL
    emails = await list_of_emails()
    if emails is None or len(emails) == 0:
        return {"code": "ERR_01", "message": "Chưa có email"}
    # logging the user in
    
    # fetching emails from this user "tu**h*****1@gmail.com"
    f = open("config/config.json", "r")
    config_mail = json.load(f)
    try:
        for email in emails:
            email_domain = email.email.split('@')[1]
            imap_host = config_mail[f"{email_domain}"]['host']
            print(imap_host)
            print(email.email)
            print(email.secret_code)
            for email_search in email.email_list.split(','):
                # calling function to check for email under this label
                # print(email_search)
                con = imaplib.IMAP4_SSL(imap_host)
                con.login(email.email, email.secret_code)
                con.select('INBOX')
                await get_emails(con,email_search,search('UNSEEN FROM', email_search, con))
                print("Close 1")
                con.close()

    except ValueError:
        return {"code": "ERR_01", "message": "Lỗi kết nối mail"}
            
    return {"code": "SUCCESS", "message": "Update thành công"}
    # msgs = await get_emails('hashan324l@gmail.com',search('FROM', 'hashan324l@gmail.com', con))
# Uncomment this to see what actually comes as data
# print(msgs)
 
