#!/usr/bin/python
from SOAPpy import WSDL
import re
import sys

def get_Records(name, offset_number):
	a = wsdlObjectWoRMS.getAphiaRecords(name, like='true', fuzzy='true', marine_only='false', offset=offset_number)
	return(a)

def process_worms_output(records):
    for b in records:
            record = str(b)
            t_family = re.compile("family': '[A-Z][a-z]+idae")
            m_family = t_family.search(record)
            if m_family:
                family = m_family.group().replace("family': '","")
                t_name = re.compile("scientificname': '[A-Z][a-z]+[ a-z]*")
                m_name = t_name.search(record)
                if m_name:
                   name = m_name.group().replace("scientificname': '","")
                   t_authority = re.compile("authority': '[\(\)A-Za-z ]+")
                   m_authority = t_authority.search(record)
                   if m_authority:
                       authority = m_authority.group().replace("authority': '","")
                       t_valid = re.compile("valid_name': '[\(\)A-Za-z ]+")
                       m_valid = t_valid.search(record)
                       if m_valid:
                           valid = m_valid.group().replace("valid_name': '","")
                           print '\n', name, authority
                           print 'Accepted name:', valid
                           print family
                       else:
                           print '\n', name, authority
                           print 'Accepted name: None'
                           print family

def get_all_worms_records(taxon_name):
    start = 1
    max_capacity = 50
    records = []
    print 'get_all_worms_records: fetching records', start, 'to', max_capacity, 'for taxon', taxon_name
    a = get_Records(str(taxon_name), start)
    if not a == None:
        for i in a:
            records.append(i)
        while len(records) == max_capacity:
            start = start + 50
            max_capacity = max_capacity + 50
            print 'get_all_worms_records: fetching records', start, 'to', max_capacity, 'for taxon', taxon_name
            b = get_Records(str(taxon_name), start)
            if not b == None:
                for i in b:
                    records.append(i)
        print 'get_all_worms_records: returning', len(records), 'records for taxon', taxon_name
        process_worms_output(records)

wsdlObjectWoRMS = WSDL.Proxy('http://www.marinespecies.org/aphia.php?p=soap&wsdl=1')

if len(sys.argv) == 1:
    print '  USAGE: ./worms.py taxon_name1 taxon_name2 ... taxon_nameN'
    print '  EXAMPLE: ./worms.py Mytilus\ edulis Tellinidae'
    print '  ERROR: Enter one or more taxon names'

target_names = sys.argv[1:]
for a in target_names:
    get_all_worms_records(a)
    print '\n'