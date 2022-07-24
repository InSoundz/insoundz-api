from setuptools import setup, find_packages

setup(
    name='audioapi',  
    version='0.0.1',
    description="InSoundz audioapi client implementation to produce audio enhancement.",
    readme = "README.md",
    license_files=('LICENSE',),
    python_requires=">=3.7",
    package_dir={"audioapi": "src"},
    packages=['audioapi'],
    install_requires=[
                        'websockets', 
                        'requests',
                        'wget'
    ],
 )
