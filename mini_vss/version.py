
from datetime import datetime

from semantic_version import Version

# v = semantic_version.Version('0.1.1')
# .major
# v.minor
# v.patch
# v.prerelease


class VSSVersion:
    def __init__(self, version_data):
        self.version = Version(version_data["version"])
        self.file = version_data["file"]
        self.sign = version_data["sign"]
        self.desc = version_data["desc"]

        if "date" in version_data:
            self.date = datetime.strptime(version_data["date"], "%m/%d/%Y %H:%M:%S")
        else:
            self.date = datetime.now()

    def to_dict(self):
        def_dict = self.__dict__
        def_dict['date'] = self.date.strftime("%m/%d/%Y %H:%M:%S")
        def_dict['version'] = str(self.version)
        return def_dict

    def __repr__(self):
        return "v{}({})".format(self.version, self.date)

    # def __le__(self, other):
    #     if not isinstance(other, self.__class__):
    #         return NotImplemented
    #     return self.version <= other.version

    # def __ge__(self, other):
    #     if not isinstance(other, self.__class__):
    #         return NotImplemented
    #     return self.version >= other.version

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.version < other.version

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.version > other.version
