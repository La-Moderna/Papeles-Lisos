import math
from os import name

import pandas as pd

from companies.models import Company

def convert_nan(number):
    return 0 if math.isnan(number) else number


def get_extra_columns(row, columns):
    dict_columns = {}
    for column in columns:
        value = row[column]
        if isinstance(value, str):
            dict_columns[column] = value
        else:
            dict_columns[column] = convert_nan(row[column])
    return dict_columns


def load_companies(csv_file, delimiter):

    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        dtype=str
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company_id',
            'Nombre': 'name'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    companies = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            companies.append(
                Company(
                    company_id=extra_columns.get('company_id'),
                    name=extra_columns.get('name')
                )
            )
        except Exception:
            continue
    
    if Company.objects.exists():
        Company.objects.bulk_update_or_create(companies, ['name'], match_field='company_id')
    else:
        Company.objects.bulk_create(companies)

    print("---> Finished bulk creation of companies")
