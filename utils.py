from typing import Dict

from calculations import calculate_square_meters


def get_current_saw_number(user_id: str, block_number: str, user_data: dict):
    if user_id in user_data:
        current_saw_number = user_data[user_id]['current_saw_number']
        if current_saw_number:
            found_saw = user_data[user_id]['available_saws'][current_saw_number]
            if found_saw:
                if block_number in found_saw['blocks_decommissioned']:
                    return current_saw_number
    return False


def create_slabs(block_number: str, start: int, end: int, width: int, length: int, thickness: int) -> Dict:
    new_slabs: dict = {}
    for i in range(start, end):
        square_meters = calculate_square_meters(width_mm=width, length_mm=length)
        new_slabs[f"{block_number}-{i}"] = {
            "width": width,
            "length": length,
            "thickness": thickness,
            "square_meters": square_meters
        }
    return new_slabs


# def process_slab_number(message):
#     user_id: str = str(message.split()[0])
#     split_message: str = message.split()
#     block_number = split_message[1]
#     slab_number: str = split_message[2]
#     slab_width: int = int(split_message[3])
#     slab_length: int = int(split_message[4])
#     slab_thickness: int = int(split_message[5])
#     if not block_number or not slab_number or not slab_width or not slab_length or not slab_thickness:
#         print(user_id,
#               f"block: {block_number}, #: {slab_number}, w: {slab_width}, l: {slab_length}, th: {slab_thickness}")
#     else:
#         print(user_id,
#               f"block:OK {block_number}, #: {slab_number}, w: {slab_width}, l: {slab_length}, th: {slab_thickness}")
#
#
# process_slab_number("/slab 12 1-4 650 1200 50")
