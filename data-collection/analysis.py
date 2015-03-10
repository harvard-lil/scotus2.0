import csv

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
        fieldnames = [u'Year', u'Citation is rotten but is available through an archive', u'Citation is rotten and not available through an archive', u'Citation is not rotten',]
        writer = csv.writer(csvfile)
        
        writer.writerow(fieldnames)
        for row in d3_formatted:
            writer.writerow(row)



if __name__ == "__main__":

    get_rot_and_archive_counts()
    #get_rot_per_year()