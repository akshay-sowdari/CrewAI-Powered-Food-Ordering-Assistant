import pandas as pd

# def menu_reader():
#     df = pd.read_excel('./data/food_menu.xlsx')
#     return df.to_dict(orient='records')




import re
def parse_user_order(user_input: str):
    """
    Parse user's natural language order and extract items with quantities.
    Returns [{'item': 'Item Name', 'quantity': int}]
    """
    pattern = r'(?:(\d+)\s*x?\s*)?([a-zA-Z ]+?)(?:,|and|$)'
    matches = re.findall(pattern, user_input)

    order_list = []
    for qty, item in matches:
        item = item.strip().title()
        if not item:
            continue
        quantity = int(qty) if qty else 1
        order_list.append({"item": item, "quantity": quantity})

    # Merge duplicate items
    merged = {}
    for o in order_list:
        merged[o["item"]] = merged.get(o["item"], 0) + o["quantity"]

    return [{"item": k, "quantity": v} for k, v in merged.items()]



print(parse_user_order("I want 2 cold coffee and may be sandwich 1 "))

