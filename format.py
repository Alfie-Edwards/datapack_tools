import re
from datapack_tools.scopes import *
import data_types as dt

EFFECT_IDS = {
   "speed":1,
   "slowness":2,
   "haste":3,
   "mining_fatigue":4,
   "strength":5,
   "instant_health":6,
   "instant_damage":7,
   "jump_boost":8,
   "nausea":9,
   "regeneration":10,
   "resistance":11,
   "fire_resistance":12,
   "water_breathing":13,
   "invisibility":14,
   "blindness":15,
   "night_vision":16,
   "hunger":17,
   "weakness":18,
   "poison":19,
   "wither":20,
   "health_boost":21,
   "absorption":22,
   "saturation":23,
   "glowing":24,
   "levitation":25,
   "luck":26,
   "unluck":27,
   "slow_falling": 28,
   "conduit_power": 29,
   "dolphins_grace": 30,
   "bad_omen": 31,
   "hero_of_the_village": 32,
}

def recursive_to_string(o, *, format="{}", list_format='[{}]', dict_format='{{{}}}', tag_format='{}:{}', deliminator=','):
   def _recursive_to_string(o, list_format, dict_format, tag_format, deliminator):
      if isinstance(o, dict):
         return dict_format.format(
            deliminator.join(
               [tag_format.format(key, _recursive_to_string(o[key], list_format, dict_format, tag_format, deliminator)) for key in o]))
      elif isinstance(o, list):
         return list_format.format(
            deliminator.join(
               _recursive_to_string(item, list_format, dict_format, tag_format, deliminator) for item in o))
      else:
         return str(o)
   return format.format(_recursive_to_string(o, list_format, dict_format, tag_format, deliminator))


def parse_color(hex_code):
   return int(hex_code[1:], 16)

def parse_effect(effect):
   if isinstance(effect, str):
      name = effect.lower().replace(" ", "_").replace("'", "")
      if EFFECT_IDS.contains_key(name):
         return dt.byte(EFFECT_IDS[name])
      else:
         raise LookupError(f"No effect named {effect}")
   else:
      return dt.byte(effect)


def parse_text(text):
   def tokenise(text):
      pos = 0
      tokens = []
      for match in re.finditer(r'(?<!\\)(\*\*|__|\+\+|~~|\?\?| \{[^}]+\}|\{[^}]+\} ?)', text):
        if match.start() > pos:
            tokens.append(text[pos:match.start()])
        tokens.append(text[match.start():match.end()])
        pos = match.end()
      if pos < len(text):
        tokens.append(text[pos:])
      return tokens

   sections = []
   with Scope(sections):
      options = {} # {color:#12312,font=comic sans} text {color:,font:}
      bold = False # **text**
      italic = False # __text__
      underlined = False # ++text++
      strikethrough = False # ~~text~~
      obfuscated = False # ??text??
      for token in tokenise(text):
         if token == "**":
            bold = not bold
         elif token == "__":
            italic = not italic
         elif token == "++":
            underlined = not underlined
         elif token == "~~":
            strikethrough = not strikethrough
         elif token == "??":
            obfuscated = not obfuscated
         elif token.beginswith("{") or token.beginswith(" {"):
            for option in token.strip()[1:-1].split(","):
               i = option.find(":")
               if i != -1:
                  key = option[0:i]
                  value = option[i+1:-1]
                  if value:
                     options[key] = value
                  else: # If value is blank reset it to default
                     options.remove(key)
         else:
            with ListItem({}):
               Tag("text", token)
               if bold:
                  Tag("bold", "true")
               if italic:
                  Tag("italic", "true")
               if underlined:
                  Tag("underlined", "true")
               if strikethrough:
                  Tag("strikethrough", "true")
               if obfuscated:
                  Tag("obfuscated", "true")
               for key in options:
                  Tag(key, options[key])

   if len(sections) == 0:
      sections = {}
   elif len(sections) == 1:
      sections = sections[0]

   return "'{}'".format(recursive_to_string(sections, tag_format='"{}":"{}"'))

