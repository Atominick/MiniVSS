
from typing import List
import json
import os

from .platform import VSSPlatform



class VSSClientConfig:
    name = "Test Repo"
    url = ""
    public_key = ""


class VSSPlatformConfigs:
    def __init__(self, params: dict):
        self.name: str = params["name"]
        self.local_path = params["local_path"]
        self.remote_path = params["remote_path"]
        self.working_file = params["working_file"]

        info_file_path = os.path.join(self.local_path, 'info.json')

        # try:
        f = open(info_file_path)
        json_data = json.load(f)
        self.platform = VSSPlatform(json_data)
        f.close()
        # except Exception as e:
        #     print("Cant`t initialize local platfrom {}. {}".format(self.local_path, e))
        #     sys.exit(0)


    def to_dict(self):
        return {"name": self.name, "local_path": self.local_path,"remote_path": self.remote_path, "working_file": self.working_file}

    def __str__(self) -> str:
        return "{}".format(self.local_path)


# TODO: move basic conf(remote)
basic_conf_file = '''{
    "basic_remote": "http://updates.atominick.info/",
    "platforms": [] }'''
class VSSConfigs:
    def __init__(self, working_folder) -> None:
        self.platform_configs: List[VSSPlatformConfigs] = []
        self.config_file_path = os.path.join(working_folder, 'conf.json')

        # try:
        f = open(self.config_file_path)
        data = json.load(f)
        self.basic_remote = data["basic_remote"]
        platforms_list = data["platforms"]
        f.close()

        for p_conf in platforms_list:
            new_p_conf = VSSPlatformConfigs(p_conf)
            self.platform_configs.append(new_p_conf)
        # except Exception as e:
        #     print("Can`t init configs. {}".format(e))
        #     sys.exit(0)


    def save(self):
        def json_encode():
            platform_c_list = []
            for platform_c in self.platform_configs:
                platform_c_list.append(platform_c.to_dict())
            json_dict = { "platforms": platform_c_list, "basic_remote": self.basic_remote }
            return json_dict

        with open(self.config_file_path, "w") as f:
            json.dump(json_encode(), f, indent=4)
