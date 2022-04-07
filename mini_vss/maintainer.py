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


    def generate_client_config_file(self, dst):
        public_key_path = os.path.join(working_folder, signature.standart_public_key_name)
        public_key = signature.load_key(public_key_path)
        public_key_str = signature.key_to_str(public_key)

        content = ""
        for pc in self.configs.platform_configs:
            print("\"{}\" platform found".format(pc))

            header = "class VSS{}ClientConfig(object):".format(pc.name.capitalize())
            content += "\n\n{}\n    name = \"{}\"\n    url = \"{}\"\n    public_key = \'\'\'{}\'\'\'\n".format(
                header, pc.name, pc.remote_path, public_key_str)

        path = os.path.join(dst, "client_config.py")
        with open(path, 'w') as f:
            f.write(content)
            print("{} written".format(path))

    def add_version(self, version_name, platform=""):
        def copy_working_file(src_file, dst_folder):
            s_filename, s_file_extension = os.path.splitext(os.path.basename(src_file))
            dst_filename = s_filename + "_" + str(version_name.replace(".", "_")) + s_file_extension
            dst = os.path.join(dst_folder, dst_filename)
            print("copying {} as {}".format(src_file, dst))
            try:
                shutil.copy(src_file, dst)
                # print("copying finished!")
            except FileNotFoundError:
                print("No {} file found!".format(src_file))
                sys.exit(0)
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

    # def add_remote(self, remote_url):
    #     self.configs.remote_urls.append(remote_url)
    #     self.configs.save()

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

        remote_path = remote or urllib.parse.urljoin(self.configs.basic_remote, platform_name + '/')
        platform_c_params = {
            "name": platform_name,
            "local_path": platform_path,
            "remote_path": remote_path,
            "working_file": working_file,}
        new_platform_conf = configs.VSSPlatformConfigs(platform_c_params)
        self.configs.platform_configs.append(new_platform_conf)
        self.configs.save()

        print("Platform data saved to config".format())
