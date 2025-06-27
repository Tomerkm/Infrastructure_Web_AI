import os
import ast
from selenium.webdriver import Chrome, Firefox, Edge, Safari

from alumnium import Alumni
from pytest import fixture
from dotenv import load_dotenv

# Use For Mapping To The Correct Browser According User Input
gb_browsers_storage = {"chrome": Chrome,
                       "firefox": Firefox,
                       "edge": Edge,
                       "safari": Safari
                       }

# Use For Mapping Variables To Original API Key Names
gb_api_keys_mapping_storage = {
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "ollama": ""
}


# Use To Read Environment Variables From .env File
@fixture(scope="session", autouse=True)
def load_global_var():
    load_dotenv()


# Convert The String To List Of Tuples - More Comfortable
@fixture(scope="session", autouse=True)
def convert_action_to_list_tuple(load_global_var):
    return ast.literal_eval(os.environ["ACTION"])


@fixture(scope="session", autouse=True)
def set_api_key(load_global_var):
    global gb_api_keys_mapping_storage

    model = os.environ["MODEL_NAME"].lower().strip()

    # If User Insert model name with version, it will find the model name only for mapping
    for key in gb_api_keys_mapping_storage.keys():
        if key in model or key in model:
            model = key
            break

    if not (model in "aws_meta" or "aws_meta" in model):
        model_api_key_name = gb_api_keys_mapping_storage[model]
        os.environ[model_api_key_name] = os.environ["API_KEY"]


# Init Browser And Get URL To Start Test It
@fixture(scope="session", autouse=True)
def driver(load_global_var):
    global gb_browsers_storage

    driver = gb_browsers_storage[os.environ["BROWSER"].lower().strip()]()
    driver.get(os.environ["URL"])
    yield driver
    driver.quit()


# Get Alumni
@fixture(scope="session", autouse=True)
def al(load_global_var, driver, convert_action_to_list_tuple):
    al = Alumni(driver)
    yield al
    al.quit()
