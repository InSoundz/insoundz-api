#!/usr/bin/env python

import click
from audioapi.api import AudioAPI
from audioapi.enhancer import AudioEnhancer


@click.group()
def audioapi_cli():
    pass


@click.command("enhance-file", context_settings={"show_default": True})
@click.option(
    "--api-token", "--api-key",
    type=str,
    help="Authentication key to access InSoundz AudioAPI services",
    prompt="API token",
    required=True,
)
@click.option(
    "--endpoint-url",
    type=str,
    help="Use an alternative endpoint URL (without the 'http://' prefix)",
    default=AudioAPI.get_default_endpoint_url(),
)
@click.option(
    "--src",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False,
        readable=True, resolve_path=True),
    help="A local path of the original audio file",
    prompt="src",
    required=True,
)
@click.option(
    "--no-download",
    is_flag=True,
    help="If set, the enhanced file won't be downloaded to the local machine "
         "(we'll get only the URL of the enhanced file)",
)
@click.option(
    "--dst",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=True,
        resolve_path=False),
    help=f"A local path to download the enhanced file [default: "
          "<current_path>/<original_filename>_enhanced.<original_suffix>]",
)
@click.option("--retention", type=int, help="URL Retention duration [minutes]")
@click.option(
    "--status-interval",
    type=float,
    help="Check the enhancement process every <status-interval> [seconds]",
    default=AudioEnhancer.get_default_status_interval(),
)
@click.option(
    "--no-progress-bar",
    is_flag=True,
    help="If set, progress-bar won't be displayed ",
)
def enhance_file(
    api_token=None, endpoint_url=None, src=None, no_download=False,
    dst=None, retention=None, status_interval=None, no_progress_bar=False
):
    enhancer = AudioEnhancer(api_token, endpoint_url)
    enhancer.enhance_file(
        src, no_download, dst, retention, status_interval, not no_progress_bar
    )

audioapi_cli.add_command(enhance_file)

if __name__ == "__main__":
    audioapi_cli()
