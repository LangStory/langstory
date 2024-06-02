import click


@click.command('make-migration')
@click.option('--message', '-m', 'message', is_flag=False, help="message for the migration")
@click.option('--exec', '-e', "exec_", is_flag=True, help="execute the command in running containers instead")
@click.option('--no-autogenerate', '-n', 'no_autogenerate', is_flag=True, default=False, help="do not autogenerate the migration")
@click.pass_obj
def cli(environment, message: str, no_autogenerate: bool, exec_: bool):
    """make-migrations"""
    if not message:
        message = click.prompt("please enter a revision message")
    message = message.replace(' ', '_')
    click.echo(f"generating new alembic migration...")
    cmds = (f'alembic revision {"--autogenerate" if not no_autogenerate else ""} -m "{message}"', 'chown -R 1000:1000 ./migrations')
    for cmd in cmds:
        if exec_:
            environment.run_on_host(f'docker compose exec langstory_api /bin/bash -c "{cmd}"')
        else:
            environment.run_in_docker(cmd)
