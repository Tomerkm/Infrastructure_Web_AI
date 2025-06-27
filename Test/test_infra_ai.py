# All Fixtures Are Found In conftest.py file
import asyncio
import os

import allure


async def browser_use_run(browser_use_agent):
    history = await browser_use_agent.run()
    result = history.final_result()

    assert result, f"Result is {result}"


def alumnium_run(convert_action_to_list_tuple, al):
    commands_mapping = {"do": al.do,
                        "check": al.check,
                        "get": al.get
                        }

    for command_al_info in convert_action_to_list_tuple:

        data_len = len(command_al_info)
        if data_len < 2:
            print(f"Data Len Should be 2 or 3 and not {data_len}")
            continue

        op_command = command_al_info[0].lower().strip()

        if not (op_command in ["do", "check", "get"]):
            print(f"OP Command need be one of the values: do, check, get and not {op_command}")
            continue

        text_command = command_al_info[1].strip()

        if "get" == op_command:
            expected_result = command_al_info[2].strip()
            data_result = commands_mapping[op_command](text_command)
            assert data_result == expected_result, f"Got Result = {data_result}, Expected Result = {expected_result}"

        else:
            commands_mapping[op_command](text_command)
@allure.title("Test Web AI")
@allure.description("This Test Tests Alumnium And Browser Use")
def test_web_browser_and_alumnium(convert_action_to_list_tuple, set_api_key, al, driver, browser_use_agent):
    if os.environ["FRAMEWORK"].lower().strip() == "Alumnium".lower():
        alumnium_run(convert_action_to_list_tuple=convert_action_to_list_tuple, al=al)
    elif os.environ["FRAMEWORK"].lower().replace(" ", "") == "Browser Use".lower().replace(" ", ""):
        asyncio.run(browser_use_run(browser_use_agent=browser_use_agent))
