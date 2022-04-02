# !/usr/bin/env python3

import urllib.parse
import shutil
import sys
import os

from .platform import VSSPlatform
from . import signature
from . import configs

working_folder = '.vss'
platforms_folder_name = 'platforms'



def create_dir(path):
    try:
        os.mkdir(path)
        print("Directory {} created".format(path))
    except FileExistsError:
        print("Directory {} exists".format(path))
        sys.exit(0)

def init_vss_folder(force_reinit=False):
    if force_reinit:
        try:
            shutil.rmtree(working_folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    # if os.path.exists(working_folder)
        # print("Something is initialized".format(working_folder))

    create_dir(working_folder)
    print("Initializing VSS repo...".format(working_folder))

    repositories_folder = os.path.join(working_folder, 'platforms')
    create_dir(repositories_folder)
    signature.create_keypair(working_folder)

    conf_filepath = os.path.join(working_folder, "conf.json")
    with open(conf_filepath, "w") as f:
        f.write(configs.basic_conf_file)


class VSSMaintainer:
    def __init__(self) -> None:
        self.configs = configs.VSSConfigs(working_folder)

    def generate_client_config_file(self, platform, dst):
        public_key_path = os.path.join(working_folder, signature.standart_public_key_name)
        public_key = signature.load_key(public_key_path)
        public_key_str = signature.key_to_str(public_key)
        # print(public_key_str)

        platform_configs: configs.VSSPlatformConfigs = None

        for pc in self.configs.platform_configs:
            if pc.name == platform:
                platform_configs = pc
                print("\"{}\" platform found".format(platform))

        if platform_configs:
            header = "from mini_vss.configs import VSSClientConfig\n\nclass VSSClientConfigInitialized(VSSClientConfig):"
            content = "\n{}\n    name = \"{}\"\n    url = \"{}\"\n    public_key = \'\'\'{}\'\'\'\n".format(
                header, platform_configs.name, platform_configs.remote_path, public_key_str)

            path = os.path.join(dst, "vss_client_configs.py")
            with open(path, 'w') as f:
                f.write(content)
                print("{} written".format(path))
        else:
            print("No such platform!")

    def add_version(self, version_name, platform=""):
        def copy_working_file(src_file, dst_folder):
            s_filename, s_file_extension = os.path.splitext(os.path.basename(src_file))
            dst_filename = s_filename + "_" + str(version_name) + s_file_extension
            dst = os.path.join(dst_folder, dst_filename)
            print("copying {} as {}".format(src_file, dst))
            shutil.copy(src_file, dst)
            # print("copying finished!")
            return dst

        private_key_path = os.path.join(working_folder, signature.standart_private_key_name)
        private_key = signature.load_key(private_key_path)

        for platform_c in self.configs.platform_configs:
            if not platform or platform_c.name == platform:
                unique_version_name = True

                for version in platform_c.platform.versions:
                    if version.version == version_name:
                        print("Platform \"{}\" has {} version!!!".format(platform_c.name, version_name))
                        unique_version_name = False

                if unique_version_name:
                    print("\nAdding version {} to \"{}\"".format(version_name, platform_c.name))
                    copied_filepath = copy_working_file(platform_c.working_file, platform_c.local_path)
                    info_filepath = os.path.join(platform_c.local_path, "info.json")
                    current_platform = platform_c.platform
                    current_platform.add_version(version_name, copied_filepath, private_key)
                    current_platform.save(info_filepath)

    def add_platform(self, platform_name, working_file, remote=""):
        platform_path = os.path.join(working_folder, platforms_folder_name, platform_name)
        create_dir(platform_path)

        relative_public_key_path = os.path.join(working_folder, signature.standart_public_key_name)
        public_key = signature.load_key(relative_public_key_path)

        info_filepath = os.path.join(platform_path, "info.json")

        platform_params = { "name": platform_name,
                            "filename": os.path.basename(working_file),
                            "versions": [] }
        new_platform = VSSPlatform(platform_params)
        new_platform.save(info_filepath)
        print("Platform \"{}\" created.".format(platform_name))

        remote_path = remote or urllib.parse.urljoin(self.configs.basic_remote, platform_name)
        platform_c_params = {
            "name": platform_name,
            "local_path": platform_path,
            "remote_path": remote_path,
            "working_file": working_file,}
        new_platform_conf = configs.VSSPlatformConfigs(platform_c_params)
        self.configs.platform_configs.append(new_platform_conf)
        self.configs.save()

        print("Platform data saved to config".format())

    # def add_remote(self, remote_url):
    #     self.configs.remote_urls.append(remote_url)
    #     self.configs.save()


'''
def load_versions():
         # json.dump(
        #     {"a": 1, "b": 2},
        #     open("sample.json", "w"))
    if os.path.isfile(json_path):
        print("Reading current versions")
    else:
        print("No versions yet. Creating")

def add_version(version=None, file=None):
    # check if there isn`t this version yet
    # versions

    if not file:
        # get filename from configured location
        filename = 'Readme.md'

    print("Adding {} version".format(version))
    sign = signature.sign(filename)
    # move file
    # add record to versions.json
    # if signature.('Readme.md', signature):
        # print("Ok")
    print("Signature is: {}".format(signature))

def serialize():
    versions_dicts = []
    for v in versions:
        versions_dicts.append(v.to_dict())

    parent_dict = {
        "app_name": app_name,
        # "author": author,
        "last_update": str(datetime.now()),
        "available_versions": versions_dicts
    }

    json_string = json.dumps(parent_dict, indent=4)
    return json_string

def init(force_reinit=False):
    def init_client_config_file(app_name='xxx', update_urls=[], public_key='', timeout=30, retries=3):
        class_start = "class ClientConfig(object):"
        attr_dict = { "APP_NAME" : app_name, "UPDATE_URLS": update_urls, "MAX_DOWNLOAD_RETRIES": retries, "PUBLIC_KEY": public_key }
        with open(os.path.join(working_folder, client_conf_filename), 'w') as f:
            f.write(class_start)
            for key in attr_dict:
                value = attr_dict[key]

                # put quotes around strings
                if isinstance(value, str):
                    value = "\"{}\"".format(value)

                new_str = "\n    {} = {}".format(key, value)
                f.write(new_str)

    if force_reinit:
        if os.path.isdir(working_folder):
            print("Deleting old {}".format(working_folder))
            try:
                shutil.rmtree(working_folder)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

    try:
        os.mkdir(working_folder)
        print("Directory {} created".format(working_folder))
    except FileExistsError:
        print("Directory {} exists".format(working_folder))
        return

    print("Initializing...".format(working_folder))
    # init_client_config_file()
    # platform.init()
    signature.create_keypair()
'''
