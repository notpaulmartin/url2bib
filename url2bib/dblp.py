import re
import requests
import urllib.parse
import xml.etree.ElementTree as ET


def get_dblp_bibtexs(paper_title):
    encoded_search_term = urllib.parse.quote(paper_title)
    url = f'https://dblp.org/search/publ/api?q={encoded_search_term}'
    res = requests.get(url)
    assert res.ok

    xml_root = ET.fromstring(res.text)
    hits = xml_root.findall('.//hit')
    bibtexs = []
    for hit in hits:
        dblp_url = hit.find('.//url').text
        dblp_title = hit.find('.//title').text
        # Check if the normalised paper title matches
        if re.sub(r'[^\w ]', '', dblp_title).lower() != re.sub(r'[^\w ]', '', paper_title).lower():
            print(f'Discarding false hit: {dblp_title}')
            continue
        try:
            # Get the bibtex
            res = requests.get(f'{dblp_url}.bib')
            bibtexs.append(res.text)
        except:
            print(f'couldn\'t get bib for {dblp_url}')

    return bibtexs
