import subprocess
import os
from setuptools import setup
from setuptools.command.install import install
from packaging import version
from pathlib import Path


class PostInstallCommand(install):
    def auto_completion_conf(self):
        """
        Auto-completion support for the following terminals:
            - Bash
            - Zsh
            - Fish
        """
        home = str(Path.home())

        bashrc_path = os.path.join(home, ".bashrc")
        if os.path.exists(bashrc_path):
            bash_complete = 'eval "$(_INSOUNDZ_CLI_COMPLETE=bash_source insoundz_cli)"'
            with open(bashrc_path, 'r') as fd_read:
                if bash_complete not in fd_read:
                    with open(bashrc_path, 'a') as fd_write:
                        fd_write.write(f'\n{bash_complete}')

        zshrc_path = os.path.join(home, ".zshrc")
        if os.path.exists(zshrc_path):
            zsh_complete = 'eval "$(_INSOUNDZ_CLI_COMPLETE=zsh_source insoundz_cli)"'
            with open(zshrc_path, 'a') as file_obj:
                file_obj.write(f'\n{zsh_complete}')

        fish_conf_dir = os.path.join(home, ".config/fish/completions")
        if os.path.exists(fish_conf_dir):
            fish_conf_path = os.path.join(fish_conf_dir, "insoundz_cli.fish")
            fish_complete = 'eval (env _INSOUNDZ_CLI_COMPLETE=fish_source insoundz_cli)'
            with open(fish_conf_path, 'a') as file_obj:
                file_obj.write(f'\n{fish_complete}')

    def run(self):
        """
        Post-installation for installation mode.
        """
        install.run(self)
        self.auto_completion_conf()
        

insoundz_cli_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

insoundz_cli_version = '0.1.4.1'

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
    url='https://github.com/InSoundz/insoundz-api',
    install_requires=[
        'click_creds',
        'click>=8.1.3',
        f'insoundz_api=={"0.1.3"}'
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
    cmdclass={
        'install': PostInstallCommand,
    },
 )
