# datapack_tools
A set of python tools for working with Minecraft Java Edition Datapacks

## Scopes
Lots of the library is built around a scoping mechanism. All of the functions for setting the properties of things like items and mobs act on the current scope.

The point of scoping is to make it easier to traverse through the complex trees of lists and dictionaries which come with json. A scope can be any object, but it's generally a list or dictionary. The current scope is stored in a stack, so when you exit a scope the current scope returns to whetever it was previously.

To push an object onto the scope stack, you wrap it in a `Scope()` object, and use the `with` keyword:
```
from datapack_tools.items import *

special_coal = Item("coal")
with Scope(special_coal):
   # functions to setup your item
   name("Special Coal)
   enchantment("fire_aspect", 3)
```

There are also three utility classes which extend the `Scope` class:
 - `RelativeScope(path)` Is a shortcut to scope through mulitple levels of dictionaries and lists.
 - `Tag(key, value)` Is a shortcut to add an entry to a dictionary scope.
 - `ListItem(value)` Is a shortcut to add an item to a list scope.
Since these types inherit from `Scope`, you do not need to wrap them in a `Scope` object id you want to scope into them.
All three of these types are used extensively in this library so that's the best place to look for examples.

## Items Example
```
from datapack_tools.items import *

items = {}
with Scope(items):
   with Tag("old_rod", Item("fishing_rod")):
      name("Old Rod")
      lore("catch yourself")
      lore("some dinner")

   with Tag("super_rod", Item("fishing_rod")):
      name("Super Rod")
      lore("gotta catch \\'em all!")
      enchantment("luck_of_the_sea", 5)
      enchantment("lure", 5)

for item_name in items:
   function = commands.item_give(items[item_name])
   name = "items/" + item_name
   write_function(name, function, "example_namespace", "datapack_path")
```

## Mobs Example
```
from datapack_tools.mobs import *

mobs = {}
with Scope(mobs):
   with Tag("target_dummy", Mob("husk")):
      tag("target_dummy")
      silent()
      attribute("max_health", 1024)
      no_ai()

   with Tag("warden", Mob("iron_golem")):
      tag("warden")
      name("Warden")
      effect(10, 1)
      effect(11, 2)
      attribute("follow_range", 4)
      attribute("movement_speed", 0.15)
      attribute("armor", 27)
      attribute("armor_toughness", 100)
      attribute("attack_knockback", 20)

for mob_name in mobs:
   function = commands.mob_summon(mobs[mob_name])
   name = "mobs\\" + mob_name
   write_function(name, function, "example_namespace", "datapack_path")
```

## Advancements Example
```
from datapack_tools.advancements import *

advancements = {}
with Scope(advancements):
   with Tag("exploration/root", Advancement()):
      name("Exploration")
      description("Discover hidden areas around the map")
      icon_item("compass")
      background_block("white_terracotta")
      criteria_impossible()

   with Tag("exploration/escape", Advancement()):
      name("Escape")
      description("Escape the map")
      parent("example_namespace:exploration/root")
      icon_item("oxeye_daisy")
      hidden()
      criteria_location(122, 241, -23, 126, 244, -21)


for advancement_name in advancements:
   advancement = advancements[advancement_name]
   write_advancement(advancement_name, advancement, "example_namespace", "datapack_path")
```

## Removing Vanilla Advancements
```
import datapack_tools.vanilla_data
from datapack_tools.advancements import NULL_ADVANCEMENT

for name in vanilla_data.get_advancement_names():
   write_advancement(name, NULL_ADVANCEMENT, "minecraft", "datapack_path")
```
