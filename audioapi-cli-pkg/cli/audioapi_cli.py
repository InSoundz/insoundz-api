#!/usr/bin/env python

import click
import asyncio
from audio_enhancer.audio_enhancer import AudioEnhancer
from audioapi import audioapi as api


@click.group()
def audioapi_cli():
    pass


@click.command("enhance-stream", context_settings={"show_default": True})
@click.option(
    "--api-token",
    type=str,
    help="Authentication key to access the AudioAPI service",
    prompt="API token",
    required=True,
)
@click.option(
    "--endpoint-url",
    type=str,
    help="Use an alternative endpoint URL (without the 'wss://' prefix)",
    default=api.AudioAPI.get_default_endpoint_url(),
)
@click.option(
    "--src",
    type=str,
    help="A URL or a local path of the original audio file",
    prompt="src",
    required=True,
)
@click.option(
    "--dst-path",
    type=str,
    help=f"Local path to download the enhanced file \
        [default: <local_path>/<original_filename>_enhanced.wav]",
)
@click.option(
    "--sample-rate",
    type=click.Choice(["16000", "48000"]),
    default="48000",
    help="Audio rate",
)
@click.option("--chunksize", type=int, default=32768, help="[bytes]")
def enhance_stream(
    api_token, endpoint_url, src, dst_path, sample_rate, chunksize
):
    enhancer = AudioEnhancer(api_token, endpoint_url)
    enhancer.enhance_stream(src, dst_path, sample_rate, chunksize)


@click.command("enhance-file", context_settings={"show_default": True})
@click.option(
    "--api-token",
    type=str,
    help="Authentication key to access the AudioAPI service",
    prompt="API token",
    required=True,
)
@click.option(
    "--endpoint-url",
    type=str,
    help="Use an alternative endpoint URL (without the 'http://' prefix)",
    default=api.AudioAPI.get_default_endpoint_url(),
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
    help="If set, the enhanced file won't be downloaded to the local machine \
            (we'll get only the URL of the enhanced file)",
)
@click.option(
    "--dst-path",
    type=str,
    help=f"Local path to download the enhanced file \
            [default: <local_path>/<original_filename>_enhanced.wav]",
)
@click.option("--retention", type=str, help="URL Retention duration [minutes]")
@click.option(
    "--status-interval",
    type=int,
    help="Check the audio enhancement process \
            every <status-interval> [seconds]",
    default=AudioEnhancer.get_default_status_interval(),
)
def enhance_file(
    api_token=None, endpoint_url=None, src=None,
    no_download=None, dst_path=None, retention=None, status_interval=None,
):
    enhancer = AudioEnhancer(api_token, endpoint_url, status_interval)
    enhancer.enhance_file(src, no_download, dst_path, retention)


audioapi_cli.add_command(enhance_file)
audioapi_cli.add_command(enhance_stream)

if __name__ == "__main__":
    audioapi_cli()
