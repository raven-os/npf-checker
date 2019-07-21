import os
import json
import requests
import semver
import core
import core.log as log
import core.checks.base as base
import core.checks.utils as utils


class VersionReqsResolvabilityCheck(base.CheckWithManifest):
    def __init__(self, pkg):
        super().__init__(pkg, list(pkg.manifest['dependencies'].items()))
        log.s("Checking the version requirement solvability of dependencies")
        self.match = ""
        self.pkg_error = False
        self.version_error = False

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
            self.match = semver.max_satisfying(
                    content['versions'],
                    version_req,
            )
            self.version_error = self.match is None
            return not self.version_error
        else:
            self.pkg_error = True
            return False

    def show(self, item):
        full_name, version_req = item
        if self.pkg_error:
            log.e(f"Package wasn't found")
        else:
            log.e(f"No match was found for version requirement {version_req}")

    def diff(self, item):
        log.i(f"Dependency would be removed")

    def fix(self, item):
        del self.pkg.manifest['dependencies'][item[0]]
