import toml
import core.args

global _config


def load():
    global _config
    _config = toml.load(core.args.get_args().config)


def get():
    return _config
