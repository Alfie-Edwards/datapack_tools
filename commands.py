from datapack_tools.format import recursive_to_string

def item_give(item):
   tags = recursive_to_string(item["tag"])
   id = item["id"].strip('"')
   return f"give @s {id}{tags}\n"

def mob_summon(mob):
   tags = recursive_to_string(mob["tag"])
   id = mob["id"].strip('"')
   return f"summon {id} ~ ~ ~ {tags}\n"

def inventory_set_block(inventory):
   inventory = recursive_to_string(inventory)
   return f"data modify block ~ ~ ~ Items set value {inventory}\n"
