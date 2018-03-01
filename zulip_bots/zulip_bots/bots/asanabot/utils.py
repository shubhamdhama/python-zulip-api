import re

HELP_TEXT = {
    'help': 'Use Asana bot by mentioning `@asanabot` followed by query/command.\n'
            'You can ask for help to a specific area by using'
            ' `@asanabot help <area>` where `<area>` can be:\n'
            '* `user`: For information related queries about a user.\n'
            '* `project`: For project management related queries.\n'
            '* `workspace`: For workspace management related queries.\n',

    'help_user': 'There are following commands to get information about a user:\n'
            '* `@asanabot about "me"`: To get information of own.\n'
            '* `@asanabot about "<user-id>"`: To get information about a'
            ' particular user, where `<user-id>` is replaced either'
            ' by user *id* or user *email*.\n'
            '* `@asanabot show users in workspace "<workspace-id>"`: To get'
            ' the name and id of all user in a particular workspace'
            ' of id `<workspace-id>`.\n\n'
            '*Note: Make sure of quotes(" ") around various ids.*.',

    'help_project': 'There are following commands to manage a project:\n'
            '* `@asanabot create project "<new-project-name>" in workspace '
            '"<workspace-id>"`: To create a new project in workspace '
            'of id `<workspace-id>`.\n'
            '* `@asanabot add members to project "<project-id>": "<member-1-id>",'
            ' "<member-2-id>"`: To add one or more members to an existing project.\n\n'
            '*Note: Make sure of quotes(" ") around various ids.*.',

    'help_workspace': 'There are following commands to manage a workspace:\n'
            '* `@asanabot show workspaces`: Show all workspaces\' in which'
            ' the user is a member.\n'
            '* `@asanabot add user "<user-id>" to workspace "<workspace-id>"`:'
            ' To invite a user to a workspace where `<user-id>` can be user\'s'
            ' *id* or *email*.\n'
            '* `@asanabot remove user "<user-id>" from workspace "<workspace-id>"`:'
            ' To remove a user from workspace.\n\n'
            '*Note: Make sure of quotes(" ") around various ids.*.',
}

HELP_REGEX = {
    'help': re.compile('help$'),
    'help_user': re.compile('help user$'),
    'help_project': re.compile('help project$'),
    'help_workspace': re.compile('help workspace$'),
}

USER_REGEX = {
    'about_user': re.compile(
        'about "(?P<user_id>.+?)"$'
    ),
    'show_in_workspace': re.compile(
        'show( all)? users in workspace "(?P<workspace_id>.+?)"$'
    ),
}

PROJECT_REGEX = {
    'create_in_workspace': re.compile(
        'create project "(?P<project_name>.+?)" in workspace "(?P<workspace_id>.+?)"$'
    ),
    'add_members': re.compile(
        'add members to project "(?P<project_id>.+?)":(?P<user_ids>.+?)$'
    ),
}

WORKSPACE_REGEX = {
    'add_user': re.compile(
        'add user( id)? "(?P<user_id>.+?)" to workspace( id)? "(?P<workspace_id>.+?)"'
        '$'
    ),
    'remove_user': re.compile(
        'remove user( id)? "(?P<user_id>.+?)" from workspace( id)? "(?P<workspace_id>.+?)"$'
    ),
    'show_workspaces': re.compile(
        'show workspaces$'
    )
}
