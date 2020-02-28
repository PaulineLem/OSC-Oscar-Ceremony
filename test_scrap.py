from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import csv
import json

def infobox(actor) :

    acteur = actor["entity"].split()
    name = ""
    for part in acteur:
        name += "_{}". format(part)
    query = name[1:]
    url = 'https://en.wikipedia.org/wiki/'+query
    raw = urlopen(url)
    soup = bs(raw)
    table = soup.find('table',{'class':'infobox biography vcard'})
    for tr in table.find_all('tr') :
        if(tr.text[:4] == 'Born'):
            k=0
            indice_date = 0
            while k<len(tr.text) and indice_date == 0:
                if tr.text[k]=="(" :
                    indice_date = k+1
                k+=1
            i = len(tr.text)
            indice_place = 0
            while i >0 and indice_place ==0:
                if tr.text[k]==",":
                    indice_place = k+1
                k-=1
            actor["date"] = tr.text[indice_date:indice_date+10]
            actor["place"] = tr.text[indice_place:]
        if(tr.text[:11] == 'Nationality'):
            nationality = tr.text[11:]
            actor["nationality"] = nationality
        if(tr.text[:11] == 'Citizenship'):
            citizenship = tr.text[11:]
            actor["citizenship"] = citizenship  
    return actor


def write_json_file(list):
    actors_not_found = []
    data = []
    with open(r'data_json_v2.json', mode='w') as json_file:
        for k in list:
            try : 
                content_list = infobox(k)     
                data.append(content_list)
            except:
                actors_not_found.append(k)
                print('Je ne trouve pas l\'url')
        json.dump(data, json_file)
    return(actors_not_found)



# liste = ['Ralph_Fiennes', 'Hilary_Swank','Tom_Cruise',  'Jean_Dujardin' ]
# write_json_file(liste)



def list_generation():
    liste = []
    with open(r'data_csv.csv', mode='r') as csv_data_file:
        readCSV = csv.reader(csv_data_file, delimiter=',')
        for row in readCSV:
            if row[0]!='year':
                if int(row[0])>2000 and (row[1] in ['ACTOR IN A LEADING ROLE', 'ACTOR IN A SUPPORTING ROLE', 'ACTRESS IN A LEADING ROLE', 'ACTRESS IN A SUPPORTING ROLE']):
                    name = row[3].split(" ", 1)
                    if len(name)>1:
                        actor = {"entity": row[3], "year": row[0], "category" : row[1], "winner" : row[2], "name":name[0], "surname":name[1]}
                    else:
                        actor = {"entity": row[3], "year": row[0], "category" : row[1], "winner" : row[2], "name":name[0], "surname":""}
                    try :
                        liste.append(actor)
                    except:
                        print(actor)
    liste_not_found = write_json_file(liste)
    return liste_not_found

# write_csv_file(liste)

print(list_generation())




