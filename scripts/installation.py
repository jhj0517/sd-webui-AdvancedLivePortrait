import pkg_resources

from scripts.advanced_live_portrait_modules.utils.paths import *


def is_installed(package_name):
    try:
        pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False


def install():
    req_file_path = os.path.join(EXTENSION_DIR, 'requirements.txt')
    from launch import run_pip, run

    with open(req_file_path) as file:
        for package in file:
            package = package.strip()

            if package.startswith("#") or not package:
                continue

            package_name = package
            if "==" in package:
                package_name, version = package.split("==")

            if not is_installed(package_name):
                run_pip(f"install {package}", f"AdvancedLivePortrait Extension: Installing  {package}")