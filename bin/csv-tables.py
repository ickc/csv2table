#!/usr/bin/env python3

"""
Panflute filter to parse CSV in fenced YAML code blocks
e.g.

```markdown
~~~csv
title: "*Great* Title"
has-header: False
width: 0.25, 0.25, 0.25, 0.25
alignment: AlignLeft, AlignRight, AlignCenter, AlignDefault
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
        reader = csv.reader(f)
        body = []
        for row in reader:
            cells = [panflute.TableCell(*panflute.convert_text(x)) for x in row]
            body.append(panflute.TableRow(*cells))
        # get no of columns for header
        f.seek(0)
        noOfColumn = len(list(reader)[0])
    # read YAML metadata
    try:
        caption = options.get('title')
        width = options.get('width')
        alignment = options.get('alignment')
        has_header = options.get('has-header',True)
    except AttributeError:
        caption = None
        width = None
        alignment = None
        has_header = True
    # get caption
    if caption != None:
        caption = panflute.convert_text(caption)[0].content
    # get width
    if width != None:
        width = [float(x) for x in width.split(",")]
    # get alignment
    if alignment != None:
        alignment = [x.strip() for x in alignment.split(",")]
    # finalize table according to metadata
    header = body.pop(0) if has_header else panflute.TableRow(*[panflute.TableCell() for i in range(noOfColumn)])
    table = panflute.Table(*body, header=header, caption=caption, width=width, alignment=alignment)
    return table

# We'll only run this for CodeBlock elements of class 'csv'
if __name__ == '__main__':
    panflute.toJSONFilter(panflute.yaml_filter, tag='csv', function=fenced_csv)
