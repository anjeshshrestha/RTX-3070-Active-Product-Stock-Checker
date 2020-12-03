import requests
import re
import json
import tkinter as tk
import threading
import time
from discord_webhook import DiscordWebhook

print("Made by anjeshshrestha")
#open the files
bbfile = open("stores/bestbuy.txt","r").readlines() 
ccfile = open("stores/canadacomputers.txt","r").readlines() 
mefile = open("stores/memoryexpress.txt","r").readlines() 
nefile = open("stores/newegg.txt","r").readlines()

#first line of file is webhook address
bb_webhook = DiscordWebhook(url=bbfile.pop())
cc_webhook = DiscordWebhook(url=ccfile.pop())
me_webhook = DiscordWebhook(url=mefile.pop())
ne_webhook = DiscordWebhook(url=nefile.pop())

bbstock_dict = dict()
mestock_dict = dict()
nestock_dict = dict()
ccstock_dict = dict()
azstock_dict = dict()
bbstock_dict['Last Update'] = 'Updating'
mestock_dict['Last Update'] = 'Updating'
nestock_dict['Last Update'] = 'Updating'
ccstock_dict['Last Update'] = 'Updating'
azstock_dict['Last Update'] = 'Updating'

#read the files and items codes in the file
bestbuy_webcode = {}
for item in bbfile[1:]:
    code, name = item.split(',')
    bestbuy_webcode[code] = name

canadacomputer_webcode = {}
for item in ccfile[1:]:
    code, name = item.split(',')
    canadacomputer_webcode[code] = name

memoryexpress_webcode = {}
for item in mefile[1:]:
    code, name = item.split(',')
    memoryexpress_webcode[code] = name

newegg_webcode = {}
for item in nefile[1:]:
    code, name = item.split(',')
    newegg_webcode[code] = name

headers = {
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4159.2 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'accept-language': 'en-US,en;q=0.9'
}

def bestBuy():
    try:
        for key, value in bestbuy_webcode.items():
            x = requests.get("https://www.bestbuy.ca/ecomm-api/availability/products?skus=" + key, headers=headers)
            stockstatus = json.loads(x.content.decode('utf-8-sig').encode('utf-8'))
            if stockstatus['availabilities'][0]['shipping']['purchasable'] == 'true':
                #print(value, '| In Stock')
                bbstock_dict[value] = 'In Stock'
                bb_webhook.set_content("IN STOCK:\n" + value + "\nhttps://www.bestbuy.ca/en-ca/product/" + key)
                bb_webhook.execute()
            else:
                #print(value, '| Out of Stock')
                bbstock_dict[value] = 'Out of Stock'
            time.sleep(1)
        bbstock_dict['Last Update'] = time.strftime('%H:%M:%S %p')
    except Exception as e:
        print('bb',e)
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def memoryExpress():
    try:        
        for key, value in memoryexpress_webcode.items():
            x = requests.get("https://www.memoryexpress.com/Products/" + key)
            stockstatus = x.text
            y = re.search("c\-capr\-inventory\-store__availability\ InventoryState_(\w+)", stockstatus)
            if y.group(1) == 'BackOrder':
                #print(value, '| Out of Stock')
                mestock_dict[value] = 'Out of Stock'
            elif y.group(1) == 'InStock':
                #print(value, '| In Stock')
                mestock_dict[value] = 'In Stock'
                me_webhook.set_content("IN STOCK:\n" + value + "\nhttps://www.memoryexpress.com/Products/" + key)
                me_webhook.execute()
            time.sleep(1)
        mestock_dict['Last Update'] = time.strftime('%H:%M:%S %p')
    except Exception as e:
        print('me',e)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def newEgg():
    try:
        for key, value in newegg_webcode.items():
            sub_key = key[7:]
            product_code = sub_key[0:2] + '-' + sub_key[2:5] + '-' + sub_key[5:]
            x = requests.get("https://www.newegg.ca/product/api/ProductRealtime?ItemNumber=" + product_code, headers=headers)
            stockstatus = x.json()
            if stockstatus['MainItem']['Stock'] == 0:
                #print(value, '| Out of Stock')
                nestock_dict[value] = 'Out of Stock'
            else:
                #print(value, '| In Stock')
                nestock_dict[value] = 'In Stock'
                ne_webhook.set_content("IN STOCK:\n" + value + "\nhttps://www.newegg.ca/p/" + key)
                ne_webhook.execute()
            time.sleep(1)
        nestock_dict['Last Update'] = time.strftime('%H:%M:%S %p')
    except Exception as e:
        print('me',e)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def canadaComputers():
    try:
        for key, value in canadacomputer_webcode.items():
            x = requests.get("https://www.canadacomputers.com/product_info.php?ajaxstock=true&itemid=" + key, headers=headers)
            stockstatus = x.json()
            if stockstatus['avail'] == 0:
                #print(value, '| Out of Stock')
                ccstock_dict[value] = 'Out of Stock'
            else:
                #print(value, '| In Stock')
                ccstock_dict[value] = 'In Stock'
                cc_webhook.set_content("IN STOCK:\n" + value + "\nhttps://www.canadacomputers.com/product_info.php?cPath=1&item_id=" + key)
                cc_webhook.execute()
            time.sleep(1)
        ccstock_dict['Last Update'] = time.strftime('%H:%M:%S %p')
    except Exception as e:
        print('cc',e)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Amazon():
    try:
        for key, value in amazon_webcode.items():
            x = requests.get('https://ca.camelcamelcamel.com/product/' + key, headers=headers)
            stockstatus = x.text
            if 'class="green">$0.00' in stockstatus:
                #print(value, '| Out of Stock')
                azstock_dict[value] = 'Out of Stock'
            else:
                #print(value, '| In Stock')
                azstock_dict[value] = 'In Stock'
            time.sleep(1)
        azstock_dict['Last Update'] = time.strftime('%H:%M:%S %p')
    except Exception as e:
        print('az',e)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def allCheck():
    print('\n-------------BEST BUY-------------')
    bestBuy()
    print('\n------------MEMORY EXPRESS-------------')
    memoryExpress()
    print('\n-------------NEW EGG-------------')
    newEgg()
    print('\n-------------CANADA COMPUTERS-------------')
    canadaComputers()
    print('\n-------------AMAZON-------------')
    amazon()
    print('Done')
#allCheck()

def dictonary_formater(stock, dictionary):
    stock.config(state='normal')
    stock.delete("1.0","end")
    stock.config(state='disabled')
    for key, value in dictionary.items():
        stock.config(state='normal')
        stock.insert(tk.END, key + ' | ')
        if value == 'Out of Stock':
            stock.insert(tk.END, value + '\n', 'red')
        else:
            stock.insert(tk.END, value + '\n', 'green')
        stock.config(state='disabled')
    
def update_time():
    current_time = time.strftime('%H:%M:%S %p - %Z - %A %d %Y')
    clock.config(text=current_time)
    clock.after(1000,update_time)

def update_bb():
    t1 = threading.Thread(target=bestBuy, args=())
    t1.start()
    dictonary_formater(bbstock, bbstock_dict)
    bbstock.after(30000,update_bb)
    
def update_me():
    t1 = threading.Thread(target=memoryExpress, args=())
    t1.start()
    dictonary_formater(mestock, mestock_dict)
    mestock.after(30000,update_me)
    
def update_ne():
    t1 = threading.Thread(target=newEgg, args=())
    t1.start()
    dictonary_formater(nestock, nestock_dict)
    nestock.after(30000,update_ne)
    
def update_cc():
    t1 = threading.Thread(target=canadaComputers, args=())
    t1.start()
    dictonary_formater(ccstock, ccstock_dict)
    ccstock.after(30000,update_cc)

def update_az():
    t1 = threading.Thread(target=Amazon, args=())
    t1.start()
    dictonary_formater(azstock, azstock_dict)
    ccstock.after(30000,update_az)

root = tk.Tk()
root.title('RTX 3070 Stock Checker')
#root.resizable(False, False)

#root.geometry('2000x1000')
col0 = tk.Label(root,width='90')
col0.grid(row=0,column=0)
col1 = tk.Label(root,width='130')
col1.grid(row=0,column=1)
row5 = tk.Label(root,height='1')
row5.grid(row=5,column=0)

rtx = tk.Label(root, text = "RTX 3070 Stock Checker", font=('times', 24, 'bold'))
rtx.grid(row=0, column=0)

clock = tk.Label(root, text = time.strftime('%H:%M:%S %p - %Z - %A %d %Y'), font=('times', 24, 'bold'))
clock.grid(row=0, column=1)

#footer = tk.Label(root,text = "\n\n\n\nUpdates about every 60 seconds -PikaPika", font=('times',24,'bold'))
#footer.grid(row=5, column=0)

bestbuy = tk.Label(root, text = "BestBuy", font=('times',24,'bold'))
bestbuy.grid(row=1,column=0)
bbstock = tk.Text(root, width="75", height="22")
bbstock.tag_config("red", foreground="red")
bbstock.tag_config("green", foreground="green")
bbstock.grid(row=2,column=0)
bbstock.config(state='disabled')


memoryexpress = tk.Label(root, text = "MemoryExpress", font=('times',24,'bold'))
memoryexpress.grid(row=3,column=0)
mestock = tk.Text(root, width="75", height="19")
mestock.tag_config("red", foreground="red")
mestock.tag_config("green", foreground="green")
mestock.grid(row=4,column=0)
mestock.config(state='disabled')


newegg = tk.Label(root, text = "Newegg", font=('times',24,'bold'))
newegg.grid(row=1,column=1)
nestock = tk.Text(root, width="110", height="22")
nestock.tag_config("red", foreground="red")
nestock.tag_config("green", foreground="green")
nestock.grid(row=2,column=1)
nestock.config(state='disabled')

canadacomputers = tk.Label(root, text = "CanadaComputers", font=('times',24,'bold'))
canadacomputers.grid(row=3,column=1)
ccstock = tk.Text(root, width="110", height="19")
ccstock.tag_config("red", foreground="red")
ccstock.tag_config("green", foreground="green")
ccstock.grid(row=4,column=1)
ccstock.config(state='disabled')

update_time()
update_bb()
update_me()
update_ne()
update_cc()

root.mainloop()
