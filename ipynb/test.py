#!/usr/bin/env python3
import panflute

def action(elem, doc):
    if isinstance(elem, panflute.CodeBlock):
        print(elem, "="*80)
    if isinstance(elem, panflute.Table):
        print(elem.header, "="*80)
        print(elem.content, "="*80)

if __name__ == '__main__':
    panflute.run_filter(action)