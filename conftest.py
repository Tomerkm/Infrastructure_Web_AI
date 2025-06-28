from dotenv import load_dotenv
# Order is matter, Alumni call constructor and init the provider to the default openapi.
# So I load env before it happening
# Use To Read Environment Variables From .env File
load_dotenv()

import os
import ast
from selenium.webdriver import Chrome, Firefox, Edge, Safari
from browser_use import Agent
from browser_use.llm import ChatAnthropic
from browser_use.llm import ChatGoogle
from browser_use.llm import ChatOpenAI
from browser_use.llm import ChatAzureOpenAI
from browser_use.llm import ChatGroq

from alumnium import Alumni
from pytest import fixture

# Use For Mapping To The Correct Browser According User Input
gb_browsers_storage = {"chrome": Chrome,
                       "firefox": Firefox,
                       "edge": Edge,
                       "safari": Safari
                       }

# Use For Mapping Variables To Original Providers API Key Names
gb_api_keys_mapping_storage = {
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "ollama": "OLLAMA_API_KEY",
    "azure": "AZURE_OPENAI_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "grok": "GROK_API_KEY",
    "novita": "NOVITA_API_KEY"
}

model_name = os.environ["MODEL_NAME"].lower().strip()

# Use For Mapping To Function Directly And Send Model By Correct Name
gb_mapping_to_providers_api = \
{
    "anthropic": (ChatAnthropic, {"model_name": model_name}),
    "google": (ChatGoogle, {"model": model_name}),
    "openai": (ChatOpenAI, {"model": model_name}),
    "azure": (ChatAzureOpenAI, {"model": model_name}),
    "grok": (ChatGroq, {"model": model_name}),
}


# Convert The String To List Of Tuples - More Comfortable
@fixture(scope="session", autouse=True)
def convert_action_to_list_tuple():
    # Only Alummnium Support This Format
    if os.environ["FRAMEWORK"].lower().strip() != "Alumnium".lower():
        return None
    else:
        return ast.literal_eval(os.environ["ACTION"])


@fixture(scope="session", autouse=True)
def set_api_key():
    global gb_api_keys_mapping_storage

    provider = os.environ["ALUMNIUM_MODEL"].lower().strip()
    if "ollama" in provider or provider in "ollama":
        return None

    # If User Insert provider name with version, it will find the provider name only for mapping
    for key in gb_api_keys_mapping_storage.keys():
        if key in provider or key in provider:
            provider = key
            break

    if not (provider in "aws_meta" or "aws_meta" in provider):
        provider_api_key_name = gb_api_keys_mapping_storage[provider]
        os.environ[provider_api_key_name] = os.environ["API_KEY"]


# Init Browser And Get URL To Start Test It
@fixture(scope="session", autouse=True)
def driver():
    # Only Alummnium Use Driver - Selenium
    if os.environ["FRAMEWORK"].lower().strip() != "Alumnium".lower():
        yield None
    else:
        global gb_browsers_storage

        driver_res = gb_browsers_storage[os.environ["BROWSER"].lower().strip()]()
        driver_res.get(os.environ["URL"])
        yield driver_res
        driver_res.quit()


# Get Alumni
@fixture(scope="session", autouse=True)
def al(driver, set_api_key, convert_action_to_list_tuple):
    # Only Alummnium Use Driver - Selenium
    if os.environ["FRAMEWORK"].lower().strip() != "Alumnium".lower():
        yield None
    else:
        al_res = Alumni(driver)
        yield al_res
        al_res.quit()


@fixture(scope="session", autouse=True)
def browser_use_agent(set_api_key):
    # Only Relevant To Browser Use
    if os.environ["FRAMEWORK"].lower().replace(" ", "") != "Browser Use".lower().replace(" ", ""):
        yield None
    else:
        global gb_mapping_to_providers_api

        provider_key = os.environ["ALUMNIUM_MODEL"].lower().strip()
        provider_func_call, kwargs = gb_mapping_to_providers_api[provider_key]

        url = os.environ["URL"]
        action = os.environ["ACTION"]

        agent = Agent(
            task=f"Go To {url} Website, And {action}",
            llm=provider_func_call(**kwargs),
        )

        yield agent
