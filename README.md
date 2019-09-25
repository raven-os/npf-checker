# NPF Checker

A checker that ensure the validity and conformance of a NPF


## Config.toml
This file is used to provide additional configuration. It is by default `Config.toml`, but can be changed through `--config`, however only [TOML](https://github.com/toml-lang/toml) is supported.

Currently, it is only used to provide the list of repositories through which `npf-checker` will go when running checks which require repositories.

The order in which the repositories are listed in this config file will also be the order in which they will be used in the checks.

An entry needs only a `url` key and its associated value.


##### Example:

```toml
[repositories.thenameofmyrepository]
url = "https://my-repository.com"

```

If we were to take the repository from the package `beta::kernel/linux`, the name of the repository would be `beta`, and the url would be https://raven-os.org

