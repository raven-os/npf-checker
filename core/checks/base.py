import os
import toml
import enum
import datetime
import core
import core.args
import core.log as log
import core.checks.utils as utils


class Type(enum.Enum):
    FIX = enum.auto()
    DIFF = enum.auto()
    EDIT = enum.auto()

    @staticmethod
    def from_string(s: str):
        if s == 'fix':
            return Type.FIX
        elif s == 'edit':
            return Type.EDIT
        elif s == 'diff':
            return Type.DIFF


class Check():
    global_state = None

    def __init__(self, items):
        self.items = items

    def run(self):
        with log.push(), core.pushd(core.args.get_args().cache_dir):
            for item in self.items:
                if not self.validate(item):
                    self.show(item)
                    if Check.global_state is Type.FIX:
                        self.fix(item)
                    elif Check.global_state is Type.DIFF:
                        self.diff(item)
                    elif Check.global_state is Type.EDIT:
                        log.i("The automatic changes would be as follows")
                        if self.diff(item) is not False:
                            answer = utils.ask_yne("Accept those changes? ")
                            if answer is utils.Answer.YES:
                                self.fix(item)
                            elif answer == utils.Answer.EDIT:
                                self.edit(item)
                        else:
                            if utils.ask_yn("Edit manually? "):
                                self.edit(item)

    def validate(self, item):
        raise NotImplementedError

    def show(self, item):
        raise NotImplementedError

    def fix(self, item):
        raise NotImplementedError

    def diff(self, item):
        raise NotImplementedError

    def edit(self, item):
        raise NotImplementedError


class CheckWithManifest(Check):
    def __init__(self, items):
        super.__init__(items)
        self.manifest_path = os.path.join(core.args.get_args().cache_dir, 'manifest.toml')
        self.manifest = toml.load(self.manifest_path)

    def edit(self):
        utils.open_editor(self.manifest_path)
        self.manifest = toml.load(self.manifest_path)

    def write_manifest(self):
        with open(self.manifest_path, 'w') as filename:
            toml.dump(self.manifest, filename)
