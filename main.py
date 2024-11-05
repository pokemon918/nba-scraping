from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the webdriver
driver = webdriver.Chrome()

try:
    # Read links from file
    with open('links.txt', 'r') as file:
        player_links = file.readlines()
    
    # Initialize list to store all players' data
    all_players_data = []
    
    for link in player_links:
        try:
            # Clean the link and extract player name
            link = link.strip()
            player_name = link.split('/')[-1].replace('-', ' ').title()
            
            # Construct full URL
            full_url = f"https://www.nba.com{link}"
            
            print(f"Scraping data for {player_name}...")
            
            driver.get(full_url)
            
            # Wait for the element with the specific class to be present
            table_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Block_blockContent__6iJ_n"))
            )

            # Scroll the table section into view
            driver.execute_script("arguments[0].scrollIntoView(true);", table_section)
            time.sleep(1)
            
            # Find the table within the section
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Block_blockContent__6iJ_n table"))
            )
            
            # Get headers (only for the first player)
            if not all_players_data:
                headers = ['Player Name']  # Add player name column
                for header in table.find_elements(By.TAG_NAME, "th"):
                    headers.append(header.text)
            
            # Get table rows
            for row in table.find_elements(By.TAG_NAME, "tr")[1:]:  # Skip header row
                row_data = [player_name]  # Add player name as first column
                for cell in row.find_elements(By.TAG_NAME, "td"):
                    row_data.append(cell.text)
                if row_data:  # Only append non-empty rows
                    all_players_data.append(row_data)
            
            # Add a small delay between requests to be respectful to the server
            time.sleep(2)
            
        except Exception as e:
            print(f"Error scraping {player_name}: {str(e)}")
            continue
    
    # Create DataFrame with all players' data
    df = pd.DataFrame(all_players_data, columns=headers)
    
    # Save to Excel
    df.to_excel("nba_players_stats.xlsx", index=False)
    print("Data successfully saved to nba_players_stats.xlsx")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    driver.quit()