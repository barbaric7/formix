from selenium.webdriver.common.by import By

def extract_questions(driver):
    mcq_blocks = []
    question_blocks = driver.find_elements(By.XPATH, "//div[@role='listitem']")

    for block in question_blocks:
        try:
            radios = block.find_elements(By.XPATH, ".//div[@role='radio']")

            if len(radios) == 0:
                continue

            try:
                question_text = block.find_element(
                    By.XPATH, ".//div[@role='heading']"
                ).text.strip()
            except:
                continue

            options = []
            elements = []

            for radio in radios:
                try:
                    option_text = radio.get_attribute("data-value")
                    
                    if not option_text:
                        option_text = radio.get_attribute("aria-label")

                    if option_text:
                        options.append(option_text.strip())
                        elements.append(radio)
                except:
                    continue

            if options:
                mcq_blocks.append({
                    "question": question_text,
                    "options": options,
                    "elements": elements
                })

        except:
            continue

    return mcq_blocks