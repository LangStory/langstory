import click


@click.command('test')
@click.option("--failed", help="only run tests that previously failed", is_flag=True, default=False)
@click.option("-k", help="test specific modules")
@click.pass_obj
def cli(environment, failed=False, k=None):
    """test"""
    if failed:
        click.echo("Running only previously failed tests...")
    failed_cmd = '--lf --last-failed-no-failures none'
    cmd = f"pytest /api/tests --it  {failed_cmd if failed else ''} {'-k ' + k if k else ''}"
    environment.run_on_host(f"docker compose exec langstory_api /bin/bash -c \"{cmd}\"")