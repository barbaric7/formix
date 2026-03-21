import time
import base64
import os
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.print_page_options import PrintOptions
from config import FORM_URL, EDGE_PROFILE_PATH
from scraper import extract_questions
from evaluator import get_final_answer
from form_filler import fill_student_details, click_option, submit_form


def setup_driver():
    options = Options()
    options.add_argument(f"--user-data-dir={EDGE_PROFILE_PATH}")
    options.add_argument("--start-maximized")

    service = Service("msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    return driver


def slow_scroll_to_bottom(driver):
    print("Scrolling to load MCQs...")

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(1)

        new_position = driver.execute_script(
            "return window.pageYOffset + window.innerHeight"
        )
        full_height = driver.execute_script(
            "return document.body.scrollHeight"
        )

        if new_position >= full_height:
            break

    time.sleep(2)

def save_as_pdf(driver):
    print("\nPreparing to save PDF...")
    
    # We must switch to the default content out of the iframe
    driver.switch_to.default_content()
    
    # 1. Grab the actual page title for the default name
    page_title = driver.title
    if not page_title:
        page_title = "Google_Form"
        
    # Clean the title so Windows doesn't crash from invalid filename characters
    safe_title = re.sub(r'[\\/*?:"<>|]', "", page_title).strip()
    filename = f"{safe_title}.pdf"
    
    # 2. Dynamically find the user's default Downloads folder
    downloads_folder = os.path.join(Path.home(), "Downloads")
    full_path = os.path.join(downloads_folder, filename)
    
    print(f"Generating PDF as: {filename}")
    
    print_options = PrintOptions()
    print_options.background = True 
    
    pdf_base64 = driver.print_page(print_options)
    
    # 3. Save it directly to the Downloads folder
    with open(full_path, "wb") as f:
        f.write(base64.b64decode(pdf_base64))
        
    print(f"✅ PDF saved successfully to: {full_path}")
    
    # Switch back to the iframe so we can click the submit button next
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        driver.switch_to.frame(iframes[0])


def main():
    print("🚀 Starting Form Automation System")

    driver = setup_driver()
    driver.get(FORM_URL)

    time.sleep(5)  # allow full page render
    
    # Switch to Google Form iframe if present
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        print("Switching to form iframe...")
        driver.switch_to.frame(iframes[0])
        time.sleep(2)

    # ----------------------------
    # STEP 1: Fill Student Details
    # ----------------------------
    print("Filling student details...")
    # fill_student_details(driver)
    # time.sleep(2)

    # ----------------------------
    # STEP 2: Scroll to Load MCQs
    # ----------------------------
    slow_scroll_to_bottom(driver)

    # ----------------------------
    # STEP 3: Extract MCQs
    # ----------------------------
    print("Extracting MCQs...")
    questions = extract_questions(driver)
    print(f"Total MCQs found: {len(questions)}")

    if len(questions) == 0:
        print("❌ No MCQs detected. Stopping.")
        input("Press Enter to close browser...")
        return

    # ----------------------------
    # STEP 4: Solve and Click
    # ----------------------------
    # for i, q in enumerate(questions, 1):
    #     print("\n====================================")
    #     print(f"Q{i}: {q['question']}")

    #     for opt in q["options"]:
    #         print(" -", opt)

    #     final_answer = get_final_answer(q["question"], q["options"])
    #     print("Selected:", final_answer)
    #     click_option(driver, final_answer, q["options"], q["elements"])
    #     time.sleep(1)

    # print("\n✅ All MCQs processed.")

    # ----------------------------
    # STEP 5: Save PDF & Submit
    # ----------------------------
    
    # Save the filled form as a PDF in the same directory as the script
    save_as_pdf(driver)
    
    # Click the submit button
    # submit_form(driver)

    input("\nPress Enter to close browser...")


if __name__ == "__main__":
    main()