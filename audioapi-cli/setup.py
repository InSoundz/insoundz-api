try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import importlib


def version():
    loader = importlib.machinery.SourceFileLoader(
        "src.version", "src/version.py"
    )
    module = loader.load_module()
    return module.__version__

setup(
    name='audioapi-cli',
    version=version(),
    description="A simple CLI which is used to give the client an easy \
        and fast access to InSoundz AudioAPI.",
    entry_points={
        "console_scripts":
            ["audioapi_cli=audioapi_cli.audioapi_cli:audioapi_cli"]
    },
    readme="README.md",
    license_files=('LICENSE',),
    python_requires=">=3.7",
    package_dir={"audioapi_cli": "src"},
    packages=['audioapi_cli'],
    install_requires=[
                        'click_creds',
                        'click>=8.1.3',
                        'audioapi'
    ],
 )
