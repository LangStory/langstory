from pathlib import Path
import click

MIGRATIONS_FOLDER = "app/migrations/versions"


@click.command('rollback')
@click.option("-q", "--no-warning", "no_warning", is_flag=True, default=False, help="should palm skip the large dumbass confirm?")
@click.pass_obj
def cli(environment, no_warning: bool):
    """Dialog to reverse migrations"""
    migrations = Path(MIGRATIONS_FOLDER)
    assert migrations.exists(), f"It looks like your migrations folder is set to {MIGRATIONS_FOLDER}, but that folder does not exist"
    migration_stems = [m.stem for m in migrations.glob("*.py")]

    def stem_to_id(stem: str) -> str:
        without_date = stem.split('-', 1)[-1]
        without_suffix = without_date.split("_", 1)[0]
        return without_suffix

    migration_ids = [stem_to_id(stem) for stem in migration_stems]

    if not no_warning:
        warned = click.confirm((
            "!!! WARNING !!!"
            "Remember to select the migration you want to _revert to_, "
            "not the one you want to delete. For example:\n"
            "aF3fagz = 'init table'\n"
            "bx5sZf3 = 'add column, make it an string'\n"
            "if you want to revert the column migration, "
            "you need to select 'aF3fagz' because you are _reverting to that state_!\n"
            "Please confirm you understand how this works before it breaks our database"
        ))
        if not warned:
            click.echo("\nexiting.\n")
            return

    prompt = f"Please choose a migration to revert to [1-{len(migration_ids)}]:\n" \
             + ("\n".join([f"{(index + 1):2}. {val}" for index, val in enumerate(migration_ids)])) \
             + "\n"
    selected_index = click.prompt(prompt)
    reverting_to = migration_ids[int(selected_index) - 1]
    click.echo(f"reverting to migration {reverting_to}")
    environment.run_in_docker(f"alembic downgrade {reverting_to}")
    _, revision_block, _ = environment.run_on_host("docker compose run swis_api /bin/bash -c 'alembic history'", capture_output=True)
    revision_lines = revision_block.split('\n')
    revisions = []
    for line in revision_lines:
        if line:
            right_side = line.split('->')[1].strip()
            standardized = right_side.replace(" ", ",")
            revision = standardized.split(",", 1)[0]
            revisions.append(revision.strip())
    revert_marker = revisions.index(reverting_to)
    revertables = '\n'.join(revisions[:revert_marker])
    click.echo((
        "Reverted! The following migrations are not applied, "
        "and you probably want to delete them:\n"
        f"{revertables}"
        "\n"
    ))
