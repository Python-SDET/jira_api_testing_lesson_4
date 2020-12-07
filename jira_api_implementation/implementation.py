import yaml
import json
from jira_api_wrapper.jira_api import JiraApi
from jira_api_implementation import default_entity_path


class JiraImplementation:
    def __init__(self, entity_json=None):
        # Set default issue json
        entity_input_stream = open(default_entity_path, 'r')
        default_entity_json = yaml.load(entity_input_stream, Loader=yaml.SafeLoader)
        self.default_issue_json = default_entity_json['issue']
        self.default_sprint_json = default_entity_json['sprint']
        if entity_json:
            if 'issue' in entity_json:
                self.default_issue_json = entity_json['issue']

        self.jira_api = JiraApi()
        self.project = self.Project(self)
        self.issue = self.Issue(self)
        self.sprint = self.Sprint(self)

    def query(self, query_string):
        return self.jira_api.query(query_string)

    class Project:
        def __init__(self, implementation):
            self.project_url = r'rest/api/3/project/'
            self.implementation = implementation

        def get_project(self, project_id=None):
            return self.implementation.jira_api.get_entity(self.project_url, project_id)

    class Issue:
        def __init__(self, implementation):
            self.issue_url = r'rest/api/2/issue/'
            self.implementation = implementation

        def get_issue(self, issue_id=None):
            return self.implementation.jira_api.get_entity(self.issue_url, issue_id)

        def create_issue(self, issue_json=None):
            if not issue_json:
                issue_json = self.implementation.default_issue_json
            return self.implementation.jira_api.create_update_entity(self.issue_url, issue_json)

        def set_story_points(self, point_value, issue_id=None):
            issue_json = {'fields': {'customfield_10026': point_value}}
            return self.implementation.jira_api.create_update_entity(self.issue_url, issue_json, issue_id)

        def update_summary(self, revised_summary, issue_id=None):
            issue_json = {'fields': {'summary': revised_summary}}
            return self.implementation.jira_api.create_update_entity(self.issue_url, issue_json, issue_id)

        def update_description(self, revised_description, issue_id=None):
            issue_json = {'fields': {'description': revised_description}}
            return self.implementation.jira_api.create_update_entity(self.issue_url, issue_json, issue_id)

        def update_labels(self, label_list, issue_id=None):
            issue_json = self.implementation.default_issue_json
            del issue_json['fields']
            issue_json['fields'] = {'labels': label_list}
            return self.implementation.jira_api.create_update_entity(self.issue_url, issue_json, issue_id)

    class Sprint:
        def __init__(self, implementation):
            # A board number of 1 is used for the initial proof of concept
            # If additional boards are used, new code to handle that will be needed
            self.sprint_url = r'/rest/agile/1.0/'
            self.implementation = implementation

        def get_sprint(self, sprint_id=None):
            return self.implementation.jira_api.get_entity(self.sprint_url + r'board/1/sprint', sprint_id)

        def create_sprint(self, sprint_json=None):
            if not sprint_json:
                sprint_json = self.implementation.default_sprint_json
            return self.implementation.jira_api.create_update_entity(self.sprint_url + r'sprint/', sprint_json)

        def set_name(self, sprint_id, sprint_name):
            sprint_json = {'name': sprint_name}
            return self.implementation.jira_api.partial_sprint_update(
                self.sprint_url + r'sprint/', sprint_json, sprint_id)
