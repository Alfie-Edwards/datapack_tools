from datapack_tools.scopes import *

class Advancement(dict):
   def __init__(self):
      dict.__init__(self)

def parent(category):
   Tag("parent", category)

def name(name):
   with RelativeScope("display."):
      Tag("title", name)

def hidden():
   with RelativeScope("display."):
      Tag("hidden", "true")

def description(description):
   with RelativeScope("display."):
      Tag("description", description)

def icon_item(item_name):
   with RelativeScope("display.icon."):
      Tag("item", "minecraft:{}".format(item_name))

def frame(frame_type):
   with RelativeScope("display."):
      Tag("frame", frame_type)

def background_block(block):
   with RelativeScope("display."):
      Tag("background", "minecraft:textures/block/{}.png".format(block))

def criteria_impossible():
   with RelativeScope("criteria.imposible."):
      Tag("trigger", "minecraft:impossible")

def criteria_item(item):
   with RelativeScope("criteria.has_{}.".format(item_name)):
      Tag("trigger", "minecraft:inventory_changed")
      with Tag("conditions", {}):
         with Tag("items", []):
            with ListItem({}):
               Tag("item", item["id"])
               if "Count" in item:
                  Tag("count", item["Count"])
               if "tag" in item:
                  Tag("nbt", recursive_to_string(item["tag"]))


def criteria_location(x1, y1, z1, x2, y2, z2):
   with RelativeScope("criteria.in_bounds."):
      Tag("trigger", "minecraft:location")
      with Tag("conditions", {}):
         with Tag("position", {}):
            with Tag("x", {}):
               Tag("min", x1)
               Tag("max", x2)
            with Tag("y", {}):
               Tag("min", y1)
               Tag("max", y2)
            with Tag("z", {}):
               Tag("min", z1)
               Tag("max", z2)

def reward_recipe(item_name):
   with RelativeScope("rewards.recipes["):
      ListItem("minecraft:{}".format(item_name))

def reward_xp(xp):
   with RelativeScope("rewards."):
      Tag("experience", xp)

def reward_function(function):
   with RelativeScope("rewards."):
      Tag("function", function)

NULL_ADVANCEMENT = Advancement()
with Scope(NULL_ADVANCEMENT):
   criteria_impossible()
