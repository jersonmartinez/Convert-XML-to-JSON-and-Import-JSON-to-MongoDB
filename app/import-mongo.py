import os
import xmltodict
import json
import requests
from pymongo import MongoClient

class getScriptXML:
    def __init__(self, url, save_folder, filename):
        self.url = url
        self.save_folder = save_folder
        self.filename = filename

    def getData(self):
        if not os.path.isdir(self.save_folder):
            os.system("mkdir " + self.save_folder)

        path = self.save_folder + "/" + self.filename

        response = requests.get(self.url)
        with open(path, 'wb') as file:
            file.write(response.content)
        
        self.convertXMLtoJSON(path)

    def convertXMLtoJSON(self, path):
        with open(path, "r") as xmlfileObj:
            #Converting xml data to dictionary
            data_dict = xmltodict.parse(xmlfileObj.read())
            xmlfileObj.close()
            
            #Creating JSON object using dictionary object
            jsonObj = json.dumps(data_dict)

        if not os.path.isdir("JSON"):
            os.system("mkdir " + "JSON")

        #storing json data to json file
        with open("JSON/sports.json", "w") as jsonfileObj:
            jsonfileObj.write(jsonObj)
            jsonfileObj.close()
        
        self.importJSONtoMongoDB()

    def getDB(self):
        mongoClient = MongoClient("mongodb://root-master:password-master@mongodb:27017/?authMechanism=DEFAULT&authSource=db-sports")

        return mongoClient["db-sports"]

    def importJSONtoMongoDB(self):
        db = self.getDB()
        Collection = db["sports"]

        with open('JSON/sports.json') as file:
            file_data = json.load(file)

        if isinstance(file_data, list):
            Collection.insert_many(file_data)
        else:
            Collection.insert_one(file_data)

if __name__ == "__main__":
    getScriptXML(
        'https://fx-nunchee-assets.s3.amazonaws.com/data/sports.xml',
        'XML',
        'sports.xml'
    ).getData()