import os, csv, re


def clean_urls():
    """Some extracted URLs have some junk in them. Usually some trailing chars.
    In the logic below, we trim anything that feels obviously wrong, and we 
    dump it to a log. We then write our cleaned urls to a new CSV.
    """

    cleaned_rows = []

    count = 0 

    with open('./results/raw-urls.csv', 'rb') as csvfile:
        url_reader = csv.DictReader(csvfile)
        for row in url_reader:
        
            url = row['URL in opinion']
        
            # kill any weird screen scraping remainders
            url = re.sub(r'(<.*)*', '', url)
        
            # kill trailing paragraph tags
            url = re.sub(r'(\(.*)*', '', url)
            url = re.sub(r'(\).*)*', '', url)
        
            # trim any remaining weird punctuation
            url = url.rstrip('\'\",.:;!?')
        
            # finally, trim off any remaining whitespace
            url = url.rstrip()
        
            if url != row['URL in opinion']:
                print "Changed the following URL in %s" % row['Case name']
                print "From, %s" % row['URL in opinion']
                print "To, %s\n" % url
                count+=1
            
                row['URL in opinion'] = url
            
            cleaned_rows.append(row)
        

    print "Changed %i URLs" % count
    
    
    # Write our cleaned URLs to a new CSV
    with open('./results/cleaned-urls.csv', 'a') as csvfile:
        fieldnames = [u'URL in opinion', u'CL address', u'Timetravel URL', u'Case name', u'Date opinion was filed', u'Opinion download URL', u'Citation count', u'CL ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in cleaned_rows:
            writer.writerow(row)



def dedupe_urls():
    """Dedupe our list of URLs. If the URL exists in the list, and the other
    instances have the same Case name, let's remove the dupe.
    """

    original_rows = []
    deduped_rows = []

    with open('./results/cleaned-urls.csv', 'rb') as csvfile:
        url_reader = csv.DictReader(csvfile)
        for row in url_reader:
            original_rows.append(row)
            
    for row in original_rows:
        row_in_deduped_rows = False
        for deduped_row in deduped_rows:
            if (row['URL in opinion'] == deduped_row['URL in opinion'] and row['Case name'] == deduped_row['Case name']):
                row_in_deduped_rows = True
               
        if not row_in_deduped_rows:
            deduped_rows.append(row)
        else:
            print "The following URL from, %s, appears to be a dupe. Removed." % row['Case name']
            print "%s\n" % deduped_row['URL in opinion']
                
    print "Started with %i URLs. After deduping, we have %i." % (len(original_rows), len(deduped_rows))

    # Write our cleaned URLs to a new CSV
    with open('./results/deduped-and-cleaned-urls.csv', 'a') as csvfile:
        fieldnames = [u'URL in opinion', u'CL address', u'Timetravel URL', u'Case name', u'Date opinion was filed', u'Opinion download URL', u'Citation count', u'CL ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in deduped_rows:
            writer.writerow(row)


def combine_rot_columns():
    """
    if link ==1 pr link == s404
        rot column = 1
    else
        rot column = 0


    read in results/first-version-urls-with-rot-check-deduped-and-cleaned-urls.csv

    loop through rows, adjust, write back out
    """

    rot_combined_rows = []

    # Consolidated our two columns of rot into one called Rot
    with open('results/first-version-urls-with-rot-check-deduped-and-cleaned-urls.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:

            if row['Rot'] == None:

                rotten = 0

                if row['Link rot '] == '1' or row['Ref rot'] == 's404':
                    rotten = 1

                row['Rot'] = rotten


            rot_combined_rows.append(row)


    # replace our string values wtih our numerical values
    for row in rot_combined_rows:
        archive_values = row['Archive Source']
        archive_values = archive_values.replace('IA', '1')
        archive_values = archive_values.replace('NARA', '2')
        archive_values = archive_values.replace('National Archives and Records Administration', '2')
        archive_values = archive_values.replace('archive-it', '3')
        archive_values = archive_values.replace('Archive-It', '3')
        archive_values = archive_values.replace('archive.today', '4')
        archive_values = archive_values.replace('Stanford Web Archive', '5')
        archive_values = archive_values.replace('Stanford Web Archives', '5')
        archive_values = archive_values.replace('Icelandic Web Archive', '6')
        archive_values = archive_values.replace('Icelandic Web Archives', '6')
        archive_values = archive_values.replace('UK Web Archive', '7')
        archive_values = archive_values.replace('UK Web Archives', '7')
        archive_values = archive_values.replace('UK National Archives Web Archive', '8')
        row['Archive Source'] = archive_values

    # Write our cleaned URLs to a new CSV
    with open('./results/consolidated-rot-vals.csv', 'a') as csvfile:
        fieldnames = [u'URL in opinion', u'Timetravel URL', u'Rot', u'Archive', u'Archive Source', u'CL address', u'Case name', u'Date opinion was filed', u'Opinion download URL', u'Citation count', u'CL ID', u'Link rot ', u'Ref rot']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


        for row in rot_combined_rows:
            writer.writerow(row)



if __name__ == "__main__":
    #clean_urls()
    #dedupe_urls()
    combine_rot_columns()