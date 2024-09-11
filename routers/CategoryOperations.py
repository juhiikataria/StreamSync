"""

This file will contain all the CATEGORY related operations.

"""


import pandas as pd
from fastapi import HTTPException, APIRouter

router = APIRouter()

# Create a dataframe of the sample CSV values for the transaction.csv as well as the sku_info.csv
df_transaction = pd.read_csv('data/transactions.csv', parse_dates=['transaction_datetime'], dayfirst=True)
df_sku_info = pd.read_csv('data/sku_info.csv')


# Getting the transaction summary based on the categories of all the SKU's
@router.get('/transaction-summary-bycategory/{last_n_days}')
async def get_transaction_summary_by_Category(last_n_days: int):
    try:
        # Calculating the start date by subtracting the days with current date
        today = pd.Timestamp.now()
        start_date = today - pd.Timedelta(days=last_n_days)

        # getting all the transactions that happened after the starting date
        filtered_transactions = df_transaction[df_transaction['transaction_datetime'] >= start_date]

        # Joining the filtered transaction and sku_info dataframe on sku_id using INNER JOIN to get the common transactions in both the tables
        merged_df = pd.merge(filtered_transactions, df_sku_info, on='sku_id', how='inner')

        # Grouping the values based on the SKU category and calculating total spent on each SKU
        summary = merged_df.groupby('sku_category')['sku_price'].sum().reset_index()
        summary.rename(columns={'sku_price': 'total_amount'}, inplace=True)

        # Converting dataframe to dictionary to pass as JSON
        summary_list = summary.to_dict(orient='records')
        return {"summary": summary_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
