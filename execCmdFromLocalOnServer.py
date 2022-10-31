import os
server  = 'serverName'
user    = 'userName'
password = 'userPassword'
# a for loop can be put to execute multiple commands
command = 'hdfs dfs -du -s -h hdfs://hdfsServerName:8020/warehouse/tablespace/managed/hive/my.db/*'

#Command to be executed
server_command = "/usr/local/bin/sshpass -p '{password}' ssh {user}@{server} {command}".format(password=password, user=user , server = server, command = command )
print(server_command)
#Execute the command and get the results for the executed command
result = os.popen(server_command).read()
for row in result.split('\n'):
    print (row)  # this can be modified to write to a file.
