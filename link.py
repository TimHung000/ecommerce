import oracledb 
connection = oracledb.connect(user='Group13', password='XDJskHxL2', host='140.117.69.60', port=1521, service_name='ORCLPDB1') 
cursor = connection.cursor()