import json
import requests
import semver
import core.log as log
import core.checks.base as base


class VersionReqsResolvabilityCheck(base.CheckWithManifest):
    def __init__(self, pkg):
        super().__init__(pkg, list(pkg.manifest['dependencies'].items()))
        self.highest_version = ""
        self.pkg_error = False
        self.version_error = False

    def run(self):
        log.s("Checking the version requirement solvability of dependencies")
        super().run()

    def validate(self, item):
        self.pkg_error = False
        self.version_error = False
        full_name, version_req = item
        log.i(f"Checking {full_name}#{version_req}")
        repository, rest = full_name.split('::')
        category, name = rest.split('/')
        resp = requests.get(f'https://{repository}.raven-os.org/api/p/{category}/{name}')
        if resp.ok:
            content = json.loads(resp.content)
            match = semver.max_satisfying(
                    content['versions'],
                    version_req,
            )
            if match is None:
                self.version_error = True
                self.highest_version = semver.max_satisfying(
                        content['versions'],
                        '*',
                )
                return False
            return True
        else:
            self.pkg_error = True
            return False

    def show(self, item):
        full_name, version_req = item
        if self.pkg_error:
            log.e(f"Package wasn't found")
        elif self.version_error:
            log.e(f"No version was found for requirement {version_req}")

    def diff(self, item):
        if self.pkg_error:
            log.i(f"Dependency would be removed")
        elif self.version_error:
            log.i(f"The version would be changed to the highest available: '{self.highest_version}'")

    def fix(self, item):
        if self.pkg_error:
            del self.pkg.manifest['dependencies'][item[0]]
        elif self.version_error:
            self.pkg.manifest['dependencies'][item[0]] = self.highest_version
        self.write_pkg_manifest()
