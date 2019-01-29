from lxml import etree
from sickle.utils import xml_to_dict


def import_string(xml_data):
    tree = etree.fromstring(xml_data)

    for element in tree.iter():
        if element.tag == '{http://www.openarchives.org/OAI/2.0/}record':
            assert element[0].tag == '{http://www.openarchives.org/OAI/2.0/}metadata'
            assert element[0][0].tag == '{http://www.openarchives.org/OAI/2.0/oai_dc/}dc'
            metadata = xml_to_dict(element[0][0], strip_ns=True)


SAMPLE_DATA = """<?xml version="1.0" standalone="no"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
  <ListRecords>
    <record>
      <metadata>
        <oai_dc:dc>
          <dc:title>Bibliothèque et Archives nationales du Québec (BAnQ)</dc:title>
          <dc:identifier />
          <dc:AccrualPeriodicity />
          <dc:description>Site web du Québec collecté par BAnQ</dc:description>
          <dc:language>FR</dc:language>
          <dc:subject>Bibliothèques, Archives, Gouvernemental</dc:subject>
          <dc:contributor>Bibliothèque at Archives nationales du Québec</dc:contributor>
          <dc:rights>Publicly available</dc:rights>
          <dc:date>Captured 6 times between 2018-08-28 and 2018-10-19</dc:date>
          <dc:format>nb:6, size:204Mb</dc:format>
        </oai_dc:dc>
      </metadata>
    </record>
    <record>
      <metadata>
        <oai_dc:dc>
          <dc:title>Directeur général des élections du Québec (DGE)</dc:title>
          <dc:identifier>http://lvldif0a:8080/wayback/*/https://donnees.electionsmunicipales.quebec/resultats/resultats.html</dc:identifier>
          <dc:AccrualPeriodicity />
          <dc:description>Site web du Québec collecté par BAnQ</dc:description>
          <dc:language>FR</dc:language>
          <dc:subject>Sujet 1, Gouvernemental, Élection provinciale 2014, Élection provinciale 2012, Élection
            municipale 2017</dc:subject>
          <dc:contributor>Bibliothèque at Archives nationales du Québec</dc:contributor>
          <dc:rights>Publicly available</dc:rights>
          <dc:date>Captured 8 times between 2018-09-05 and 2018-10-19</dc:date>
          <dc:format>nb:13, size:6507Mb</dc:format>
        </oai_dc:dc>
      </metadata>
    </record>
    <record>
      <metadata>
        <oai_dc:dc>
          <dc:title>Organisme de test #1000 &lt;a href='http://news.google.fr' target='_new'&gt;Test&lt;/a&gt;</dc:title>
          <dc:identifier>http://lvldif0a:8080/wayback/*/http://test.org</dc:identifier>
          <dc:AccrualPeriodicity>Monthly, cron:0 0 8 5,6 * *</dc:AccrualPeriodicity>
          <dc:description>Site web du Québec collecté par BAnQ</dc:description>
          <dc:language>FR</dc:language>
          <dc:subject>Sujet 1</dc:subject>
          <dc:contributor>Bibliothèque at Archives nationales du Québec</dc:contributor>
          <dc:rights>Publicly available</dc:rights>
          <dc:date>Captured 8 times between 2018-03-05 and 2018-06-07</dc:date>
          <dc:format>nb:8, size:8Mb</dc:format>
        </oai_dc:dc>
      </metadata>
    </record>
  </ListRecords>
</OAI-PMH>
"""

if __name__ == "__main__":
    import_string(SAMPLE_DATA)
