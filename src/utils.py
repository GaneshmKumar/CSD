""" Built in imports """
import json

"""
returns json file content
"""
def load_config_file(config_file):
    config_folder = 'config/'
    return json.load(open(config_folder + config_file))
