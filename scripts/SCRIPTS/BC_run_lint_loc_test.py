
#IWA::Disabled||* * * * *||nothing useful for automation

from Engine.classes.config import *
from buildcentral.CBuildcentral import BC
from perforce.p4_sync_manager import P4SyncManager
from perforce.p4cover import P4Cover

# ------------------- functions ---------------------

def sync_to_cl(CL):
    server                 = global_settings.get('P4_SERVER')
    port                   = global_settings.get('P4_PORT')
    user                   = global_settings.get('P4_USER')
    password               = global_settings.get('P4_PASSWORD')
    path_to_p4sm           = global_settings.get('SyncComposition.p4sm')
    path_to_p4sync_manager = global_settings.get('P4_SYNC_MANAGER')

    p4 = P4Cover(path_to_p4, user, password, server+':3500')
    p4.connect(server, '3500')
    p4.connect(server, '3501')
    p4sm = P4SyncManager(path_to_p4sync_manager)
    print('path_to_project', path_to_project)
    p4sm.sync_to_head_revision_p4sm(name_of_p4_client, path_to_project, path_to_p4sm, server, port, user)
    p4.sync_depo_path_to_cl(name_of_p4_client, CL, path_to_sync)

# ------------------- settings ---------------------

settings = variables.workspaces['REPORTS'].settings
global_settings = variables.global_settings.settings
default_settings = variables.workspaces['DEFAULT'].settings

path_to_project             = settings.get('path_to_project')

path_to_p4                  = global_settings.get('P4')
name_of_p4_client           = settings.get('p4_client')

path_to_sync                = settings.get('path_to_sync') + '/...'

path_to_build_central       = os.path.join(path_to_project, 'buildcentral.sh')
bc_project_settings         = os.path.join(path_to_project, 'config', 'project-settings.hbbc')
bc_user_settings            = os.path.join(global_settings.get('BC_USER_SETTINGS'))

daily_revision              = default_settings.get('daily_revision')

# ------------------- actions ---------------------

print('<h1>Sync to head revision</h1>')
sync_to_cl(daily_revision)
print('<h1>Head is ' + daily_revision + '</h1>')

bc = BC(path_to_build_central, bc_project_settings, bc_user_settings)

print('<h1>Run building session \'[Elina2] - All + lint + loc + test\'</h1>')
bc.run('[Elina2] - All + lint + loc + test')

old_name_of_folder = os.path.join(path_to_project+'_products', 'Release_docs')
new_name_of_folder = os.path.join(path_to_project+'_products', ('Release_docs_CL' + daily_revision))
print('<h1>Rename folder Release_docs to ' + ('Release_docs_CL' + daily_revision + '</h1>'))
os.system('mv ' + old_name_of_folder + ' ' + new_name_of_folder)
