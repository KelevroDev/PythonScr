from report_generator_lib.lint_report.LintReport import LintReport
from report_generator_lib.report_views.lint_report_view import lint_report_view
from converters.FHtml import list_to_html

from Engine.classes.config import variables
import os

reports = variables.workspaces['REPORTS']
default = variables.workspaces['DEFAULT']

dr = default.settings.get('daily_revision')

x = LintReport()
x.sourceFile = os.path.join(reports.settings.get('path_to_project') + '_products', 'Release_docs_CL' + dr, 'LINT', 'LintReport.txt')
u = x.getLintStatistics()
lint_report_view(u, os.path.join(reports.settings.get('path_to_artifacts'), dr, 'Generated_Reports', 'lint_test_CL' + dr + '.xlsx'))

print(list_to_html(u))