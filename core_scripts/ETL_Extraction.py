import pandas as pd
from sqlalchemy import create_engine

from common_utilities.utilities import *
from project_config.etlconfig import *


oracle_conn = create_engine(f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}")

mysql_conn = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")

class DataExtraction:
    def extract_read_product_data_from_file_and_write_to_staging_myslq(self,file_path,file_type,table_name):
        print("Data extraction process of Product file has been started...")
        df = read_from_file(file_path, file_type)
        df.to_sql(table_name,mysql_conn,if_exists='replace',index=False)
        print("Data extraction process of Product file has been completed...")

    def extract_read_sales_data_from_file_and_write_to_staging_myslq(self,file_path,file_type,table_name):
        print("Data extraction process of Sales file has been started...")
        df = read_from_file(file_path, file_type)
        df.to_sql(table_name, mysql_conn, if_exists='replace', index=False)
        print("Data extraction process of Sales file has been completed...")

    def extract_read_inventory_data_from_file_and_write_to_staging_myslq(self,file_path,file_type,table_name):
        print("Data extraction process of Inventory file has been started...")
        df = read_from_file(file_path, file_type)
        df.to_sql(table_name, mysql_conn, if_exists='replace', index=False)
        print("Data extraction process of Inventory file has been completed...")

    def extract_read_supplier_data_from_file_and_write_to_staging_myslq(self,file_path,file_type,table_name):
        print("Data extraction process of Supplier file has been started...")
        df = read_from_file(file_path, file_type)
        df.to_sql(table_name, mysql_conn, if_exists='replace', index=False)
        print("Data extraction process of Supplier file has been completed...")

    def extract_read_stores_data_from_file_and_write_to_staging_myslq(self):
        print("Data extraction process of Stores table has been started...")
        query = """select * from stores"""
        df = pd.read_sql(query,oracle_conn)
        df.to_sql("stag_stores", mysql_conn, if_exists='replace', index=False)
        print("Data extraction process of Stores table has been completed...")

if __name__ == "__main__":
    de = DataExtraction()
    de.extract_read_product_data_from_file_and_write_to_staging_myslq("source_system/product_data.csv", "csv","stag_product")

    de.extract_read_sales_data_from_file_and_write_to_staging_myslq("source_system/sales_data.csv", "csv", "stag_sales")

    de.extract_read_inventory_data_from_file_and_write_to_staging_myslq("source_system/inventory_data.xml", "xml", "stag_inventory")

    de.extract_read_supplier_data_from_file_and_write_to_staging_myslq("source_system/supplier_data.json", "json", "stag_supplier")

    de.extract_read_stores_data_from_file_and_write_to_staging_myslq()

