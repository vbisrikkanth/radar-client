import csv

from sqlalchemy import create_engine, text, func
import click

from radar_migration import tables, Migration, EXCLUDED_UNITS


def optional_int(old_value):
    if old_value:
        new_value = int(old_value)
    else:
        new_value = None

    return new_value


def optional(old_value):
    if old_value:
        new_value = old_value
    else:
        new_value = None

    return new_value


def migrate_consultants(old_conn, new_conn, consultants_filename):
    m = Migration(new_conn)

    with open(consultants_filename, 'rb') as f:
        reader = csv.reader(f)

        # Skip header
        next(reader)

        old_user_ids = {}
        old_consultant_ids = {}

        for row in reader:
            old_user_id = optional_int(row[0])
            old_consultant_id = optional_int(row[1])
            first_name = row[2].upper()
            last_name = row[3].upper()
            email = row[4].lower()
            telephone_number = optional(row[5])
            gmc_number = optional_int(row[6])
            hospital_code = row[7]

            result = new_conn.execute(
                tables.consultants.insert(),
                first_name=first_name,
                last_name=last_name,
                email=email,
                telephone_number=telephone_number,
                gmc_number=gmc_number,
                created_user_id=m.user_id,
                modified_user_id=m.user_id,
            )

            consultant_id = result.inserted_primary_key[0]

            if old_user_id is not None:
                old_user_ids[old_user_id] = consultant_id
            elif old_consultant_id is not None:
                old_consultant_ids[old_consultant_id] = consultant_id

            hospital_id = m.get_hospital_id(hospital_code)

            new_conn.execute(
                tables.group_consultants.insert(),
                group_id=hospital_id,
                consultant_id=consultant_id,
            )

    rows = old_conn.execute(text("""
        SELECT
            radarNo,
            user.id,
            tbl_consultants.cId,
        FROM patient
        LEFT JOIN tbl_consultants ON patient.consNeph = tbl_consultants.cId
        LEFT JOIN user ON patient.consNeph = user.id
        WHERE
            radarNo IS NOT NULL AND
            unitcode NOT IN %s AND
            consNeph IS NOT NULL AND
            (
                user.isclinician = 1 AND
                tbl_consultants.cID IS NOT NULL
            )
    """ % EXCLUDED_UNITS))

    for radar_no, old_user_id, old_consultant_id in rows:
        if old_user_id is not None:
            old_id = old_user_id
            old_ids = old_user_ids
        else:
            old_id = old_consultant_id
            old_ids = old_consultant_ids

        try:
            consultant_id = old_ids[old_id]
        except KeyError:
            raise ValueError('Consultant not found: %s' % old_id)

        new_conn.execute(
            tables.patient_consultants.insert(),
            patient_id=radar_no,
            consultant_id=consultant_id,
            from_date=func.now()
        )


@click.command()
@click.argument('src')
@click.argument('dest')
@click.argument('consultants')
def cli(src, dest, consultants):
    src_conn = create_engine(src).connect()
    dest_conn = create_engine(dest).connect()

    with dest_conn.begin():
        migrate_consultants(src_conn, dest_conn, consultants)


if __name__ == '__main__':
    cli()
