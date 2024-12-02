import os
import agentql
from playwright.sync_api import sync_playwright
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
os.environ["AGENTQL_API_KEY"] = os.getenv("AGENTQL_API_KEY")
INITIAL_URL = "https://simplywall.st/welcome?r=%2Fdashboard"


EMAIL_QUERY = """
{
    login_form{
        email_input

    }
}
"""

VERIFY_QUERY = """
{
    login_form{
        verify_not_robot_checkbox
    }
}
"""

PASSWORD_QUERY = """
{
    login_form{
        password_input
        continue_button
    }
}
"""


with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
    page = agentql.wrap(browser.new_page())
    page.goto(INITIAL_URL)

    #use query_elements() method to find button on bottom of page
    response = page.query_elements(EMAIL_QUERY)
    response.login_form.email_input.fill(EMAIL)
    page.wait_for_timeout(1000)



    verify_response = page.query_elements(VERIFY_QUERY)
    verify_response.login_form.verify_not_robot_checkbox.click()
    page.wait_for_timeout(1000)

    response.login_form.continue_button.click()

    password_response = page.query_elements(PASSWORD_QUERY)
    password_response.login_form.password_input.fill(PASSWORD)
    page.wait_for_timeout(1000)

    password_response.login_form.continue_button.click()

    page.wait_for_page_ready_state()