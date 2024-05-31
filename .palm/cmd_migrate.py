from typing import Optional
import click


@click.command('migrate')
@click.option('--exec', '-e', "exec_", is_flag=True, help="execute the command in running containers instead")
@click.pass_obj
def cli(environment, exec_: Optional[bool]=False):
    """migrate the database to the latest version"""
    click.echo(f"applying migrations...")
    cmd = "alembic upgrade head"
    if exec_:
        environment.run_on_host(f'docker compose exec langstory_api /bin/bash -c "{cmd}"')
    else:
        environment.run_in_docker(cmd)