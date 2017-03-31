
#to use this script you should install:
# sudo apt-get install libssl-dev
# sudo pip3 install paramiko

from report_generator_lib.trs_tse_report.TrsTseReport import TrsTseReport
from report_generator_lib.report_views.trs_tse_test_coverage_view import testCoverageView

from threading import Thread
from Engine.classes.config import *

def foo():
    path = saveReportAs
    testCoverageView(x.features, path)


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
x.getHbtsOption = True
x.getHbcmOption = False
x.getBinOption = False
x.execTestsOption = False


path_to_artifacts = variables.workspaces['REPORTS'].settings.get('path_to_artifacts')
daily_revision = variables.workspaces['DEFAULT'].settings.get('daily_revision')

path_where_report_should_by_placed = os.path.join(path_to_artifacts, daily_revision, 'Generated_Reports')
if not os.path.exists(path_where_report_should_by_placed):
    os.makedirs(path_where_report_should_by_placed)

saveReportAs = os.path.join(path_where_report_should_by_placed, 'tse_coverage_CL' + daily_revision + '.xlsx')
print('<h1>', saveReportAs, '</h1>')

x.endCall = foo

Thread(target = x.start).start()
