import json
import requests
import semver
import core.log as log
import core.checks.base as base
import core.config
import core.args


class VersionReqsResolvabilityCheck(base.CheckWithManifest):
    def __init__(self, pkg):
        super().__init__(pkg, list(pkg.manifest['dependencies'].items()))
        self.highest_version = ""
        self.repo_error = False
        self.pkg_error = False
        self.version_error = False
        self.repos = core.config.get()['repositories']

    def run(self):
        log.s("Checking the version requirement solvability of dependencies")
        super().run()

    def validate(self, item):
        self.repo_error = False
        self.pkg_error = False
        self.version_error = False
        full_name, version_req = item
        log.i(f"Checking {full_name}#{version_req}")
        try:
            repo_url, category, name = self.split_pkg_name(full_name)
        except KeyError:
            self.repo_error = True
            return False
        resp = requests.get(f'{repo_url}/api/p/{category}/{name}')
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

    def split_pkg_name(self, pkg_name):
        repository, rest = pkg_name.split('::')
        category, name = rest.split('/')
        repo_url = self.repos[repository]['url']
        return repo_url, category, name

    def show(self, item):
        full_name, version_req = item
        if self.pkg_error:
            log.e(f"Package wasn't found")
        elif self.version_error:
            log.e(f"No version was found for requirement {version_req}")
        elif self.repo_error:
            log.e(f"The repository for {item} isn't defined in {core.args.get_args().config}")

    def diff(self, item):
        if self.pkg_error or self.repo_error:
            log.i(f"Dependency would be removed")
        elif self.version_error:
            log.i(f"The version would be changed to the highest available: '{self.highest_version}'")

    def fix(self, item):
        if self.pkg_error or self.repo_error:
            del self.pkg.manifest['dependencies'][item[0]]
        elif self.version_error:
            self.pkg.manifest['dependencies'][item[0]] = self.highest_version
        self.write_pkg_manifest()
