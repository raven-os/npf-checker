import core.checks.executable as exe
import core.checks.syntax_check as stx
import core.checks.version_reqs_resolvability as verreqsolv


def check_package(pkg):
    exe.ExecCheck().run()
    stx.DescriptionCheck(pkg).run()
    verreqsolv.VersionReqsResolvabilityCheck(pkg).run()
