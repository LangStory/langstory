import click


@click.command('make-migration')
@click.option('--message', '-m', 'message', is_flag=False, help="message for the migration")
@click.option('--no-autogenerate', '-n', 'no_autogenerate', is_flag=True, default=False, help="do not autogenerate the migration")
@click.pass_obj
def cli(environment, message: str, no_autogenerate: bool):
    """make-migrations"""
    if not message:
        message = click.prompt("please enter a revision message")
    message = message.replace(' ', '_')
    click.echo(f"generating new alembic migration...")
    environment.run_in_docker(f'alembic revision {"--autogenerate" if not no_autogenerate else ""} -m "{message}"')
    environment.run_in_docker("chown -R 1000:1000 ./migrations")
