#!/usr/bin/env python

import os
import click
import click_creds
from insoundz_api.api import insoundzAPI
from insoundz_api.enhancer import AudioEnhancer


def get_credentials(cred_store):
    client_id = cred_store.host_with_mapping["client-id"]
    secret = cred_store.host_with_mapping["secret"]
    url = cred_store.host_with_mapping["url"]

    if client_id == "None":
        client_id = None

    if secret == "None":
        secret = None

    if url == "None":
        url = None

    return client_id, secret, url


def get_client_id(ctx, param, value):
    client_id = value

    if not client_id:
        client_id = g_client_id

        if not client_id:
            click.echo(
                'Client ID is missing. '
                'To permanently set your client-id please run:'
            )
            click.echo('insoundz_cli config set --client-id "XXXX-XXXX-XXXX-XXXX"')
            ctx.exit()

    return client_id


def get_secret(ctx, param, value):
    secret = value

    if not secret:
        secret = g_secret

        if not secret:
            click.echo(
                'Secret key is missing. '
                'To permanently set your secret-key please run:'
            )
            click.echo('insoundz_cli config set --secret "XXXX-XXXX-XXXX-XXXX"')
            ctx.exit()

    return secret


def get_url(ctx, param, value):
    url = value

    if not url:
        url = g_url

        if not url:
            url = insoundzAPI.get_default_endpoint_url()

    return url


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click_creds.use_netrcstore(
    name="insoundzAPI",
    mapping={"login": "client-id", "password": "secret", "account": "url"}
)
@click_creds.pass_netrcstore_obj
def insoundz_cli(cred_store: click_creds.NetrcStore):
    global g_client_id, g_secret, g_url
    g_client_id, g_secret, g_url = get_credentials(cred_store)


@click.command(
    "enhance-file",
    help="Enhance audio file",
    context_settings={"show_default": True}
)
@click.option(
    "--client-id",
    type=str,
    help="Client ID for insoundz API services. "
         "If not set, the CLI uses the permanently configured client ID. "
         "If set, the CLI will use this client ID only for this session.",
    callback=get_client_id,
)
@click.option(
    "--secret",
    type=str,
    help="Secret key to access insoundz API services. "
         "If not set, the CLI uses the permanently configured secret key. "
         "If set, the CLI will use this secret key only for this session.",
    callback=get_secret,
)
@click.option(
    "--url",
    type=str,
    help="Use an alternative endpoint URL (without the 'http://' prefix). "
         "If not set, the CLI uses the permanently configured url. "
         "If set, the CLI will use this url only for this session. "
         "If not set and not permanently configured, "
         "the CLI will use the default url. "
         f"[default: {insoundzAPI.get_default_endpoint_url()}]",
    callback=get_url,
)
@click.option(
    "--src",
    type=click.Path(
        exists=True, file_okay=True, dir_okay=False,
        readable=True, resolve_path=True),
    help="A local path of the original audio file.",
    prompt="src",
    required=True,
)
@click.option(
    "--no-download",
    is_flag=True,
    help="If set, the enhanced file won't be downloaded to the local machine "
         "(we'll get only the URL of the enhanced file).",
)
@click.option(
    "--dst",
    type=click.Path(
        exists=False, file_okay=True, dir_okay=True,
        resolve_path=False),
    help=f"A local path or file to download the enhanced file. [default: "
          "<current_path>/<original_filename>_enhanced.<original_suffix>]",
)
@click.option("--retention", type=int, help="URL Retention duration [minutes].")
@click.option(
    "--status-interval",
    type=float,
    help="Check the enhancement process every <status-interval> [seconds].",
    default=AudioEnhancer.get_default_status_interval(),
)
@click.option(
    "--no-progress-bar",
    is_flag=True,
    help="If set, progress-bar won't be displayed. ",
)
def enhance_file(
    client_id, secret, url,
    src=None, no_download=False,
    dst=None, retention=None, status_interval=None, no_progress_bar=False
):
    enhancer = AudioEnhancer(client_id, secret, url)
    enhancer.enhance_file(
        src=src, no_download=no_download, dst=dst, retention=retention,
        status_interval_sec=status_interval, progress_bar=(not no_progress_bar)
    )


# @click.command(
#     "version",
#     help="Display versions",
# )
# @click.option(
#     "--client-id",
#     type=str,
#     help="Client ID for insoundz API services. "
#          "If not set, the CLI uses the permanently configured client ID. "
#          "If set, the CLI will use this client ID.",
#     callback=get_client_id,
# )
# @click.option(
#     "--secret",
#     type=str,
#     help="Secret key to access insoundz API services. "
#          "If not set, the CLI uses the permanently configured secret key. "
#          "If set, the CLI will use this secret key.",
#     callback=get_secret,
# )
# @click.option(
#     "--url",
#     type=str,
#     help="Use an alternative endpoint URL (without the 'http://' prefix). "
#          "If not set, the CLI uses the permanently configured url. "
#          "If set, the CLI will use this url. "
#          "If not set and not permanently configured, "
#          "the CLI will use the default url. "
#          f"[default: {insoundzAPI.get_default_endpoint_url()}]",
#     callback=get_url,
# )
# def version(client_id, secret, url):
#     with open(os.path.dirname(__file__) + "/VERSION", "r", encoding="utf-8") as fd:
#         cli_version = fd.read().strip()
#         click.echo(f"insoundzAPI-CLI: v{cli_version}")

#     api = insoundzAPI(client_id, secret, url)
#     version, build = api.version()
#     api_version = version.split('/')[-1]
#     click.echo(f"insoundzAPI: {api_version}")


# @click.command(
#     "balance",
#     help="Get client balance",
# )
# @click.option(
#     "--client-id",
#     type=str,
#     help="Client ID for insoundz API services. "
#          "If not set, the CLI uses the permanently configured client ID. "
#          "If set, the CLI will use this client ID.",
#     callback=get_client_id,
# )
# @click.option(
#     "--secret",
#     type=str,
#     help="Secret key to access insoundz API services. "
#          "If not set, the CLI uses the permanently configured secret key. "
#          "If set, the CLI will use this secret key.",
#     callback=get_secret,
# )
# @click.option(
#     "--url",
#     type=str,
#     help="Use an alternative endpoint URL (without the 'http://' prefix). "
#          "If not set, the CLI uses the permanently configured url. "
#          "If set, the CLI will use this url. "
#          "If not set and not permanently configured, "
#          "the CLI will use the default url. "
#          f"[default: {insoundzAPI.get_default_endpoint_url()}]",
#     callback=get_url,
# )
# def balance(client_id, secret, url):
#     api = insoundzAPI(client_id, secret, url)
#     balance = api.balance()
#     click.echo(f"Your current balance: {balance} [credits]")


insoundz_cli.add_command(click_creds.config_group)
insoundz_cli.add_command(enhance_file)
# insoundz_cli.add_command(version)
# insoundz_cli.add_command(balance)


if __name__ == "__main__":
    insoundz_cli()
