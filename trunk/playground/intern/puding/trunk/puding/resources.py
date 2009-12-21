import json
import os
from xdg import BaseDirectory


class ResourceManager(object):
    def __init__(self):
        self.CACHE_HOME = os.path.join(BaseDirectory.xdg_cache_home, "puding")
        # creating cache home if it doesn't exist
        if not os.path.isdir(self.CACHE_HOME):
            os.makedirs(self.CACHE_HOME)
        self.CONFIG_HOME = BaseDirectory.save_config_path("puding")
        self.CONFIG_FILE = os.path.join(self.CONFIG_HOME, "settings.json")
        self.DATA_HOME = BaseDirectory.save_data_path("puding")
        self.DATA_PATH = map(self.append_app_name, BaseDirectory.xdg_data_dirs)
        self.DEV_HOME = os.path.abspath(os.path.dirname(__file__))

    def load_settings(self):
        with open(self.CONFIG_FILE, "r") as f:
            settings = json.loads(f.read())

        return settings

    def save_settings(self, dict):
        with open(self.CONFIG_FILE, "w") as f:
            f.writelines(json.dumps(dict))

    def append_app_name(self, path):
        return os.path.join(path, "puding")

    def get_data_file(self, rel_path):
        dev_path = os.path.join(self.DEV_HOME, rel_path)

        if os.path.isfile(dev_path):
            return dev_path
        else:
            for path in self.DATA_PATH:
                prod_path = os.path.join(path, rel_path)

                if os.path.isfile(prod_path):
                    return prod_path

        return None

