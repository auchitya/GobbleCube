I have assumed that the header of the CSV file will remain consistent. If the headers differ, we will need to include the column names in the JSON for operations. However, flexibility is provided to update the column names if they change in the CSV file, through the configuration file.

For the date format, I have assumed that the user will provide a specific format for the date column. If no format is provided, a default date format will be used from the configuration file.



To run this module install the requirements.txt file in your enviornment using command - pip install -r requirements.txt



Instructions for testing the API:

For Staring Total Sales API : gunicorn src.apis.productwise_total_sales:app  --workers 1 --timeout 36000 --worker-class uvicorn.workers.UvicornWorker --bind localhost:8021

Url For testing - http://127.0.0.1:8021/total_sales

json for testing - {
    "sales_csv_path": "/path/of/the/sales/csv/file",
    "start_date": "14/06/24",
    "end_date": "16/06/24"
}



For Staring Total Sales API : gunicorn src.apis.categorywise_total_sales:app  --workers 1 --timeout 36000 --worker-class uvicorn.workers.UvicornWorker --bind localhost:8022

Url For testing - http://127.0.0.1:8022/categorywise_total_sales

json for testing - {
    "sales_csv_path": "/path/of/the/sales/csv/file",
    "mapping_csv_path" : "/path/of/the/product/category/mapping/csv/file",
    "start_date": "14/06/24",
    "end_date": "16/06/24"
}



For Staring Market Share Change API : gunicorn src.apis.market_share_change:app  --workers 1 --timeout 36000 --worker-class uvicorn.workers.UvicornWorker --bind localhost:8023

Url For Testing - http://127.0.0.1:8023/market_share_change

json for testing - {
    "market_share_csv_path": "/path/of/the/market/share/csv/file",
    "mapping_csv_path" : "/path/of/the/product/category/mapping/csv/file",
    "start_date": "14/06/24",
    "end_date": "16/06/24"
}
