import json
import os
import sys
from datetime import datetime
import requests
from pyhandytools.file import FileUtils
from sparkdesk_web.utils import decode
from sparkdesk_web.web import create_chat_header, create_request_header
from sparkdesk_web.core import SparkWeb

NEW_CHAT = "SparkDesk AI chat"

class SparkWeb0(SparkWeb):
    def __init__(self, cookie, fd, GtToken, ChatID=""):
        super().__init__(cookie, fd, GtToken, ChatID)

    def continuous_chat(self, history_path: str = './history/', history_file_path: str = "", question: str = "", chat_id : str = ""):
        FileUtils.check_dir_path(history_path)
        if history_file_path == "" or history_file_path is None or not os.path.exists(history_file_path):
            history_file_path = os.path.join(history_path, f'history_{str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))}.json')
        else:
            history0 = json.load(open(history_file_path, 'r', encoding='utf-8'))
            self.__chat_history.extend(history0)
        try:
            self.__create_chat(NEW_CHAT)
