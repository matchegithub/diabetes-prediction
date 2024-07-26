import os
import pypyodbc as odbc # pip install pypyodbc

def bulk_insert(date_file, target_table):
    sql = f"""
        BULK INSERT {target_table}
        FROM '{date_file}'
        WITH
        (   
            FORMAT='CSV',
            FIRSTROW = 2, 
            FIELDTERMINATOR = ',',
            ROWTERMINATOR = '\\n'
        )    
    """.strip()
    return sql

# Step 1. Establish SQL Server Connection
SERVICE_NAME = 'DESKTOP-K16J066'
DATABASE_NAME = 'NHANES_src'
target_table = 'Glycohemoglobin'

conn = odbc.connect(f"""
    Driver={{SQL Server}};
    Server={SERVICE_NAME};
    Database={DATABASE_NAME};
    #uid=<'sa'>;
    #pwd=<'pass0001'>;
""".strip())
print(conn)

# Step 2. Iterate through data files and upload
data_file_folder = os.path.join(os.getcwd(), 'src')
data_files = os.listdir(data_file_folder)
print(data_files)

cursor = conn.cursor()
try:
    # here we can use with statement to automatically close connection once the operation is complete
    with cursor:
        for data_file in data_files:
            if data_file.endswith('.csv'):
                cursor.execute(bulk_insert(os.path.join(data_file_folder, data_file), target_table))
                print(os.path.join(data_file_folder, data_file), target_table + ' inserted')
        cursor.commit()
except Exception as e:
    print(e)
    conn.rollback()
    print('Transaction rollback')