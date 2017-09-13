from math import inf
from sickle import Sickle
from sys import stderr


AIT_COLLECTIONS = "https://archive-it.org/oai"
def ait_partner_records(organization_id):
    return "https://archive-it.org/oai/organizations/{:04d}".format(organization_id)


def eprint(*args, **kwargs):
    print(*args, file=stderr, **kwargs)

def get_ait_organization_id(record):
    if len(record.header.setSpecs) == 1 and record.header.setSpecs[0][:13] == 'organization:':
        return int(record.header.setSpecs[0][13:])
    else:
        eprint(record.header.identifier, record.header.setSpecs)
        raise ValueError("Can't find organization from setspecs.")

def get_ait_collection_id(record):
    if record.header.identifier[:34] ==  'http://archive-it.org/collections/':
        return int(record.header.identifier[34:])
    else:
        eprint(record.header.identifier)
        raise ValueError("Can't parse collection number.")

def collection_id_range(records):
    oids = [ get_ait_collection_id(record) for record in records ]
    if len(oids) > 1:
        return (min(oids), max(oids))
    else:   
        eprint(oids)
        raise ValueError("Can't get collection id number range.")

# collection_list_query = "https://archive-it.org/oai?verb=ListRecords&metadataPrefix=oai_dc"
# sample_collection_query = "https://archive-it.org/oai/organizations/1036?verb=ListRecords&metadataPrefix=oai_dc&resumptionToken=0,447"

ait = Sickle(AIT_COLLECTIONS)
records = ait.ListRecords(metadataPrefix='oai_dc')
record = records.next()



    # for record in ait.ListRecords(metadataPrefix='oai_dc'):
    #     print("{}\t{}".format(get_ait_organization_id(record), get_ait_collection_id(record)))
