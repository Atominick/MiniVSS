# !/usr/bin/env python

from typing import Callable, List, Union
import urllib.parse
import requests
import os

from semantic_version import Version

from .configs import VSSClientConfig
from .platform import VSSPlatform
from .version import VSSVersion
from . import signature



class VSSClient:
    def __init__(self, configs: VSSClientConfig):
        self.configs = configs
        self.public_key = signature.str_to_key(self.configs.public_key)

        self.updating_callback: Callable[[int], None] = None
        self.platform = VSSPlatform()
        self.update()


    def download_version_file(self, url, dest):
        chunk_size=8192
        with requests.get(url, stream=True) as r:
            lenght = int(r.headers.get('content-length'))
            length_in_chunks = lenght / chunk_size
            r.raise_for_status()
            with open(dest, 'wb') as f:
                chunks = 0
                for chunk in r.iter_content(chunk_size=chunk_size):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.

                    #if chunk:
                    chunks += 1

                    if self.updating_callback:
                        procentage = chunks / length_in_chunks * 100
                        self.updating_callback(procentage)

                    f.write(chunk)

    def update(self):
        try:
            info_file_url = urllib.parse.urljoin(self.configs.url, "info.json")
            json_data = requests.get(info_file_url, timeout=5).json()
            self.platform = VSSPlatform(json_data)
        except Exception:
            print("Can`t load data from {}...".format(info_file_url))

    def find_vss_version(self, vss_version_or_str: Union[VSSVersion, str]) -> VSSVersion:
        if isinstance(vss_version_or_str, str):
            for v in self.platform.versions:
                if v.version == Version(vss_version_or_str):
                    return v
            print("Can`t find {}".format(vss_version_or_str))
        elif isinstance(vss_version_or_str, VSSVersion):
            return vss_version_or_str
        else:
            NotImplemented

    def get_available_versions(self) -> List[VSSVersion]:
        return self.platform.versions

    def download(self, version: Union[VSSVersion, str]):
        version = self.find_vss_version(version)
        file_url = urllib.parse.urljoin(self.configs.url, version.file)
        dst = version.file

        self.download_version_file(file_url, dst)

        if signature.check(dst, version.sign, self.public_key):
            print("File \"{}\" downloaded successfully".format(dst))
            return dst
        else:
            print("Hashes are differents. Something went wrong :(\nDeleting \"{}\" for safety reasons".format(dst))
            os.remove(dst)
            return

    def upgrade_to(self, version_to_install: Union[VSSVersion, str]):
        version_to_install = self.find_vss_version(version_to_install)

        temp_filepath = self.download(version_to_install)
        program_name = self.platform.dest_filename
        os.rename(temp_filepath, program_name)
        print("Version changed to {}".format(version_to_install))

    def get_current_version(self) -> VSSVersion:
        if os.path.exists(self.platform.dest_filename):
            for v in self.platform.versions:
                if signature.check(self.platform.dest_filename, v.sign, self.public_key):
                    # print("Hash of {} is identical to {}".format(self.platform.dest_filename, v))
                    return v
                else:
                    # print("Hashes are differents. Something went wrong :(\nDeleting \"{}\" for safety reasons".format(dst))
                    pass
        else:
            print("{} not found".format(self.platform.dest_filename))

    def get_latest_version(self) -> VSSVersion:
        if self.platform.versions:
            return max(self.platform.versions)

    def upgrade_to_latest(self):
        cv = self.get_current_version()
        print("Current version is {}".format(cv))
        lv = self.get_latest_version()
        if lv == cv:
            print("Current version is up to date")
        else:
            print("New version found. Upgrading from {} to {}".format(cv ,lv))
            self.upgrade_to(lv)