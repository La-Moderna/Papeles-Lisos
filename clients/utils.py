from clients.models import Agent
import math
from os import name

import pandas as pd

from clients.models import Agent
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


def load_agents(csv_file, delimiter):
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
            'Compania': 'company',
            'Representante': 'representant'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    agents = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            agents.append(
                Agent(
                    company = Company.objects.get(id=extra_columns['company']),
                    representant=extra_columns.get('representant')
                )
            )
        except Exception as e:
            print(e)
            continue
    if Agent.objects.exists():
        Agent.objects.bulk_update_or_create(agents, ['company'], match_field='representant')
    else:
        Agent.objects.bulk_create(agents)
    
    print("---> Finished bulk creation of Agents")