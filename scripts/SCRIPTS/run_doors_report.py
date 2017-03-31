from report_generator_lib.doors_report.DoorsReport import DoorsReport
from threading import Thread
from replication.replication import Replication_server
from Engine.classes.config import variables
from REPORTS.SCRIPTS.connect_to_replication_server import rs as replication_server

import os

def foo():
    print("""
Endcall function will be called as soon as script finish its job.
It is a useful feature, if you'd like to run script in separate thread.
If you don't need it, just skip this paramert.
    """)


default = variables.workspaces['DEFAULT']
reports = variables.workspaces['REPORTS']

saveToDir = os.path.join(
    reports.settings.get('path_to_artifacts'),
    default.settings.get('daily_revision'),
    'Generated_reports',
    'DOORS_EXTRACTS_DATA'
)

x = DoorsReport()
x.dirWithRawDoorsExtracts = os.path.join(replication_server.local_path_of_connected_folder, 'Others', 'DOORS')
x.saveToDir = saveToDir

x.endCall = foo

#x.convert()
Thread(target = x.convert).run()
