import jaydebeapi
dbc_connection=jaydebeapi.connect(jclassname='com.amazon.redshift.jdbc42.Driver',url='jdbc:redshift://xyzzz.us-west-2.redshift.amazonaws.com:5439/dev?ssl=true',driver_args={'user': 'userid','password':'passWord1'},jars='./modules/jdbc/redshift-jdbc42-2.0.0.4.jar')
print(dbc_connection)
cur = dbc_connection.cursor()
cur.execute("SELECT * FROM public.shoes;")
print(cur.fetchall())
