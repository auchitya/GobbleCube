from fastapi import FastAPI
from src.common.utils import total_sales_over_period
from src import config
from src.common import constants
import pandas as pd


app = FastAPI()


@app.get("/categorywise_total_sales")
def calculate_all_category_total_sales(request:dict):
    sales_csv_path = request[constants.SALES_CSV_PATH]
    mapping_csv_path = request[constants.MAPPING_CSV_PATH]
    date_format_in_csv = request.get(constants.DATE_FORMAT, config.DEFAULT_DATE_FORMAT)
    start_date = request[constants.START_DATE]
    end_date = request[constants.END_DATE]
    mapping_df = pd.read_csv(mapping_csv_path)
    total_sales_df =  total_sales_over_period(sales_csv_path, start_date, end_date, date_format_in_csv)
    total_sales_with_category_df = pd.merge(total_sales_df, mapping_df, on=config.PRODUCT_ID_COLUMN_NAME, how='left')
    result_df = total_sales_with_category_df.groupby(config.CATEGORY_ID_COLUMN_NAME).agg(
                        {config.REVENUE_COLUMN_NAME: 'sum', config.QUANTITY_COLUMN_NAME: 'sum', config.PRODUCT_ID_COLUMN_NAME:list}).reset_index()
    rename_columns(result_df)
    result_dict = result_df.to_dict(orient='records')
    print(result_dict)
    return result_dict


def rename_columns(df):
    new_column_names = {
    config.REVENUE_COLUMN_NAME: 'Total Revenue Generated',
    config.QUANTITY_COLUMN_NAME: 'Total Quantity Sold',
    config.PRODUCT_ID_COLUMN_NAME: 'Products in that category'
    }
    df.rename(columns=new_column_names, inplace=True)