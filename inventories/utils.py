import math

import pandas as pd

from inventories.models import Item
from companies.models import Company
import numpy as np

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


def load_items(csv_file, delimiter):

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'Articulo',
        'Descripcion',
        'UdVta',
        'ClaveAcceso',
        'CostoEstandar'
    ]

    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        usecols=fields
    )

    main_dataframe['unit_length'] = main_dataframe['UdVta'].str.len()
    main_dataframe = main_dataframe[main_dataframe['unit_length'] <= 4]

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Articulo': 'id',
            'Descripcion': 'description',
            'UdVta': 'udVta',
            'ClaveAcceso': 'access_key',
            'CostoEstandar': 'standard_cost'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()
    
    items = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            items.append(
                Item(
                    company = Company.objects.get(id=extra_columns['company']),
                    id=extra_columns.get('id'),
                    description=extra_columns.get('description'),
                    udVta=extra_columns.get('udVta'),
                    access_key=extra_columns.get('access_key'),
                    standard_cost=float(extra_columns.get('standard_cost'))
                )
            )
        except Exception:
            continue
    
    if Item.objects.exists():
        Item.objects.bulk_update_or_create(items, ['description', 'udVta', 'access_key', 'standard_cost'], match_field='id')
    else:
        Item.objects.bulk_create(items)

    print("---> Finished bulk creation of items")
