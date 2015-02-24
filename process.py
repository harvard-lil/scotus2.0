import os, json, re, csv, sys
from pprint import pprint

reload(sys);
sys.setdefaultencoding("utf8")

data_dir = './data/'

#######
# Below is some fairly raw logic for extracting URLs from the CourtListener.org
# bulk SCOTUS download. To use this, unpack the tarball you get from
# curl -LO https://www.courtlistener.com/api/bulk-data/document/scotus.tar.gz
# into a directory called 'data'.
#
# If things worked, you'll see a csv called raw-urls.csv in the results
# directory (you'll probably need to create the results dir)
#######

# A forgiving regex for a URL
url_pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def find_all_urls(text):
    """return a list of all urls in chunk of text"""
    return re.findall(url_pattern, text)

def format_timetravel_date(date):
    """timetravel likes deas in yyyymmdd format"""
    date_pieces = date.split('-')
    return "%s%s%s151530" % (date_pieces[0], date_pieces[1], date_pieces[2])
    
def cleanup_encoding(value_to_encode):
    """There was a lot of debugging happending when this logic was
    written. This is probably not needed."""
    return str(value_to_encode).encode('utf8')

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
            if find_all_urls(u_string):
                urls += find_all_urls(u_string)

        # html key
        if 'html' in data and data['html']:
            u_string = data['html'].encode('utf-8').replace('\n', '')
            if find_all_urls(u_string):
                urls += find_all_urls(u_string)

        # html_lawbox
        if 'html_lawbox' in data and data['html_lawbox']:
            u_string = data['html_lawbox'].encode('utf-8').replace('\n', '')
            if find_all_urls(u_string):
                urls += find_all_urls(u_string)

        # plain_text key
        if 'plain_text' in data and data['plain_text']:
            u_string = data['plain_text'].encode('utf-8').replace('\n', '')
            if find_all_urls(u_string):
                urls += find_all_urls(u_string)

        if urls:
            for url in set(urls):

                url = cleanup_encoding(url)                
                date_filed = cleanup_encoding(data['date_filed'])
                timetravel_address = "http://timetravel.mementoweb.org/list/%s/%s" % (format_timetravel_date(date_filed), url)
                cl_id = cleanup_encoding(data['id'])
                case_name = cleanup_encoding(data['citation']['case_name'])
                cl_address = u'http://courtlistener.org' + cleanup_encoding(data['absolute_url'])
                opinion_url = cleanup_encoding(data['download_url'])
                citation_count = cleanup_encoding(data['citation_count'])
                
                row = {'URL in opinion': url, 'CL address': cl_address, 'Timetravel URL': timetravel_address, 'Case name': case_name, 'Date opinion was filed': date_filed, 'Opinion download URL': opinion_url, 'Citation count':  citation_count, 'CL ID': cl_id}

                rows.append(row)


with open('results/raw-urls.csv', 'a') as csvfile:
    fieldnames = [u'URL in opinion', u'CL address', u'Timetravel URL', u'Case name', u'Date opinion was filed', u'Opinion download URL', u'Citation count', u'CL ID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in rows:
        writer.writerow(row)
