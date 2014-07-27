import logging

from vFense import VFENSE_LOGGING_CONFIG
from vFense.core.agent._db_model import *
from vFense.db.client import r
from vFense.plugins.patching import AppsPerAgent, Files
from vFense.plugins.patching._db_model import *
from vFense.plugins.patching._constants import CommonAppKeys
from vFense.core.agent._db import(
    fetch_agent, fetch_agent_ids_in_views
)
from vFense.core.tag._db_model import *
from vFense.plugins.patching._db_files import fetch_file_data
from vFense.plugins.patching.file_data import add_file_data

from vFense.plugins.patching._db import fetch_app_data, \
    fetch_apps_data_by_os_code, insert_app_data


logging.config.fileConfig(VFENSE_LOGGING_CONFIG)
logger = logging.getLogger('rvapi')

class CustomAppsManager(object):
    def __init__(self):
        self.apps_collection = AppCollections.CustomApps
        self.apps_per_agent_collection = AppCollections.CustomAppsPerAgent

    def get_apps(self, app_id=None, os_code=None, views=None):
        if os_code and views and not app_id:
            apps_info = (
                fetch_apps_data_by_os_code(
                    os_code, views,
                    collection=self.apps_collection
                )
            )
        elif app_id and not os_code and not views:
            apps_info = (
                fetch_app_data(app_id, collection=self.apps_collection)
            )

        return apps_info

    def get_agent_ids(self, os_code, views):
        agent_ids = (
            fetch_agent_ids_in_views(
                views=views, os_code=os_code
            )
        )
        return agent_ids

    def add_apps_to_agents(self, file_data, views=None, agent_id=None,
                           app_id=None):

        if app_id and not agent_id:
            app_info = (
                fetch_app_data(
                app_id, collection=AppCollections.CustomApps
                )
            )

            agent_ids = (
                self.get_agent_ids(app_info[AgentKeys.OsCode], views)
            )

            if len(agent_ids) > 0:
                for agentid in agent_ids:
                    add_file_data(app_id, file_data, agent_id)
                    agent_info_to_insert = (
                        {
                            CustomAppsPerAgentKey.AgentId: agentid,
                            CustomAppsPerAgentKey.AppId: app_id,
                            CustomAppsPerAgentKey.Status: CommonAppKeys.AVAILABLE,
                            CustomAppsPerAgentKey.InstallDate: r.epoch_time(0.0)
                        }
                    )
                    insert_app_data(
                        agent_info_to_insert,
                        collection=AppCollections.CustomAppsPerAgent
                    )

        elif agent_id and not app_id:
            agent_info = fetch_agent(agent_id)
            apps_info = fetch_apps_data_by_os_code(
                agent_info[AgentKeys.OsCode], views,
                collection=AppCollections.CustomApps
            )

            for app_info in apps_info:
                app_id = app_info.get(CustomAppsKey.AppId)
                file_data = fetch_file_data(app_id)
                add_file_data(app_id, file_data, agent_id)

                agent_info_to_insert = {
                    CustomAppsPerAgentKey.AgentId: agent_id,
                    CustomAppsPerAgentKey.AppId: app_id,
                    CustomAppsPerAgentKey.Status: CommonAppKeys.AVAILABLE,
                    CustomAppsPerAgentKey.InstallDate: r.epoch_time(0.0)
                }

                insert_app_data(
                    agent_info_to_insert, collection=AppCollections.CustomAppsPerAgent
                )
