#!/usr/bin/env python3

"""
Panflute filter to parse CSV in fenced YAML code blocks
e.g.

```markdown
~~~csv
title: "*Great* Title"
has-header: False
column-width:
  - 0.1
  - 0.2
  - 0.3
  - 0.4
alignment: [AlignLeft, AlignRight, AlignCenter, AlignDefault]
---
**_Fruit_**,~~Price~~,_Number_,`Advantages`
*Bananas~1~*,$1.34,12~units~,"Benefits of eating bananas 
(**Note the appropriately
rendered block markdown**):    

- _built-in wrapper_        
- ~~**bright color**~~

"
*Oranges~2~*,$2.10,5^10^~units~,"Benefits of eating oranges:

- **cures** scurvy
- `tasty`"
~~~
```
"""

import io
import csv
import panflute

def fenced_csv(options, data, element, doc):
    # read csv and convert to panflute table representation
    with io.StringIO(data) as f:
        reader = list(csv.reader(f))
        body = []
        for row in reader:
            cells = [panflute.TableCell(*panflute.convert_text(x)) for x in row]
            body.append(panflute.TableRow(*cells))
        # get no of columns for header
        noOfColumn = len(reader[0])
    # read YAML metadata
    try:
        caption = options.get('title')
        column_width = options.get('column-width')
        table_width = options.get('table-width',1.0)
        alignment = options.get('alignment')
        has_header = options.get('has-header',True)
    except AttributeError:
        caption = None
        column_width = None
        table_width = 1.0
        alignment = None
        has_header = True
    # get caption
    if caption != None:
        caption = panflute.convert_text(caption)[0].content
    # get column_width
    if column_width == None:
        column_width_abs = [max([max([len(line) for line in row[i].split("\n")]) for row in list(reader)]) for i in range(noOfColumn)]
        column_width_tot = sum(column_width_abs)
        column_width = [column_width_abs[i]/column_width_tot*float(table_width) for i in range(noOfColumn)]
    # get alignment
    if alignment != None:
        parsed_alignment = []
        for i in range(noOfColumn):
            if alignment[i].lower() == "l":
                parsed_alignment.append("AlignLeft")
            elif alignment[i].lower() == "c":
                parsed_alignment.append("AlignCenter")
            elif alignment[i].lower() == "r":
                parsed_alignment.append("AlignRight")
            else:
                parsed_alignment.append("AlignDefault")
        alignment = parsed_alignment
    # finalize table according to metadata
    header = body.pop(0) if has_header else None # panflute.TableRow(*[panflute.TableCell() for i in range(noOfColumn)]) # for panflute < 1.4.3
    table = panflute.Table(*body, header=header, caption=caption, width=column_width, alignment=alignment)
    return table

# We'll only run this for CodeBlock elements of class 'csv'
if __name__ == '__main__':
    panflute.toJSONFilter(panflute.yaml_filter, tag='csv', function=fenced_csv)