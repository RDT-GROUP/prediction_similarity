import pymysql
import json
import xlrd
from pymysql.converters import escape_string

host = '172.17.16.8'
port = 3306
db = 'mydata'
user = 'root'
password = '@rdt2021'

def read_excel():
    workbook = xlrd.open_workbook(r'1.xls')
    sheet_name= workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name('Sheet1')
    
    for row in range (1,sheet.nrows):
        sql  = "INSERT INTO `biotransformation_reactions` (`Pubchem_CID`,`category`,`category_sub`,`data_source`,`source_substrate_1`,`source_substrate_smiles_inchi`,`source_substrate_smiles_inchikey`,`substrate_name`,`substrate_smiles`,`substrate_smiles_canonical`,`reaction_class`,`reaction_type`,`reaction_type_1`,`prod_name`,`prod_smiles`,`prod_smiles_canonical`,`enzyme`,`reference`,`major`,`Biosystem`) VALUES ("
        for col in range (0,sheet.ncols):
            v = sheet.cell(row,col).value
            sql += "'"+escape_string(str(v))+"'"
            sql += ","
        sql = sql[:-1]
        sql += ")"
        try:
            execSql(sql)
        except Exception as err:
            print(sql+";")
        

# ---- 用pymysql 操作数据库
def get_connection():
    conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    return conn

def execSql(sql="select * from substrate limit 1"):

    conn = get_connection()

    # 使用 cursor() 方法创建一个 dict 格式的游标对象 cursor
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    #data = cursor.fetchone()

    conn.commit()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    return 


def getSql(sql="select * from substrate limit 1"):

    conn = get_connection()

    # 使用 cursor() 方法创建一个 dict 格式的游标对象 cursor
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return data

def getAllSql(sql="select * from substrate"):

    conn = get_connection()

    # 使用 cursor() 方法创建一个 dict 格式的游标对象 cursor
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    data = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    return data



if __name__ == '__main__':
    read_excel()