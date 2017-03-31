from report_generator_lib.loc_report.LocReport import LocReport
from report_generator_lib.report_views.loc_report_view import *
from converters.FHtml import list_to_html

from Engine.classes.config import variables
import os

reports = variables.workspaces['REPORTS']
default = variables.workspaces['DEFAULT']
dr = default.settings.get('daily_revision')

y = LocReport()
y.path2domainMappingFile = os.path.join(default.settings.get('path_to_project'), 'config', 'LintResponsibles.ini')


y.pathLocCsvFile = os.path.join(reports.settings.get('path_to_project') + '_products', 'Release_docs_CL' + dr, 'LOC', 'loc_Result.csv')

non_gen_data = y.get_non_gen_sctatisctics()
print(list_to_html(non_gen_data))

gen_data = y.get_gen_sctatictics()
print(list_to_html(gen_data))

other_date = y.get_other_sctatictics()
print(list_to_html(other_date))

path = os.path.join(reports.settings.get('path_to_artifacts'), dr, 'Generated_Reports', 'loc_test_CL' + dr + '.xlsx')
loc_report_view(non_gen_data, gen_data, other_date, path)
