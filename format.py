import re
from datapack_tools.scopes import *

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


def parse_text(text):
   def tokenise(text):
      pos = 0
      tokens = []
      for match in re.finditer(r'(?<!\\)(\*\*|__|\+\+|~~|\?\?)', text):
        if match.start() > pos:
            tokens.append(text[pos:match.start()])
        tokens.append(text[match.start():match.end()])
        pos = match.end()
      if pos < len(text):
        tokens.append(text[pos:])
      return tokens

   sections = []
   with Scope(sections):
      bold = False # **
      italic = False # __
      underlined = False # ++
      strikethrough = False # ~~
      obfuscated = False # ??
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
   if len(sections) == 0:
      sections = {}
   elif len(sections) == 1:
      sections = sections[0]

   return "'{}'".format(recursive_to_string(sections, tag_format='"{}":"{}"'))

