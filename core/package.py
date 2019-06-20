import shutil
import os
import tarfile
import core
import toml


class Package:
    def __init__(self, npf_path):
        self.cache = core.args.get_args().cache_dir
        self.npf_path = npf_path
        self.is_effective = False

    def unwrap(self):
        if os.path.exists(self.cache):
            shutil.rmtree(self.cache)
        os.makedirs(self.cache)
        with tarfile.open(self.npf_path, 'r') as tar:
            tar.extractall(self.cache)
        self.manifest_path = os.path.join(self.cache, 'manifest.toml')
        self.manifest = toml.load(self.manifest_path)
        self.is_effective = self.manifest['kind'] == 'effective'
        data = os.path.join(self.cache, 'data.tar.gz')
        if os.path.exists(data):
            with tarfile.open(data, 'r:gz') as tar:
                tar.extractall(self.cache)
            os.remove(data)

    def check(self):
        print('TODO: Package.check()')

    def wrap(self):
        self.create_manifest_toml()
        if self.is_effective:
            self.create_data_tar()
        self.create_nest_file()

    def create_manifest_toml(self):
        print('TODO: Package.create_manifest_toml()')
        pass

    def create_data_tar(self):
        with core.pushd(self.cache):
            for root, _, filenames in os.walk('.'):
                for name in filenames:
                    print(os.path.join(root, name))
            with tarfile.open('data.tar.gz', 'w:gz') as archive:
                archive.add('./')

    def create_nest_file(self):
        with core.pushd(self.cache):
            new_nest_file_path = os.path.basename(self.npf_path) + '.new'
            with tarfile.open(new_nest_file_path, 'w') as nest_file:
                nest_file.add('manifest.toml')
                if self.is_effective:
                    nest_file.add('data.tar.gz')
            os.remove('manifest.toml')
            if self.is_effective:
                os.remove('data.tar.gz')
        new_path = f'{self.npf_path}.new'
        os.rename(os.path.join(self.cache, new_nest_file_path), new_path)
