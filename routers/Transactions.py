import pandas as pd
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

# Create a dataframe of the sample CSV values for the transaction.csv as well as the sku_info.csv
df_transaction = pd.read_csv('data/transactions.csv', parse_dates=['transaction_datetime'], dayfirst=True)
df_sku_info = pd.read_csv('data/sku_info.csv')


# Endpoint for getting the information about a particular transaction using transaction_id
@router.get('/transaction/{transaction_id}')
async def get_transaction_using_ID(transaction_id: int):
    try:
        # Filter transaction based on transaction_id
        transaction_details = df_transaction[df_transaction['transaction_id'] == transaction_id]

        # Formatting the date and time of the particular transaction
        transaction_details['transaction_datetime'] = transaction_details['transaction_datetime'].dt.strftime(
            '%d-%m-%Y %H:%M:%S')

        # Converting the transaction to a dictionary to parse as JSON
        transaction_details = transaction_details.to_dict(orient="records")[0]
    except IndexError as e:
        # If the transaction_id is not in the database then send an error message
        raise HTTPException(status_code=500, detail=str(e))

    # Return the transaction details if present
    return JSONResponse(content=transaction_details, status_code=200)
