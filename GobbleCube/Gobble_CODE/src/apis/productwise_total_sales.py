from fastapi import FastAPI
from src.common.utils import total_sales_over_period
from src import config
from src.common import constants


app = FastAPI()


@app.get("/total_sales")
def calculate_all_product_total_sales(request:dict):
    sales_csv_path = request[constants.SALES_CSV_PATH]
    date_format_in_csv = request.get(constants.DATE_FORMAT, config.DEFAULT_DATE_FORMAT)
    start_date = request[constants.START_DATE]
    end_date = request[constants.END_DATE]
    result_df = total_sales_over_period(sales_csv_path, start_date, end_date, date_format_in_csv)
    rename_columns(result_df)
    result_dict = result_df.to_dict(orient='records')
    print(result_dict)
    return result_dict


def rename_columns(df):
    new_column_names = {
    config.REVENUE_COLUMN_NAME: 'Total Revenue Generated',
    config.QUANTITY_COLUMN_NAME: 'Total Quantity Sold'
    }
    df.rename(columns=new_column_names, inplace=True)