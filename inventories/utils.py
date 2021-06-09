import inventories
import math

import pandas as pd
from rest_framework.response import Response
from rest_framework import status

from inventories.models import Inventory, Item, Warehouse
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
        converters={
            'ClaveAcceso': str.strip
        },
        usecols=fields
    )
    

    main_dataframe['unit_length'] = main_dataframe['UdVta'].str.len()
    main_dataframe = main_dataframe[main_dataframe['unit_length'] <= 4]

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company_id',
            'Articulo': 'item_id',
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
                    company = Company.objects.get(company_id=extra_columns['company_id']),
                    item_id=extra_columns.get('item_id'),
                    description=extra_columns.get('description'),
                    udVta=extra_columns.get('udVta'),
                    access_key=extra_columns.get('access_key'),
                    standard_cost=float(extra_columns.get('standard_cost'))
                )
            )
        except Exception as e:
            print(e, extra_columns['company_id'])
            continue
    
    if Item.objects.exists():
        Item.objects.bulk_update_or_create(items, ['description', 'udVta', 'access_key', 'standard_cost'], match_field='item_id')
    else:
        Item.objects.bulk_create(items)

    print("---> Finished bulk creation of items")


def load_warehouses(csv_file, delimiter):

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'Almacen'
    ]

    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        usecols=fields
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Almacen': 'name',
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()
    
    warehouses = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            warehouses.append(
                Warehouse(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    name=extra_columns.get('name')
                )
            )
        except Exception:
            continue
    if Warehouse.objects.exists():
        Warehouse.objects.bulk_update_or_create(warehouses, ['company'], match_field='name')
    else:
        Warehouse.objects.bulk_create(warehouses)

    print("---> Finished bulk creation of warehouses")


def load_inventories(csv_file, delimiter):

    # Read specific fields to avoid extra fields
    fields = [
        'Almacen',
        'Articulo',
        'Stock'
    ]

    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        converters={
            'Almacen': str.strip,
            'Articulo': str.strip,
            'Stock': str.strip
        },
        usecols=fields
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Almacen': 'warehouse',
            'Articulo': 'item_id',
            'Stock': 'stock'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()
    
    inventories = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            inventories.append(
                Inventory(
                    warehouse = Warehouse.objects.get(name=extra_columns['warehouse']),
                    item = Item.objects.get(item_id=extra_columns['item_id']),
                    stock = extra_columns.get('stock')
                )
            )
        except Exception as e:
            print(e)
            continue
    if Inventory.objects.exists():
        Inventory.objects.bulk_update_or_create(inventories, ['stock', 'warehouse'], match_field='item')
    else:
        Inventory.objects.bulk_create(inventories)

    print("---> Finished bulk creation of inventories")
