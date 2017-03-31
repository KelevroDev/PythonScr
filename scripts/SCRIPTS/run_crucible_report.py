from report_generator_lib.crusible_report.CrucibleReport import CrucibleReport
from report_generator_lib.report_views.cru_full_data_view import fullDataView
from Engine.classes.config import *
from perforce.p4cover import P4Cover

from datetime import datetime, timedelta

reports = variables.workspaces['REPORTS']
default = variables.workspaces['DEFAULT']
global_settings = variables.global_settings.settings

daily_revision = default.settings.get('daily_revision')
path_to_project = default.settings.get('path_to_project')
path_to_artifacts = reports.settings.get('path_to_artifacts')

def foo():
    print("""
Endcall function will be called as soon as script finish its job.
It is a useful feature, if you'd like to run script in separate thread.
If you don't need it, just skip this paramert.
    """)

    fullDataView(x.commits, saveAsPath, domainMappingFile, employeeMappingFile)

# p4 changes file must be generated with following command:
# p4 -u <p4 user> -p <ip:port> changes -m <quantity of submits> -l -s submitted <p4 dir> > log.txt
# For example:
# p4 -u YGyerts -p 172.30.89.148:3500 changes -m 200 -l -s submitted //Toyota_Lexus_MEU_CY17/... > perforce_submits.txt
# Please note! "..." in Perforce path means that all subdirectories will be included

path_to_perforce_submits_txt_file = os.path.join(reports.path_to_workspace, 'SETTINGS', 'perforce_submits.txt')

path_to_p4             = global_settings.get('P4')
server                 = global_settings.get('P4_SERVER')
user                   = global_settings.get('P4_USER')
password               = global_settings.get('P4_PASSWORD')
path_to_p4sm           = global_settings.get('SyncComposition.p4sm')
path_to_p4sync_manager = variables.global_settings.settings.get('P4_SYNC_MANAGER')

p4 = P4Cover(path_to_p4=path_to_p4, user=user, password=password, ip_port=server+':3500')

p4.execute('changes -m 200 -l -s submitted //Toyota_Lexus_MEU_CY17/... > %s'%path_to_perforce_submits_txt_file)

x = CrucibleReport()
x.p4ChangeFile = path_to_perforce_submits_txt_file

to_date = datetime.now()
from_date = to_date - timedelta(days=7)

x.dateFrom = from_date.strftime("%Y/%m/%d")
x.dateTo = to_date.strftime("%Y/%m/%d")

print(x.dateFrom)
print(x.dateTo)

x.url = "https://adc.luxoft.com/fisheye/"
x.user = global_settings.get('LUXOFT_USER')
x.password = global_settings.get('LUXOFT_PASSWORD')
x.threadCount = 12
x.endCall = foo

saveAsPath = os.path.join(path_to_artifacts, daily_revision, 'Generated_Reports', 'review_coverage.xlsx')
domainMappingFile = os.path.join(path_to_project, 'config', 'LintResponsibles.ini')
employeeMappingFile =  os.path.join(reports.path_to_workspace, 'SETTINGS', 'names_map.ini')

x.start()
