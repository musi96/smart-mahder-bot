# Telegram Bot Admin Features

## Overview
I've added comprehensive admin features to your Telegram bot for user management and broadcasting. Your admin user ID `1952017668` has exclusive access to these commands.

## New Admin Commands

### 1. `/broadcast <message>`
**Purpose**: Send a message to all bot users
**Usage**: `/broadcast Hello everyone! New materials have been added.`
**Features**:
- Sends message to all registered users
- Shows success/failure statistics
- Rate limited to prevent issues
- Only accessible by admin

### 2. `/users`
**Purpose**: Get total user count
**Usage**: `/users`
**Shows**: Simple user count statistics

### 3. `/stats`
**Purpose**: Detailed bot statistics
**Usage**: `/stats`
**Shows**:
- Total users
- Users with usernames
- New users in last 7 days
- Bot information

### 4. `/export`
**Purpose**: Export user list
**Usage**: `/export`
**Features**:
- Lists all users with their details
- Includes usernames, names, join dates
- Handles long lists by splitting messages

## User Tracking
The bot now automatically tracks:
- User ID
- Username
- First and last name
- Join date
- Last interaction date

## Data Storage
- User data is stored in `users.json`
- Automatically created and maintained
- Persistent across bot restarts

## Security
- All admin commands check user ID `1952017668`
- Non-admin users get "not authorized" message
- User data is stored locally

## Technical Details

### Key Functions Added:
- `load_users()` - Load user data from file
- `save_users()` - Save user data to file
- `add_user()` - Add/update user information
- `get_user_count()` - Get total user count
- `get_all_user_ids()` - Get list of all user IDs

### Modified Functions:
- `start()` - Now tracks users when they start the bot
- `main()` - Added admin command handlers

## Usage Examples

1. **Check user count**:
   ```
   /users
   ```

2. **Send broadcast**:
   ```
   /broadcast Welcome to our updated bot! New Economics materials added.
   ```

3. **View detailed stats**:
   ```
   /stats
   ```

4. **Export user list**:
   ```
   /export
   ```

## Benefits
- Track bot growth and usage
- Communicate directly with all users
- Monitor bot performance
- Export user data for analysis

All features are ready to use once the bot is restarted!