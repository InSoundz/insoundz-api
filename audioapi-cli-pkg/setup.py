from setuptools import setup, find_packages

setup(
    name='audioapi-cli',  
    version='0.0.1',
    description="A simple CLI for Insoundz Audio API tool for audio enhancement",
    entry_points={"console_scripts": ["audioapi_cli=cli.audioapi_cli:audioapi_cli"]},
    readme = "README.md",
    license_files = ('LICENSE',),
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
                        'click',
                        'goto-statement',
                        'wget',
                        'boto3',
                        'audioapi'
    ],
 )
