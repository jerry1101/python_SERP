"""
<url>
<loc>
http://www.totalwine.com/beer/ale/brown-ale/american-brown-ale/avery-ellies-brown-ale/p/99771126?s=216&igrules=true&tab=3
</loc>
<lastmod>2017-04-18</lastmod>
<changefreq>daily</changefreq>
<priority>0.8</priority>
<image:image>
<image:loc>
http://www.totalwine.com/media/sys_master/twmmedia/h5a/h3a/8808057438238.png
</image:loc>
<image:title>Avery Ellie's Brown Ale</image:title>
</image:image>
</url>
"""

from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
#from lxml.etree.ElementTree import Element, SubElement, Comment, tostring
from bs4 import BeautifulSoup
#from lxml import etree as ET


def generate_url_node(brand,link,image_link,last_mod,change_freq,priority_):
    url = Element('url')

    loc = Element('loc')
    loc.text = link

    lastmod = Element('lastmod')
    lastmod.text= last_mod
    changefreq = Element('changefreq')
    changefreq.text = change_freq
    priority = Element('priority')
    priority.text = priority_
    image_image =Element('image:image')
    image_loc = Element('image:loc')
    image_loc.text = image_link
    image_image.append(image_loc)
    image_title = Element('image:title')
    image_title.text = brand
    image_image.append(image_title)
    url.append(loc)
    url.append(lastmod)
    url.append(changefreq)
    url.append(priority)
    url.append(image_image)

    return url


def main():
    last_mod = '2018-02-20'
    change_freq = 'daily'
    priority_ = '0.8'
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
    urlset.set('xsi:schemaLocation',
               'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')

    lines = open('input.txt',encoding="utf8").read().split("\n")

    print(lines)
    # tempv = line.split(' ')
    iterlines = iter(lines)
    next(iterlines)
    for line in iterlines:
        id, title, brand, link, price, description, image_link, gtin, availability, condition, product_type, product_category, item_group_id, custom_label_0, custom_label_1, custom_label_2 \
            = line.split('\t')
        #print('brand :' + brand)
        #print('link :' + link)
        #print('image_link :' + image_link)

        urlset.append(generate_url_node(title,link,image_link,last_mod,change_freq,priority_))

    #bs = BeautifulSoup(ET.tostring(urlset).decode(), "xml")

    #print(bs.prettify())
    #tree = ET.ElementTree(urlset)
    #tree.write('output.xml', pretty_print=True, xml_declaration=True)

    text_file = open("Output1.xml", "w")

    text_file.write(ET.tostring(urlset).decode())

    text_file.close()



if __name__ == '__main__':
    main()

