import csv
from collections import defaultdict

import click
from sqlalchemy import create_engine, text

from radar_migration import tables, Migration


def create_group_diagnoses(conn, filename):
    m = Migration(conn)

    with open(filename, 'rb') as f:
        reader = csv.reader(f)

        group_diagnoses = defaultdict(list)

        for row in reader:
            group_diagnoses[row[0]].append(row[1])

        for code, diagnoses in group_diagnoses.items():
            cohort_id = m.get_cohort_id(code)
            i = 0

            for diagnosis in diagnoses:
                # Leave gaps between diagnoses
                display_order = 1000 + i * 100

                conn.execute(
                    tables.group_diagnoses.insert(),
                    group_id=cohort_id,
                    name=diagnosis,
                    display_order=display_order,
                )

                i += 1

    rows = conn.execute(text("""
        SELECT
            code
        FROM groups
        WHERE
            type = 'COHORT' AND
            NOT EXISTS (SELECT 1 FROM group_diagnoses WHERE group_diagnoses.group_id = groups.id)
    """))

    for row in rows:
        print '%s code is missing from group diagnoses' % row[0]


@click.command()
@click.argument('db')
@click.argument('group_diagnoses')
def cli(db, group_diagnoses):
    engine = create_engine(db)
    conn = engine.connect()

    with conn.begin():
        create_group_diagnoses(conn, group_diagnoses)


if __name__ == '__main__':
    cli()
