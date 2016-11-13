#!/usr/bin/env python3

"""
Panflute filter to parse CSV in fenced YAML code blocks
"""

import io
import csv
import panflute as pf


def fenced_action(options, data, element, doc):
    # We'll only run this for CodeBlock elements of class 'csv'
    try:
        title = options.get('title')
        # get has_header
        has_header = options.get('has-header',True)
        width = options.get('width')
        alignment = options.get('alignment')
    except AttributeError:
        width = None
        title = None
        has_header = True
        alignment = None

    # get title
    if title != None:
        title = pf.convert_text(title)[0].content
    # get width
    if width != None:
        width = [float(x) for x in width.split(",")]
    # get alignment
    if alignment != None:
        alignment = [x.strip() for x in alignment.split(",")]

    with io.StringIO(data) as f:
        reader = csv.reader(f)
        body = []
        for row in reader:
            cells = [pf.TableCell(*pf.convert_text(x)) for x in row]
            body.append(pf.TableRow(*cells))
        # get no of columns for header
        f.seek(0)
        noOfColumn = len(list(reader)[0])
    
    # Todo: When has_header = False, it should return a list of empty row
    header = body.pop(0) if has_header else pf.TableRow(*[pf.TableCell() for i in range(noOfColumn)])
    table = pf.Table(*body, header=header, caption=title, width=width, alignment=alignment)
    return table


if __name__ == '__main__':
    pf.toJSONFilter(pf.yaml_filter, tag='csv', function=fenced_action)