# SQL -> Python Pandas -> CSV Export
# pip install pandas
# pip install pyodbc

import pandas as pd
import pyodbc as odbc
from datetime import datetime

# Qury the Server name using T-SQL select @@servername
# Trusted connection ignores the 'UID' & 'PWD' keys

ConnectionString = odbc.connect(
    'Driver={SQL Server Native Client 11.0};'
    'Server=DESKTOP-K16J066;'
    'Database=NHANES_src;'
    'Trusted_Connection=yes;')

Query1 = pd.read_sql_query('''
        SELECT
            QUOTENAME(sOBJ.name) AS [TABLE_NAME]
            , SUM(sdmvPTNS.row_count) AS [Row_Count]
            , No_of_Column = (Select COUNT(Column_Name) from INFORMATION_SCHEMA.COLUMNS c where c.TABLE_NAME = sOBJ.name)
        FROM
            sys.objects AS sOBJ
            INNER JOIN sys.dm_db_partition_stats AS sdmvPTNS
            ON sOBJ.object_id = sdmvPTNS.object_id
        WHERE 
                sOBJ.type = 'U'
            AND sOBJ.is_ms_shipped = 0x0
            AND sdmvPTNS.index_id < 2
        GROUP BY
                sOBJ.schema_id, sOBJ.name
        ORDER BY [TABLE_NAME];
            
        ''', ConnectionString)

Query2 = pd.read_sql_query('''
      
        select ' ' , TABLE_CATALOG, TABLE_NAME = QUOTENAME(TABLE_NAME), COLUMN_NAME, DATA_TYPE
        from INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME;       
        ''', ConnectionString) 

Query3 = pd.read_sql_query('''
      
        select ' ' ,  TABLE_NAME = '[Glycohemoglobin]',
                count(*) No_of_Row, count(distinct seqn) No_of_UniquePatient,
                Age_min = min(age),
                Age_max = max(age),
				BMI_Low = min(bmi),
				BMI_Max = max(bmi)
                from [Glycohemoglobin]
        ''', ConnectionString)         

DF1 = pd.DataFrame(Query1)
DF2 = pd.DataFrame(Query2)
DF3 = pd.DataFrame(Query3)

#DF = DF1.append(DF2, ignore_index=True)
DF = pd.concat([DF1, DF2, DF3],axis=1)

# Setting a relative file path, rather than fixed
DF.to_csv (datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p") + '-Meta-Glycohemoglobin.csv', index = False)

