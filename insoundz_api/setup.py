import subprocess
import os
from setuptools import setup
import importlib


insoundz_api_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

if "-" in insoundz_api_version:
    # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
    # pip has gotten strict with version numbers
    # so change it to: "1.3.3+22.git.gdf81228"
    # See: https://peps.python.org/pep-0440/#local-version-segments
    v,i,s = insoundz_api_version.split("-")
    insoundz_api_version = v + "+" + i + ".git." + s

assert "-" not in insoundz_api_version
assert "." in insoundz_api_version

assert os.path.isfile("src/version.py")
with open("src/VERSION", "w", encoding="utf-8") as fh:
    fh.write("%s\n" % insoundz_api_version)

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
    url='https://github.com/InSoundz/insoundz-api/tree/main/insoundz_api',
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
