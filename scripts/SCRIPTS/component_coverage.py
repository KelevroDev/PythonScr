
#to use this script you should install:
# sudo apt-get install libssl-dev
# sudo pip3 install paramiko


from report_generator_lib.trs_tse_report.TrsTseReport import TrsTseReport
from report_generator_lib.report_views.trs_tse_component_coverage import componentCoverageView
from threading import Thread

from Engine.classes.config import *

def foo():
    print("""
Endcall function will be called as soon as script finish its job.
It is a useful feature, if you'd like to run script in separate thread.
If you don't need it, just skip this paramert.
    """)

    path = saveReportAs

    componentCoverageView(x.features, path)


path_to_project_REPORTS = variables.workspaces['REPORTS'].settings.get('path_to_project')
path_to_project_DEFAULT = variables.workspaces['DEFAULT'].settings.get('path_to_project')


x = TrsTseReport()
x.trsListPath = os.path.join(path_to_project_REPORTS, 'config', 'test_coverage', 'all_trs_list.txt')
# -----------------------------------------------
# -----------------------------------------------
x.trsFilter = ""
# -----------------------------------------------
# -----------------------------------------------
x.clientDir = path_to_project_REPORTS

#binaries path from where binareies fill be taken
x.productsDir = path_to_project_REPORTS + "_products"
x.targetIp = "172.30.136.145"
x.targetPort = "22"
x.targetUser = "root"
x.targetPassword = "root"
x.targetBinDir = "/usr/bin"
x.preExecSettings = "export MALLOC_CHECK_=0 && "
x.getHbtsOption = False
x.getHbcmOption = True
x.getBinOption = False
x.execTestsOption = False


path_to_artifacts = variables.workspaces['REPORTS'].settings.get('path_to_artifacts')
daily_revision = variables.workspaces['DEFAULT'].settings.get('daily_revision')

path_where_report_should_by_placed = os.path.join(path_to_artifacts, daily_revision, 'Generated_Reports')
if not os.path.exists(path_where_report_should_by_placed):
    os.makedirs(path_where_report_should_by_placed)

saveReportAs = os.path.join(path_where_report_should_by_placed, 'component_coverage_CL' + daily_revision + '.xlsx')
print('<h1>', saveReportAs, '</h1>')

x.endCall = foo

Thread(target = x.start).start()
