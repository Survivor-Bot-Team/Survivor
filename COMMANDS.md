# 📜 Metal Wings - Survivor Tournament Bot Commands

Complete reference guide for all available Discord slash commands.

## 🔒 Permission Levels

- **🛡️ Higher Staff**: Full access to all commands
- **👑 Commanders**: Registration and signup commands  
- **🆘 Support Team**: Role management commands
- **👤 Everyone**: Basic utility commands

---

## 🛠️ System Commands

### `/start`
**Permission**: Higher Staff Only  
**Description**: Activate the Warzone tournament system  
**Usage**: `/start`  
**Response**: ✅ Confirmation message that the system is activated

### `/shutdown`
**Permission**: Higher Staff Only  
**Description**: Safely shut down the bot  
**Usage**: `/shutdown`  
**Response**: 🛑 Bot shutdown confirmation, then bot goes offline

### `/clear-sheet`
**Permission**: Higher Staff Only  
**Description**: Clear all data from the connected Google Sheet  
**Usage**: `/clear-sheet`  
**Safety**: Requires typing `CONFIRM CLEAR` within 30 seconds  
**Response**: ⚠️ Confirmation prompt, then success/timeout message

### `/help`
**Permission**: Everyone  
**Description**: Display comprehensive command menu with categories  
**Usage**: `/help`  
**Response**: 📜 Categorized list of all available commands (ephemeral)

---

## 🏆 Tournament Management

### `/winners`
**Permission**: Higher Staff Only  
**Description**: Post tournament winners and automatically update roles  
**Usage**: `/winners [tour_type] [close_role] [new_role] [user_1] [user_2] [user_3] [user_4] [user_5] [judge] [screenshot]`

**Parameters**:
- `tour_type`: Choose between "Main-Tour" or "Parllel-Tour"
- `close_role`: Role to remove from winners
- `new_role`: Role to assign to winners  
- `user_1`: First winner (required)
- `user_2-5`: Additional winners (optional)
- `judge`: Match judge/referee
- `screenshot`: Optional match result screenshot

**Features**:
- Automatically removes old role and assigns new role to all winners
- Posts results in current channel AND appropriate results channel
- Includes timestamp, judge info, and tournament branding
- Error handling for role hierarchy issues

**Example**: `/winners tour_type:Main-Tour close_role:@Round1-Main new_role:@Round2-Main user_1:@Player1 judge:@Judge1`

---

## 🎤 Queue Distribution

### `/cc-all`
**Permission**: Higher Staff Only (Round 1 Only)  
**Description**: Distribute players from Round 1 queue into Warzone voice channels  
**Usage**: `/cc-all [loop_start] [loop_times]`

**Parameters**:
- `loop_start`: Starting position in queue (integer)
- `loop_times`: Number of players to distribute (integer)

**Function**: Moves players from warzone lobby voice channel to individual war zone channels

### `/wz-all`
**Permission**: Higher Staff Only  
**Description**: Create signup message for specific round and warzone  
**Usage**: `/wz-all [round_no] [warzone_no]`

**Parameters**:
- `round_no`: Tournament round number (2, 3, 4, etc.)
- `warzone_no`: Specific warzone number (1, 2, 3, etc.)

**Features**:
- Round-specific emoji reactions
- Auto-deletes after 2 minutes
- Creates signup embed with tournament branding

---

## ⚖️ Team Management

### `/team_balance`
**Permission**: Everyone  
**Description**: Balance two teams based on player skill levels  
**Usage**: `/team_balance [levels]`

**Parameters**:
- `levels`: Comma-separated player levels (e.g., "48,50,51,35,51,50,50,37,51,52")

**Algorithm**: 
- Calculates optimal team distribution for fairness
- Shows both teams with individual levels and team averages
- Minimizes skill gap between teams

**Example**: `/team_balance levels:48,50,51,35,51,50,50,37,51,52`

**Output**:
```
Team 1: [50, 51, 50, 37, 52] - Average: 48.0
Team 2: [48, 51, 35, 50, 51] - Average: 47.0
```

---

## 📝 Registration & Signup Commands



### `/sign_up_sat`
**Permission**: Commanders Only  
**Description**: Post Saturday signup for Round1-Parallel tournament  
**Usage**: `/sign_up_sat`

**Features**:
- 20-minute countdown timer
- Warning at 18 minutes
- Auto-closes signup at 20 minutes
- Saturday-specific branding and messaging
- Reaction-based participation (✅ to join)

### `/sign_up_sun`
**Permission**: Commanders Only  
**Description**: Post Sunday signup for Round1-Main tournament  
**Usage**: `/sign_up_sun`

**Features**:
- 20-minute countdown timer
- Warning at 18 minutes  
- Auto-closes signup at 20 minutes
- Sunday-specific branding and messaging
- Reaction-based participation (✅ to join)

### `/sign_off`
**Permission**: Everyone  
**Description**: Post sign-off message for players to leave queue  
**Usage**: `/sign_off`

**Features**:
- Allows players to remove themselves from tournament queue
- Reaction-based system (❌ to leave)

---

## 🛡️ Support Tools

### `/support-give-role`
**Permission**: Support Team Only  
**Description**: Assign a role to a specific user  
**Usage**: `/support-give-role [user] [role]`

**Parameters**:
- `user`: Discord member to receive the role
- `role`: Role to assign

**Features**:
- Automatic logging to support logs channel
- Error handling for permission issues
- Confirmation message with details

### `/support-remove-role`
**Permission**: Support Team Only  
**Description**: Remove a role from a specific user  
**Usage**: `/support-remove-role [user] [role]`

**Parameters**:
- `user`: Discord member to lose the role
- `role`: Role to remove

**Features**:
- Automatic logging to support logs channel
- Error handling for permission issues
- Confirmation message with details

---

## ⏰ Utility Commands

---

## 📊 Channel & Role Requirements

### Channel Access Control
Commands are restricted to specific channels based on roles:

- **Warzone Channels**: Role-specific access (e.g., War-zone-1 requires Warzone#1.1 role)
- **Registration Channels**: Open for registration commands
- **Results Channels**: Auto-posting for winner announcements
- **Support Channels**: Logging for support actions

### Role Hierarchy
Bot requires elevated permissions to manage roles:
- Bot role must be higher than managed roles
- Requires "Manage Roles" permission
- Role hierarchy respected for all operations

---

## 🔧 Error Handling

All commands include comprehensive error handling:

- **Permission Checks**: Clear denial messages for unauthorized users
- **Parameter Validation**: Input verification and helpful error messages  
- **Role Management**: Hierarchy and permission conflict resolution
- **Timeout Handling**: Graceful handling of expired operations
- **API Limits**: Rate limiting and retry logic for Discord API

---

## 📝 Logging & Audit Trail

Commands automatically log to appropriate channels:
- **Support Actions**: Logged to support-logs channel
- **Registration Events**: Google Sheets integration
- **System Events**: Console logging for administrators
- **Error Events**: Detailed error logging for troubleshooting

---

## 🚀 Quick Reference

| Command | Permission | Primary Use | Auto-Delete |
|---------|------------|-------------|-------------|
| `/help` | Everyone | Documentation | ✅ Ephemeral |
| `/winners` | Staff | Tournament Results | ❌ Persistent |
| `/team_balance` | Everyone | Fair Teams | ❌ Persistent |
| `/cc-all` | Staff | Queue Distribution | ❌ Action-based |
| `/support-give-role` | Support | Moderation | ✅ Logged |

---

**Note**: All commands use Discord's slash command system. Type `/` in Discord to see available commands with auto-complete and parameter hints. 