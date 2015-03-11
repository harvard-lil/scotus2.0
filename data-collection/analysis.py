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




if __name__ == "__main__":

    #get_rot_and_archive_counts()
    #get_rot_per_year()
    get_acrhive_dist_per_year()