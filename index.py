from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_player_links():
    # Initialize the webdriver (Chrome in this example)
    driver = webdriver.Chrome()
    
    try:
        # Navigate to the page containing the table
        driver.get("https://www.nba.com/players")
        
        # Wait for the table to be present
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "players-list")))
        
        # Find all player links in the table
        player_links = table.find_elements(By.CSS_SELECTOR, "td.primary.text a[href^='/player/']")
        
        # Extract and store the player URLs
        player_urls = []
        for link in player_links:
            href = link.get_attribute('href')
            # Extract just the /player/number/name part
            player_path = href.split('player/')[1].rstrip('/')
            player_urls.append(f"/player/{player_path}")
            
        return player_urls
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Always close the browser
        driver.quit()

# Run the scraper
if __name__ == "__main__":
    player_links = scrape_player_links()
    
    # Save the results to a file
    with open('links.txt', 'w') as f:
        for link in player_links:
            f.write(f"{link}\n")
    
    print(f"Player links have been saved to links.txt")