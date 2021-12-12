from copy import deepcopy

import datapack_tools.items as items
from datapack_tools.items import Item
import datapack_tools.data_types as dt
import datapack_tools.format as fm
from datapack_tools.scopes import *

class Mob(dict):
   def __init__(self, mob_id):
      dict.__init__(self)
      with Scope(self):
         id(mob_id)

def id(id):
   Tag("id", dt.string(f"minecraft:{id}"))

# If using hide=True, you will need to clean up the marker armor stands when
# the mob dies. This can be done by running the following command:
# tp @e[tag=name_hider] ~ -1000 ~
def name(name, always_show=False, hide=False):
   with RelativeScope("tag."):
      Tag("CustomName", fm.parse_text(name))
      Tag("CustomNameVisible", dt.bool(always_show))
   if hide:
      name_hider = Mob("armor_stand")
      with Scope(name_hider):
         tag("name_hider")
         armor_stand_invisible()
         armor_stand_marker()
      passenger(name_hider)

def passenger(passenger):
   with RelativeScope("tag.Passengers[]."):
      for key in passenger:
         # Passengers don't have their tags under the "tag" top-level.
         if key == "tag":
            for nested_key in passenger["tag"]:
               Tag(nested_key, deepcopy(passenger["tag"][nested_key]))
         else:
            Tag(key, deepcopy(passenger[key]))

def age(age):
   with RelativeScope("tag."):
      Tag("Age", dt.int(age))

def holding(item, *, drop=False):
   with RelativeScope("tag.HandDropChances["):
      ListItem(dt.float(2 if drop else 0), index=0)
   with RelativeScope("tag.HandItems["):
      ListItem(item, index=0)

def holding_nothing():
   with RelativeScope("tag.HandItems["):
      ListItem({}, index=0)
      ListItem({}, index=1)

def offhand(item, *, drop=False):
   with RelativeScope("tag.HandDropChances["):
      ListItem(dt.float(2 if drop else 0), index=1, pad=dt.float(0))
   with RelativeScope("tag.HandItems["):
      ListItem(item, index=1, pad={})

def effect(id, level, duration=2147483647):
   with RelativeScope("tag.ActiveEffects[]."):
      Tag("Id", fm.parse_effect(id))
      Tag("Amplifier", dt.byte(level))
      Tag("Duration", dt.int(duration))
      Tag("ShowParticles", dt.FALSE)

def dialogue(text):
   tag("Dialogue")
   with RelativeScope("tag.HandDropChances["):
      ListItem(dt.float(0), index=1, pad=dt.float(0))
   with RelativeScope("tag.HandItems["):
      with ListItem(Item("barrier"), index=1, pad={}):
         items.count(1)
         with RelativeScope("tag."):
            Tag("dialogue", fm.parse_text(text))

def attribute(id, value):
   with RelativeScope("tag.Attributes[]."):
      Tag("Name", f"generic.{id}")
      Tag("Base", value)

def tag(tag):
   with RelativeScope("tag.Tags["):
      ListItem(tag)

def no_ai():
   with RelativeScope("tag."):
      Tag("NoAI", dt.TRUE)

def no_gravity():
   with RelativeScope("tag."):
      Tag("NoGravity", dt.TRUE)

def invulnerable():
   with RelativeScope("tag."):
      Tag("Invulnerable", dt.TRUE)

def silent():
   with RelativeScope("tag."):
      Tag("Silent", dt.TRUE)

def armor_stand_invisible():
   with RelativeScope("tag."):
      Tag("Invisible", dt.TRUE)

def armor_stand_marker():
   with RelativeScope("tag."):
      Tag("Marker", dt.TRUE)

def helmet(item, *, drop=False):
   with RelativeScope("tag.ArmorDropChances["):
      ListItem(dt.float(2 if drop else 0), index=3, pad=dt.float(0))
   with RelativeScope("tag.ArmorItems["):
      ListItem(item, index=3, pad={})

def chestplate(item, *, drop=False):
   with RelativeScope("tag.ArmorDropChances["):
      ListItem(dt.float(2 if drop else 0), index=2, pad=dt.float(0))
   with RelativeScope("tag.ArmorItems["):
      ListItem(item, index=2, pad={})

def leggings(item, *, drop=False):
   with RelativeScope("tag.ArmorDropChances["):
      ListItem(dt.float(2 if drop else 0), index=1, pad=dt.float(0))
   with RelativeScope("tag.ArmorItems["):
      ListItem(item, index=1, pad={})

def boots(item, *, drop=False):
   with RelativeScope("tag.ArmorDropChances["):
      ListItem(dt.float(2 if drop else 0), index=0)
   with RelativeScope("tag.ArmorItems["):
      ListItem(item, index=0)

def villager_type(biome=None, profession=None):
   with RelativeScope("tag.VillagerData."):
      Tag("level", dt.int(99))
      if profession is not None:
         Tag("profession", profession)
      if biome is not None:
         Tag("type", biome)

def villager_trade(sell, buy, buy2=None, *, hide_buy_lore=True):
   if hide_buy_lore:
      if "tag" in buy and "display" in buy["tag"] and "Lore" in buy["tag"]["display"]:
         buy["tag"]["display"].pop("Lore")
      if buy2 is not None and "tag" in buy2 and "display" in buy2["tag"] and "Lore" in buy2["tag"]["display"]:
         buy2["tag"]["display"].pop("Lore")

   with RelativeScope("tag.Offers.Recipes[]."):
      Tag("buy", buy)
      if buy2 is not None:
         Tag("buyB", buy2)
      Tag("sell", sell)

def villager_age_locked():
   with RelativeScope("tag."):
      Tag("AgeLocked", dt.TRUE)

def rabbit_type(rabbit_type):
   with RelativeScope("tag."):
      Tag("RabbitType", dt.int(rabbit_type))

def snow_golem_pumpkin(pumpkin):
   with RelativeScope("tag."):
      Tag("Pumpkin", dt.bool(pumpkin))

def creeper_fuse(fuse):
   with RelativeScope("tag."):
      Tag("Pumpkin", dt.int(fuse))

def creeper_charged():
   with RelativeScope("tag."):
      Tag("powered", dt.TRUE)

def uuid(id1, id2, id3, id4):
   with RelativeScope("tag."):
      Tag("UUID", dt.int_list(id1, id2, id3, id4))

def projectile_owner(id1, id2, id3, id4):
   with RelativeScope("tag."):
      Tag("UUID", dt.int_list(id1, id2, id3, id4))

def tropical_fish_variant(variant):
   with RelativeScope("tag."):
      Tag("Variant", dt.int(variant))

def baby():
   with RelativeScope("tag."):
      Tag("IsBaby", dt.TRUE)

def death_loot_table(loot_table_id):
   with RelativeScope("tag."):
      Tag("DeathLootTable", loot_table_id)

def persistence_required():
   with RelativeScope("tag."):
      Tag("PersistenceRequired", dt.TRUE)

def can_pickup_loot():
   with RelativeScope("tag."):
      Tag("CanPickUpLoot", dt.TRUE)

def cannot_pickup_loot():
   with RelativeScope("tag."):
      Tag("CanPickUpLoot", dt.FALSE)
