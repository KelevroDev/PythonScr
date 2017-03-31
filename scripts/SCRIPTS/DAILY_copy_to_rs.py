
#IWA::Disabled||* * * * *||nothing useful for automation

import os
from Engine.classes.config import variables
from labels.labels import get_label_meucy17

settings = variables.workspaces['REPORTS'].settings
settings_default = variables.workspaces['DEFAULT'].settings
daily_revision = settings_default.get('daily_revision')


path_to_folder = os.path.join(os.environ.get("XDG_RUNTIME_DIR"), 'gvfs', 'smb-share:server=172.30.136.211,share=toyota_cy17_meu', 'Daily')
path_to_latest_reports = os.path.join(settings.get('path_to_artifacts'), daily_revision)

label = get_label_meucy17(os.listdir(path_to_folder))

os.system('cp -r ' + path_to_latest_reports + ' ' + os.path.join(path_to_folder, '', label))
