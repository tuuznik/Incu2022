import re
from typing import List, Tuple

class DataHandler:
    def __init__(self) -> None:
        self.email_pattern = re.compile(r"[a-zA-z0-9]+@[a-z]+\.[a-z]+")
        self.username_pattern = re.compile(r"[a-zA-Z0-9]+")
        # minimum 7 characters
        self.password_pattern = re.compile(r"[a-zA-Z0-9\W]{7,}")
        self.description_pattern = re.compile(r"[a-zA-Z0-9\W]+")
        self.taskid_pattern = re.compile(r"[a-zA-Z0-9]+")
        self.completion_pattern = re.compile(r"True|False")
        self.patterns = {"email": self.email_pattern, 
                         "name" : self.username_pattern, 
                         "password": self.password_pattern, 
                         "description": self.description_pattern, 
                         "task_id": self.taskid_pattern,
                         "completed": self.completion_pattern}

    def check_options(self, expected_params_number: int, expected_params: List, params_list: List) -> Tuple:
        """
        Verifies if enough number of parameters were given for specific option. If so, parameters are compared to
        expected pattern and checked against required format.
        Parameters:
        expected_params_number (int) : number of expected parameters
        expected_params (List) : list of expected parameters
        params_list (List) : list of given parameters
        Returns:
        status (bool): information of whether operation succeeded or not
        msg (string): error logs or empty string (in case of success)
        data (dict): dictionary of verified parameters       
        """
        data = {}
        msg = ''
        print(params_list)
        if len(params_list) != expected_params_number:
            msg = "Not enough arguments to register a new user. Type **help** to see command details."
            return False, msg, None
        else:
            for i in range(len(expected_params)):
                option = expected_params[i]
                pattern = self.patterns[option]
                argument = params_list[i]
                result = pattern.match(argument)
                if not result:
                    msg = f"Incorrect {option} given. Operation failed."
                    return False, msg, None
                else:
                    data[option] = result.group(0)
            return True, msg, data

    def save_token(self, token: str):
        """
        Save token used for To Do App authentication to a txt file as a workaround to keep the information about currently
        logged in user.
        Parameters:
        token (string) : token used for To Do App authentication
        Returns:
        None
        """
        with open("token.txt", "w", encoding = 'utf-8') as f:
            f.write(token)

    def read_token(self) -> str:
        """
        Read token from a txt file.
        Parameters:
        Returns:
        token (string) : token used for To Do App authentication
        """
        with open("token.txt", "r", encoding = 'utf-8') as f:
            token = f.readline()
        return "".join(token)

    def remove_token(self):
        """
        Remove token from a txt file.
        Parameters:
        Returns:
        """
        open("token.txt", "w").close()
