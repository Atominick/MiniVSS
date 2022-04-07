
from typing import List
import json
import os

import semantic_version

from .version import VSSVersion
from . import signature


standart_platform_params = {
    "name": "No name",
    "filename": "",
    "versions": [] }
class VSSPlatform:
    def __init__(self, param_dict: dict = standart_platform_params):
        self.name = param_dict["name"]
        self.dest_filename = param_dict["filename"]
        self.versions: List[VSSVersion] = []
        version_list = param_dict['versions']
        for version_data in version_list:
            self.versions.append(VSSVersion(version_data))


    def save(self, json_filepath):
        def to_dict():
            j_dict = {}
            j_dict['name'] = self.name
            j_dict['filename'] = self.dest_filename

            ver_arr = []
            for ver in self.versions:
                ver_arr.append(ver.to_dict())
            j_dict['versions'] = ver_arr
            return j_dict

        with open(json_filepath, "w") as f:
            json.dump(to_dict(), f, indent=4)

    def add_version(self, version_name: semantic_version.Version, v_file_path, private_key):
        sign = signature.generate(v_file_path, private_key)

        filename = os.path.basename(v_file_path)
        version_data_dict = {
            "version": version_name,
            "sign": sign,
            "desc": "",
            "file": filename }
        new_version = VSSVersion(version_data_dict)
        self.versions.append(new_version)
