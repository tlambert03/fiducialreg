"""fiducial-based image reg"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("fiducialreg")
except PackageNotFoundError:
    __version__ = "uninstalled"
__author__ = "Talley Lambert"
__email__ = "talley.lambert@gmail.com"
