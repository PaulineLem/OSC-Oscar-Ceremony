from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import csv


def infobox(query) :
    query = query
    content_list = []
    url = 'https://en.wikipedia.org/wiki/'+query
    raw = urlopen(url)
    soup = bs(raw)
    table = soup.find('table',{'class':'infobox biography vcard'})
    name = query.split('_')
    data = {'name':name[0], 'surname':name[1]}
    for tr in table.find_all('tr') :
        # if len(tr.contents) > 1:
        #     content_list.append([tr.contents[0].text.encode('utf-8'), tr.contents[1].text.encode('utf-8')])
        # elif tr.text:
        #     content_list.append([tr.text.encode('utf-8')])
        # print(tr.text)
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
            data['date'] = tr.text[indice_date:indice_date+10]
            data['place'] = tr.text[indice_place:]
            # content_list.append([{'date': tr.text[indice_date:indice_date+10], 'place': tr.text[indice_place:]}])   
        if(tr.text[:11] == 'Nationality'):
            nationality = tr.text[11:]
            data['nationality'] = nationality
            # content_list.append([{'nationality':nationality}])
        if(tr.text[:11] == 'Citizenship'):
            citizenship = tr.text[11:]
            data['citizenship'] = citizenship
            # content_list.append([{'citizenship':nationality}])
    content_list.append([data])

        # content_list.append([{'date': tr.text[indice_date:indice_date+10], 'place': tr.text[indice_place:], 'nationality':nationality}])

    
    return content_list
    # result = {}
    # exceptional_row_count = 0
    # for tr in table.find_all('tr'):
    #     if tr.find('th'):
    #         result[tr.find('th').text] = tr.text
    #     else:
    #         # the first row Logos fall here
    #         exceptional_row_count += 1
    # if exceptional_row_count > 1:
    #     print('WARNING ExceptionalRow>1: ', table)
    # return result

def write_csv_file(list):
    actors_not_found = []

    with open(r'data_actors-actresses.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for k in list:
            try : 
                content_list = infobox(k)     
                writer.writerows(content_list)
            except:
                actors_not_found.append(k)
                print('Je ne trouve pas l\'url')
    return(actors_not_found)

# print(infobox('Jean_Dujardin'))
# print(infobox('Tom_Cruise'))
# print(infobox('Hilary_Swank'))
# print(infobox('Ralph_Fiennes'))

# liste = ['Ralph_Fiennes', 'Hilary_Swank','Tom_Cruise',  'Jean_Dujardin' ]


def list_generation():
    liste = []
    with open(r'data_csv.csv', mode='r') as csv_data_file:
        readCSV = csv.reader(csv_data_file, delimiter=',')
        for row in readCSV:
            if row[0]!='year':
                if int(row[0])>2000 and (row[1] in ['ACTOR IN A LEADING ROLE', 'ACTOR IN A SUPPORTING ROLE', 'ACTRESS IN A LEADING ROLE', 'ACTRESS IN A SUPPORTING ROLE']):
                    acteur = row[3].split()
                    name = ''
                    for part in acteur:
                        name += '_{}'. format(part)
                    try :
                        liste.append(name[1:])
                    except:
                        print(acteur)

    list_not_found = write_csv_file(liste)
    return liste_not_found

# write_csv_file(liste)

print(list_generation())


