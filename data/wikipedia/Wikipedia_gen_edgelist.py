# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import xml.etree.ElementTree as etree

# <codecell>

xmlpath="./wikipedia.xml"

# <markdowncell>

# for event, elem in etree.iterparse(xmlpath):
#     if elem.tag=='page':
#         txt=elem.find('./revision/text')
#         if len(txt.text)>10:
#             break
#     
#             

# <codecell>

pagedict={}

# <codecell>

with open("enwiki_title_id.dat",'w') as f:
    for event, elem in etree.iterparse(xmlpath):
        if elem.tag=='page':
            if elem.find('ns').text=='0':
                pagedict[elem.find('title').text]=int(elem.find('id').text)
                print(elem.find('id').text,elem.find('title').text, sep='\t', file=f)

                red=elem.find('redirect')  #Some wikipedia pages have redirects
                if red is not None:
                    pagedict[red.attrib['title']]=int(elem.find('id').text)
                    print(elem.find('id').text,red.attrib['title'], sep='\t', file=f)
        

# <codecell>

def upper_firstchar(st):
    if len(st)<2:
        return st.upper()
    else:
        return st[0].upper()+st[1:]

with open("enwiki_edgelist.dat",'w') as g:
    for event, elem in etree.iterparse(xmlpath):
        if elem.tag=='page':
            if elem.find('ns').text=='0':
                pid=int(elem.find('id').text)
                ptxt=elem.find('./revision/text').text
                
                linklist=[pid]
                for link in re.findall(r"\[\[(.*?)\]\]", ptxt):
                    wptitle=link.split('|')[0]
                    canonical_title=upper_firstchar(wptitle)
                    try:
                        linklist.append(pagedict[canonical_title])
                    except KeyError:
                        pass
                print(' '.join(str(i) for i in linklist), file=g)
                
        

# <codecell>

  

