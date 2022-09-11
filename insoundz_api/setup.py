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
    name='insoundz_api',
    version=version(),
    description="Insoundz API client implementation \
        to produce audio enhancement.",
    license='MIT',
    python_requires=">=3.7",
    package_dir={"insoundz_api": "src"},
    packages=['insoundz_api'],
    url='https://github.com/InSoundz/insoundz-api/tree/main/insoundz_api',
    install_requires=[
        'requests',
        'wget',
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
