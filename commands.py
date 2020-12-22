from datapack_tools.format import recursive_to_string

def item_give(item):
   tags = recursive_to_string(item["tag"])
   id = item["id"].strip('"')
   return "give @s {}{}\n".format(id, tags)

def mob_summon(mob):
   tags = recursive_to_string(mob["tag"])
   id = mob["id"].strip('"')
   return "summon {} ~ ~ ~ {}\n".format(id, tags)

def inventory_set_block(inventory):
   inventory = recursive_to_string(inventory)
   return "data modify block ~ ~ ~ Items set value {}\n".format(inventory)
