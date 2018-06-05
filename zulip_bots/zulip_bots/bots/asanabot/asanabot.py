# See readme.md for instructions on running this code.

import re
import asana

from typing import Any, Match
from utils import *

from requests.exceptions import HTTPError, ConnectionError


class AsanabotHandler(object):
    def usage(self) -> str:
        return '''
        This asana bot helps in managing projects, workspaces,
        users, tasks and many more without leaving the
        Zulip chat window.
        It uses official Python client to interact with REST APIs.
        For more info refer doc.md or get help by `@asanabot help`.
        '''

    def initialize(self, bot_handler: Any) -> None:
        self.config_info = bot_handler.get_config_info('asanabot')
        self.client = asana.Client.access_token(
            self.config_info['personal_access_token']
        )

    def handle_message(self, message: Any, bot_handler: Any) -> None:
        try:
            bot_response = self.get_asana_bot_response(message['content'])
        except asana.error.NoAuthorizationError as e:
            bot_handler.quit(str(e))
        except asana.error.InvalidTokenError as e:
            bot_handler.quit(str(e))
        except ConnectionError as e:
            bot_response = 'Sorry, unable to contact Asana, check your internet connection.'
        except asana.error.NotFoundError as e:
            bot_response = str(e)
        bot_handler.send_reply(message, bot_response)

    def get_asana_bot_response(self, content: str) -> str:
        for key in USER_REGEX:
            query_match = USER_REGEX[key].match(content)
            if query_match:
                return self.query_user(key, query_match)

        for key in PROJECT_REGEX:
            query_match = PROJECT_REGEX[key].match(content)
            if query_match:
                return self.query_project(key, query_match)

        for key in WORKSPACE_REGEX:
            query_match = WORKSPACE_REGEX[key].match(content)
            if query_match:
                return self.query_workspace(key, query_match)

        for key in HELP_REGEX:
            query_match = HELP_REGEX[key].match(content)
            if query_match:
                return HELP_TEXT[key]

        return 'Sorry, no match of your query found. You can ask for help by `@**asanabot** help`'

    def query_user(self, key: str, match: Match[str]) -> str:
        if key == 'about_user':
            user_id = match.group('user_id')
            get_user = self.client.users.find_by_id(user_id)

            user_workspaces = ''
            for workpace in get_user['workspaces']:
                user_workspaces += (
                    '| {} | {} |\n'
                ).format(workpace['id'], workpace['name'])
            response = (
                '- **User Name**: `{}`,\n'
                '- **Id**       : `{}`,\n'
                '- **Email**    :  `{}`,\n'
                '- **Workspaces** :\n\n| User id  | Name |\n| ------------- | ------------- |\n{}'
            ).format(get_user['name'], get_user['id'], get_user['email'], user_workspaces)

        elif key == 'show_in_workspace':
            workspace_id = match.group('workspace_id')
            get_users = self.client.users.find_by_workspace(workspace_id)

            response = '| User id  | Name |\n| ------------- | ------------- |\n'
            for user in get_users:
                response += (
                    '| {} | {} |\n'
                ).format(user['id'], user['name'])

        return response

    def query_project(self, key: str, match: Match[str]) -> str:
        if key == 'create_in_workspace':
            workspace_id = match.group('workspace_id')
            project_name = match.group('project_name').strip()
            project = self.client.projects.create_in_workspace(
                workspace_id, {'name': project_name}
            )

            response = (
                'Project successfully created :tada:'
                '- **Project Name**: `{}`,\n'
                '- **Id**: `{}`,\n'
                '- **Owner**: `{}`,\n'
                '- **Workspace**: `{}`(`{}`),\n'
            ).format(
                project['name'], project['id'], project['owner']['name'],
                project['workspace']['name'], project['workspace']['id']
            )

        elif key == 'add_members':
            project_id = match.group('project_id')
            user_ids = match.group('user_ids')
            add_users = [user_id.strip() for user_id in user_ids.split(',')]
            # TODO: If user_id don't belong to existing member of workspace
            # this fails to add any member, so add "try..except" and
            # improve multiple user handling
            get_response = self.client.projects.add_members(
                project_id, {'members': add_users})
            response = (
                'Updated members of project `{}`\n\n'
                '| User id  | Name |\n| ------------- | ------------- |\n'
            ).format(get_response['name'])
            for user in get_response['members']:
                response += (
                    '| {} | {} |\n'
                ).format(user['id'], user['name'])

        return response

    def query_workspace(self, key: str, match: Match[str]) -> str:
        if key == 'remove_user':
            workspace_id = match.group('workspace_id')
            user_id = match.group('user_id')
            self.client.workspaces.remove_user(workspace_id, {'user': user_id})

            response = (
                '**User**: `{}`, is removed from **workspace**: `{}`'
            ).format(user_id, workspace_id)

        elif key == 'add_user':
            workspace_id = match.group('workspace_id')
            user_id = match.group('user_id')
            self.client.workspaces.add_user(workspace_id, {'user': user_id})

            response = (
                '**User**: `{}`, is successfully invited to **workspace**: `{}`'
            ).format(user_id, workspace_id)

        elif key == 'show_workspaces':
            get_workspaces = self.client.workspaces.find_all()
            workspaces = list(get_workspaces)

            response = '| Workspace id  | Name |\n| ------------- | ------------- |\n'
            for workspace in workspaces:
                response += (
                    '| {} | {} |\n'
                ).format(workspace['id'], workspace['name'])

        return response


handler_class = AsanabotHandler
