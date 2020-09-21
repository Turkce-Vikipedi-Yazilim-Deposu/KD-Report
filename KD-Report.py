#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pywikibot
from pywikibot import pagegenerators
import pywikibot.data.api as api
import pprint #Only for structuring the JSON file

def create_table_string(data, highlight=(True, False, False, False),  table_class='wikitable', style=''):
    """
    Takes a list and returns a wikitable.

    @param data: The list that is converted to a wikitable.
    @type data: List (Nested)
    @param highlight: Tuple of rows and columns that should be highlighted.
                      (first row, last row, left column, right column)
    @type highlight: Tuple
    @param table_class: A string containing the class description.
                        See wikitable help.
    @type table_class: String
    @param style: A string containing the style description.
                  See wikitable help.
    @type style: String
    """
    last_row = len(data) - 1
    last_cell = len(data[0]) - 1

    table = '{{| class="{}" style="{}"\n'.format(table_class, style)
    for key, row in enumerate(data):
        if key == 0 and highlight[0] or key == last_row and highlight[1]:
            row_string = '|-\n! ' + '\n! '.join(cell for cell in row)
        else:
            row_string = '|-'
            cells = ''
            for ckey, cell in enumerate(row):
                if ckey == 0 and highlight[2]:
                    cells += '\n! ' + cell
                elif ckey == last_cell and highlight[3]:
                    cells += '\n! ' + cell
                else:
                    cells += '\n| ' + cell
            row_string += cells

        table += row_string + '\n'
    table += '|}'
    return table

#def pageViewNumber(site,item):
#    req = api.Request(site=site, parameters={'action': 'query', 'titles': item, 'prop': 'pageviews'})
#    pprint.pprint(req.submit()['query']['pages'][str(item.pageid)]['pageviews'])

def main():

    site = pywikibot.Site('tr', 'wikipedia')

    logPage = pywikibot.Page(site, 'User:'+site.username()+'/Log/KD Raporu')

    cat = pywikibot.Category(site, 'Kayda değerliği belirsiz maddeler')
    allPages = pagegenerators.CategorizedPageGenerator(cat, recurse=True,namespaces=0)

    report = [{"#"},{'Madde'},{'Tartışma'}]

    for index,page in enumerate(allPages):
        talkPage = page.toggleTalkPage()
        item = pywikibot.ItemPage.fromPage(page)
        item.get()

        #for link in item.sitelinks:
        #    print(link)

        #talkPageSize - şablonlardan arındırılmış sayfa uzunluğu
        #WikidataNumber - wikidata sayfası varsa numarası
        #Diğer wiki sitelinks
        #KD şablonunu ekleyen kişi
        #KD eklenme tarihi
        #KD eklenirken yazılan açıklama
        #sayfanın 2020 yılında okunma sayısı

        report.append(["{0:04d}".format(index), "[[:{}]]".format(page._link.title), '[[:Talk:{}]]'.format(page._link.title)])


    wikitable=create_table_string(report)

    logPage.text=wikitable
    logPage.save()

if __name__ == '__main__':
    main()
