import requests
import json
from decorators import exception_handler
from data_handling_helpers import DataHandler

class ToDoManager:
  def __init__(self) -> None:
      self.headers = {'Content-Type': 'application/json'}
      self.app_url = "https://api-nodejs-todolist.herokuapp.com"
      self.data_handler = DataHandler()

  @exception_handler
  def register_new_user(self, data_dict) -> bool:
    """
    Handles registration of a new user.    
    Parameters:
    data_dict (Dict): dictionary with required arguments which are: username, email, password
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    # set default age to 23
    data_dict["age"] = 23
    r = self.create_and_send_request(location = f"/user/register", payload=json.dumps(data_dict), method="POST")
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    else:
      data_dict = {key: data_dict[key] for key in ('email', 'password')}
      status, msg = self.login(data_dict=data_dict)
      return status, msg


  @exception_handler 
  def login(self, data_dict):
    """
    Handles login of existing user.    
    Parameters:
    data_dict (Dict): dictionary with required arguments which are: email, password
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    r = self.create_and_send_request(location = f"/user/login", payload=json.dumps(data_dict), method="POST")
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    else:
      self.data_handler.save_token(r['token']) 
    return True, description_buffer

  @exception_handler
  def logout(self):
    """
    Handles logout of currently logged in user.    
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    r = self.create_and_send_request(location = f"/user/logout", payload={}, method="POST", token_required=True)
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    else:
      self.data_handler.remove_token()
    return True, description_buffer   

  @exception_handler
  def add_new_task(self, data_dict):
    """
    Handles adding a new task to the To Do list.    
    Parameters:
    data_dict (Dict): dictionary with required arguments which are: description
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    r = self.create_and_send_request(location = f"/task", payload=json.dumps(data_dict), method="POST", token_required=True)
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    else:
      return True, description_buffer   

  @exception_handler
  def list_all_tasks(self):
    """
    Handles listing all saved task in the To Do list.    
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    r = self.create_and_send_request(location = f"/task", payload={}, method="GET", token_required=True)
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    else:
      tasks_count = r["count"]
      description_buffer += f"There are {tasks_count} tasks added to a To Do list\n"
      if int(tasks_count) > 0:
        task_list = r["data"]
        for task in task_list:
          status_desc = "Done" if task["completed"] else "To do"
          desc = task["description"]
          id = task["_id"]
          description_buffer += f"\nTask description: {desc}\n Id: {id}\n Status: {status_desc}\n"
      return True, description_buffer   

  @exception_handler
  def show_task(self, task_id):
    """
    Handles displaying chosen task from the To Do list.
    Parameters:
    task_id (string): id of a chosen task   
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    r = self.create_and_send_request(location = f"/task/{task_id}", payload={}, method="GET", token_required=True)
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    else:
      description_buffer += f"Showing task details of task with id {task_id}\n"
      task = r["data"]
      status_desc = "Done" if task["completed"] else "To do"
      desc = task["description"]
      description_buffer += f"\nTask description: {desc}\n Status: {status_desc}\n"
      return True, description_buffer

  @exception_handler
  def change_task_status(self, data_dict, task_id):
    """
    Handles changing status of a task in the To Do list.    
    Parameters:
    task_id (string): id of a chosen task 
    data_dict (Dict): dictionary with required arguments which are: completed
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    del data_dict["task_id"]
    data_dict["completed"] = eval(data_dict["completed"])
    r = self.create_and_send_request(location = f"/task/{task_id}", payload=json.dumps(data_dict), method="PUT", token_required=True)
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    return True, description_buffer

  @exception_handler
  def remove_task(self, task_id):
    """
    Handles removing task from the To Do list.    
    Parameters:
    task_id (string): id of a chosen task 
    Returns:
    status (bool): information of whether operation succeeded or not
    msg (string): error logs or empty string (in case of success)
    """
    description_buffer= ""
    r = self.create_and_send_request(location = f"/task/{task_id}", payload={}, method="DELETE", token_required=True)
    if "error" in r.keys():
      description_buffer += r["error"]
      return False, description_buffer
    return True, description_buffer

  def create_and_send_request(self, location: str, payload: dict, method: str, token_required: bool = False):
    """
    Create HTTP request, sends it and raise exception in case of error status code of HTTP response.   
    Parameters:
    location (string): path to requested resources
    payload (dict): payload used to pass parameters
    method (string): HTTP method
    token_required (bool): determines if token should be added to a header
    Returns:
    respons.json(): json representing HTTP response
    """
    url = self.app_url + location
    if token_required:
      self.create_token_header()
    response = requests.request(method, url, headers=self.headers, data=payload)
    response.raise_for_status()
    return response.json()


  def create_token_header(self):
    """
    Modifies HTTP headers to include token  
    Parameters:
    Returns:
    """
    token = self.data_handler.read_token()
    self.headers = {
      'Authorization': f'Bearer {token}',
      'Content-Type': 'application/json'
    }
