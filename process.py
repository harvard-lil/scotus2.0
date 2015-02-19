import os, json, re, csv
from pprint import pprint

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

data_dir = './data/'

rows = []

for fn in os.listdir(data_dir):
    file_path = data_dir + fn 
    if os.path.isfile(file_path):
        json_data=open(file_path)
        data = json.load(json_data)
        json_data.close() 

        urls = []


        print "processing %s" % file_path

        # html_with_citations key
        if 'html_with_citations' in data and data['html_with_citations']:
            u_string = data['html_with_citations'].encode('utf-8').replace('\n', '')
            if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string):
                urls += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string)

        # html key
        if 'html' in data and data['html']:
            u_string = data['html'].encode('utf-8').replace('\n', '')
            if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string):
                urls += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string)

        # html_lawbox
        if 'html_lawbox' in data and data['html_lawbox']:
            u_string = data['html_lawbox'].encode('utf-8').replace('\n', '')
            if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string):
                urls += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string)

        # plain_text key
        if 'plain_text' in data and data['plain_text']:
            u_string = data['plain_text'].encode('utf-8').replace('\n', '')
            if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string):
                urls += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', u_string)

        if urls:
            for url in set(urls):
                row = {'URL in opinion': str(url).encode('utf8'), 'CL ID': str(data['id']).encode('utf8'), 'Case name': str(data['citation']['case_name']).encode('utf8'), 'CL address': u'http://courtlistener.org' + str(data['absolute_url']).encode('utf8'), 'Date opinion was filed': str(data['date_filed']).encode('utf8'), 'Opinion download URL': str(data['download_url']).encode('utf8'), 'Citation count':  str(data['citation_count']).encode('utf8')}

                rows.append(row)


with open('urls.csv', 'a') as csvfile:
    fieldnames = [u'URL in opinion', u'CL ID', u'Case name', u'CL address', u'Date opinion was filed', u'Opinion download URL', u'Citation count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)
