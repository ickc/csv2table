#!/usr/bin/env python3
import panflute
import io
import csv
import yaml

def json2markdown(*json):
    """
    convert a panflute json into markdown
    """
    # this should work, probably panflute has a bug?
#     md = panflute.convert_text(json, input_format='json', output_format='markdown')
    # temporary solution: plain text instead
    md = ''.join([panflute.stringify(item, newlines=False) for item in json])
    return md

def get_table_options(elem):
    """
    parse the content of Table in json and returns a dictionary of options
    # get
    get_caption
    get_alignment
    get_width
    get_header
    get_content
    @todo
    """
    options = {}
    options['caption'] = elem.caption
    options['alignment'] = elem.alignment
    options['width'] = elem.width
    options['header'] = elem.header
    options['markdown'] = True
    return options

def parse_table_options(options):
    """
    parse the options:
    # trasnform (width do nothing?)
    caption2markdown
    alignment_list2string
    header_tobool                    @done
    """
    options['caption'] = json2markdown(panflute.Para(*options['caption']))
    # parse alignment
    parsed_alignment = []
    for alignment in options['alignment']:
        if alignment == "AlignLeft":
            parsed_alignment.append("L")
        elif alignment == "AlignCenter":
            parsed_alignment.append("C")
        elif alignment == "AlignRight":
            parsed_alignment.append("R")
        elif alignment == "AlignDefault":
            parsed_alignment.append("D")
    options['alignment'] = "".join(parsed_alignment)
    options['table-width'] = sum(options['width'])
    options['header'] = bool(panflute.stringify(options['header']))
    return

def get_table_body(options, elem):
    """
    from elem, get full table body including header row if any
    """
    table_body = elem.content
    if options['header']:
        table_body.insert(0, elem.header)
    return table_body

def Table2list(Table):
    """
    convert a pandoc table into a 2D list
    """
    return [[json2markdown(*cell.content) for cell in row.content] for row in Table]


def list2csv(table_list):
    with io.StringIO() as file:
        writer = csv.writer(file)
        writer.writerows(table_list)
        csv_table = file.getvalue()
    return csv_table

def options2yaml(options):
    return yaml.dump(options)

def action(elem, doc):
    """
    combine_header_content           @done
    Table2list                       @done
    # prepare code block
    toyaml                           @done
    tocsv                            @done
    """
    if isinstance(elem, panflute.Table):
        options = get_table_options(elem)
        parse_table_options(options)
        table_body = get_table_body(options, elem)
        table_list = Table2list(table_body)
        csv_table = list2csv(table_list)
        yaml_metadata = options2yaml(options)
        code_block = "---\n" + yaml_metadata + "---\n" + csv_table
        return panflute.CodeBlock(code_block, classes=["table"])
        # yaml.dump(data, stream=None)
    return

if __name__ == '__main__':
    panflute.run_filter(action)