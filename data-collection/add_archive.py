import os, csv, re, json, time, pytz
from dateutil import parser, relativedelta
import requests

tz = pytz.timezone('America/New_York')


def format_timetravel_date(date):
    """timetravel likes dates in yyyymmddhhmmss format"""
    #date_pieces = date.split('/')
    #return "%s%s%s" % (date_pieces[0], date_pieces[1], date_pieces[2])

    dt = parser.parse(date)
    if dt.tzinfo == None:
        dt = dt.replace(tzinfo = tz)

    return dt
    
def cleanup_encoding(value_to_encode):
    """There was a lot of debugging happending when this logic was
    written. This is probably not needed."""
    return str(value_to_encode).encode('utf8')


def check_archive_availablility():

    with open('../results/consolidated-network.csv', 'rb') as csvfile:
        url_reader = csv.DictReader(csvfile)
        for row in url_reader:


            archive_status = 0
        
            url = row['URL in opinion']
            date_filed = cleanup_encoding(row['Date opinion was filed'])
            tt_date = format_timetravel_date(date_filed)

            tt_address = "http://timetravel.mementoweb.org/api/json/{0}/{1}".format(tt_date.strftime('%Y%m%d'), url)
            print tt_address
            r = requests.get(tt_address)
            try:
                parsed_json = r.json()
                
                closest_memento_date = parser.parse(parsed_json['mementos']['closest']['datetime'])

                #print tt_date.strftime('%Y%m%d')
                #print closest_memento_date.strftime('%Y%m%d')
                d = closest_memento_date - tt_date
                time_difference_in_days = int(d.total_seconds() / 86400)
                if time_difference_in_days <= 14:
                    archive_status = 1
                

            except ValueError:
                pass
                #print 'No JSON available'
            


            row["Archive within 14 days"] = archive_status

            time.sleep(2)
    
            # Write our cleaned URLs to a new CSV
            with open('../results/consolidated-network-with-tt-14-day.csv', 'a') as csvfile:
                fieldnames = [u'URL in opinion', u'Timetravel URL', u'Rot', u'Archive', u'Archive Source', u'CL address', u'Case name', u'Date opinion was filed', u'Opinion download URL', u'Citation count', u'CL ID', u'Link rot', u'Ref rot', u'IP owner handle', u'IP owner name', u'HTTP status code', u'Archive within 14 days']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                #writer.writeheader()
                writer.writerow(row)


check_archive_availablility()