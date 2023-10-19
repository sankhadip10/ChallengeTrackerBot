# Discord Daily Challenge Bot 

## 📌 Overview
The Discord Daily Challenge Bot is designed to streamline the verification process for participants in daily coding challenges. As the developer community grows, manually verifying each submission becomes a daunting task. This bot not only automates the verification process but also offers features like maintaining a leaderboard and tracking participant eligibility for rewards.

## 🌟 Features

- **Event Management**: Admins can easily create or delete events, specifying details like duration, start and end dates, and token rewards.
  
- **User Registration**: Users can register for specific events to participate and post their progress.
  
- **Progress Posting**: Users can post their daily progress for an event, including a link to their LinkedIn post and the day they're posting for.
  
- **Streak Tracking**: Users can check their current streak for a specific event, ensuring they're on track.
  
- **Eligibility Verification**: Admins can view a list of users eligible for rewards for a specific event, making reward distribution seamless.
  
- **Data Export**: Admins can export a list of eligible users for an event to an Excel file for further processing or record-keeping.
  
- **Token Distribution**: Admins can distribute tokens to eligible users for a specific event, rewarding participants for their efforts.
  
- **Help Command**: A comprehensive help command that provides users with information on available commands and their usage.

## 📖 Usage

### Event Management

GeneralCommands:
  description: "Commands available for all users"
  commands:
    - name: **"Register for an Event"**
      command: "!register <event_name>"
      example: "!register EventName"
      
    - name: **"Post Progress for an Event"**
      command: "!post <event_name> <linkedin_post_link> <day_number> <total_challenge_days>"
      example: "!post EventName https://www.linkedin.com/feed/update/urn:li:activity:1234567890/ 5 30"
      notes:
        - "Make sure to copy the link exactly as it is."
        - "The day_number represents the current day number of the event."
        - "The total_challenge_days represents the total number of days the event lasts."
        
    - name: **"List All Events"**
      command: "!listEvents"
      example: "!listEvents"
      
    - name: **"Check Current Streak for an Event"**
      command: "!checkStreak <event_name>"
      example: "!checkStreak EventName"

### AdminCommands:
  ## description: "Commands available for admins only"
  
  commands:
    - name: **"Create a New Event"**
      command: "!createEvent <event_name> <start_date> <end_date> <token_rewards>"
      example: "!createEvent EventName 30 01-01-2023 30-01-2023 50"
      
    - name: **"Delete an Event"**
      command: "!deleteEvent <event_name>"
      example: "!deleteEvent EventName"
      
    - name: **"Check Eligibility for Rewards"**
      command: "!eligibility <event_name>"
      example: "!eligibility EventName 1"
      
    - name: **"Export List of Eligible Users"**
      command: "!export <event_name>"
      example: "!export EventName"
      
    - name: **"Distribute Tokens to Eligible Users"**
      command: "!distributeTokens <event_name>"
      example: "!distributeTokens EventName"


### General

1. **Help Command**
!help

## 🚀 Getting Started

### Prerequisites

- Ensure you have Python 3.10 installed. If not, download and install it from [Python's official website](https://www.python.org/downloads/).

### Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sankhadip10/ChallengeTrackerBot.git
   cd ChallengeTrackerBot
   
2. **Install Dependencies**:
   ```bash
    pip install -r requirements.txt
   
3. **Run the bot**:
python bot_core.py

**Why is BotCommander Needed**?
The BotCommander role (or a similar role specified in your config.py) is essential for several reasons:

**Access Control**: Not all commands should be accessible to every user. Some commands, especially administrative ones, should only be available to trusted users or moderators. By designating a BotCommander role, you can ensure that only users with this role can execute certain privileged commands.

**Prevent Abuse**: Without role-based access control, any user could potentially misuse the bot, leading to spam, incorrect data, or even potential security risks. By restricting certain commands to the BotCommander role, you can mitigate these risks.

**Ease of Management**: Having a designated role for bot command execution makes it easier to manage who has access to what commands. If a new moderator joins the server, you can simply assign them the BotCommander role, and they'll have the necessary permissions.

Flexibility: By configuring the role in the config.py file, you can easily change the role name or add multiple roles with command execution privileges, giving you flexibility in how you manage your bot's permissions.

## 🛠️ Configuration & Setup

### Configuring the Bot

1. **Bot Token**: 
   - Navigate to the `config.py` file in the root directory.
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual Discord bot token.
     ```python
     BOT_TOKEN = "YOUR_ACTUAL_BOT_TOKEN"
     ```

2. **Sauce Labs Credentials**:
   - If you're using Sauce Labs for any functionality, you'll need to set up your credentials.
   - Navigate to [Sauce Labs](https://saucelabs.com/) and obtain your username and access key.
   - In the `config.py` file, replace `XXXXX` with your Sauce Labs username and `YYYYYY` with your access key.
     ```python
     sauce_options_un = "YOUR_SAUCE_LABS_USERNAME"
     sauce_options_access_key = "YOUR_SAUCE_LABS_ACCESS_KEY"
     ```

### Data Validation

The bot currently uses web scraping techniques to validate data from LinkedIn posts. While this method is effective, it's worth noting that web scraping can be fragile due to potential changes in the website's structure. 

In the future, switching to official APIs for data validation. However, the current scraping method was chosen due to cost constraints, as many official APIs are not free.

### Test Cases

The bot is rigorously tested with more than 50 test cases to ensure its reliability and efficiency. This extensive testing ensures that the bot functions as expected and can handle various scenarios and edge cases.

---

## 🆘 Support

If you encounter any issues or require further assistance, feel free to reach out via email: [sankhadip10.das@gmail.com](mailto:sankhadip10.das@gmail.com).

## 🚀 Roadmap

The potential for this bot is vast, and there are several enhancements planned for the future:

- **API Integration**: The bot can be further enhanced through API contributions, allowing for more seamless data retrieval and processing.
- Instead of web scraping, consider integrating with official APIs (like LinkedIn's API) for more robust and reliable data validation. This would reduce the bot's dependency on the structure of web pages, which can change over time.

- **Email Notifications**: 
- Send emails to participants who are selected for rewards.
- Notify participants who didn't make the cut.
- Daily reminders for users who haven't updated their progress.

- **User Feedback**: Incorporate user feedback to continually improve the bot's features and user experience.

- **Integration with Other Platforms**: Expand the bot's capabilities to track progress on other platforms beyond LinkedIn.

- **Advanced Analytics**: Implement advanced analytics to provide insights into user participation, engagement levels, and more.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check and create issues
