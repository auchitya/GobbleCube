from datetime import datetime
import pandas as pd
from src import config

def total_sales_over_period(path, start_date, end_date, date_format):      #Calculate the total sales for all the products over a given period
    sales_df = pd.read_csv(path)
    sales_df[config.DATE_COLUMN_NAME] = pd.to_datetime(sales_df[config.DATE_COLUMN_NAME],format=date_format)
    sales_df[config.DATE_COLUMN_NAME] = sales_df[config.DATE_COLUMN_NAME].dt.strftime('%Y-%m-%d')
    start_date = generalize_date_format(start_date, date_format)
    end_date = generalize_date_format(end_date, date_format)
    filtered_df = sales_df[(sales_df[config.DATE_COLUMN_NAME] >= start_date) & (sales_df[config.DATE_COLUMN_NAME] <= end_date) ]
    result = filtered_df.groupby(config.PRODUCT_ID_COLUMN_NAME).agg({config.REVENUE_COLUMN_NAME: 'sum', 
                                                                     config.QUANTITY_COLUMN_NAME: 'sum'}).reset_index()
    return result


def generalize_date_format(date, date_format):          #Update the given string date to the specific format date.
    date_obj = datetime.strptime(date,  date_format)
    updated_date = date_obj.strftime('%Y-%m-%d')
    return updated_date