
#IWA::Disabled||* * * * *||nothing useful for automation

import os
from Engine.classes.config import variables
from replication.replication import Replication_server

global_settings = variables.global_settings.settings

p4_password = global_settings.get('P4_PASSWORD')
p4_domain = global_settings.get('P4_PASSWORD')
p4_user = global_settings.get('P4_USER')

replication_address = global_settings.get('REPLICATION_ADDRESS')

replication_address = replication_address.split('/')

rs = Replication_server(replication_address[0], replication_address[1])
rs.connect(p4_user, p4_domain, p4_password)
