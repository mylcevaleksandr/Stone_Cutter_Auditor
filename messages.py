from typing import List

from prettytable import PrettyTable, HRuleStyle, VRuleStyle


# function to create pretty table
def create_pretty_table(field_names: List[str], rows: List[List:str],
                        title: str = "Welcome! These are all input options:", column_widths=(15, 27)):
    table = PrettyTable(hrules=HRuleStyle.ALL, vrules=VRuleStyle.ALL, header=True, header_style='upper')
    table.align = 'l'
    table.title = title
    table.field_names = field_names
    table.max_width = 0
    table.max_table_width = 42
    table.min_table_width = 42
    table._max_border_width = 1
    table._title_max_width = 40

    for idx, col in enumerate(table.field_names):
        table.align[col] = 'l'
        table.max_width[col] = column_widths[idx]

    table.add_rows(rows)

    return f'```\n{table}```'


def start_message() -> str:
    table = create_pretty_table(
        field_names=["Commands", "Input Options"],
        rows=[
            ["/start", "Start interaction with bot"],
            ["/saw", "<number>"],
            ["/block", "<number> <m3>"],
            ["/update block", "<number> <new m3>"],
            ["/delete block", "<number>"],
            ["/slab", "<number> <width mm> <height mm> <thickness mm>"],
            ["/update slab", "<number> <width> <height> or <thickness> <value mm>"],
            ["/delete slab", "<number>"],
            ["/tech", "<number> <width number> <height number>"],
            ["/update tech", "<id> <width> or <length> <value mm>"],
            ["/delete tech", "<id>"],
            ["/pass", "<number> <width mm> <height mm> <thickness mm>"],
            ["/update pass", "<number> <width> <height> or <thickness> <value mm>"],
            ["/delete pass", "<number>"],
        ])
    return table


def no_data_found_message() -> str:
    return "No user data found."


def select_saw_message() -> str:
    return "Please enter command: /saw <number> to select saw number first"


def empty_entry_message(key: str, saw_number: str) -> str:
    table = create_pretty_table(field_names=[key], rows=[["This entry is currently empty"]],
                                title=f"Saw #: {saw_number} selected")
    return table


def bad_value_entered(data: str) -> str:
    return (f"The data you have entered: {data} is incorrect format. Please review and enter the command again or "
            f"enter /start or /saw <number> to see all options")


def block_all_commands_message(saw_number: str = "") -> str:
    title = f"Saw # {saw_number}. " if saw_number else ""
    title += "All available block commands:"
    table = create_pretty_table(
        field_names=["commands", "input options"],
        rows=[
            ["/block", "<number>" "<m3>"],
            ["/update block", "<number> <new m3>"],
            ["/delete block", "<number>"],
            ["/saw <number>", "To see other commands"],
            ["/start", "To see other commands"]
        ],
        title=title
    )
    return table


def block_decommissioned_message(block_number: str, saw_number: str) -> str:
    table = f"Block number {block_number} saved for saw number {saw_number}."
    return table


def blocks_decommissioned_message(key, value, saw_number) -> str:
    unique_keys = ["number", "m3"]

    row_values = [[key, value] for key, value in value.items()]

    table = create_pretty_table(field_names=unique_keys, rows=row_values,
                                title=f"Saw # {saw_number}, {key}")
    return table


def confirm_block_update_message(block_number: str, block_value: str, new_block_value: str) -> str:
    return f"It seems like you're trying to make changes to existing block number; {block_number}. Current value is: {block_value} m3, new value will be: {new_block_value} m3. Type /yes to keep the changes or /no to discard them."


def confirm_block_delete_message(saw_number: str, block_number: str, block_value: str):
    return f"Block number; {block_number} with a value of {block_value} m3 will be deleted from saw number {saw_number}. Type /yes to delete or /no to keep it."


def slabs_added_message():
    return "Added slabs to saw number:"


def entry_already_exists_message():
    return "Slab already exists"


def new_slabs_message(key, value, saw_number) -> str:
    title = key
    field_names = ["number", "w", "l", "t", "m2"]
    rows = []
    for slab_number, slab_data in value.items():
        rows.append(
            [slab_number, str(slab_data["width"]), str(slab_data["length"]), str(slab_data["thickness"]), str(slab_data["square_meters"])])

    table = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}", column_widths=(15,15,15,15,15))
    return table


def tech_cuts_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block #", "w", "l", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["square_meters"])])

    table = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return table


def new_blocks_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block #", "w", "l", "h", "m2"]
    rows = []
    for item in value:
        for key, value in item.items():
            rows.append(
                [key, str(value["width"]), str(value["length"]), str(value["height"]), str(value["square_meters"])])

    table = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}")
    return table
