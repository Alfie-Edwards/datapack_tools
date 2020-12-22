import glob
import json
import os
import re
import zipfile

DEFAULT_INSTALL_DIRECTORY = os.path.join(os.getenv("APPDATA"), ".minecraft")
ADVANCEMENT_PATH = "data/minecraft/advancements/"
LOOT_TABLE_PATH = "data/minecraft/loot_tables/"


def _get_jar(install_directory, version):
   if version is None:
      version = get_latest_release_version(install_directory)

   jar_path = os.path.join(install_directory, "versions", version, "{}.jar".format(version))
   return zipfile.ZipFile(jar_path)


def get_versions(install_directory=DEFAULT_INSTALL_DIRECTORY):
   pattern = os.path.join(install_directory, "versions", "*", "")
   return [path.split("\\")[-2] for path in glob.glob(pattern)]


def get_latest_release_version(install_directory=DEFAULT_INSTALL_DIRECTORY):
   pattern = re.compile(r"\d+(\.\d+)*")
   release_versions = [version for version in get_versions(install_directory) if re.fullmatch(pattern, version)]
   latest_version = None
   for version in release_versions:
      if latest_version is None:
         latest_version = version
      else:
         subversions = [int(v) for v in version.split(".")]
         subversions_latest = [int(v) for v in latest_version.split(".")]
         if subversions > subversions_latest:
            latest_version = version
   return latest_version


def get_advancement_names(*, install_directory=DEFAULT_INSTALL_DIRECTORY, version=None):
   with _get_jar(install_directory, version) as jar:
      names = jar.namelist()
      return [name[len(ADVANCEMENT_PATH):-5] for name in names if name.startswith(ADVANCEMENT_PATH)]


def get_advancement(name, *, install_directory=DEFAULT_INSTALL_DIRECTORY, version=None):
   with _get_jar(install_directory, version) as jar:
      json = jar.read(ADVANCEMENT_PATH + name)
      return json.loads(json)


def get_loot_table_names(*, install_directory=DEFAULT_INSTALL_DIRECTORY, version=None):
   with _get_jar(install_directory, version) as jar:
      names = jar.namelist()
      return [name[len(LOOT_TABLE_PATH):-5] for name in names if name.startswith(LOOT_TABLE_PATH)]


def get_loot_table(name, *, install_directory=DEFAULT_INSTALL_DIRECTORY, version=None):
   with _get_jar(install_directory, version) as jar:
      json = jar.read(LOOT_TABLE_PATH + name)
      return json.loads(json)