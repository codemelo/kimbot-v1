from telethon import TelegramClient as TelethonClient, events
import asyncio


class TelegramClient:
    def __init__(self, api_id, api_hash, phone_number, message_controller):
        self.client = TelethonClient('tg-session', api_id, api_hash)
        self.phone = phone_number
        self.mc = message_controller
        self.channels = None

    async def set_channels(self, channel_ids):
        if self.channels is not None:
            return

        await self.login_and_authorize()

        channels = []
        for cid in channel_ids:
            channel = await self.client.get_entity(cid)
            channels.append(channel)

        self.channels = channels
        return self.channels

    async def login_and_authorize(self):
        # Log in to Telegram
        await self.client.start(self.phone)

        # Ensure you're authorization
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            auth_code = input('Enter the code: ')
            await self.client.sign_in(self.phone, auth_code)

    async def start_telegram_listener(self):
        previous_msg = None

        while True:
            try:
                await self.login_and_authorize()

                @self.client.on(events.NewMessage(chats=self.channels))
                async def handler(event):
                    nonlocal previous_msg
                    msg_obj = event.message
                    if msg_obj.raw_text != previous_msg:  # handle duplicates
                        self.mc.process_message(msg_obj)
                    previous_msg = msg_obj.raw_text

                print('Listening for new messages...')
                await self.client.run_until_disconnected()

            except (OSError, asyncio.TimeoutError) as e:
                print(f"Connection error: {e}. \nReconnecting in 5 seconds...")
                await asyncio.sleep(5)  # Wait for 5 seconds before reconnecting

    async def search_channels_by_substring(self, substring):
        await self.client.start(self.phone)

        # Get all dialogs (chats)
        dialogs = await self.client.get_dialogs()

        # Filter channels with the given substring
        channels = [dialog for dialog in dialogs if dialog.is_channel and substring.lower() in dialog.title.lower()]

        for channel in channels:
            print(f'Channel: {channel.title} (ID: {channel.id})')

    async def get_past_messages_starting_with(self, startswith_str):
        await self.client.start(self.phone)

        messages = []
        # Get past messages for each channel
        for c in self.channels:
            async for m in self.client.iter_messages(c):
                if m.raw_text is not None and m.raw_text.startswith(startswith_str):
                    messages.append(m)
                    print("Retrieved message...")

        return messages

    async def get_all_messages(self):
        await self.client.start(self.phone)

        messages = []
        # Get past messages for each channel
        for c in self.channels:
            async for m in self.client.iter_messages(c):
                if m.message is not None:
                    messages.append(m)
                    print("Retrieved message...")

        return messages
