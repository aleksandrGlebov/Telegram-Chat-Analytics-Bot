# Telegram Chat Statistics Analyzer

This Telegram bot provides functionalities to analyze chat statistics in Telegram. It allows you to upload a chat history in JSON format and obtain various statistical insights, including:

1. Top 20 users by message count.
2. Top 10 most frequently used words.
3. Chat activity graph by day.
4. Graph of the top 5 dates with the highest message count.
5. Graph of the top 5 dates with the lowest message count.

## Usage

1. Install the required dependencies by running the command `pip install -r requirements.txt`.

2. Create a `config.json` file in the same directory as the bot's source code and add the following information:

    ```json
    {
    "bot_token": "YOUR_BOT_TOKEN"
    }
    ```

3. Start the bot by running the command `python main.py` in the command line.

4. Find the created bot in Telegram and start it.

5. Upload the chat history file in JSON format using the `/upload` command. The file should be exported from Telegram and contain chat message information.

6. The bot will process the uploaded chat history file and send you the analysis results in the form of graphs and text messages.

7. You can cancel the current operation at any time using the `/cancel` command.

## Commands

- `/start` - Start the interaction with the bot.
- `/upload` - Upload a chat history file in JSON format.
- `/cancel` - Cancel the current operation.

## Dependencies

The following dependencies are required to run this Telegram bot:

- python-telegram-bot
- matplotlib
- numpy
- statsmodels

Install them by running the command `pip install -r requirements.txt`.

## Notes

- Please ensure that your bot has access to chat messages and the permission to send messages.
