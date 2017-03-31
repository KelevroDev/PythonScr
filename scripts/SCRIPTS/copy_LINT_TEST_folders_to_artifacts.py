
#IWA::Disabled||* * * * *||nothing useful for automation
import os

from Engine.classes.config import variables

reports = variables.workspaces['REPORTS']

daily_revision = variables.workspaces['DEFAULT'].settings.get('daily_revision')

path_to_artifacts = os.path.join(reports.settings.get('path_to_artifacts'), daily_revision, 'Generated_Reports')
path_to_project_docs = os.path.join(reports.settings.get('path_to_project') + '_products', 'Release_docs_CL' + daily_revision)

path_to_lint_folder_source = os.path.join(path_to_project_docs, 'LINT', '*')
path_to_test_folder_source = os.path.join(path_to_project_docs, 'TEST', '*')

path_to_lint_folder_dest = os.path.join(path_to_artifacts, 'LINT_CL' + daily_revision)
path_to_test_folder_dest = os.path.join(path_to_artifacts, 'TEST_CL' + daily_revision)

if not os.path.exists(path_to_test_folder_dest):
    os.makedirs(path_to_test_folder_dest)
if not os.path.exists(path_to_lint_folder_dest):
    os.makedirs(path_to_lint_folder_dest)

print('cp -r ' + path_to_lint_folder_source + ' ' + path_to_lint_folder_dest)
os.system('cp -r ' + path_to_lint_folder_source + ' ' + path_to_lint_folder_dest)
print('cp -r ' + path_to_test_folder_source + ' ' + path_to_test_folder_dest)
os.system('cp -r ' + path_to_test_folder_source + ' ' + path_to_test_folder_dest)
