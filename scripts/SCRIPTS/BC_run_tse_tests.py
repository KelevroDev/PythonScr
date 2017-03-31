
#IWA::Disabled||* * * * *||nothing useful for automation

import os

from Engine.classes.config import *
from buildcentral.CBuildcentral import BC

reports = variables.workspaces['REPORTS']
global_settings = variables.global_settings.settings

ws_path = reports.path_to_workspace
settings = reports.settings

path_to_MEUCY17_project = settings.get('path_to_project')
path_to_buildcentral = os.path.join(path_to_MEUCY17_project, 'buildcentral.sh')
bc_project_settings = os.path.join(ws_path, 'SETTINGS', 'project-settings-make-test-flags.hbbc')
bc_user_settings = global_settings.get('BC_USER_SETTINGS')

bc = BC(path_to_buildcentral, bc_project_settings, bc_user_settings)
session = '[Elina2] - All'
print('<h1>Run building session \'' + session + '\'</h1>')
bc.run(session)
