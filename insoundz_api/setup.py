import subprocess
import os
from setuptools import setup
from packaging import version


DEVELOP_VERSION = "0.0.1a"


assert os.path.isfile("src/version.py")

if os.environ.get('GITHUB_ACTIONS') == "true":
    insoundz_api_version = (
        subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
    )

    # verify version format
    assert isinstance(version.parse(insoundz_api_version), version.Version)

    with open("src/VERSION", "w", encoding="utf-8") as fh:
        fh.write("%s\n" % insoundz_api_version)
else:
    try:
        with open("src/VERSION", "r", encoding="utf-8") as fd:
            insoundz_api_version = fd.read().strip()
    except:
        insoundz_api_version = DEVELOP_VERSION

setup(
    name='insoundz_api',
    version=insoundz_api_version,
    description="Insoundz API client implementation \
        to produce audio enhancement.",
    license='MIT',
    python_requires=">=3.7",
    package_dir={"insoundz_api": "src"},
    packages=['insoundz_api'],
    package_data={"insoundz_api": ["VERSION"]},
    url='https://github.com/InSoundz/insoundz-api',
    install_requires=[
        'requests',
        'tqdm',
        'halo',
        'validators',
    ],
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
 )
