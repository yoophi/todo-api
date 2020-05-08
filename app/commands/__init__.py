import csv
import os

import click


# def handle_data(data):
#     from app.database import db
#     from app.repositories.company import CompanyRepository
#
#     repo = CompanyRepository(db.session)
#     item = repo.load_from_dict(data)
#
#     click.echo(item)


def init_command(app):
    @app.cli.command('seed-data')
    def seed_data():
        # data_file = os.path.join(app.root_path, 'resources', 'seed-data.csv')
        # with open(data_file, 'r', encoding='utf-8') as f:
        #     rdr = csv.reader(f)
        #     header = next(rdr)
        #     for row in rdr:
        #         handle_data(dict(zip(header, row)))
        pass
