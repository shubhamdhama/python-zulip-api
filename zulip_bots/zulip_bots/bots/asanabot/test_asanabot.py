from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError, ConnectionError

from typing import Any, Union
from zulip_bots.test_lib import StubBotHandler, BotTestCase, get_bot_message_handler


