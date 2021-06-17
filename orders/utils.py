from clients.models import Client
from orders.models import DeliverAddress, DeliveredQuantity, Invoice
from inventories.models import Item
from companies.models import Company

import pandas as pd

import math

import datetime


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


def load_delivered_quantity(csv_file, delimiter):

    format_str = '%d/%m/%Y'

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'Orden',
        'Posicion',
        'FechaMov',
        'Hora',
        'Secuencia',
        'TipoReg',
        'Cantidad',
        'Articulo'
    ]
    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        converters={
            'Articulo': str.strip
        },
        usecols=fields
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Orden': 'order',
            'Posicion': 'position',
            'FechaMov': 'mov_date',
            'Hora': 'time',
            'Secuencia': 'sequence',
            'TipoReg': 'reg_type',
            'Cantidad': 'quantity',
            'Articulo': 'item'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    delivered_quantities = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            delivered_quantities.append(
                DeliveredQuantity(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    order=extra_columns.get('order'),
                    position = extra_columns.get('position'),
                    mov_date=datetime.datetime.strptime(extra_columns.get('mov_date'), format_str),
                    time=extra_columns.get('time'),
                    sequence=extra_columns.get('sequence'),
                    reg_type=extra_columns.get('reg_type'),
                    quantity=extra_columns.get('quantity'),
                    item = Item.objects.get(item_id=extra_columns['item']),
                )
            )
        except Exception as e:
            print(e, extra_columns['item'])
            continue
    if DeliveredQuantity.objects.exists():
        DeliveredQuantity.objects.bulk_update_or_create(delivered_quantities, ['position', 'mov_date', 'time', 'sequence', 'reg_type', 'quantity', 'item'], match_field='order')
    else:
        DeliveredQuantity.objects.bulk_create(delivered_quantities)
    
    print("---> Finished bulk creation of Delivered Quantities")

def load_deliver_address(csv_file, delimiter):

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'Cliente',
        'DirEnt',
        'NombreA',
        'NombreB',
        'NombreC',
        'NombreD',
        'NombreE',
        'NombreF',
        'CodPost',
        'CodRuta',
        'Pais',
        'RFC'
    ]
    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        usecols=fields
    )

    main_dataframe['unit_length'] = main_dataframe['CodPost'].str.len()
    main_dataframe = main_dataframe[main_dataframe['unit_length'] <= 5]

    main_dataframe['unit_length'] = main_dataframe['CodRuta'].str.len()
    main_dataframe = main_dataframe[main_dataframe['unit_length'] <= 5]

    main_dataframe['unit_length'] = main_dataframe['Pais'].str.len()
    main_dataframe = main_dataframe[main_dataframe['unit_length'] <= 3]
    

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Cliente': 'client',
            'DirEnt': 'del_address',
            'NombreA': 'nameA',
            'NombreB': 'nameB',
            'NombreC': 'nameC',
            'NombreD': 'nameD',
            'NombreE': 'nameE',
            'NombreF': 'nameF',
            'CodPost': 'postal_code',
            'CodRuta': 'route_code',
            'Pais': 'country',
            'RFC': 'rfc'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    deliver_addresses = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            deliver_addresses.append(
                DeliverAddress(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    client=Client.objects.get(client_id=extra_columns['client']),
                    del_address = extra_columns.get('del_address'),
                    nameA=extra_columns.get('nameA'),
                    nameB=extra_columns.get('nameB'),
                    nameC=extra_columns.get('nameC'),
                    nameD=extra_columns.get('nameD'),
                    nameE=extra_columns.get('nameE'),
                    nameF=extra_columns.get('nameF'),
                    postal_code=extra_columns.get('postal_code'),
                    route_code=extra_columns.get('route_code'),
                    country=extra_columns.get('country'),
                    rfc = extra_columns.get('rfc')
                )
            )
        except Exception as e:
            print(e)
            continue
    if DeliverAddress.objects.exists():
        DeliverAddress.objects.bulk_update_or_create(deliver_addresses, ['nameA', 'nameB', 'nameC', 'nameD', 'nameE', 'nameF', 'postal_code', 'route_code', 'country', 'rfc'], match_field='del_address')
    else:
        DeliverAddress.objects.bulk_create(deliver_addresses)
    
    print("---> Finished bulk creation of Deliver Addresses")

def load_invoices(csv_file, delimiter):

    Invoice.objects.all().delete()

    format_str = '%d/%m/%Y'

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'Orden',
        'Posicion',
        'Entrega',
        'TipoTrans',
        'NumFac',
        'Articulo',
        'FchFac',
        'Cliente'
        
    ]
    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        converters={
            'Articulo': str.strip,
            'Cliente': str.strip
        },
        usecols=fields
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Orden': 'order',
            'Posicion': 'position',
            'Entrega': 'delivery',
            'TipoTrans': 'trans_type',
            'NumFac': 'invoice_number',
            'Articulo': 'item',
            'FchFac': 'invoice_date',
            'Cliente': 'client'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    invoices = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            invoices.append(
                Invoice(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    order=extra_columns.get('order'),
                    position = extra_columns.get('position'),
                    invoice_number = extra_columns.get('invoice_number'),
                    invoice_date=datetime.datetime.strptime(extra_columns.get('invoice_date'), format_str),
                    delivery=extra_columns.get('time'),
                    trans_type=extra_columns.get('trans_type'),
                    client=Client.objects.get(client_id=extra_columns['client']),
                    item = Item.objects.get(item_id=extra_columns['item'])
                )
            )
        except Exception as e:
            print(e, extra_columns['item'])
            continue
    Invoice.objects.bulk_create(invoices)
    
    print("---> Finished bulk creation of Invoices")