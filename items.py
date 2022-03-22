import datapack_tools.data_types as dt
import datapack_tools.format as fm
from datapack_tools.scopes import *

class Item(dict):
   def __init__(self, item_id):
      dict.__init__(self)
      with Scope(self):
         id(item_id)

# Optional argument type specifies a type function such as data_types.short
# If no value is specified a type will be automatically determined based on the python type
def custom(key, value, type=None):
   with RelativeScope("tag."):
      if type is None:
         Tag(str(key), dt.auto(value))
      else:
         tag(str(key), type(value))

def id(id):
   Tag("id", dt.string(f"minecraft:{id}"))

def name(name):
   with RelativeScope("tag.display."):
      Tag("Name", fm.parse_text(name))

def count(count):
   Tag("Count", dt.byte(count))

def unbreakable():
   with RelativeScope("tag"):
      Tag("Unbreakable", dt.TRUE)

def hide_all_flags():
   hide_flags(True, True, True, True, True, True, True)

def hide_flags(enchantments=False,
               modifiers=False,
               unbreakable=False,
               can_destroy=False,
               can_place_on=False,
               hide_others=False,
               dyed=False):
   flags = (
      (1 << 0) * int(enchantments) +
      (1 << 1) * int(modifiers) +
      (1 << 2) * int(unbreakable) +
      (1 << 3) * int(can_destroy) +
      (1 << 4) * int(can_place_on) +
      (1 << 5) * int(hide_others) +
      (1 << 6) * int(dyed)
   )
   with RelativeScope("tag"):
      Tag("HideFlags", dt.int(flags))

def lore(lore):
   with RelativeScope("tag.display.Lore["):
      ListItem(fm.parse_text(lore))

def fireworks_flight(flight):
   with RelativeScope("tag.Fireworks."):
      Tag("Flight", dt.int(flight))

def fireworks_explosion(explosion_type, colors, fade_colors, trail=False, flicker=False):
   with RelativeScope("tag.Fireworks.Explosions[]."):
      Tag("Type", explosion_type)
      if trail:
         Tag("Trail", dt.int(1))
      if flicker:
         Tag("Flicker", dt.int(1))
      Tag("FadeColors", dt.int_list(fm.parse_color(color) for color in fade_colors))
      Tag("Colors", dt.int_list(fm.parse_color(color) for color in colors))

def enchantment_glint():
   with RelativeScope("tag.Enchantments[]"):
      ListItem({})

def enchantment(id, level=1):
   with RelativeScope("tag.Enchantments[]."):
      Tag("id", dt.string(f"minecraft:{id}"))
      Tag("lvl", dt.short(level))

def attribute(id, level, *, operation=0, slot=None):
   with RelativeScope("tag.AttributeModifiers[]."):
      Tag("AttributeName", dt.string(f"generic.{id}"))
      Tag("Name", dt.string(f"generic.{id}"))
      Tag("Amount", level)
      Tag("Operation", dt.int(operation))
      Tag("UUID", dt.uuid())
      if (slot is not None):
         Tag("Slot", slot)

def potion_effect(id, level, duration):
   with RelativeScope("tag.CustomPotionEffects[]."):
      Tag("Id", fm.parse_effect(id))
      Tag("Amplifier", dt.byte(level))
      Tag("Duration", dt.int(duration))
      Tag("ShowParticles", dt.FALSE)

def potion_type(potion_type):
   with RelativeScope("tag."):
      Tag("Potion", dt.string(f"minecraft:{potion_type}"))

def potion_color(color):
   with RelativeScope("tag."):
      Tag("CustomPotionColor", fm.parse_color(color))

def can_destroy(block):
   with RelativeScope("tag.CanDestroy["):
      ListItem(dt.string(f"minecraft:{block}"))

def can_place_on(block):
   with RelativeScope("tag.CanPlaceOn["):
      ListItem(dt.string(f"minecraft:{block}"))

def spawn_egg_mob(mob):
   with RelativeScope("tag."):
      with Tag("EntityTag", mob["tag"]):
         Tag("id", mob["id"])

def armor_color(color):
   with RelativeScope("tag.display."):
      Tag("color", fm.parse_color(color))

def shield_base_color(color_id):
   with RelativeScope("tag.BlockEntityTag."):
      Tag("Base", color_id)

def shield_pattern(pattern_id, color_id):
   with RelativeScope("tag.BlockEntityTag.Patterns["):
      with ListItem({}):
         Tag("Pattern", pattern_id)
         Tag("Color", color_id)

def book_page(text):
   with RelativeScope("tag.pages["):
      ListItem(fm.parse_text(text))