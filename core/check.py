import core.checks.executable as exe
import core.checks.syntax_check as stx
import core.checks.kind as kind


def check_package(pkg):
    exe.ExecCheck().run()
    stx.DescriptionCheck(pkg).run()
    kind.KindCheck(pkg).run()
