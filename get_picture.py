import requests
import json
import csv


APIKEY = "AIzaSyCzxa9mtx31ShqP-pd3KncXvXTg-Qw3WhQ"
cx= "003201410527697407127:mm2viljoxan"

def list_generation():
    liste_not_found = []
    i=0
    with open(r'data_json_v2_pict.json', mode='r') as json_file:
        data = json.load(json_file)
        for actor in data:
            if actor.get("picture_link") == None:
                url = "https://www.googleapis.com/customsearch/v1?key="+APIKEY+"&cx="+cx+"&q="+actor["name"]+" "+actor["surname"]+"&searchType=image&num=1"
                try :
                    r = requests.get(url)
                    json_res = json.loads(r.text)
                    actor["picture_link"]= json_res["items"][0]["link"]
                    i+=1
                except:
                    liste_not_found.append(actor["entity"])
    with open(r'data_json_v2_pict.json', mode='w') as json_file:
        json.dump(data, json_file)
    return liste_not_found, i

print(list_generation())




