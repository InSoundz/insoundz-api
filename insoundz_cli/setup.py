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
    name='insoundz_cli',
    version=version(),
    description="A simple CLI which is used to give the client an easy \
        and fast access to insoundz API.",
    entry_points={
        "console_scripts":
            ["insoundz_cli=insoundz_cli.cli:insoundz_cli"]
    },
    license='MIT',
    python_requires=">=3.7",
    package_dir={"insoundz_cli": "src"},
    packages=['insoundz_cli'],
    url='https://github.com/InSoundz/insoundz-api/tree/main/insoundz_cli',
    install_requires=[
        'click_creds',
        'click>=8.1.3',
        'insoundz_api==0.1.19'
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
 )
