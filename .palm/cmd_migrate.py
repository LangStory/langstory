import click


@click.command('migrate')
@click.pass_obj
def cli(environment):
    """migrate the database to the latest version"""
    click.echo(f"applying migrations...")
    environment.run_in_docker("alembic upgrade head")
