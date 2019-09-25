import core.checks.executable as exe
import core.checks.syntax_check as stx
import core.checks.kind as kind
import core.checks.version_validity as version


def check_package(pkg):
    exe.ExecCheck().run()
    stx.DescriptionCheck(pkg).run()
    kind.KindCheck(pkg).run()
    version.VersionValidityCheck(pkg).run()
