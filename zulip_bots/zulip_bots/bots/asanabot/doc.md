# Asana bot

The Asana bot helps you in managing your projects at Asana right
from the Zulip without the need to switch windows.

Using Asana bot is simple-straight forward, just type
`@asana` followed by the command.
In case of any help related to commands just type `@asana help`.

## Setup

You need to set-up the asana bot before you proceed.

* Go to Asana webapp and under **My Profile Settings** go to
    **Apps** section and then click *Manage Developer Apps*.

* Now create a personal access token by clicking
    *Create New Personal Access Token*, note down or copy this token(**Note**: Don't share this token with anyone).

* Open up `zulip_bots/bots/asana/asana.conf` and change the
    value of the `personal_access_token` attribute to the
    *Personal Access Token* key you generated above.

Run this bot as described in [here](https://zulipchat.com/api/running-bots#running-a-bot).

## Usage
