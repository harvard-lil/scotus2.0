import os, csv, re


def clean_urls():
    """Some extracted URLs have some junk in them. Usually some trailing chars.
    In the logic below, we trim anything that feels obviously wrong, and we 
    dump it to a log. We then write our cleaned urls to a new CSV.
    """

    cleaned_rows = []

    count = 0 

    with open('./results/urls.csv', 'rb') as csvfile:
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
        fieldnames = [u'URL in opinion', u'CL ID', u'Case name', u'CL address', u'Date opinion was filed', u'Opinion download URL', u'Citation count']
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
        fieldnames = [u'URL in opinion', u'CL ID', u'Case name', u'CL address', u'Date opinion was filed', u'Opinion download URL', u'Citation count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in deduped_rows:
            writer.writerow(row)

if __name__ == "__main__":
    #clean_urls()
    dedupe_urls()