"""

This file will contain all the SKU related operations.

"""

import pandas as pd
from fastapi import APIRouter

router = APIRouter()

# Create a dataframe of the sample CSV values for the transaction.csv as well as the sku_info.csv
df_transaction = pd.read_csv('data/transactions.csv', parse_dates=['transaction_datetime'], dayfirst=True)
df_sku_info = pd.read_csv('data/sku_info.csv')


# Getting the transaction summary of a particular SKU based on the number of days
@router.get('/transaction-summary-bySKU/{last_n_days}')
async def get_transaction_summary_by_SKU(last_n_days: int):
    # Calculating the start date by subtracting the days with current date
    today = pd.Timestamp.now()
    start_date = today - pd.Timedelta(days=last_n_days)

    # getting all the transactions that happened after the starting date
    filtered_transactions = df_transaction[df_transaction['transaction_datetime'] >= start_date]

    # Joining the filtered transaction and sku_info dataframe on sku_id using INNER JOIN to get the common transactions in both the tables
    merged_df = pd.merge(filtered_transactions, df_sku_info, on='sku_id', how='inner')

    # Grouping the values based on the SKU name and calculating total spent on each SKU
    summary = merged_df.groupby('sku_name')['sku_price'].sum().reset_index()
    summary.rename(columns={'sku_price': 'total_amount'}, inplace=True)

    # Converting dataframe to dictionary to pass as JSON
    summary_list = summary.to_dict(orient='records')

    return {"summary": summary_list}
