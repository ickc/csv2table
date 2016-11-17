#!/usr/bin/env python3

"""
Panflute filter to parse CSV in fenced YAML code blocks

5 metadata keys are recognized:

-   caption: the caption of the table. If omitted, no caption will be inserted.
-   header: If true, has a header row. default: true
-   column-width: a list of relative width corresponding to the width of each columns.
    default: auto calculate from the length of line in a (potentially multiline) cell.
-   table-width: the relative width of the table (comparing to, say, \linewidth).
    default: 1.0
-   alignment: a string of characters among L,R,C,D, case-insensitive,
    corresponds to Left-aligned, Right-aligned, Center-aligned, Default-aligned respectively.
    e.g. LCRD for a table with 4 columns
    default: DDD...
-   markdown: If CSV table cell contains markdown syntax or not. default: True

When the metadata keys is invalid, the default will be used instead.

e.g.

```markdown
~~~csv
caption: "*Great* Title"
header: False
column-width:
  - 0.1
  - 0.2
  - 0.3
  - 0.4
alignment: LRC
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
    # read YAML metadata
    try:
        caption = options.get('caption')
        column_width = options.get('column-width')
        table_width = options.get('table-width',1.0)
        alignment = options.get('alignment')
        header = options.get('header',True)
        markdown = options.get('markdown',True)
    except AttributeError:
        caption = None
        column_width = None
        table_width = 1.0
        alignment = None
        header = True
        markdown = True
    # check if YAML is valid
    ## column_width set to 0 when negative, set to None when invalid
    try:
        column_width = [(float(x) if float(x) >= 0 else 0) for x in column_width]
    except (TypeError, ValueError):
        column_width = None
    ## table_width: set to 1.0 if invalid or not positive
    try:
        table_width = float(table_width) if float(table_width) > 0 else 1.0
    except (TypeError, ValueError):
        table_width = 1.0
    ## set header to True if invalid
    if not isinstance(header, bool):
        if str(header).lower() == "false":
            header = False
        else:
            header = True
    ## set markdown to True if invalid
    if not isinstance(markdown, bool):
        if str(markdown).lower() == "false":
            markdown = False
        else:
            markdown = True

    # read csv and convert to panflute table representation
    with io.StringIO(data) as f:
        raw_table_list = list(csv.reader(f))
    body = []
    for row in raw_table_list:
        if markdown:
            cells = [panflute.TableCell(*panflute.convert_text(x)) for x in row]
        else:
            cells = [panflute.TableCell(panflute.Plain(panflute.Str(x))) for x in row]
        body.append(panflute.TableRow(*cells))
    # get no of columns of the table
    number_of_columns = len(raw_table_list[0])

    # transform metadata
    ## convert caption from markdown
    if caption != None:
        caption = panflute.convert_text(str(caption))[0].content
    ## calculate column_width
    if column_width == None:
        column_width_abs = [max([max([len(line) for line in row[i].split("\n")]) for row in raw_table_list]) for i in range(number_of_columns)]
        column_width_tot = sum(column_width_abs)
        column_width = [column_width_abs[i]/column_width_tot*table_width for i in range(number_of_columns)]
    ## convert alignment string into pandoc format (AlignDefault, etc.)
    if alignment != None:
        alignment = str(alignment)
        parsed_alignment = []
        for i in range(number_of_columns):
            try:
                if alignment[i].lower() == "l":
                    parsed_alignment.append("AlignLeft")
                elif alignment[i].lower() == "c":
                    parsed_alignment.append("AlignCenter")
                elif alignment[i].lower() == "r":
                    parsed_alignment.append("AlignRight")
                else:
                    parsed_alignment.append("AlignDefault")
            except IndexError:
                for i in range(number_of_columns-len(parsed_alignment)):
                    parsed_alignment.append("AlignDefault")
        alignment = parsed_alignment

    # finalize table according to metadata
    header_row = body.pop(0) if header else None # panflute.TableRow(*[panflute.TableCell() for i in range(number_of_columns)]) # for panflute < 1.4.3
    table = panflute.Table(*body, header=header_row, caption=caption, width=column_width, alignment=alignment)
    return table

# We'll only run this for CodeBlock elements of class 'csv'
if __name__ == '__main__':
    panflute.toJSONFilter(panflute.yaml_filter, tag='csv', function=fenced_csv, strict_yaml=True)