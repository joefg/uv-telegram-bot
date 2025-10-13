# uv-telegram-bot

My personal [Telegram bot](https://core.telegram.org/bots)
template. Uses uv, Python, and SQLite as a data store.

## How to set up

1. Get an API token from [@Botfather](https://t.me/botfather).

2. Add that API token to your `.env`. See the `.env.example`
for reference.

3. `./run restore` to build your venv.

4. `./run serve` to spawn the bot.

## Available commands

| Command | Description |
| ------- | ----------- |
| `/help` | Displays help |
| `/ping` | Returns `Pong!` |
| `/account` | Enters the Accounts menu |