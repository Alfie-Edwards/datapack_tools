import io
import json
import os

def _write(path, file_contents):
   directory = os.path.dirname(path)
   if not os.path.isdir(directory):
      os.makedirs(directory)
   f = io.open(path, "w", encoding="utf-8")
   f.write(file_contents)
   f.close()

def write_function(name, function, namespace, datapack_path):
   name += ".mcfunction"
   path = os.path.join(datapack_path, "data", namespace, "functions", name)
   _write(path, function)

def write_advancement(name, advancement, namespace, datapack_path):
   name += ".json"
   path = os.path.join(datapack_path, "data", namespace, "advancements", name)
   _write(path, json.dumps(advancement, indent=3))

def write_loot_table(name, loot_table, namespace, datapack_path):
   name += ".json"
   path = os.path.join(datapack_path, "data", namespace, "loot_tables", name)
   _write(path, json.dumps(loot_table, indent=3))

def datapack_exists(dir):
   if not os.path.isdir(dir):
      return False
   mcmeta_path = os.path.join(dir, "pack.mcmeta")
   if not os.path.exists(mcmeta_path):
      return False
   return True
