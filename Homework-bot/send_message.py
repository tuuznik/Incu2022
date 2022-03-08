from flask import Flask, request
from data_handling_helpers import DataHandler
from todo_list_operations import ToDoManager
import requests
import json
import shlex

############## Bot details ##############

bot_name = 'todomanager@webex.bot'
# roomId = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vM2IzNmVjNTAtOWQ1Yy0xMWVjLWE1MTUtZTMwNTZlYzA4NWEz'
token = 'YjVlMWQxNGUtM2VjNC00MTBkLThlMGQtMzhmOTZlNGViOWVhNzk0NWUzYjgtNWMw_PE93_ed3fff69-a996-4e21-b5af-0dc3ad437459'

header = {"content-type": "application/json; charset=utf-8", 
          "authorization": "Bearer " + token}

############## Flask Application ##############
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def sendMessage():
    datahandler = DataHandler()
    to_do_manager = ToDoManager()
    webhook = request.json
    url = 'https://webexapis.com/v1/messages'
    msg = {"roomId": webhook["data"]["roomId"]}
    sender = webhook["data"]["personEmail"]
    params_list = getMessage()
    if (sender != bot_name):
        if ("help" in params_list):
            msg["markdown"] = "Welcome to **To Do Manager**!  \n Manage your To Do List in a simple and convenient way :) \n List of available commands: "\
                              "\n- **register** \n Description: Register new user \n Required arguments: username email password \n Example command: register test test@test.com testpassword"\
                              "\n- **login**\n Description: Login into To Do system \n Required arguments: email password \n Example command: login test@test.com testpassword"\
                              "\n- **addtask**\n Description: Add a new task to your list \n Required arguments: description \n Example command: addtask 'Example description'"\
                              "\n- **showall**\n Description: List all task saved in TO DO list \n  Example command: showall"\
                              "\n- **show**\n Description: Show task details \n Required arguments: task_id \n Example command: show 5ddcd1566b55da0017597239"\
                              "\n- **update**\n Description: Update task status \n Required arguments: task_id completion_status \n Example command: update 5ddcd1566b55da0017597239 True"\
                              "\n- **delete**\n Description: Remove chosen task \n Required arguments: task_id \n Example command: delete 5ddcd1566b55da0017597239"\
                              "\n- **help**"
        elif (params_list[0] == "register"):
            result, message, data = datahandler.check_options(expected_params_number=3, expected_params=['name', 'email', 'password'], params_list=params_list[1:])
            if result:
                status, message = to_do_manager.register_new_user(data_dict=data)
                if status:
                    msg["markdown"] = "User registered and logged in successfully"
                else:
                    msg["markdown"] = "User registration or login failed\n" + message
            else:
                msg["markdown"] = message
        elif (params_list[0] == "login"):
            result, message, data = datahandler.check_options(expected_params_number=2, expected_params=['email', 'password'], params_list=params_list[1:])
            if result:
                status, message = to_do_manager.login(data_dict=data)
                if status:
                    msg["markdown"] = "User logged in successfully"
                else:
                    msg["markdown"] = "Login failed\n" + message
            else:
                msg["markdown"] = message
        elif (params_list[0] == "logout"):
            status, message = to_do_manager.logout()
            if status:
                msg["markdown"] = "User logged out successfully"
            else:
                msg["markdown"] = "Logout failed\n" + message
        elif (params_list[0] == "addtask"):
            result, message, data = datahandler.check_options(expected_params_number=1, expected_params=['description'], params_list=params_list[1:])
            if result:
                status, message = to_do_manager.add_new_task(data_dict=data)
                if status:
                    msg["markdown"] = "Task added successfully"
                else:
                    msg["markdown"] = "Adding a new task failed\n" + message
            else:
                msg["markdown"] = message
        elif (params_list[0] == "showall"):
            status, message = to_do_manager.list_all_tasks()
            if status:
                msg["markdown"] = message
            else:
                msg["markdown"] = "Listing user's tasks failed\n" + message
        elif (params_list[0] == "show"):
            result, message, data = datahandler.check_options(expected_params_number=1, expected_params=['task_id'], params_list=params_list[1:])
            if result:
                status, message = to_do_manager.show_task(task_id = data['task_id'])
                if status:
                    msg["markdown"] = message
                else:
                    msg["markdown"] = "Showing task details failed\n" + message
            else:
                msg["markdown"] = message
        elif (params_list[0] == "update"):
            result, message, data = datahandler.check_options(expected_params_number=2, expected_params=['task_id', 'completed'], params_list=params_list[1:])
            if result:
                status, message = to_do_manager.change_task_status(data_dict=data, task_id = data['task_id'])
                if status:
                    msg["markdown"] = "Task status updated successfully"
                else:
                    msg["markdown"] = "Task status update failed\n" + message
            else:
                msg["markdown"] = message
        elif (params_list[0] == "delete"):
            result, message, data = datahandler.check_options(expected_params_number=1, expected_params=['task_id'], params_list=params_list[1:])
            if result:
                status, message = to_do_manager.remove_task(task_id = data['task_id'])
                if status:
                    msg["markdown"] = "Task removed successfully"
                else:
                    msg["markdown"] = "Task removal failed\n" + message
            else:
                msg["markdown"] = message
        else:
            msg["markdown"] = "Sorry! I didn't recognize that command. Type **help** to see the list of available commands."
        requests.post(url,data=json.dumps(msg), headers=header, verify=True)
    

def getMessage():
    webhook = request.json
    url = 'https://webexapis.com/v1/messages/' + webhook["data"]["id"]
    get_msgs = requests.get(url, headers=header, verify=True)
    message = get_msgs.json()['text']
    params_list = shlex.split(message)
    return params_list

app.run(debug = True)
header = {"content-type": "application/json; charset=utf-8", 
          "authorization": "Bearer " + token}
