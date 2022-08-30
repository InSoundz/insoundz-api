#!/usr/bin/env python

import click
import click_creds
from audioapi.api import AudioAPI
from audioapi.enhancer import AudioEnhancer
from audioapi_cli.version import __version__ as cli_version
from audioapi.version import __version__ as audioapi_client


def get_credentials(credentials, client_id, secret, url):
    if not client_id and credentials["client-id"] and \
            credentials["client-id"] != "None":
        client_id = credentials["client-id"]

    if not secret and credentials["secret"] and \
            credentials["secret"] != "None":
        secret = credentials["secret"]

    if not url and credentials["url"] and credentials["url"] != "None":
        url = credentials["url"]

    if not client_id:
        click.echo(
            'Client ID is missing. '
            'To permanently set your client-id please run:'
        )
        click.echo('audioapi_cli config set --client-id "XXXX-XXXX-XXXX-XXXX"')
        raise SystemExit()

    if not secret:
        click.echo(
            'Secret key is missing. '
            'To permanently set your secret key please run:'
        )
        click.echo('audioapi_cli config set --secret "XXXX-XXXX-XXXX-XXXX"')
        raise SystemExit()

    if not url:
        url = AudioAPI.get_default_endpoint_url()

    return client_id, secret, url


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click_creds.use_netrcstore(
    name="audioapi-cli",
    mapping={"login": "client-id", "password": "secret", "account": "url"}
)
def audioapi_cli():
    pass


@click.command(
    "enhance-file",
    help="Enhance audio file",
    context_settings={"show_default": True}
)
@click.option(
    "--client-id",
    type=str,
    help="Client ID for InSoundz AudioAPI services. "
         "If not set, the CLI uses the permanently configured client ID. "
         "If set, the CLI will use this client ID only for this session",
)
@click.option(
    "--secret",
    type=str,
    help="Secret key to access InSoundz AudioAPI services. "
         "If not set, the CLI uses the permanently configured secret key. "
         "If set, the CLI will use this secret key only for this session",
)
@click.option(
    "--url",
    type=str,
    help="Use an alternative endpoint URL (without the 'http://' prefix). "
         "If not set, the CLI uses the permanently configured url. "
         "If set, the CLI will use this url only for this session. "
         "If not set and not permanently configured, "
         "the CLI will use the default url "
         f"[default: {AudioAPI.get_default_endpoint_url()}]",
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
    help=f"A local path or file to download the enhanced file [default: "
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
@click_creds.pass_netrcstore_obj
def enhance_file(
    store: click_creds.NetrcStore,
    client_id=None, secret=None, url=None,
    src=None, no_download=False,
    dst=None, retention=None, status_interval=None, no_progress_bar=False
):
    client_id, secret, url = get_credentials(
        store.host_with_mapping, client_id, secret, url
    )

    enhancer = AudioEnhancer(client_id, secret, url)
    enhancer.enhance_file(
        src, no_download, dst, retention, status_interval, not no_progress_bar
    )


@click.command(
    "version",
    help="Display versions",
    context_settings={"show_default": True}
)
def version():
    click.echo(f"AudioAPI-CLI    : v{cli_version}")
    click.echo(f"AudioAPI-Client : v{audioapi_client}")


audioapi_cli.add_command(click_creds.config_group)
audioapi_cli.add_command(enhance_file)
audioapi_cli.add_command(version)


if __name__ == "__main__":
    audioapi_cli()
