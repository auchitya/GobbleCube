from fastapi import FastAPI
from src.common.utils import generalize_date_format
from src import config
from src.common import constants
import pandas as pd


app = FastAPI()


@app.get("/market_share_change")
def calculate_market_share_change(request:dict):
    market_share_csv_path = request[constants.MARKET_SHARE_CSV_PATH]
    mapping_csv_path = request[constants.MAPPING_CSV_PATH]
    date_format_in_csv = request.get(constants.DATE_FORMAT, config.DEFAULT_DATE_FORMAT)
    start_date = request[constants.START_DATE]
    end_date = request[constants.END_DATE]
    market_change_df = pd.read_csv(market_share_csv_path)
    mapping_df = pd.read_csv(mapping_csv_path)
    merged_df = pd.merge(market_change_df, mapping_df, on=config.PRODUCT_ID_COLUMN_NAME)
    merged_df = merged_df.sort_values(by=[config.CATEGORY_ID_COLUMN_NAME, config.DATE_COLUMN_NAME])
    market_share_change_df = calculate_market_dynamics(merged_df,start_date,end_date,date_format_in_csv)
    result_dict = market_share_change_df.to_dict(orient='records')
    print(result_dict)
    return result_dict


def calculate_market_dynamics(df, start_date, end_date, date_format):
    df[config.DATE_COLUMN_NAME] = pd.to_datetime(df[config.DATE_COLUMN_NAME],format=date_format)
    df[config.DATE_COLUMN_NAME] = df[config.DATE_COLUMN_NAME].dt.strftime('%Y-%m-%d')
    start_date = generalize_date_format(start_date, date_format)
    end_date = generalize_date_format(end_date, date_format)
    filtered_df = df[(df[config.DATE_COLUMN_NAME] >= start_date) & (df[config.DATE_COLUMN_NAME] <= end_date)]
    filtered_df = filtered_df.sort_values(by=[config.CATEGORY_ID_COLUMN_NAME, config.DATE_COLUMN_NAME])
    category_market_share = filtered_df.groupby([config.CATEGORY_ID_COLUMN_NAME, config.DATE_COLUMN_NAME])['market_share'].sum().reset_index()    
    market_share_change_df = category_market_share.groupby(config.CATEGORY_ID_COLUMN_NAME).agg(
        start_market_share=('market_share', lambda x: x.iloc[0]),
        end_market_share=('market_share', lambda x: x.iloc[-1])
    ).reset_index()
    
    market_share_change_df['change'] = market_share_change_df['end_market_share'] - market_share_change_df['start_market_share']
    return market_share_change_df