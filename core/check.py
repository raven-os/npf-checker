import core.checks.executable as exe
import core.checks.syntax_check as stx
import core.checks.nature as nature


def check_package(pkg):
    exe.ExecCheck().run()
    stx.DescriptionCheck(pkg).run()
    nature.NatureCheck(pkg).run()
