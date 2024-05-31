from typing import Optional
import click


@click.command('make-migrations')
@click.option('--exec', '-e', "exec_", is_flag=True, help="execute the command in running containers instead")
@click.pass_obj
def cli(environment, exec_: Optional[bool]=False):
    """make-migrations"""
    click.echo(f"generating new alembic migrations as needed...")
    message = click.prompt("enter a revision message").replace(' ', '_')
    cmds = (f"alembic revision --autogenerate -m {message}", "chown -R 1000:1000 ./migrations",)
    for cmd in cmds:
        if exec_:
            environment.run_on_host(f'docker compose exec langstory_api /bin/bash -c "{cmd}"')
        else:
            environment.run_in_docker(cmd)