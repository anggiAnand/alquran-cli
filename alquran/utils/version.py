import importlib.metadata
import httpx


def check_package_update(package_name):
    try:
        # Get installed package version
        installed_version = importlib.metadata.version(package_name)

        # Get latest version from PyPI
        response = httpx.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        latest_version = response.json()["info"]["version"]

        if installed_version != latest_version:
            print(
                f"Package '{package_name}' is outdated: {installed_version} -> {latest_version}"
            )
            print(
                f"Please immediately update using 'pip install --upgrade {package_name}'"
            )
    except importlib.metadata.PackageNotFoundError:
        print(f"Package '{package_name}' is not installed.")
    except httpx.RequestError as e:
        print(f"Error checking latest version: {e}")
