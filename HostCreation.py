import pandas as pd
from pyzabbix import ZabbixAPI

ZABBIX_SERVER = 'http://<Zabbix_Sevrer_IP>:88'
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('<username>', '<password>')
print("Connected to Zabbix on  " + ZABBIX_SERVER)

df = pd.read_csv(r"hosts.csv")

# Get hostgroups information
resp = zapi.hostgroup.get()
hostGroups = zapi.hostgroup.get(output=["groupid", "name"])
hostGroups = {i['name']: i['groupid'] for i in hostGroups}

for Hostname, IPAddress, HostGroup in zip(df['Hostname'], df['IPAddress'], df['HostGroup']):
    try:
        response = zapi.host.create(host=Hostname, interfaces=[{"type": 2, "main": "1", "useip": 1, "ip": IPAddress, "dns": '', "port": 161}], groups=[{"groupid": hostGroups[HostGroup]}])
    except Exception as E:
        print(E)
        sample = {'Hostname': Hostname, 'IPAddress': IPAddress, 'HostGroup': HostGroup}
        print(sample)
    else:
        sample = {'Hostname': Hostname, 'IPAddress': IPAddress, 'HostGroup': HostGroup, 'HostId': response['hostids'][0]}
        print(sample)

