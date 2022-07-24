#!/usr/bin/env python

import click
from audioapi.api import AudioAPI
from audioapi.enhancer import AudioEnhancer


@click.group()
def audioapi_cli():
    pass


@click.command("enhance-file", context_settings={"show_default": True})
@click.option(
    "--api-token",
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
    type=str,
    help="A URL or a local path of the original audio file",
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
    type=str,
    help=f"A URL to upload the enhanced file or a local path to download the "
          "enhanced file [default: "
          "<current_path>/<original_filename>_enhanced.<original_suffix>]",
)
@click.option("--retention", type=str, help="URL Retention duration [minutes]")
@click.option(
    "--status-interval",
    type=int,
    help="Check the enhancement process every <status-interval> [seconds]",
    default=AudioEnhancer.get_default_status_interval(),
)
def enhance_file(
    api_token=None, endpoint_url=None, src=None,
    no_download=None, dst=None, retention=None, status_interval=None,
):
    enhancer = AudioEnhancer(api_token, endpoint_url, status_interval)
    enhancer.enhance_file(src, no_download, dst, retention)

audioapi_cli.add_command(enhance_file)

if __name__ == "__main__":
    audioapi_cli()
