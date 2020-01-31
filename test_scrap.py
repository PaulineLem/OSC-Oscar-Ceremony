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
    for tr in table.find_all('tr') :
        print("content", tr.contents)
        print("text", tr.text)

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
            content_list.append([{'date': tr.text[indice_date:indice_date+10], 'place': tr.text[indice_place:]}])


            
        if(tr.text[:11] == 'Nationality'):
            nationality = tr.text[11:]
            content_list.append([{'nationality':nationality}])
        if(tr.text[:11] == 'Citizenship'):
            nationality = tr.text[11:]
            content_list.append([{'citizenship':nationality}])

        # content_list.append([{'date': tr.text[indice_date:indice_date+10], 'place': tr.text[indice_place:], 'nationality':nationality}])

    
    write_csv_file(content_list, query)
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

def write_csv_file(content_list, name):
    with open(r'{}.csv'.format(name), mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter='')
        print(content_list)
        writer.writerows(content_list)

print(infobox('Jean_Dujardin'))
print(infobox('Tom_Cruise'))
print(infobox('Hilary_Swank'))
print(infobox('Ralph_Fiennes'))






# [[b'Jean Dujardin'], [b'Dujardin in 2019'], [b'Born', b'Jean Edmond Dujardin (1972-06-19) 19 June 1972 (age\xc2\xa047)Rueil-Malmaison, France'], [b'Occupation', b'\nActor\ntelevision director\ncomedian\n'], [b'Years\xc2\xa0active', b'1996\xe2\x80\x93present'], [b'Spouse(s)', b'Ga\xc3\xablle Dujardin (?\xe2\x80\x932003)Alexandra Lamy(m.\xc2\xa02009; div.\xc2\xa02014)[1]Nathalie P\xc3\xa9chalat (m.\xc2\xa02018)'], [b'Children', b'3']]