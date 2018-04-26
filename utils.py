#parsing libraries
import xmltodict
import csv

# global result variable
OUTPUT = {"ID":[],"TYPE":[],"VALUE":[]}

Devices = {
    '0' : "Temperature sensors",
    '1' : "Humidity sensors",
    '2' : "Motion sensors",
    '3' : "Alien Presence detectors", 
    '4' : "Dark Matter detectors",
    '5' : "Top Secret detectors"}
    
def deserialize(response, type):
    if (type == "Application/json"):
        return response.json()

    elif (type == "Application/xml"):
        return xmltodict.parse(response.text)["device"]

    elif (type == "text/csv"):
        d = {'device_id':[],
             'sensor_type':[],
             'value':[]}
        reader = csv.DictReader(response.text.splitlines())        
        for row in reader:
            for key in row:
                d[key].append(row[key])        
        return d
    
    return "not relevant"
    
def saveData(data,type):
    #print(type, data)
    if (type == "Application/xml"):
        for key in data:
            if key == "@id":
                OUTPUT["ID"].append([data.get(key)])  
            if key == "type":
                OUTPUT["TYPE"].append([data.get(key)])   
            if key == "value":
                OUTPUT["VALUE"].append([data.get(key)])  

    elif (type == "Application/json"):
        for key in data:
            if key == "device_id":
                OUTPUT["ID"].append([data.get(key)])  
            if key == "sensor_type":
                OUTPUT["TYPE"].append([data.get(key)]) 
            if key == "value":
                OUTPUT["VALUE"].append([data.get(key)])  
                
    elif (type == "text/csv"):
        for key in data:
            if key == "device_id":
                OUTPUT["ID"].append(data.get(key))  
            if key == "sensor_type":
                OUTPUT["TYPE"].append(data.get(key)) 
            if key == "value":
                OUTPUT["VALUE"].append(data.get(key)) 
                
def debugData(urls,headers):
    print("\nKey:")
    print(headers['Session'])
    print("\nUrls:")
    for i in range(len(urls)):
        print(urls[i])
    print('\n')
       
def formatOutput():
    #Collecting raw data (list with lists)
    L1 = [item for sublist in OUTPUT["ID"] for item in sublist]
    L2 = [item for sublist in OUTPUT["TYPE"] for item in sublist]
    L3 = [item for sublist in OUTPUT["VALUE"] for item in sublist]
    
    #Storing collected data into a dict
    FINAL = {"ID":L1,"TYPE":L2,"VALUE":L3}
    #print(FINAL)
    print("\n- RESULTS -")
    for i in range(len(Devices)):
        t=0;
        print("\n",Devices[str(i)],": ") #device name
        for j in FINAL["TYPE"]:
            if j == str(i) or j==i: #ordering data by device type
                print("Device-|",FINAL["ID"][t],"|:",FINAL["VALUE"][t])
            t+=1 
