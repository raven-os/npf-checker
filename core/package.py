import shutil
import os
import tarfile
import core
import enum
import toml


class Kind(enum.Enum):
    EFFECTIVE = 'effective'
    VIRTUAL = 'virtual'


class Package:
    def __init__(self, npf_path):
        self.cache = core.args.get_args().cache_dir
        self.npf_path = npf_path

    def unwrap(self):
        if os.path.exists(self.cache):
            shutil.rmtree(self.cache)
        os.makedirs(self.cache)
        with tarfile.open(self.npf_path, 'r') as tar:
            tar.extractall(self.cache)
        self.manifest_path = os.path.join(self.cache, 'manifest.toml')
        self.manifest = toml.load(self.manifest_path)
        data = os.path.join(self.cache, 'data.tar.gz')
        if os.path.exists(data):
            with tarfile.open(data, 'r:gz') as tar:
                tar.extractall(self.cache)
            os.remove(data)
