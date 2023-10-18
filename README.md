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

1. **Create a New Event**
!create_event <event_name> <duration> <start_date> <end_date> <token_rewards>

Example:
!create_event "30 Days of Code" 30 "2023-11-01" "2023-11-30" 100

2. **Delete an Event**
!delete_event <event_name>

Example:
!delete_event "30 Days of Code"

3. **List All Events**
!list_events

### Participant Interaction

1. **Register for an Event**
!register <event_name>

Example:
!register "30 Days of Code"

2. **Post Progress for an Event**
!post_progress <event_name> <linkedin_post_link> <day_number> <total_challenge_days>

Example:
!post_progress "30 Days of Code" "https://linkedin.com/post/xyz" 5 30

3. **Check Current Streak for an Event**
!check_streak <event_name>

Example:
!check_streak "30 Days of Code"

### Admin Commands

1. **Check Eligibility for Rewards**
!check_eligibility <event_name>

Example:
!check_eligibility "30 Days of Code"

2. **Export List of Eligible Users**
!export_eligible <event_name>

Example:
!export_eligible "30 Days of Code"

3. **Distribute Tokens to Eligible Users**
!distribute_tokens <event_name>

Example:
!distribute_tokens "30 Days of Code"

### General

1. **Help Command**
!help

## 🆘 Support

If you encounter any issues or require further assistance, feel free to reach out via email: [sankhadip10.das@gmail.com](mailto:sankhadip10.das@gmail.com).

## 🚀 Roadmap

The potential for this bot is vast, and there are several enhancements planned for the future:

- **API Integration**: The bot can be further enhanced through API contributions, allowing for more seamless data retrieval and processing.

- **Email Notifications**: 
- Send emails to participants who are selected for rewards.
- Notify participants who didn't make the cut.
- Daily reminders for users who haven't updated their progress.

- **User Feedback**: Incorporate user feedback to continually improve the bot's features and user experience.

- **Integration with Other Platforms**: Expand the bot's capabilities to track progress on other platforms beyond LinkedIn.

- **Advanced Analytics**: Implement advanced analytics to provide insights into user participation, engagement levels, and more.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check and create issues
