import core.checks.executable as exe


def check_package(package):
    exe.ExecCheck(package).run()
