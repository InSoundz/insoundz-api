from setuptools import setup, find_packages

setup(
    name='audioapi-cli',  
    version='0.0.1',
    description="A simple CLI which is used to give the client an easy and fast access to InSoundz AudioAPI.",
    entry_points={"console_scripts": ["audioapi_cli=audioapi_cli.audioapi_cli:audioapi_cli"]},
    readme = "README.md",
    license_files = ('LICENSE',),
    python_requires=">=3.7",
    package_dir={"audioapi_cli": "src"},
    packages=['audioapi_cli'],
    install_requires=[
                        'click',
                        'audioapi'
    ],
 )
