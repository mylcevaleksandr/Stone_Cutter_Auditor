from typing import List, OrderedDict

from prettytable import PrettyTable, HRuleStyle, VRuleStyle


# function to create pretty table
def create_pretty_table(field_names: List[str], rows: List[List:str],
                        title: str = "Welcome! These are all input options:"):
    table = PrettyTable(hrules=HRuleStyle.ALL, vrules=VRuleStyle.ALL, header=True, header_style='upper')
    table.align = 'l'
    table.title = title
    table.field_names = field_names
    table.add_rows(rows)

    return f'```\n{table}```'


def start_message() -> str:
    table_start = create_pretty_table(
        field_names=["Commands", "Input Options"],
        rows=[
            ["/start", "Start interaction with bot"],
            ["/saw", "/saw <number>"],
            ["/block", "/block, <number>, <cubic meters>"],
            ["/slab", "/slab, <number>, <width>, <height>, <thickness>"],
            ["/tech", "/tech, <block number>, <width>, <height>"]
        ])
    return table_start


def empty_entry_message(key: str, saw_number: str) -> str:
    message = create_pretty_table(field_names=[key], rows=[["This entry is currently empty"]],
                                  title=f"Saw #: {saw_number} selected")
    return message


def block_decommissioned_message(block_number: str, saw_number: str) -> str:
    message = f"Block number {block_number} saved for saw number {saw_number}."
    return message


def blocks_decommissioned_message(key, value, saw_number) -> str:
    unique_keys = ["number", "m3"]

    row_values = [[key, value] for key, value in value.items()]

    message = create_pretty_table(field_names=unique_keys, rows=row_values,
                                  title=f"Saw # {saw_number}, {key}")
    return message


def new_slabs_message(key, value, saw_number) -> str:
    title = key
    field_names = ["number", "w", "l", "t", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["thickness"]), str(value["square_meters"])])

    message = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return message


def tech_cuts_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block #", "w", "l", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["square_meters"])])

    message = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return message


def new_blocks_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block #", "w", "l", "h", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["height"]), str(value["square_meters"])])

    message = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return message
