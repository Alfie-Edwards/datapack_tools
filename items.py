import datapack_tools.data_types as dt
import datapack_tools.format as fm
from datapack_tools.scopes import *

class VanillaItem(dict):
   def __init__(self, id):
      dict.__init__(self)
      with Scope(self):
         Tag("id", '"minecraft:{}"'.format(id))

class Item(dict):
   def __init__(self, id):
      dict.__init__(self)
      with Scope(self):
         Tag("id", '"minecraft:{}"'.format(id))
         with RelativeScope("tag."):
            Tag("HideFlags", dt.int(63))
            Tag("Unbreakable", dt.TRUE)

def id(id):
   with RelativeScope("tag.display."):
      Tag("Name", fm.parse_text(name))

def name(name):
   with RelativeScope("tag.display."):
      Tag("Name", fm.parse_text(name))

def count(count):
   Tag("Count", dt.byte(count))

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

def enchantment(id, level=1):
   with RelativeScope("tag.Enchantments[]."):
      Tag("id", '"minecraft:{}"'.format(id))
      Tag("lvl", dt.short(level))

def attribute(id, level, *, operation=0, slot=None):
   with RelativeScope("tag.AttributeModifiers[]."):
      Tag("AttributeName", dt.string("generic.{}".format(id)))
      Tag("Name", dt.string("generic.{}".format(id)))
      Tag("Amount", level)
      Tag("Operation", dt.int(operation))
      Tag("UUID", dt.uuid())
      if (slot is not None):
         Tag("Slot", slot)

def potion_effect(id, level, duration):
   with RelativeScope("tag.CustomPotionEffects[]."):
      Tag("Id", dt.byte(id))
      Tag("Amplifier", dt.byte(level))
      Tag("Duration", dt.int(duration))
      Tag("ShowParticles", dt.FALSE)

def potion_type(potion_type):
   with RelativeScope("tag."):
      Tag("Potion", '"minecraft:{}"'.format(potion_type))

def potion_color(color):
   with RelativeScope("tag."):
      Tag("CustomPotionColor", fm.parse_color(color))

def can_destroy(block):
   with RelativeScope("tag.CanDestroy["):
      ListItem('"minecraft:{}"'.format(block))

def can_place_on(block):
   with RelativeScope("tag.CanPlaceOn["):
      ListItem('"minecraft:{}"'.format(block))

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