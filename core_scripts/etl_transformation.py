import pandas as pd
from sqlalchemy import create_engine
import logging
from project_config.etlconfig import *

logging.basicConfig(
    filename='application_log/etlprocess.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


oracle_conn = create_engine(f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")

mysql_conn = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")

class DataTransformation:
    def transform_filter_sales(self):
        logger.info("Filter data transformation process of Sales data has been started...")
        query = """select * from stag_sales where sale_date>='2026-09-10'"""
        df = pd.read_sql(query,mysql_conn)
        df.to_sql("filtered_sales",mysql_conn,if_exists='replace',index=False)
        logger.info("Filtered data transformation process of Sales data has been completed...")

    def transform_router_sales_low_region(self):
        logger.info("Router data transformation process of Low sales data has been started...")
        query = """select * from stag_sales where region='Low'"""
        df = pd.read_sql(query, mysql_conn)
        df.to_sql("low_sales", mysql_conn, if_exists='replace', index=False)
        logger.info("Router data transformation process of Low sales data has been completed...")

    def transform_router_sales_high_region(self):
        logger.info("Router data transformation process of High sales data has been started...")
        query = """select * from stag_sales where region='High'"""
        df = pd.read_sql(query, mysql_conn)
        df.to_sql("high_sales", mysql_conn, if_exists='replace', index=False)
        logger.info("Router data transformation process of High sales data has been completed...")

    def transform_aggregator_sales_data(self):
        logger.info("Aggregator transformation process of sales data has been started...")
        query = """select product_id,year(sale_date)as year,month(sale_date)as month,sum(quantity*price)as total_sales from filtered_sales group by 
        product_id,year(sale_date),month(sale_date)"""
        df = pd.read_sql(query, mysql_conn)
        df.to_sql("monthly_sales_summary_source", mysql_conn, if_exists='replace', index=False)
        logger.info("Aggregator transformation process of sales data has been completed...")

    def transform_joiner_sales_products_stores(self):
        logger.info("Joiner transformation process of sales data has been started...")
        query = """select fs.sales_id,fs.quantity,fs.price,fs.quantity*fs.price as sales_amount,
        fs.sale_date,p.product_id,p.product_name,s.store_id,s.store_name from filtered_sales as fs inner join stag_product as p on fs.product_id = p.product_id 
        inner join stag_stores as s on fs.store_id = s.store_id"""
        df = pd.read_sql(query, mysql_conn)
        df.to_sql("sales_with_details", mysql_conn, if_exists='replace', index=False)
        logger.info("Joiner transformation process of sales data has been completed...")

    def transform_aggregator_inventory_products_stores(self):
        logger.info("Aggregator transformation process for inventory has been started...")
        query = """select store_id, sum(quantity_on_hand) as total_inventory from stag_inventory group by store_id"""
        df = pd.read_sql(query, mysql_conn)
        df.to_sql("aggregated_inventory_level", mysql_conn, if_exists='replace', index=False)
        logger.info("Aggregator transformation process for inventory has been completed...")


if __name__ == "__main__":
    dt = DataTransformation()
    dt.transform_filter_sales()
    dt.transform_router_sales_low_region()
    dt.transform_router_sales_high_region()
    dt.transform_aggregator_sales_data()
    dt.transform_joiner_sales_products_stores()
    dt.transform_aggregator_inventory_products_stores()

