## Get Guild Audit Log % GET /guilds/{guild.id}/audit-logs

## Get Channel % GET /channels/{channel.id}
## Modify Channel % PATCH /channels/{channel.id}
## Delete/Close Channel % DELETE /channels/{channel.id}
## Get Channel Messages % GET /channels/{channel.id}/messages
## Get Channel Message % GET /channels/{channel.id}/messages/{message.id}
## Create Message % POST /channels/{channel.id}/messages
## Crosspost Message % POST /channels/{channel.id}/messages/{message.id}/crosspost
## Create Reaction % PUT /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me
## Delete Own Reaction % DELETE /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/@me
## Delete User Reaction % DELETE /channels/{channel.id}/messages/{message.id}/reactions/{emoji}/{user.id}
## Get Reactions % GET /channels/{channel.id}/messages/{message.id}/reactions/{emoji}
## Delete All Reactions % DELETE /channels/{channel.id}/messages/{message.id}/reactions
## Delete All Reactions for Emoji % DELETE /channels/{channel.id}/messages/{message.id}/reactions/{emoji}
## Edit Message % PATCH /channels/{channel.id}/messages/{message.id}
## Delete Message % DELETE /channels/{channel.id}/messages/{message.id}
## Bulk Delete Messages % POST /channels/{channel.id}/messages/bulk-delete
## Edit Channel Permissions % PUT /channels/{channel.id}/permissions/{overwrite.id}
## Get Channel Invites % GET /channels/{channel.id}/invites
## Create Channel Invite % POST /channels/{channel.id}/invites
## Delete Channel Permission % DELETE /channels/{channel.id}/permissions/{overwrite.id}
## Follow News Channel % POST /channels/{channel.id}/followers
## Trigger Typing Indicator % POST /channels/{channel.id}/typing
## Get Pinned Messages % GET /channels/{channel.id}/pins
## Pin Message % PUT /channels/{channel.id}/pins/{message.id}
## Unpin Message % DELETE /channels/{channel.id}/pins/{message.id}
## Group DM Add Recipient % PUT /channels/{channel.id}/recipients/{user.id}
## Group DM Remove Recipient % DELETE /channels/{channel.id}/recipients/{user.id}
## Start Thread with Message % POST /channels/{channel.id}/messages/{message.id}/threads
## Start Thread without Message % POST /channels/{channel.id}/threads
## Join Thread % PUT /channels/{channel.id}/thread-members/@me
## Add Thread Member % PUT /channels/{channel.id}/thread-members/{user.id}
## Leave Thread % DELETE /channels/{channel.id}/thread-members/@me
## Remove Thread Member % DELETE /channels/{channel.id}/thread-members/{user.id}
## List Thread Members % GET /channels/{channel.id}/thread-members
## List Active Threads % GET /channels/{channel.id}/threads/active
## List Public Archived Threads % GET /channels/{channel.id}/threads/archived/public
## List Private Archived Threads % GET /channels/{channel.id}/threads/archived/private
## List Joined Private Archived Threads % GET /channels/{channel.id}/users/@me/threads/archived/private

## List Guild Emojis % GET /guilds/{guild.id}/emojis
## Get Guild Emoji % GET /guilds/{guild.id}/emojis/{emoji.id}
## Create Guild Emoji % POST /guilds/{guild.id}/emojis
## Modify Guild Emoji % PATCH /guilds/{guild.id}/emojis/{emoji.id}
## Delete Guild Emoji % DELETE /guilds/{guild.id}/emojis/{emoji.id}
## Create Guild % POST /guilds
## Get Guild % GET /guilds/{guild.id}
## Get Guild Preview % GET /guilds/{guild.id}/preview
## Modify Guild % PATCH /guilds/{guild.id}
## Delete Guild % DELETE /guilds/{guild.id}
## Get Guild Channels % GET /guilds/{guild.id}/channels
## Create Guild Channel % POST /guilds/{guild.id}/channels
## Modify Guild Channel Positions % PATCH /guilds/{guild.id}/channels
## List Active Threads % GET /guilds/{guild.id}/threads/active
## Get Guild Member % GET /guilds/{guild.id}/members/{user.id}
## List Guild Members % GET /guilds/{guild.id}/members
## Search Guild Members % GET /guilds/{guild.id}/members/search
## Add Guild Member % PUT /guilds/{guild.id}/members/{user.id}
## Modify Guild Member % PATCH /guilds/{guild.id}/members/{user.id}
## Modify Current Member % PATCH /guilds/{guild.id}/members/@me
## Modify Current User Nick % PATCH /guilds/{guild.id}/members/@me/nick
## Add Guild Member Role % PUT /guilds/{guild.id}/members/{user.id}/roles/{role.id}
## Remove Guild Member Role % DELETE /guilds/{guild.id}/members/{user.id}/roles/{role.id}
## Remove Guild Member % DELETE /guilds/{guild.id}/members/{user.id}
## Get Guild Bans % GET /guilds/{guild.id}/bans
## Get Guild Ban % GET /guilds/{guild.id}/bans/{user.id}
## Create Guild Ban % PUT /guilds/{guild.id}/bans/{user.id}
## Remove Guild Ban % DELETE /guilds/{guild.id}/bans/{user.id}
## Get Guild Roles % GET /guilds/{guild.id}/roles
## Create Guild Role % POST /guilds/{guild.id}/roles
## Modify Guild Role Positions % PATCH /guilds/{guild.id}/roles
## Modify Guild Role % PATCH /guilds/{guild.id}/roles/{role.id}
## Delete Guild Role % DELETE /guilds/{guild.id}/roles/{role.id}
## Get Guild Prune Count % GET /guilds/{guild.id}/prune
## Begin Guild Prune % POST /guilds/{guild.id}/prune
## Get Guild Voice Regions % GET /guilds/{guild.id}/regions
## Get Guild Invites % GET /guilds/{guild.id}/invites
## Get Guild Integrations % GET /guilds/{guild.id}/integrations
## Delete Guild Integration % DELETE /guilds/{guild.id}/integrations/{integration.id}
## Get Guild Widget Settings % GET /guilds/{guild.id}/widget
## Modify Guild Widget % PATCH /guilds/{guild.id}/widget
## Get Guild Widget % GET /guilds/{guild.id}/widget.json
## Get Guild Vanity URL % GET /guilds/{guild.id}/vanity-url
## Get Guild Widget Image % GET /guilds/{guild.id}/widget.png
## Get Guild Welcome Screen % GET /guilds/{guild.id}/welcome-screen
## Modify Guild Welcome Screen % PATCH /guilds/{guild.id}/welcome-screen
## Modify Current User Voice State % PATCH /guilds/{guild.id}/voice-states/@me
## Modify User Voice State % PATCH /guilds/{guild.id}/voice-states/{user.id}
## Get Guild Template % GET /guilds/templates/{template.code}
## Create Guild from Guild Template % POST /guilds/templates/{template.code}
## Get Guild Templates % GET /guilds/{guild.id}/templates
## Create Guild Template % POST /guilds/{guild.id}/templates
## Sync Guild Template % PUT /guilds/{guild.id}/templates/{template.code}
## Modify Guild Template % PATCH /guilds/{guild.id}/templates/{template.code}
## Delete Guild Template % DELETE /guilds/{guild.id}/templates/{template.code}

## Get Invite % GET /invites/{invite.code}
## Delete Invite % DELETE /invites/{invite.code}

## Create Stage Instance % POST /stage-instances
## Get Stage Instance % GET /stage-instances/{channel.id}
## Modify Stage Instance % PATCH /stage-instances/{channel.id}
## Delete Stage Instance % DELETE /stage-instances/{channel.id}

## Get Sticker % GET /stickers/{sticker.id}
## List Nitro Sticker Packs % GET /sticker-packs
## List Guild Stickers % GET /guilds/{guild.id}/stickers
## Get Guild Sticker % GET /guilds/{guild.id}/stickers/{sticker.id}
## Create Guild Sticker % POST /guilds/{guild.id}/stickers
## Modify Guild Sticker % PATCH /guilds/{guild.id}/stickers/{sticker.id}
## Delete Guild Sticker % DELETE /guilds/{guild.id}/stickers/{sticker.id}

## Get Current User % GET /users/@me
## Get User % GET /users/{user.id}
## Modify Current User % PATCH /users/@me
## Get Current User Guilds % GET /users/@me/guilds
## Leave Guild % DELETE /users/@me/guilds/{guild.id}
## Create DM % POST /users/@me/channels
## Create Group DM % POST /users/@me/channels
## Get User Connections % GET /users/@me/connections

## List Voice Regions % GET /voice/regions

## Create Webhook % POST /channels/{channel.id}/webhooks
## Get Channel Webhooks % GET /channels/{channel.id}/webhooks
## Get Guild Webhooks % GET /guilds/{guild.id}/webhooks
## Get Webhook % GET /webhooks/{webhook.id}
## Get Webhook with Token % GET /webhooks/{webhook.id}/{webhook.token}
## Modify Webhook % PATCH /webhooks/{webhook.id}
## Modify Webhook with Token % PATCH /webhooks/{webhook.id}/{webhook.token}
## Delete Webhook % DELETE /webhooks/{webhook.id}
## Delete Webhook with Token % DELETE /webhooks/{webhook.id}/{webhook.token}
## Execute Webhook % POST /webhooks/{webhook.id}/{webhook.token}
## Execute Slack-Compatible Webhook % POST /webhooks/{webhook.id}/{webhook.token}/slack
## Execute GitHub-Compatible Webhook % POST /webhooks/{webhook.id}/{webhook.token}/github
## Get Webhook Message % GET /webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
## Edit Webhook Message % PATCH /webhooks/{webhook.id}/{webhook.token}/messages/{message.id}
## Delete Webhook Message % DELETE /webhooks/{webhook.id}/{webhook.token}/messages/{message.id}