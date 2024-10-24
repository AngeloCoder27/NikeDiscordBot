# Nike Discount Bot

This Discord bot checks for discounts on Nike products and notifies users in specified channels. It uses Selenium to scrape data from the Nike website and sends updates to Discord when new discounts are found.

## Features

- **Check Discounts**: Fetch current Nike discounts and display them in the channel.
- **Channel Management**: Add or remove channels for notifications.
- **Scheduled Checks**: Automatically checks for discounts every hour.
- **Data Persistence**: Stores settings and data in a JSON file.

## Requirements

- Python 3.8 or higher
- Discord.py library
- Selenium
- ChromeDriver

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install discord.py selenium
   ```

3. **Download ChromeDriver**:
   - Make sure the version of ChromeDriver matches your installed version of Chrome.
   - Place the `chromedriver` executable in the appropriate directory (`/home/angelocoder27/chromedriver-linux64/chromedriver` in this code).

4. **Set up your bot token**:
   - Replace the empty string in `bot.run('')` with your actual Discord bot token.

5. **Create a JSON file**:
   - Create a file named `nike_data.json` in the same directory as your script with the following content:
     ```json
     {
       "show_discount_shoes": true,
       "last_seen": [],
       "channels": []
     }
     ```

## Commands

- `!discount`: Shows current Nike discounts in the channel.
- `!add_channel [channel_id]`: Adds the specified channel to the notification list. If no channel ID is provided, it adds the current channel.
- `!remove_channel [channel_id]`: Removes the specified channel from the notification list. If no channel ID is provided, it removes the current channel.

## Usage

1. Start the bot by running the script:
   ```bash
   python <script_name>.py
   ```

2. Use the commands in any channel where the bot is present.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Discord.py](https://discordpy.readthedocs.io/en/stable/) - Discord API wrapper for Python
- [Selenium](https://www.selenium.dev/) - Web automation framework
