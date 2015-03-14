import csv
from collections import OrderedDict

def get_rot_and_archive_counts():

    total_urls = 0
    
    total_rotten = 0
    total_with_archive = 0
    total_rotten_with_archive = 0

    total_rotten_with_archive = 0
    percent_rotten_with_archive = 0

    with open('../results/final-raw.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:

            if total_urls >= 555:
                break

            total_urls += 1

            if row['Rot'] == '1':
                total_rotten += 1

            if row['Archive'] == '1':
                total_with_archive += 1

            if row['Rot'] == '1' and row['Archive'] == '1':
                total_rotten_with_archive += 1


    percent_rotten = total_rotten / float(total_urls)
    percent_with_archive = total_with_archive / float(total_urls)
    percent_rotten_with_archive = total_rotten_with_archive / float(total_rotten)


    print "Total URLs in opinions, %i\n" % total_urls

    print "Total rotten, %i" % total_rotten
    print "Percent rotten, %0.2f\n" % percent_rotten

    print "Total archive, %i" % total_with_archive
    print "Percent with archive, %0.2f\n" % percent_with_archive

    print "Total rotten with an archive %s" %total_rotten_with_archive
    print "Perecent rotten with an archive %0.2f\n" % percent_rotten_with_archive


def get_rot_per_year():

    year_totals = {}
    year_rot_vals = {}
    year_archive_vals = {}

    for i in range(1996, 2015):
        year_totals[str(i)] = 0
        year_rot_vals[str(i)] = 0
        year_archive_vals[str(i)] = 0

    with open('../results/final-raw.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            year = row['Date opinion was filed'].split('/')[2]

            year_totals[year] += 1

            if row['Rot'] == '1':
                if row['Archive'] == '1':
                    year_archive_vals[year] += 1
                else:
                    year_rot_vals[year] += 1

    # it's easy to feed d3 a csv file. build it here.
    d3_formatted = []

    for i in range(1996, 2015):
        year = str(i)

        year_total = year_totals[year] - (year_rot_vals[year] + year_archive_vals[year])

        d3_formatted.append([year, str(year_archive_vals[year]), str(year_rot_vals[year]), str(year_total), ])
    
    with open('year-rot-d3.csv', 'a') as csvfile:
        fieldnames = [u'Year', u'Rotten. Not available through an archive', u'Rotten. Available through an archive', u'Not rotten',]
        writer = csv.writer(csvfile)
        
        writer.writerow(fieldnames)
        for row in d3_formatted:
            writer.writerow(row)



def get_acrhive_dist_per_year():

    year_archive_vals = OrderedDict()

    for i in range(1996, 2015):
        year_archive_vals[str(i)] = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}

    with open('../results/final-raw.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:

            year = row['Date opinion was filed'].split('/')[2]

            if not  row['Archive Source'].startswith('***'):
                archive_sources = row['Archive Source'].split(',')

                for archive_source in archive_sources:

                    if archive_source and archive_source != '0':
                        archive_source = archive_source.strip()
                        #print "appending %s to %s" % (archive_source, year)
                        year_archive_vals[year][archive_source] += 1


    print year_archive_vals

    with open('archive-dist-d3.csv', 'a') as csvfile:
        fieldnames = [u'Year', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', ]
        writer = csv.writer(csvfile)
        
        writer.writerow(fieldnames)
        for k,v in year_archive_vals.iteritems():
            writer.writerow([k, v['1'], v['2'], v['3'], v['4'], v['5'], v['6'], v['7'], v['8'], ])



def get_top_n_web_hosts():

    ip_owners = {'akamai': 0, 'amazon': 0, 'softlayer': 0, 'fastly': 0, 'rackspace': 0, 
        'google': 0, 'edgecast': 0, 'microsoft': 0, 'qwest': 0, 'cloudflare': 0, 'cdnetworks': 0, 'level3': 0}

    total = 0

    with open('../results/final-raw.csv', 'rU') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total += 1
            ip_owner = row['IP owner name']
            ip_owner = ip_owner.lower()

            if 'akamai' in ip_owner:
                ip_owners['akamai'] += 1

            if 'amazon' in ip_owner or 'amzn' in ip_owner:
                ip_owners['amazon'] += 1

            if 'soft' in ip_owner:
                ip_owners['softlayer'] += 1

            if 'fastly' in ip_owner:
                ip_owners['fastly'] += 1

            if 'rackspace' in ip_owner:
                ip_owners['rackspace'] += 1

            if 'goog' in ip_owner:
                ip_owners['google'] += 1

            if 'edgecast' in ip_owner:
                ip_owners['edgecast'] += 1

            if 'microsoft' in ip_owner:
                ip_owners['microsoft'] += 1

            if 'qwest' in ip_owner:
                ip_owners['qwest'] += 1

            if 'cloudflare' in ip_owner:
                ip_owners['cloudflare'] += 1

            if 'cdnetworks' in ip_owner:
                ip_owners['cdnetworks'] += 1

            if 'level' in ip_owner:
                ip_owners['level3'] += 1


    for k,v in ip_owners.iteritems():
        percent_cloud = v / float(total)
        print '<tr>'
        print '    <th scope="row">1</th>'
        print '    <td>%s</td>' % k
        print '    <td>%i/%0.2f</td>' % (v, percent_cloud)
        print '</tr>'
        
if __name__ == "__main__":

    #get_rot_and_archive_counts()
    #get_rot_per_year()
    #get_acrhive_dist_per_year()
    get_top_n_web_hosts()