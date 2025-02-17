from selenium import webdriver
import pytest
import logging
from selenium.common.exceptions import NoSuchElementException

# Top 10 languages test data (simplified examples)
LANGUAGES = [
    {"name": "English", "data": {"first": "John", "last": "Doe", "message": "Hello World"}},
    {"name": "Mandarin", "data": {"first": "张伟", "last": "王芳", "message": "你好世界"}},
    {"name": "Hindi", "data": {"first": "राजेश", "last": "सिंह", "message": "नमस्ते दुनिया"}},
    {"name": "Spanish", "data": {"first": "José", "last": "Muñoz", "message": "Hola Mundo"}},
    {"name": "Arabic", "data": {"first": "محمد", "last": "علي", "message": "مرحبا بالعالم"}},
    {"name": "Bengali", "data": {"first": "রহিম", "last": "করিম", "message": "হ্যালো ওয়ার্ল্ড"}},
    {"name": "French", "data": {"first": "François", "last": "Dupont", "message": "Bonjour le monde"}},
    {"name": "Russian", "data": {"first": "Иван", "last": "Петров", "message": "Привет мир"}},
    {"name": "Portuguese", "data": {"first": "João", "last": "Silva", "message": "Olá Mundo"}},
    {"name": "Urdu", "data": {"first": "احمد", "last": "خان", "message": "ہیلو ورلڈ"}}
]

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_international_form_submission(browser):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    browser.get("https://www.threatpointer.com/contact")
    logging.info("Starting international form validation tests")
    
    for lang in LANGUAGES:
        try:
            logging.info(f"\n{'='*40}\nTesting {lang['name']} language submission\n{'='*40}")
            
            # Fill form fields
            browser.find_element(By.NAME, "first").send_keys(lang["data"]["first"])
            browser.find_element(By.NAME, "last").send_keys(lang["data"]["last"])
            browser.find_element(By.NAME, "message").send_keys(lang["data"]["message"])
            logging.debug("Filled name and message fields")
            
            # Add other fields with language-specific test data
            browser.find_element(By.NAME, "company").send_keys("Test Company - " + lang["name"])
            browser.find_element(By.NAME, "email").send_keys("test@example.com")
            browser.find_element(By.NAME, "phone").send_keys("+1234567890")
            
            logging.info("Submitting form...")
            browser.find_element(By.XPATH, "//button[contains(text(),'Send Message')]").click()
            
            # Verify submission
            try:
                success_message = browser.find_element(By.CSS_SELECTOR, ".success-message").text
                logging.info(f"Success message received: '{success_message}'")
                assert "Thank you" in success_message
            except NoSuchElementException:
                error_message = browser.find_element(By.CSS_SELECTOR, ".error-message").text
                logging.error(f"Submission failed for {lang['name']}. Error: {error_message}")
                raise
            finally:
                logging.debug(f"Page source after submission:\n{browser.page_source[:500]}...")
                
            browser.back()
            logging.info(f"{lang['name']} test completed successfully\n")
            
        except Exception as e:
            logging.error(f"Test failed for {lang['name']}: {str(e)}")
            raise
            
    logging.info("All international language tests completed") 