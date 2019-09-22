import os
import core.log as log
import core.checks.base as base
import core.checks.utils as utils


class KindCheck(base.CheckWithManifest):
    def __init__(self, pkg):
        super().__init__(pkg, [None])

    def run(self):
        log.s("Checking package kind")
        super().run()

    def validate(self, _):
        length = len(os.listdir(self.pkg.cache))
        return (self.pkg.is_effective and length != 1) \
            or (not self.pkg.is_effective and length == 1)

    def show(self, _):
        if self.pkg.is_effective:
            log.e("Package is effective but is missing a data.tar.gz")
        else:
            log.e("Package is virtual but has a data.tar.gz")

    def diff(self, _):
        target = 'virtual' if self.pkg.is_effective else 'effective'
        log.i(f"Package kind would be changed to {target}")

    def fix(self, _):
        target = 'virtual' if self.pkg.is_effective else 'effective'
        self.pkg.manifest['kind'] = target
        self.pkg.is_effective = not self.pkg.is_effective
        self.write_pkg_manifest()

    def edit(self, _):
        if self.pkg.is_effective:
            ans = self._ask_1or2("Would you like to edit the manifest.toml (1) "
                                  "or to add files to the package (2)? ")
            if ans == 1:
                super().edit(_)
            elif ans == 2:
                utils.open_shell(self.pkg.cache)
        else:

            ans = self._ask_1or2("Would you like to edit the manifest.toml (1) "
                                 "or to remove the files from the package? (2) ")
            if ans == 1:
                super().edit(_)

    @staticmethod
    def _ask_1or2(question):
        while True:
            ans = log.q(question)
            if ans == '1':
                return 1
            elif ans == '2':
                return 2
            else:
                log.w("Only recognized answers are 1 and 2")
