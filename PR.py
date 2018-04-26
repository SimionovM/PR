import requests
import json
from threading import Thread, Lock
import threading
import time
import csv
import xml.etree.ElementTree as ET
import utils


url = 'https://desolate-ravine-43301.herokuapp.com'
mutex = Lock()
urls = []
threadList = []
response = []
n=0
retry = True

def Request(n):
    try:
        a = requests.get(urls[n], headers = headers)
        processResult(a)
        
    except requests.exceptions.RequestException as e:
        print ('Error: ', e, '\nRetrying...\n')
        retry = True


def processResult(result):
    format = result.headers['Content-Type']
    deviceBody = utils.deserialize(result,format)
    utils.saveData(deviceBody, format)


def postRequest(url):
    try:
        r = requests.post(url)
    except requests.exceptions.RequestException as e:
        print ('Error: ', e, '\nRetrying...\n')
        return postRequest(url)
    return r


def threading(urls):
    for i in range(0,len(urls)):
        t = Thread(target=Request, args=[i])
        t.start()
        threadList.append(t)
            
    for i in range(0, len(urls)):
        t.join()
       

while(retry):
    r = postRequest(url)
    headers = {'Session': r.headers.get('Session')}
    body = r.json()
    retry = False
    for n in range(len(body)):
        urls.append(url + str(body[n]['path']))
    utils.debugData(urls, headers)
    threading(urls)
    

time.sleep(20)
utils.formatOutput()  
