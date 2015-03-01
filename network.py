import csv, time, tldextract, requests, json, subprocess, requests

import dns.resolver

# In the below logic we add http and other network values
# for our urls

def get_ip_owner(url):

    # Get name from the URL
    name_parts = tldextract.extract(url)
    name = name_parts.subdomain + '.' + name_parts.domain + '.' + name_parts.suffix

    print "name from parts %s" % name

    try:
        answers = dns.resolver.query(name, 'A')
        ip_address = answers[0].address
        return ip_address
    except Exception as e:
            print e

def get_arin_data(ip_address):
    """
    Given an IP, return what ARIN has listed for the owner
    """

    # Some common cloud hosts
    cloud_providers = ['amazon', 'rackspace', 'softlayer', 'microsoft', 'google']

    org_name = ''
    org_handle = ''

    try:
        # get org from IP from ARIN API
        url = 'http://whois.arin.net/rest/ip/' + ip_address
        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        jr = json.loads(r.text)    

        if 'net' in jr and 'orgRef' in jr['net'] and '@name' in jr['net']['orgRef']:
            org_name = jr['net']['orgRef']['@name']
            org_handle = jr['net']['orgRef']['@handle']
                
    except Exception as e:
            print e

    return (org_name, org_handle)
    #return org_handle

def get_ripe_data(ip_address):
	# Sometimes the IP isn't owned by ARIN.
    #
    # we should likely be using the api, 
    # http://rest.db.ripe.net/search.json?query-string=83.141.55.10

    cloud_providers = ['amazon', 'rackspace', 'softlayer', 'microsoft', 'google']

                
    whois_output = subprocess.check_output(['whois', '-h', 'riswhois.ripe.net', ip_address])
    
    tokenized = whois_output.split('\n')

    org_handle = ''

    for token in tokenized:
        if token.startswith('descr:'):
            descr_tokens = token.split(':')
            # try to get an org handle by grabbing
            # the first chunk before the space
            org_handle = descr_tokens[1].strip()
            

    return org_handle

def get_response_code(url):
    
    try:
        r = requests.get(url, timeout=2)
        return r.status_code
    except requests.exceptions.Timeout:
        return "Request timeout"
    except:
        return 'Unable to get response code'


if __name__ == "__main__":

    augmented_rows = []

    # read CSV
    with open('partial-checked.csv', 'rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            url = row['URL in opinion']
            print "URL in opinion, %s" % url

            ip = get_ip_owner(url)
            print "IP for URL, %s" % ip

            ip_owner_org_handle = "Couldn't find IP owner's handle."
            ip_owner_org_name = "Couldn't find IP owner's name."


            if ip:
                data_from_arin = get_arin_data(ip)
                org_name_from_arin = data_from_arin[0]
                org_handle_from_arin = data_from_arin[1]

                if org_handle_from_arin and org_handle_from_arin != 'RIPE':
                    ip_owner_org_handle = org_handle_from_arin
                    ip_owner_org_name = org_name_from_arin
                else:
                    org_name_from_ripe = get_ripe_data(ip)
                    if org_name_from_ripe:
                        ip_owner_org_name = org_name_from_ripe

            print "IP owner handle, %s" % ip_owner_org_handle
            print "IP owner name, %s" % ip_owner_org_name

            http_status = get_response_code(url)
            print "HTTP status, %s\n" % http_status

            row['IP owner handle'] = ip_owner_org_handle
            row['IP owner name'] = ip_owner_org_name
            row['HTTP status code'] = http_status

            augmented_rows.append(row)

            time.sleep(.5)


    # Write our cleaned URLs to a new CSV
    with open('./results/deduped-and-cleaned-and-network-urls.csv', 'a') as csvfile:
        fieldnames = [u'URL in opinion', u'Timetravel URL', u'Rot', u'Archive', u'Archive Source', u'CL address', u'Case name', u'Date opinion was filed', u'Opinion download URL', u'Citation count', u'CL ID', u'Link rot', u'Ref rot', u'IP owner handle', u'IP owner name', u'HTTP status code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


        for row in augmented_rows:
            writer.writerow(row)
    