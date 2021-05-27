import io
import json
import os
import re

def _write(path, file_contents):
   directory = os.path.dirname(path)
   if not os.path.isdir(directory):
      os.makedirs(directory)
   f = io.open(path, "w", encoding="utf-8")
   f.write(file_contents)
   f.close()

def _split_path(path):
   return re.split(r'[/\]+', path)

def write_function(name, function, namespace, datapack_path):
   name += ".mcfunction"
   path = os.path.join(datapack_path, "data", namespace, "functions", *_split_path(name))
   _write(path, function)

def write_advancement(name, advancement, namespace, datapack_path):
   name += ".json"
   path = os.path.join(datapack_path, "data", namespace, "advancements", *_split_path(name))
   _write(path, json.dumps(advancement, indent=3))

def write_loot_table(name, loot_table, namespace, datapack_path):
   name += ".json"
   path = os.path.join(datapack_path, "data", namespace, "loot_tables", *_split_path(name))
   _write(path, json.dumps(loot_table, indent=3))

def datapack_exists(dir):
   mcmeta_path = os.path.join(*_split_path(dir), "pack.mcmeta")
   if not os.path.exists(mcmeta_path):
      return False
   return True
