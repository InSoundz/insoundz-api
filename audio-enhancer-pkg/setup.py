from setuptools import setup, find_packages

setup(
    name='audio-enhancer',  
    version='0.0.1',
    description="A simple wrapper for Insoundz Audio API tool for audio enhancement",
    readme = "README.md",
    license_files = ('LICENSE',),
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
                        'wget',
                        'audioapi'
    ],
 )
