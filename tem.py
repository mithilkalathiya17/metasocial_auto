import json
import time
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from helper import get_selenium_base_uc_driver
from xl import update_google_sheet
from PIL import Image
import base64
from urllib.parse import urlparse
from io import BytesIO
import random
import glob

# Load data from JSON files
with open("profile_creation_data2.json", "r") as file:
    json_data = json.load(file)

with open("profile_creation_data2.json", "r") as file:
    users = json.load(file)

# Dictionary for game categories and links
word_link_dict = {
    # "Crazy": "https://www.atmhtml5games.com/category/crazy-games/",
    # "Dress up": "https://www.atmhtml5games.com/category/dress-up-games/",
    # "Girls": "https://www.atmhtml5games.com/category/girls-games/",
    # "Playhop": "https://www.atmhtml5games.com/category/play-hop-games/",
    # "Poki": "https://www.atmhtml5games.com/category/poki-games/",
    # "Thop": "https://www.atmhtml5games.com/category/thop-games/",
    # "Top 100": "https://www.atmhtml5games.com/category/top-free-games/",
    # "Trending": "https://www.atmhtml5games.com/category/trending-games/",
    # "RPG": "https://www.atmhtml5games.com/category/rpg-games/",
    # "Action": "https://www.atmhtml5games.com/category/action-games/",
    # "Adventure": "https://www.atmhtml5games.com/category/adventure-games/",
    # "Casual": "https://www.atmhtml5games.com/category/casual-games/",
    # "Multiplayer": "https://www.atmhtml5games.com/category/multiplayer-games/",
    # "Racing": "https://www.atmhtml5games.com/category/racing-games/",
    # "Simulation": "https://www.atmhtml5games.com/category/simulation-games/",
    # "Sports": "https://www.atmhtml5games.com/category/sports-games/",
    # "Strategy": "https://www.atmhtml5games.com/category/strategy-games/"


    "Adventure": "https://pocigames.com/adventure",
    "Shooting ": "https://pocigames.com/shooting",
    "3D ": "https://pocigames.com/3d",
    "Sports ": "https://pocigames.com/sports",
    "Hypercasual ": "https://pocigames.com/hypercasual",
    "Puzzles ": "https://pocigames.com/puzzles",
    "Clicker ": "https://pocigames.com/clicker",
    "Girls ": "https://pocigames.com/girls",
    "Action ": "https://pocigames.com/action",
    "Cooking ": "https://pocigames.com/cooking",
    "Racing ": "https://pocigames.com/racing",
    "Fighting ": "https://pocigames.com/fighting",
    "Boys ": "https://pocigames.com/boys",
    "Multiplayer ": "https://pocigames.com/multiplayer",
    "Bejeweled ": "https://pocigames.com/bejeweled"
}

def generate_image(category):

    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--accept-lang=en-US") 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    time.sleep(1)
    driver.get("https://www.writecream.com/ai-image-generator-free-no-sign-up/")
    time.sleep(3)

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(8)

    input_box = driver.find_element(By.XPATH, "//textarea[@id='promptText']")
    input_box.click()
    time.sleep(2)
#https://www.atmhtml5games.com
    prompt = f"Create a vibrant and engaging image for my games website https://pocigames.com/ . The topic is '{category} games '. Include colorful cartoon-style characters, extreme challenges, and fun obstacles. The background should be vibrant and dynamic, with an exciting, chaotic feel. Boldly display the topic name just for once. The image should be strictly related to given topic. Do not include any text other than given topic."
    input_box.send_keys(prompt)
    time.sleep(5)

    # generate_button = driver.find_element(By.ID, "modelQualityButton")
    # generate_button.click()
    # time.sleep(15)

    generate_button = driver.find_element(By.XPATH, "//button[@id='generateOutput']")
    generate_button.click()
    time.sleep(25)

    # driver.execute_script("window.scrollBy(0, 300);")
    # time.sleep(2)

    image_element = driver.find_element(By.XPATH, "//div[@class='outputBoxes']//img")
    image_url = image_element.get_attribute("src")
    print("Generated Image URL:", image_url)

    response = requests.get(image_url)
    image_data = response.content

    with open("generated_image.jpg", "wb") as file:
        file.write(image_data)

    print("Image saved successfully!")
    driver.quit()

    return image_data






def extract_only_html_content(data_):
    html_content = re.search(r"(<html.*?>.*?</html>)", data_, re.DOTALL)
    return html_content.group(1) if html_content else None

def generate_blog_content(category, category_url):
    driver = get_selenium_base_uc_driver()
    driver.get("https://www.getmerlin.in/")
    time.sleep(2)

    if "Merlin" not in driver.title and "GPT" not in driver.page_source:
        print("Merlin did not load correctly.")
        driver.quit()
        return None, None, None, None

    input_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
    )
    input_element.send_keys("Hii.")
    time.sleep(1)
    input_element.send_keys(Keys.ENTER)

    first_button_xpath = "(//button//p[contains(text(), 'Gemini 2.0 Flash')])[2]"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, first_button_xpath))
    ).click()
    time.sleep(2)

    second_button = driver.find_element(
        By.XPATH, "(//p[contains(text(), 'DeepSeek V3 (US-hosted)')])[2]"
    )
    second_button.click()
    time.sleep(3)

    blog_title = f"{category} Games"
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@data-placeholder='Type your prompt here']")
        )
    )
    input_box.send_keys(
        f"""'{blog_title}' based on this game title, kindly provide me a short description related to it. only the description, nothing else."""
    )
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    time.sleep(60)

    all_response_data = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//div[contains(@class, 'chat-message assistant-message')]//div[@id='animation-variants-provider']",
            )
        )
    )

    game_description = None
    for data in all_response_data[::-1]:
        game_description = data.text
        break

    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@data-placeholder='Type your prompt here']")
        )
    )
    input_box.click()
    time.sleep(2)

    description_content = f"""Write a detailed blog post about '{blog_title}' and provide it in HTML format. Follow these guidelines:

1. Content must be well-structured with proper paragraphs (use single line breaks between paragraphs)
2. Include the word {category} naturally 2-3 times, and each time, assign it to the URL: {category_url} and provide strong tag to it. 
3. Maintain consistent spacing - no extra wide gaps
4. Use proper punctuation and capitalization
5. Keep sentences concise but engaging
6. Length should be about 300-500 words
7. Provide the HTML with all basic tags (html, head, body, etc.)

Return only the formatted text content, no headings or extra labels."""
    
    driver.execute_script(
        "arguments[0].innerText = arguments[1];",
        input_box,
        description_content,
    )
    time.sleep(2)
    input_box.send_keys(Keys.ENTER)
    time.sleep(50)

    all_response_data = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//div[contains(@class, 'chat-message assistant-message')]//div[@id='animation-variants-provider']",
            )
        )
    )

    blog_content = None
    for data in all_response_data[::-1]:
        blog_content = data.text
        break

    html_blog_content = extract_only_html_content(blog_content)

    prompt_text = """Ok, now please provide me only comma seperated keywords related to this blog, atleast 4-5, nothing else."""
    prompt_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[@data-placeholder='Type your prompt here']")
        )
    )
    prompt_field.click()
    time.sleep(10)

    driver.execute_script(
        "arguments[0].innerText = arguments[1];", prompt_field, prompt_text
    )
    time.sleep(5)
    prompt_field.send_keys(Keys.ENTER)
    time.sleep(60)

    all_response_data = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//div[contains(@class, 'chat-message assistant-message')]//div[@id='animation-variants-provider']",
            )
        )
    )

    blog_tags = None
    for data in all_response_data[::-1]:
        blog_tags = data.text
        break

    time.sleep(1)
    driver.quit()
    time.sleep(2)

    return game_description, html_blog_content, blog_tags, blog_title

def signup_and_update_profile(user,driver):
    time.sleep(3)

    # First Name
    username_field = driver.find_element(By.XPATH, '//input[@id="username"]')
    username_field.clear()
    username_field.send_keys(user["username"])

    email_field = driver.find_element(By.XPATH, "//input[@id='email']")
    email_field.clear()
    email_field.send_keys(user["email"])

    password_field = driver.find_element(By.XPATH, '//input[@id="password"]')
    password_field.clear()
    password_field.send_keys(user["password"])

    confirm_password_field = driver.find_element(By.XPATH, '//input[@id="confirm_password"]')
    confirm_password_field.clear()
    confirm_password_field.send_keys(user["password"])

    gender_dropdown = Select(driver.find_element(By.XPATH, "//select[@id='gender']"))
    gender_dropdown.select_by_value(user["gender"])

    checkbox = driver.find_element(
        By.XPATH,
        '//form[@id="register"]//label[@for="accept_terms"]',
    )
    checkbox.click()

    submit_button = driver.find_element(By.XPATH, "//button[@id='sign_submit']")
    submit_button.click()
    time.sleep(10)

    try:
    # If still on the registration page (signup failed), check for error message using XPath
        if driver.find_element(By.XPATH, '//form[@id="register"]//i[contains(@class, "fa fa-exclamation-circle")]'):
            print("User already exists, logging in instead...")
            login_user(user, driver)  # Log in
            return True  # Return True to indicate login was used
    except:
        pass

    go_to_profile(user)
    return False  # Return False to indicate fresh signup

#login 
def login_user(user,driver):
    driver.get("https://meta.mactan.com.br/")
    time.sleep(3)
    
    login_username_field = driver.find_element(By.XPATH, "//input[@id='username']")
    login_username_field.click()
    login_username_field.clear()
    login_username_field.send_keys(user["username"])

    login_password_field = driver.find_element(By.XPATH, "//input[@id='password']")
    login_password_field.click()
    login_password_field.clear()
    login_password_field.send_keys(user["password"])

    login_button = driver.find_element(By.XPATH,"//div[@class='login_signup_combo']/div[@class='login__']")
    login_button.click()
    time.sleep(5)


def go_to_profile(user):
    image_path = os.path.abspath("profile_picture.jpg")  # Change this to your image file name
    
    photo_input = driver.find_element(By.XPATH, "//div[@class='upload-image' and contains(@onclick, 'document.getElementById('avatar')')]")
    photo_input.send_keys(image_path)
    time.sleep(4)
    # photosave_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Save')]")
    # photosave_button.click()
    # time.sleep(4)
    # #submit to step 2 butten 
    # driver.execute_script("window.scrollBy(0, 300);") 
    # time.sleep(4)
    gotostep2_button = driver.find_element(By.XPATH, "//font[text()='Save and continue']")
    gotostep2_button.click()
    time.sleep(4)
    print("Profile photo uploaded successfully!")
    time.sleep(4)

    name_fields = driver.find_element(By.XPATH, "//input[@id='first_name']")
    name_fields.clear()
    name_fields.send_keys(user["first_name"])

    last_fields = driver.find_element(By.XPATH, "//input[@id='last_name']")
    last_fields.clear()
    last_fields.send_keys(user["last_name"])

    country_dropdown = Select(driver.find_element(By.XPATH, "//select[@name='country']"))
    country_dropdown.select_by_value(user["country"])

    gotostep1_button = driver.find_element(By.XPATH, "//font[text()='Save and continue']")
    gotostep1_button.click()
    time.sleep(4)
    # save
    gotostep3_button = driver.find_element(By.XPATH, "//font[text()='Save and continue']")
    time.sleep(2)
    gotostep3_button.click()
    print("Profile updated successfully!")
    time.sleep(5)

    #final 
    final_button = driver.find_element(By.XPATH, "//div[@class='clearfix mt20']/button[@type='submit']")
    time.sleep(2)
    final_button.click()
    print("Profile updated successfully!")
    time.sleep(5)

def go_to_blog(user,blog_title,game_description, blog_content, blog_tags, image_data ):
    blog_url = "https://meta.mactan.com.br/create-blog/"
    driver.get(blog_url)
    time.sleep(5)
#//input[@name='title']
    blog_title_field = driver.find_element(By.XPATH, "//input[@id='blog_title']")
    blog_title_field.clear()
    blog_title_field.send_keys(blog_title)

    game_description_field = driver.find_element(By.XPATH, "//textarea[@id='new-blog-desc']")
    game_description_field.clear()
    game_description_field.send_keys(game_description)
    time.sleep(8)

    open_tool = driver.find_element(By.ID, "mceu_29-open") 
    open_tool.click()
    time.sleep(5)
    Source_code = driver.find_element(By.XPATH, "//span[contains(text(),'Source code')]") 
    Source_code.click()
    time.sleep(3)

    content_of_blog = driver.find_element(By.XPATH, "//div[@role='application']//textarea")
    content_of_blog.send_keys(blog_content)
    time.sleep(5)
        
    ok_tool = driver.find_element(By.XPATH, "//span[contains(text(), 'Ok')]")
    ok_tool.click()
    time.sleep(5)
        
    upload_button = driver.find_element(By.XPATH, "//div[@class='wow_fcov_image']//div[@class='upload_ad_image']")    
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", upload_button
    )
    time.sleep(2)
    upload_button = driver.find_element(By.ID, "thumbnail")    
    upload_button.send_keys(os.path.abspath(image_data))

    category_dropdown_field = driver.find_element(By.XPATH, "//select[@id='blog_category']/option[contains(., 'Jogos')]")
    category_dropdown_field.click()

    blog_tags_field = driver.find_element(By.XPATH, "(//input[@placeholder='Tag'])[1]")
    blog_tags_field.clear()
    blog_tags_field.send_keys(blog_tags)
    blog_tags_field.send_keys(Keys.ENTER)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # button
    # publish_button = driver.find_element(By.XPATH, "//font[contains(text(), 'Publish')]")
    # driver.execute_script(
    #     "arguments[0].scrollIntoView({block: 'center'});", publish_button
    # )
    # time.sleep(2)
    # publish_button.click()
    time.sleep(15)

    print("Blog published successfully!")
    time.sleep(10)
    landing_page = driver.current_url
    print("Current URL:", landing_page)
    time.sleep(5)
    driver.quit()
    return landing_page

def add_logo_to_image(image_path, logo_base64, output_path, logo_width):
    image = Image.open(image_path)

    if logo_base64.startswith("data:image/webp;base64,"):
        logo_base64 = logo_base64.replace("data:image/webp;base64,", "")
    elif logo_base64.startswith("data:image/png;base64,"):
        logo_base64 = logo_base64.replace("data:image/png;base64,", "")
    elif logo_base64.startswith("data:image/jpg;base64,"):
        logo_base64 = logo_base64.replace("data:image/jpg;base64,", "")
    elif logo_base64.startswith("data:image/jpeg;base64,"):
        logo_base64 = logo_base64.replace("data:image/jpeg;base64,", "")

    logo_data = base64.b64decode(logo_base64)
    logo = Image.open(BytesIO(logo_data))

    logo_ratio = logo_width / float(logo.size[0])
    logo_height = int(float(logo.size[1]) * float(logo_ratio))
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    image_width, image_height = image.size
    position = (0, image_height - logo_height - 10)
    image.paste(logo, position, logo)
    image.save(output_path)

def logo_file_to_base64(logo_path):
    with open(logo_path, "rb") as image_file:
        return "data:image/png;base64," + base64.b64encode(image_file.read()).decode('utf-8')

        

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_argument("--accept-lang=en-US") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    while True:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
    
        website_url = "https://meta.mactan.com.br/register"
        driver.get(website_url)
        used_login = signup_and_update_profile(users, driver)
    
        for category, category_url in word_link_dict.items():
            max_retries = 3
            retry_count = 0
            success = False
        
            while not success and retry_count < max_retries:
                try:
                    print(f"\nProcessing category: {category} (Attempt {retry_count + 1})")
                    
                    print("Generating main image...")
                    generate_image(category)

                    print("\nAdding logo to image...")
                    try:
                        logo_base64 = logo_file_to_base64("pociwatermark.png")
                        add_logo_to_image(
                            "generated_image.jpg",
                            logo_base64,
                            "generated_image.jpg",
                            200
                        )
                        print("Logo added successfully to generated_image.jpg")
                    except Exception as e:
                        print(f"Error adding logo: {e}")
                        print("Continuing with original image without logo")

                    print("\nGenerating blog content...")
                    game_description, blog_content, blog_tags, blog_title = generate_blog_content(category, category_url)

                    landing_page = go_to_blog(
                        users,
                        blog_title,
                        game_description,    
                        blog_content, 
                        blog_tags, 
                        os.path.abspath("generated_image.jpg"),
                        
                    )

                    if landing_page == "https://meta.mactan.com.br/create-blog/":
                        raise Exception("Failed to publish blog")

                    parsed_uri = urlparse(landing_page)
                    base_landing_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}/"
                    print(f"Base landing URL extracted: {base_landing_url}")

                    sheet_name = re.sub(r'[^\w\s-]', '', category).strip().replace(' ', '_')

                    success = update_google_sheet(
                        name=users["first_name"],
                        email=users["email"],
                        password=users["password"],
                        blog_url=base_landing_url,
                        landing_page=landing_page,
                        blog_tags=blog_tags,
                        name_type=f"Blog Post - {category}",
                        status="DONE",
                        sheet_name=sheet_name
                    )

                    if not success:
                        print(f"Warning: Failed to update Google Sheet for {category}")
                    else:
                        print(f"Successfully processed category: {category}")
                
                except Exception as e:
                    retry_count += 1
                    print(f"Error processing category {category}: {str(e)}")
                
                    if retry_count < max_retries:
                        print(f"Restarting category {category}...")
                        try:
                            driver.quit()
                        except:
                            pass
                    
                        # Reinitialize driver for retry
                        driver = webdriver.Chrome(options=chrome_options)
                        driver.get("https://meta.mactan.com.br/")
                        login_user(users, driver)
                    else:
                        print(f"Max retries reached for category {category}. Moving to next category.")
        
        # Wait 30 minutes between categories (except after the last one)
       # Wait 30 minutes between categories (except after the last one)
            if category != list(word_link_dict.keys())[-1]:
                sleep_time = random.randint(3600, 7200)  # Random between 1-2 hours
                hours = sleep_time // 3600
                minutes = (sleep_time % 3600) // 60
                print(f"Waiting {hours} hour(s) and {minutes} minutes before next category...")
                driver.quit()
                time.sleep(sleep_time)
                
                # Reinitialize driver for next category
                driver = webdriver.Chrome(options=chrome_options)
                driver.get("https://meta.mactan.com.br/")
                login_user(users, driver)

        print("All categories processed. Exiting program.")
        try:
            driver.quit()
        except:
            pass
        time.sleep(7200)
    
    # "username": "pocigames",
    # "email": "pocigamesbacklinks@gmail.com",
    # "password": "#poci@games#backlinks!07#",
    # "confirm_password": "#poci@games#backlinks!07#",