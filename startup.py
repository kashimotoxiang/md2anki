import sys
from collections import namedtuple
import csv
import os
fields = ["Q:", "A:", "E:"]


def write_csv_dict(filename, content, fieldnames):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(content)


class Item():
    fieldname = None
    value = None

    def __init__(self):
        self.fieldname = ''
        self.value = []


def update_fields(item, item_dict):
    try:
        value_str = '\n'.join(item.value)
        value_str = value_str.strip()
        value_str = value_str.replace('\n', '<br>')
        item_dict.update({item.fieldname: value_str})
    except Exception as e:
        print(e)


def process_block(block):
    item_dict = {}
    item = Item()
    for line in block:
        if line in fields:
            # previous
            if len(item.value) != 0:
                update_fields(item, item_dict)
            item.fieldname = line
            item.value = []
        else:
            item.value.append(line)
    else:
        if len(item.value) != 0:
            update_fields(item, item_dict)

    return item_dict


def get_blocks(content):
    blocks = []
    buffer = []
    begin_flag = False
    for line in content:
        if line == '``````':
            # toggle
            begin_flag = False if begin_flag is True else True
        else:
            if begin_flag is True:
                buffer.append(line)
            else:
                if len(buffer) > 0:
                    blocks.append(buffer)
                    buffer = []
    return blocks


def main(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = [x.strip() for x in f.readlines()]

    blocks = get_blocks(content)

    insert_item = []
    for item in blocks:
        __insert_item = process_block(item)
        insert_item.append(__insert_item)
    savepath = os.path.splitext(filepath)[0]+'-output.csv'
    write_csv_dict(filename=savepath, content=insert_item, fieldnames=fields)


if __name__ == '__main__':
    main(sys.argv[1])
