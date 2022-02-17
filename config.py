# [https://stackoverflow.com/questions/472000/usage-of-slots]
# [https://towardsdatascience.com/understand-slots-in-python-e3081ef5196d]

# [https://stackoverflow.com/questions/49883177/how-does-lru-cache-from-functools-work]


import os
import configparser
from functools import lru_cache


class Config:

    __slots__ = (
        'config_filepath',

        'api_service_name',
        'api_version',
        'developer_key'
    )

    config_filepath: str

    api_service_name: str
    api_version: str
    developer_key: str

    def __init__(self, _config_filepath):
        self.config_filepath = _config_filepath
        _cfg = configparser.ConfigParser()
        _cfg.read(self.config_filepath)

        self.api_service_name = _cfg['service']['api_service_name']
        self.api_version = _cfg['service']['api_version']
        self.developer_key = _cfg['creds']['developer_key']


@lru_cache()
def get_config(_config_filepath):
    return Config(_config_filepath)
