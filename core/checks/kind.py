import os
import core.log as log
import core.checks.base as base
import core.checks.utils as utils


class KindCheck(base.CheckWithManifest):
    def __init__(self, pkg):
        super().__init__(pkg, [None])
        log.s("Checking package kind")

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

    def edit(self, _):
        if self.pkg.is_effective:
            ans = log.q("Would you like to edit the manifest.toml (1) "
                        "or to add files to the package (2)? ")
            if ans == "1":
                super().edit(_)
            elif ans == "2":
                utils.open_shell(self.pkg.cache)
            else:
                log.w("Only recognized answers are 1 and 2")
        else:
            ans = log.q("Would you like to edit the manifest.toml (1) "
                        "or to remove the files from the package? (2) ")
            if ans == "1":
                super().edit(_)
            elif ans == "2":
                pass  # The rewrap at the end will ignore the files if the kind is virtual
            else:
                log.w("Only recognized answers are 1 and 2")
