# Python Telegram Bot for Vercel Deployment

This is a simple Python Telegram bot designed to be easily deployed on Vercel.

## Features

*   `/start` command: Welcomes the user.
*   `/links` command: Displays a set of useful links as inline keyboard buttons.
*   Ready for serverless deployment on Vercel.

## Prerequisites

1.  **Telegram Bot Token:**
    *   Talk to [BotFather](https://t.me/BotFather) on Telegram.
    *   Create a new bot by sending the `/newbot` command.
    *   Follow the instructions and BotFather will give you an API token. Keep this token safe!
2.  **Vercel Account:**
    *   Sign up or log in to [Vercel](https://vercel.com/).

## Deployment to Vercel

1.  **Fork or Clone this Repository:**
    *   You can fork this repository to your GitHub/GitLab/Bitbucket account or clone it to your local machine.

2.  **Create a New Vercel Project:**
    *   On your Vercel dashboard, click on "Add New..." -> "Project".
    *   Import your forked/cloned repository. Vercel should automatically detect it as a Python project due to the `vercel.json` file.

3.  **Configure Environment Variables:**
    *   In the Vercel project settings, navigate to "Settings" -> "Environment Variables".
    *   Add the following environment variable:
        *   `TELEGRAM_BOT_TOKEN`: Your Telegram bot API token obtained from BotFather.

4.  **Deploy:**
    *   Vercel will automatically build and deploy your project. Once the deployment is complete, Vercel will provide you with a domain for your bot (e.g., `your-project-name.vercel.app`).

5.  **Set the Webhook:**
    *   Your Telegram bot needs to know where to send updates. You'll do this by setting a webhook.
    *   Open your browser and go to the following URL, replacing `<YOUR_BOT_TOKEN>` with your bot token and `<YOUR_VERCEL_APP_URL>` with the domain Vercel gave you:
        ```
        https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_VERCEL_APP_URL>
        ```
    *   For example:
        ```
        https://api.telegram.org/bot1234567890:ABCDEFGHIJKLMN0PQRSTUVWXYZ/setWebhook?url=https://my-telegram-bot.vercel.app
        ```
    *   If it's successful, you'll see a JSON response like: `{"ok":true,"result":true,"description":"Webhook was set"}`.

6.  **Test Your Bot:**
    *   Open Telegram and interact with your bot. Try the `/start` and `/links` commands.

## Project Structure

*   `app/index.py`: The main Python script for the Telegram bot.
*   `vercel.json`: Vercel deployment configuration.
*   `requirements.txt`: Python dependencies.
*   `README.md`: This file.
*   `.env.example`: Example for environment variables (though for Vercel, you set them in the dashboard).

## Local Development (Optional)

This bot can also be run locally for testing before deploying.

1.  **Set Environment Variable:**
    *   The bot reads the `TELEGRAM_BOT_TOKEN` from an environment variable. You can set this in your shell:
        ```bash
        export TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
        ```
    *   Alternatively, create a `.env` file in the root directory (you can copy `.env.example`):
        ```
        TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN_HERE"
        ```
        And then load it using a library like `python-dotenv` in your local execution, or ensure your local run configuration loads `.env` files. The provided `app/index.py`'s `if __name__ == "__main__":` block does not automatically load `.env` files; it expects `TELEGRAM_BOT_TOKEN` to be in the environment. You can install `python-dotenv` (`pip install python-dotenv`) and add a line like `from dotenv import load_dotenv; load_dotenv()` at the beginning of the `if __name__ == "__main__":` block in `app/index.py` if you prefer this method for local testing.

2.  **Run the Bot:**
    *   Navigate to the project directory and run the main script:
        ```bash
        python app/index.py
        ```
    *   The script will use `bot.infinity_polling()` to fetch updates directly from Telegram. You should see log messages in your console.

3.  **Important:** The local development setup uses polling. Vercel uses webhooks. The `app/index.py` is already structured to support both: the `handler` function for Vercel and the `if __name__ == "__main__":` block for local polling. No code changes are needed before deploying to Vercel regarding this.
