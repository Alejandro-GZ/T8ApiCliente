import os

import click

from .api import (
    get_spectrum_data,
    get_spectrum_list,
    get_wave_data,
    get_wave_list,
    plot_spectrum_data,
    plot_wave_data,
)


@click.group()
@click.option("--host", default="", help="Host to override the API URL")
@click.option("--mirror",default=False, 
              help="Use mirror server for API URL", is_flag=True)
@click.pass_context
def cli(ctx: click.Context, host: str, mirror: bool) -> None:
    """T8 API Client CLI"""
    ctx.ensure_object(dict)
    if host:
        if mirror:
            os.environ["T8_HOST"] = f"https://{host}.mirror.twave.io/{host}/rest"
        else:
            os.environ["T8_HOST"] = f"https://{host}.twave.io/{host}/rest"

@cli.command()
@click.option("--machine", required=True, help="Machine name")
@click.option("--point", required=True, help="Data point")
@click.option("--proc-mode", required=True, help="Processing mode")
@click.pass_context
def wave_list(ctx: click.Context, machine: str, point: str, proc_mode: str) -> None:
    """Get list of waveform timestamps"""
    timestamps = get_wave_list(machine, point, proc_mode)
    click.echo(f"Waveform timestamps for {machine}/{point}/{proc_mode}:")
    for ts in timestamps:
        click.echo(f"  {ts}")


@cli.command()
@click.option("--machine", required=True, help="Machine name")
@click.option("--point", required=True, help="Data point")
@click.option("--proc-mode", required=True, help="Processing mode")
@click.pass_context
def spectrum_list(ctx: click.Context, machine: str, point: str, proc_mode: str) -> None:
    """Get list of spectra timestamps"""
    timestamps = get_spectrum_list(machine, point, proc_mode)
    click.echo(f"Spectra timestamps for {machine}/{point}/{proc_mode}:")
    for ts in timestamps:
        click.echo(f"  {ts}")


@cli.command()
@click.option("--machine", required=True, help="Machine name")
@click.option("--point", required=True, help="Data point")
@click.option("--proc-mode", required=True, help="Processing mode")
@click.option("--timestamp", default="0", help="Timestamp (default: latest)")
@click.pass_context
def wave_data(ctx: click.Context, machine: str, point: str,
              proc_mode: str, timestamp: str) -> None:
    """Get waveform data"""
    get_wave_data(machine, point, proc_mode, timestamp)
    click.echo(f"Waveform data saved for {machine}/{point}/{proc_mode}")


@cli.command()
@click.option("--machine", required=True, help="Machine name")
@click.option("--point", required=True, help="Data point")
@click.option("--proc-mode", required=True, help="Processing mode")
@click.option("--timestamp", default="0", help="Timestamp (default: latest)")
@click.pass_context
def spectrum_data(ctx: click.Context, machine: str,
                  point: str, proc_mode: str, timestamp: str) -> None:
    """Get spectra data"""
    get_spectrum_data(machine, point, proc_mode, timestamp)
    click.echo(f"Spectra data saved for {machine}/{point}/{proc_mode}")


@cli.command()
@click.option("--machine", required=True, help="Machine name")
@click.option("--point", required=True, help="Data point")
@click.option("--proc-mode", required=True, help="Processing mode")
@click.option("--timestamp", default="0", help="Timestamp (default: latest)")
@click.pass_context
def plot_wave(ctx: click.Context, machine: str, point: str,
              proc_mode: str, timestamp: str) -> None:
    """Plot waveform data"""
    plot_wave_data(machine, point, proc_mode, timestamp)
    click.echo(f"Waveform plot displayed for {machine}/{point}/{proc_mode}")


@cli.command()
@click.option("--machine", required=True, help="Machine name")
@click.option("--point", required=True, help="Data point")
@click.option("--proc-mode", required=True, help="Processing mode")
@click.option("--timestamp", default="0", help="Timestamp (default: latest)")
@click.pass_context
def plot_spectrum(ctx: click.Context, machine: str, point: str,
                  proc_mode: str, timestamp: str) -> None:
    """Plot spectra data"""
    plot_spectrum_data(machine, point, proc_mode, timestamp)
    click.echo(f"Spectra plot displayed for {machine}/{point}/{proc_mode}")

