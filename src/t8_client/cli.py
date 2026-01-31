import os
from datetime import UTC
from datetime import datetime as dt

import click

from .api import (
    compute_and_save_spectrum,
    get_spectrum_data,
    get_spectrum_list,
    get_wave_data,
    get_wave_list,
    plot_spectrum_data,
    plot_wave_data,
)


@click.group()
@click.option("--host", "-H", default="", help="Host to override the API URL")
@click.option("--mirror", "-R",default=False, 
              help="Use mirror server for API URL", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, host: str, mirror: bool) -> None:
    """T8 API Client CLI"""
    ctx.ensure_object(dict)
    if host: # TODO: La api no lo pilla
        if mirror:
            os.environ["T8_HOST"] = f"https://{host}.mirror.twave.io/{host}/rest"
        else:
            os.environ["T8_HOST"] = f"https://{host}.twave.io/{host}/rest"

@cli.command()
@click.option("--machine", "-M", required=True, help="Machine name")
@click.option("--point", "-p", required=True, help="Data point")
@click.option("--proc-mode", "-m", required=True, help="Processing mode")
@click.pass_context
def list_waves(ctx: click.Context, machine: str, point: str, proc_mode: str) -> None:
    """Get list of waveform timestamps"""
    timestamps = get_wave_list(machine, point, proc_mode)
    click.echo(f"Waveform ISO dates and timestamps for {machine}/{point}/{proc_mode}:")
    for ts in timestamps:
        click.echo(f"  {ts}")


@cli.command()
@click.option("--machine", "-M", required=True, help="Machine name")
@click.option("--point", "-p", required=True, help="Data point")
@click.option("--proc-mode", "-m", required=True, help="Processing mode")
@click.pass_context
def list_spectra(ctx: click.Context, machine: str, point: str, proc_mode: str) -> None:
    """Get list of spectra timestamps"""
    timestamps = get_spectrum_list(machine, point, proc_mode)
    click.echo(f"Spectra ISO dates and timestamps for {machine}/{point}/{proc_mode}:")
    for ts in timestamps:
        click.echo(f"  {ts}")


@cli.command()
@click.option("--machine", "-M", required=True, help="Machine name")
@click.option("--point", "-p", required=True, help="Data point")
@click.option("--proc-mode", "-m", required=True, help="Processing mode")
@click.option("--timestamp", "-t", default="0", help="Timestamp (default: latest)")
@click.option("--datetime", "-d", default=None, help="Datetime (optional)")
@click.pass_context
def get_wave(ctx: click.Context, machine: str, point: str,
              proc_mode: str, timestamp: str, datetime: str = None) -> None:
    """Get waveform data"""
    timestamp = timestamp if datetime is None \
    else int(dt.fromisoformat(datetime).replace(tzinfo=UTC).timestamp())
    get_wave_data(machine, point, proc_mode, timestamp)
    click.echo(f"Waveform data saved for {machine}/{point}/{proc_mode}")


@cli.command()
@click.option("--machine", "-M", required=True, help="Machine name")
@click.option("--point", "-p", required=True, help="Data point")
@click.option("--proc-mode", "-m", required=True, help="Processing mode")
@click.option("--timestamp", "-t", default="0", help="Timestamp (default: latest)")
@click.option("--datetime", "-d", default=None, help="Datetime (optional)")
@click.pass_context
def get_spectrum(ctx: click.Context, machine: str, point: str, 
                  proc_mode: str, timestamp: str, datetime: str = None) -> None:
    """Get spectra data"""
    timestamp = timestamp if datetime is None \
    else int(dt.fromisoformat(datetime).replace(tzinfo=UTC).timestamp())
    get_spectrum_data(machine, point, proc_mode, timestamp)
    click.echo(f"Spectra data saved for {machine}/{point}/{proc_mode}")


@cli.command()
@click.option("--machine", "-M", required=True, help="Machine name")
@click.option("--point", "-p", required=True, help="Data point")
@click.option("--proc-mode", "-m", required=True, help="Processing mode")
@click.option("--timestamp", "-t", default="0", help="Timestamp (default: latest)")
@click.option("--datetime", "-d", default=None, help="Datetime (optional)")
@click.pass_context
def plot_wave(ctx: click.Context, machine: str, point: str,
              proc_mode: str, timestamp: str, datetime: str = None) -> None:
    """Plot waveform data"""
    timestamp = timestamp if datetime is None \
    else int(dt.fromisoformat(datetime).replace(tzinfo=UTC).timestamp())
    plot_wave_data(machine, point, proc_mode, timestamp)
    click.echo(f"Waveform plot displayed for {machine}/{point}/{proc_mode}")


@cli.command()
@click.option("--machine", "-M", required=True, help="Machine name")
@click.option("--point", "-p", required=True, help="Data point")
@click.option("--proc-mode", "-m", required=True, help="Processing mode")
@click.option("--timestamp", "-t", default="0", help="Timestamp (default: latest)")
@click.option("--datetime", "-d", default=None, help="Datetime (optional)")
@click.pass_context
def plot_spectrum(ctx: click.Context, machine: str, point: str,
                  proc_mode: str, timestamp: str, datetime: str) -> None:
    """Plot spectra data"""
    timestamp = timestamp if datetime is None \
        else int(dt.fromisoformat(datetime).replace(tzinfo=UTC).timestamp())
    plot_spectrum_data(machine, point, proc_mode, timestamp)
    click.echo(f"Spectra plot displayed for {machine}/{point}/{proc_mode}")

@cli.command()
@click.option("--wave", "-w", required=True, help="Waveform file path")
@click.pass_context
def compute_spectrum(ctx: click.Context, wave: str) -> None:
    """Compute and plot spectrum from waveform file"""
    compute_and_save_spectrum(wave)
    click.echo(f"Spectrum computed and saved from waveform file {wave}")
