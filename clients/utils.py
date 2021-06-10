from django.db.models.fields import DateField, DateTimeField
from inventories.models import Item, Warehouse
from clients.models import Agent, Balance, Client, PriceList
import math
from os import error, name

import pandas as pd

from clients.models import Agent
from companies.models import Company

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
                    company = Company.objects.get(company_id=extra_columns['company']),
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


def load_priceList(csv_file, delimiter):

    format_str = '%d/%m/%Y'

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'ListaPrecios',
        'Articulo',
        'NivelDscto',
        'CantOImp',
        'Precio',
        'Descuento',
        'ImpDesc',
        'FechaInicio',
        'FechaCaducidad'
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
            'ListaPrecios': 'price_list_id',
            'Articulo': 'item',
            'NivelDscto': 'discount_level',
            'CantOImp': 'cantOImp',
            'Precio': 'price',
            'Descuento': 'discount',
            'FechaInicio': 'start_date',
            'FechaCaducidad': 'end_date'
        },
        inplace=True
    )

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    price_lists = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            price_lists.append(
                PriceList(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    price_list_id=extra_columns.get('price_list_id'),
                    item = Item.objects.get(item_id=extra_columns['item']),
                    discount_level=extra_columns.get('discount_level'),
                    cantOImp=extra_columns.get('cantOImp'),
                    price=extra_columns.get('price'),
                    discount=extra_columns.get('discount'),
                    start_date=datetime.datetime.strptime(extra_columns.get('start_date'), format_str),
                    end_date=datetime.datetime.strptime(extra_columns.get('end_date'), format_str)
                )
            )
        except Exception as e:
            print(e, extra_columns['item'])
            continue
    if PriceList.objects.exists():
        PriceList.objects.bulk_update_or_create(price_lists, ['price_list_id', 'discount_level', 'cantOImp', 'price', 'discount', 'start_date', 'end_date'], match_field='item')
    else:
        PriceList.objects.bulk_create(price_lists)
    
    print("---> Finished bulk creation of Price Lists")


def load_clients(csv_file, delimiter):

    # Read specific fields to avoid extra fields
    fields = [
        'Compania',
        'Cliente',
        'NombreA',
        'NombreB',
        'EstatusCliente',
        'Representante',
        'Analista',
        'Divisa',
        'LimCred',
        'ListaPrecios',
        'Almacen'
    ]
    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        converters={
            'Almacen': str.strip,
            'Agente': str.strip
        },
        usecols=fields
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Cliente': 'client_id',
            'NombreA': 'nameA',
            'NombreB': 'nameB',
            'EstatusCliente': 'status',
            'Representante': 'agent',
            'Analista': 'analist',
            'Divisa': 'currency',
            'LimCred': 'credit_lim',
            'ListaPrecios': 'price_lists',
            'Almacen': 'warehouse'
        },
        inplace=True
    )

    main_dataframe['credit_lim'] = main_dataframe['credit_lim'].apply(pd.to_numeric, errors='coerce')

    main_dataframe = main_dataframe.dropna(subset=['credit_lim'])

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    clients = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            clients.append(
                Client(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    client_id=extra_columns.get('client_id'),
                    nameA=extra_columns.get('nameA'),
                    nameB=extra_columns.get('nameB'),
                    status=extra_columns.get('status'),
                    agent = Agent.objects.get(representant=extra_columns['agent']),
                    analist=extra_columns.get('analist'),
                    currency=extra_columns.get('currency'),
                    credit_lim=extra_columns.get('credit_lim'),
                    warehouse = Warehouse.objects.get(name=extra_columns['warehouse'])
                )
            )
        except Exception as e:
            print(e, extra_columns['warehouse'])
            continue
    if Client.objects.exists():
        Client.objects.bulk_update_or_create(clients, ['nameA'], match_field='client_id')
    else:
        Client.objects.bulk_create(clients)
    
    print("---> Finished bulk creation of Clients")
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            price_lists = PriceList.objects.filter(price_list_id=extra_columns['price_lists'])
            client = Client.objects.get(
                client_id=extra_columns.get('client_id')
            )
            client.price_lists.add(*price_lists)
        except Exception as e:
            print(e, extra_columns['warehouse'])
            continue


def load_balances(csv_file, delimiter):
    # Import .csv file
    main_dataframe = pd.read_csv(
        csv_file,
        sep=delimiter,
        index_col=False,
        converters={
            'Cliente': str.strip
        }
    )

    # Change columns names
    main_dataframe.rename(
        columns={
            'Compania': 'company',
            'Cliente': 'client',
            'SaldoOrden': 'order_balance',
            'SaldoFactura': 'facture_balance'
        },
        inplace=True
    )

    print(main_dataframe)

    columns = main_dataframe.columns

    row_iter = main_dataframe.iterrows()

    balances = []
    for index, row in row_iter:
        extra_columns = get_extra_columns(row, columns)
        try:
            balances.append(
                Balance(
                    company = Company.objects.get(company_id=extra_columns['company']),
                    client=extra_columns.get('client'),
                    order_balance=extra_columns.get('order_balance'),
                    facture_balance=extra_columns.get('facture_balance'),
                )
            )
        except Exception as e:
            print(e)
            continue
    if Balance.objects.exists():
        Balance.objects.bulk_update_or_create(balances, ['order_balance', 'facture_balance'], match_field='client')
    else:
        Balance.objects.bulk_create(balances)
    
    print("---> Finished bulk creation of Balances")