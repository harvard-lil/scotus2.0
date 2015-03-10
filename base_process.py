import os, json, re 
from pprint import pprint


data_dir = './data/'

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
            print "========================="
            print ""
            print data['absolute_url']
            print data['date_filed']
            print data['download_url'] or "No download URL"
            print data['id']
            print data['citation_count']

        for u in set(urls):
            print u
            #pass
