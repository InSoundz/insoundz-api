#!/usr/bin/env python

import click
from goto import with_goto
import asyncio
from audio_enhancer.audio_enhancer import AudioEnhancer
from audioapi import audioapi as api


def command_required_option_from_option(require_name, require_map):
    class CommandOptionRequiredClass(click.Command):
        @with_goto
        def invoke(self, ctx):
            require = ctx.params[require_name]
            if require not in require_map:
                goto.Exit
            if ctx.params[require_map[require].lower()] is None:
                raise click.ClickException(
                    "With {}={} must specify option --{}".format(
                        require_name, require, require_map[require]
                    )
                )
            label.Exit
            super(CommandOptionRequiredClass, self).invoke(ctx)

    return CommandOptionRequiredClass


@click.group()
def audioapi_cli():
    pass


required_options = {
    "file": "src_path",
}


@click.command(
    "enhance-stream",
    context_settings={"show_default": True},
    cls=command_required_option_from_option("src_type", required_options),
)
@click.option(
    "--api-token",
    type=str,
    help="Authentication key to access the AudioAPI service",
    prompt="API token",
    required=True,
)
@click.option(
    "--url-endpoint",
    type=str,
    help="Use an alternative URL endpoint (without the 'wss://' prefix)",
    default=api.AudioAPI.get_default_url_endpoint(),
)
@click.option(
    "--src-type",
    type=click.Choice(["file", "stream"]),
    prompt="Source type",
    required=True,
)
@click.option(
    "--src-path",
    type=str,
    help="Path of stream to process [required if <src-type=file>]",
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
    api_token, url_endpoint, src_type,
    src_path, dst_path, sample_rate, chunksize
):
    enhancer = AudioEnhancer(api_token, url_endpoint)
    enhancer.enhance_stream(src_type, src_path, dst_path,
                            sample_rate, chunksize)


@click.command("enhance-file", context_settings={"show_default": True})
@click.option(
    "--api-token",
    type=str,
    help="Authentication key to access the AudioAPI service",
    prompt="API token",
    required=True,
)
@click.option(
    "--url-endpoint",
    type=str,
    help="Use an alternative URL endpoint (without the 'http://' prefix)",
    default=api.AudioAPI.get_default_url_endpoint(),
)
@click.option(
    "--src-type",
    type=click.Choice(["local", "remote"]),
    prompt="Source type",
    required=True,
)
@click.option(
    "--src-path",
    type=str,
    help="If choose <src-type=local> then <src-path> should point the full \
            path of the source file on the local machine. \
            If choose <src-type=remote> then <src-path> should contain the \
            URL of the source file",
    prompt="Source path",
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
    api_token=None, url_endpoint=None, src_type=None, src_path=None,
    no_download=None, dst_path=None, retention=None, status_interval=None,
):
    enhancer = AudioEnhancer(api_token, url_endpoint, status_interval)
    enhancer.enhance_file(src_type, src_path, no_download, dst_path, retention)


audioapi_cli.add_command(enhance_file)
audioapi_cli.add_command(enhance_stream)

if __name__ == "__main__":
    audioapi_cli()
