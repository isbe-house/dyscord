from ..objects import message


async def on_channel_create(self, object, raw_object):
    pass


async def on_channel_delete(self, object, raw_object):
    pass


async def on_channel_pins_update(self, object, raw_object):
    pass


async def on_channel_update(self, object, raw_object):
    pass


async def on_guild_ban_add(self, object, raw_object):
    pass


async def on_guild_ban_remove(self, object, raw_object):
    pass


async def on_guild_create(self, object, raw_object):
    pass


async def on_guild_delete(self, object, raw_object):
    pass


async def on_guild_emojis_update(self, object, raw_object):
    pass


async def on_guild_integrations_update(self, object, raw_object):
    pass


async def on_guild_member_add(self, object, raw_object):
    pass


async def on_guild_member_remove(self, object, raw_object):
    pass


async def on_guild_member_update(self, object, raw_object):
    pass


async def on_guild_role_create(self, object, raw_object):
    pass


async def on_guild_role_delete(self, object, raw_object):
    pass


async def on_guild_role_update(self, object, raw_object):
    pass


async def on_guild_stickers_update(self, object, raw_object):
    pass


async def on_guild_update(self, object, raw_object):
    pass


async def on_integration_create(self, object, raw_object):
    pass


async def on_integration_delete(self, object, raw_object):
    pass


async def on_integration_update(self, object, raw_object):
    pass


async def on_invite_create(self, object, raw_object):
    pass


async def on_invite_delete(self, object, raw_object):
    pass


async def on_message_create(self, message: message.Message, raw_message: dict):
    pass


async def on_message_delete(self, object, raw_object):
    pass


async def on_message_delete_bulk(self, object, raw_object):
    pass


async def on_message_reaction_add(self, object, raw_object):
    pass


async def on_message_reaction_remove(self, object, raw_object):
    pass


async def on_message_reaction_remove_all(self, object, raw_object):
    pass


async def on_message_reaction_remove_emoji(self, object, raw_object):
    pass


async def on_message_update(self, object, raw_object):
    pass


async def on_presence_update(self, object, raw_object):
    pass


async def on_ready(self):
    pass


async def on_stage_instance_create(self, object, raw_object):
    pass


async def on_stage_instance_delete(self, object, raw_object):
    pass


async def on_stage_instance_update(self, object, raw_object):
    pass


async def on_thread_create(self, object, raw_object):
    pass


async def on_thread_delete(self, object, raw_object):
    pass


async def on_thread_list_sync(self, object, raw_object):
    pass


async def on_thread_member_update(self, object, raw_object):
    pass


async def on_thread_members_update(self, object, raw_object):
    pass


async def on_thread_update(self, object, raw_object):
    pass


async def on_typing_start(self, object, raw_object):
    pass


async def on_voice_state_update(self, object, raw_object):
    pass


async def on_webhooks_update(self, object, raw_object):
    pass


async def on_interaction_create(self, object, raw_object):
    pass
