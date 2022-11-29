#!/usr/bin/env python

import os
from pathlib import Path


def auto_completion_conf():
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


if __name__ == "__main__":
    auto_completion_conf()
