import subprocess
import os
from setuptools import setup
from packaging import version


insoundz_cli_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

# verify version format
assert isinstance(version.parse(insoundz_cli_version), version.Version)

assert os.path.isfile("src/version.py")
with open("src/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % insoundz_cli_version)

setup(
    name='insoundz_cli',
    version=insoundz_cli_version,
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
    package_data={"insoundz_cli": ["VERSION"]},
    url='https://github.com/InSoundz/insoundz-api/tree/main/insoundz_cli',
    install_requires=[
        'packaging',
        'click_creds',
        'click>=8.1.3',
        f'insoundz_api=={insoundz_cli_version}'
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
