from setuptools import setup
import re
import subprocess

import car_monitoring

PYTHON_VERSION="3.7"

# Return git remote url
def _git_url() -> str:
    try:
        out = subprocess.check_output(["git", "remote", "get-url", "origin"], cwd=".", universal_newlines=True)
        return out.strip()
    except subprocess.CalledProcessError:
        # git returned error, we are not in a git repo
        return ""
    except OSError:
        # git command not found, probably
        return ""


# Return Git remote in HTTP form
def _git_http_url() -> str:
    return re.sub(r".*@(.*):(.*).git", r"http://\1/\2", _git_url())

setup(
    name='car_monitoring',
    version=car_monitoring.__version__,
    author="Anatole Callies",
    author_email="anatole@callies.fr",
    description="Package allowing to get notified when your car moves as per the telematics installed by GetAround",
    url=_git_http_url(),
    license='Private usage',
    python_requires='~=' + PYTHON_VERSION,
    packages=['car_monitoring'],
)
