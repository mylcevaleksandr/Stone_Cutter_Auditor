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
            ["/slab", "<block number> <number-(s)> <length mm> <width mm> <thickness mm>"],
            ["/update slab", "<number> <width> <length> or <thickness> <value mm>"],
            ["/delete slab", "<number>"],
            ["/tech", "<block number> <length mm> <width mm>"],
            ["/update tech", "<id> <width> or <length> <value mm>"],
            ["/delete tech", "<id>"],
            ["/pass", "<block number> <length mm> <width mm> <thickness mm>"],
            ["/update pass", "<number(id)> <width> <length> or <thickness> <value mm>"],
            ["/delete pass", "<number(id)>"],
        ])
    return table


def no_data_found_message() -> str:
    return "No user data found. Enter /start to see a lict of available commands."


def select_saw_message() -> str:
    return "Please enter command: /saw <number> to select saw number first"


def empty_entry_message(key: str, saw_number: str) -> str:
    table = create_pretty_table(field_names=[key], rows=[["This entry is currently empty"]],
                                title=f"Saw #: {saw_number} selected")
    return table


def bad_value_entered(data: str) -> str:
    return f"The data you have entered: {data} is incorrect format. Please review and enter the command again or enter /start or /saw <number> to see all options"


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


def confirm_delete_message(entry_type: str, saw_number: str, entry_number: str, entry_value: str):
    return f"{entry_type} number; {entry_number} with a value of {entry_value} m3 will be deleted from saw number {saw_number}. Type /yes to delete or /no to keep it."


def entry_updated_message(entry_type: str, key: str, new_value: str) -> str:
    return f"{entry_type} {key} updated with new value {new_value}."


def slabs_added_message(saw_number: str):
    return f"Added slabs to saw number: {saw_number}. Enter /saw {saw_number} to see all data stored for this saw."


def tech_cuts_added_message(saw_number: str):
    return f"Added slabs to saw number: {saw_number}. Enter /saw {saw_number} to see all data stored for this saw."


def entry_already_exists_message(entry_number: str, entry_value: str, saw_number: str) -> str:
    return f"Entry: {entry_number} with a value of: {entry_value}. Already exists in data of saw number: {saw_number}. Enter: /start or: /saw {saw_number} to see a list of all available commands on creating, updating, or deleting."


def new_slabs_message(key, value, saw_number) -> str:
    title = key
    field_names = ["number", "length", "width", "thick", "m2"]
    rows = []
    for slab_number, slab_data in value.items():
        rows.append(
            [slab_number, str(slab_data["length"]), str(slab_data["width"]), str(slab_data["thickness"]),
             str(slab_data["square_meters"])])

    table = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}",
                                column_widths=(15, 15, 15, 15, 15))
    return table


def tech_cuts_message(key, value, saw_number) -> str:
    title = key
    field_names = ["block#", "id", "length", "width", "m2"]
    rows = []
    for block_id, block_data in value.items():
        for cut_id, cut_data in block_data.items():
            rows.append([
                block_id,
                cut_id,
                str(cut_data.get("length", "")),
                str(cut_data.get("width", "")),
                str(cut_data.get("total", ""))])

    table = create_pretty_table(field_names=field_names, rows=rows, title=f"Saw # {saw_number}, {title}",
                                column_widths=(15, 15, 15, 15, 15))
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
