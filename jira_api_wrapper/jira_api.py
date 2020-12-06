"""
This module is a wrapper for the jira api
"""
import yaml
import requests
from requests.auth import HTTPBasicAuth
from jira_api_wrapper import jira_info_path


class JiraApi:
    """
    This class is a wrapper for the jira api
    """
    def __init__(self):
        self.url = None
        jira_info_stream = open(jira_info_path, 'r')
        jira_info = yaml.load(jira_info_stream, Loader=yaml.SafeLoader)
        self.url = jira_info['jira_url']
        self.token = jira_info['token']
        self.user_id = jira_info['user_id']
        self.headers = jira_info['headers']
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.user_id, self.token)

    def get_entity(self, entity_url, entity_id=None):
        if not entity_id:
            entity_id = ''
        entity_json = self.session.get(self.url + entity_url + entity_id)
        return entity_json

    def create_update_entity(self, entity_url, entity_json, entity_id=None):
        if not entity_id:
            issue_response = self.session.post(self.url + entity_url, headers=self.headers, json=entity_json)
        else:
            issue_response = self.session.put(self.url + entity_url + entity_id, headers=self.headers, json=entity_json)
        return issue_response

    def query(self, query_string):
        search_url = r'rest/api/2/search/?jql='
        query_response = self.session.get(self.url + search_url + query_string)
        return query_response
