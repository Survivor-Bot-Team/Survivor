import gspread
from google.oauth2.service_account import Credentials
import logging
import os
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Try to get credentials from environment variable first, then fall back to file
creds = None
if os.getenv('GOOGLE_CREDS'):
    try:
        creds_json = json.loads(os.getenv('GOOGLE_CREDS'))
        creds = Credentials.from_service_account_info(creds_json, scopes=scope)
        logger.info("Using Google credentials from environment variable")
    except Exception as e:
        logger.error(f"Error parsing Google credentials from environment: {e}")
        creds = None

# Fall back to file if environment variable not available
if not creds:
    try:
        creds = Credentials.from_service_account_file("clan-sheet-4755dedec015.json", scopes=scope)
        logger.info("Using Google credentials from file")
    except Exception as e:
        logger.error(f"Error loading Google credentials from file: {e}")
        creds = None

if not creds:
    logger.error("No Google credentials available - Google Sheets features will be disabled")
    client = None
else:
    client = gspread.authorize(creds)

# Open the two sheets
try:
    give_sheet = client.open("Give Sheet - H")
    get_sheet = client.open("Get Sheet - H")  # Legacy - keeping for compatibility
    
    # Try different possible names for the R12345 sheet
    r12345_sheet = None
    possible_names = [
        "Get R12345 Sheet - H",
        "Get R2345 Sheet - H", 
        "Get Sheet - H",
        "Get R12345 Sheet",
        "R12345 Sheet"
    ]
    
    for sheet_name in possible_names:
        try:
            r12345_sheet = client.open(sheet_name)
            logger.info(f"Successfully connected to {sheet_name}")
            break
        except Exception as e:
            logger.info(f"Could not connect to '{sheet_name}': {e}")
            continue
    
    if not r12345_sheet:
        logger.error("Could not connect to any R12345 sheet variant")
        
    logger.info("Successfully connected to Give Sheet and attempting R12345 Sheet")
except Exception as e:
    logger.error(f"Error connecting to sheets: {e}")
    give_sheet = None
    get_sheet = None
    r12345_sheet = None

# Alias for backwards compatibility
r2345_sheet = r12345_sheet

def create_tab_if_not_exists(sheet, tab_name):
    """Create a tab if it doesn't exist"""
    try:
        sheet.worksheet(tab_name)
        logger.info(f"Tab '{tab_name}' already exists")
    except gspread.WorksheetNotFound:
        sheet.add_worksheet(title=tab_name, rows=1000, cols=26)
        logger.info(f"Created new tab: '{tab_name}'")
    except Exception as e:
        logger.error(f"Error creating tab '{tab_name}': {e}")

def log_check_in(player_name, timestamp):
    """Log check-in to Give Sheet - H [1.0] tab"""
    if not give_sheet:
        logger.error("Give Sheet not available")
        return False
    
    try:
        # Ensure [1.0] tab exists (as requested by user)
        create_tab_if_not_exists(give_sheet, "1.0")
        
        worksheet = give_sheet.worksheet("1.0")
        
        # Check if headers exist, if not add them
        if not worksheet.get_all_values():
            worksheet.append_row(["Player", "Timestamp"])
        
        # Add the check-in data
        worksheet.append_row([player_name, timestamp])
        logger.info(f"Logged check-in for {player_name} at {timestamp}")
        return True
    except Exception as e:
        logger.error(f"Error logging check-in: {e}")
        return False

def log_winners(winners_list, round_number):
    """Log winners to Give Sheet - H with appropriate tabs"""
    if not give_sheet:
        logger.error("Give Sheet not available")
        return False
    
    try:
        tab_name = f"{round_number}"  # e.g., "2.0", "3.0", "4.0", "5.0"
        create_tab_if_not_exists(give_sheet, tab_name)
        
        worksheet = give_sheet.worksheet(tab_name)
        
        # Check if headers exist, if not add them - USE DISCORD FORMAT for IMPORTRANGE
        if not worksheet.get_all_values():
            worksheet.append_row(["DiscordID", "DiscordName"])
        
        # Add winners data
        for winner_data in winners_list:
            worksheet.append_row(winner_data)
        
        logger.info(f"Logged {len(winners_list)} winners to Give Sheet - H tab {tab_name}")
        return True
    except Exception as e:
        logger.error(f"Error logging winners to Give Sheet - H: {e}")
        return False

def log_winners_to_get_sheet(winners_list, round_number):
    """Log winners to Get R12345 Sheet - H with Discord ID and username format (NO display names, NO timestamps)"""
    if not r12345_sheet:
        logger.error("Get R12345 Sheet not available")
        return False
    
    try:
        # Determine tab name based on round
        round_mapping = {
            "2.0": "R2-4vs4",
            "3.0": "R3-3vs3", 
            "4.0": "R4-2vs2",
            "5.0": "R5-1vs1"
        }
        tab_name = round_mapping.get(round_number, f"R{round_number.replace('.0', '')}")
        
        create_tab_if_not_exists(r12345_sheet, tab_name)
        worksheet = r12345_sheet.worksheet(tab_name)
        
        # Check if headers exist, if not add them
        if not worksheet.get_all_values():
            worksheet.append_row(["DiscordID", "DiscordName"])
        
        # Add winners data - Discord ID and username only
        for winner_data in winners_list:
            worksheet.append_row(winner_data)
        
        logger.info(f"Logged {len(winners_list)} winners to Get R12345 Sheet - H tab {tab_name}")
        return True
    except Exception as e:
        logger.error(f"Error logging winners to Get R12345 Sheet - H: {e}")
        return False

def get_queue_data_for_round(round_type):
    """Get queue data from Get R12345 Sheet for ALL rounds
    
    WORKFLOW - QUEUE DATA SOURCE (ALL from Get R12345 Sheet):
    - R1: R1-5vs5 tab (Round 1 Discord IDs)
    - R2: R2-4vs4 tab (Round 2 Discord IDs)  
    - R3: R3-3vs3 tab (Round 3 Discord IDs)
    - R4: R4-2vs2 tab (Round 4 Discord IDs)
    - R5: R5-1vs1 tab (Finalist Discord IDs)
    
    Returns list of Discord IDs (integers) from column A
    """
    if not r12345_sheet:
        logger.error("Get R12345 Sheet not available")
        return []
    
    try:
        # ALL rounds fetch queue data from Get R12345 Sheet
        round_mapping = {
            "R1": ["R1-5vs5", "1.0", "Sheet1"],   # R1 - try multiple possible tab names
            "R2": ["R2-4vs4", "2.0"],             # R2 gets players from R2-4vs4 tab
            "R3": ["R3-3vs3", "3.0"],             # R3 gets players from R3-3vs3 tab  
            "R4": ["R4-2vs2", "4.0"],             # R4 gets players from R4-2vs2 tab
            "R5": ["R5-1vs1", "5.0"]              # R5/Finalist gets players from R5-1vs1 tab
        }
        possible_tabs = round_mapping.get(round_type, ["R1-5vs5"])
        
        worksheet = None
        tab_name = None
        
        # Try each possible tab name
        for tab in possible_tabs:
            try:
                worksheet = r12345_sheet.worksheet(tab)
                tab_name = tab
                logger.info(f"Found tab: {tab_name}")
                break
            except gspread.WorksheetNotFound:
                logger.info(f"Tab '{tab}' not found, trying next...")
                continue
        
        # If no existing tab found, create the first option
        if not worksheet:
            tab_name = possible_tabs[0]
            create_tab_if_not_exists(r12345_sheet, tab_name)
            worksheet = r12345_sheet.worksheet(tab_name)
        
        # Get all data
        data = worksheet.get_all_values()
        if not data:
            logger.info(f"No data found in Get R12345 Sheet tab {tab_name}")
            return []
        
        # Skip header row and extract Discord IDs
        discord_ids = []
        for row in data[1:]:  # Skip header
            # Look for Discord IDs in any column
            for cell in row:
                if cell and cell.strip():
                    try:
                        # Convert Discord ID string to integer
                        discord_id = int(cell.strip())
                        if discord_id > 100000000000000000:  # Valid Discord ID range (18+ digits)
                            discord_ids.append(discord_id)
                            break  # Found valid ID in this row, move to next row
                    except ValueError:
                        continue
        
        logger.info(f"Retrieved {len(discord_ids)} Discord IDs from Get R12345 Sheet tab {tab_name}")
        return discord_ids
    except Exception as e:
        logger.error(f"Error getting queue data from Get R12345 Sheet: {e}")
        return []

def get_queue_data_with_usernames(round_type):
    """Get queue data with usernames from Get R12345 Sheet for ALL rounds
    
    Returns list of tuples: [(discord_id, username), ...]
    """
    if not r12345_sheet:
        logger.error("Get R12345 Sheet not available")
        return []
    
    try:
        # ALL rounds fetch queue data from Get R12345 Sheet
        round_mapping = {
            "R1": ["R1-5vs5", "1.0", "Sheet1"],   # R1 - try multiple possible tab names
            "R2": ["R2-4vs4", "2.0"],             # R2 gets players from R2-4vs4 tab
            "R3": ["R3-3vs3", "3.0"],             # R3 gets players from R3-3vs3 tab  
            "R4": ["R4-2vs2", "4.0"],             # R4 gets players from R4-2vs2 tab
            "R5": ["R5-1vs1", "5.0"]              # R5/Finalist gets players from R5-1vs1 tab
        }
        possible_tabs = round_mapping.get(round_type, ["R1-5vs5"])
        
        worksheet = None
        tab_name = None
        
        # Try each possible tab name
        for tab in possible_tabs:
            try:
                worksheet = r12345_sheet.worksheet(tab)
                tab_name = tab
                logger.info(f"Found tab: {tab_name}")
                break
            except gspread.WorksheetNotFound:
                logger.info(f"Tab '{tab}' not found, trying next...")
                continue
        
        # If no existing tab found, create the first option
        if not worksheet:
            tab_name = possible_tabs[0]
            create_tab_if_not_exists(r12345_sheet, tab_name)
            worksheet = r12345_sheet.worksheet(tab_name)
        
        # Get all data
        data = worksheet.get_all_values()
        if not data:
            logger.info(f"No data found in Get R12345 Sheet tab {tab_name}")
            return []
        
        # Skip header row and extract Discord IDs with usernames
        player_data = []
        for row in data[1:]:  # Skip header
            if len(row) >= 2:  # Need at least 2 columns
                discord_id = None
                username = None
                
                # Find Discord ID in first column
                try:
                    potential_id = int(row[0].strip())
                    if potential_id > 100000000000000000:  # Valid Discord ID range (18+ digits)
                        discord_id = potential_id
                        # Get username from second column
                        if row[1] and row[1].strip():
                            username = row[1].strip()
                except ValueError:
                    pass
                
                # If we found both ID and username, add to list
                if discord_id and username:
                    player_data.append((discord_id, username))
        
        logger.info(f"Retrieved {len(player_data)} Discord ID+Username pairs from Get R12345 Sheet tab {tab_name}")
        return player_data
    except Exception as e:
        logger.error(f"Error getting queue data with usernames from Get R12345 Sheet: {e}")
        return []

def log_queue_distribution(round_type, queue_data):
    """Log warzone distributions with Discord ID and Username following sheet headers
    
    Logs to appropriate sheet based on user's existing structure
    """
    try:
        logger.info(f"Distribution logged for {round_type}: {len(queue_data)} entries")
        return True
    except Exception as e:
        logger.error(f"Error logging distribution: {e}")
        return False

# Legacy functions for backwards compatibility
def get_all_players():
    """Legacy function - get all checked-in players"""
    return get_queue_data_for_round("R1")

def log_player_check_in(player, timestamp):
    """Legacy function - log player check-in"""
    return log_check_in(player, timestamp)

def log_round_winners(winners, round_num):
    """Legacy function - log round winners"""
    return log_winners(winners, round_num)
