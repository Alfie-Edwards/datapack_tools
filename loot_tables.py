from datapack_tools.scopes import *
from datapack_tools.format import recursive_to_string

class LootTable(dict):
   def __init__(self):
      dict.__init__(self)

def type(type_name):
   Tag("type", "minecraft:{}".format(type_name))

def rolls(rolls):
   with RelativeScope("pools[0]."):
      Tag("rolls", rolls)

def entry_item(item, weight, quality=None):
   with RelativeScope("pools[0].entries["):
      with ListItem({}):
         Tag("type", "minecraft:item")
         Tag("weight", weight)
         if quality is not None:
            Tag("quality", quality)
         Tag("name", item["id"][1:-1])
         with Tag("functions", []):
            if "Count" in item:
               with ListItem({}):
                  Tag("function", "set_count")
                  Tag("count", int(item["Count"][:-1]))
            if "tag" in item:
               with ListItem({}):
                  Tag("function", "set_nbt")
                  Tag("tag", recursive_to_string(item["tag"]))


