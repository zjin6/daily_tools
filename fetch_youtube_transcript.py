from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# setup chrome driver
driver = webdriver.Chrome()

# get the video page
video_id = "gkKjmX23baY"
url = f"https://www.youtube.com/watch?v={video_id}"
driver.get(url)

# wait for the "Show transcript" button to be clickable
show_transcript_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button yt-icon[class='style-scope ytd-menu-renderer']"))
)

# click the "Show transcript" button
show_transcript_button.click()

# wait for the transcript to be visible
transcript = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-transcript-body-renderer"))
)

# extract the transcript text
transcript_text = transcript.text

# print the transcript text
print(transcript_text)

# close the driver
driver.quit()
