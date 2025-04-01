import requests
from gitlab_cli.config import (
    HEADERS,
    PROJECTS_ENDPOINT,
    USERS_ENDPOINT,
    GROUPS_ENDPOINT,
    CURRENT_USER_ENDPOINT,
    ERROR_REQUEST_FAILED,
)


class GitLabAPI:
    def __init__(self):
        self.headers = HEADERS

    def _make_request(self, method, url, params=None, data=None):
        """Make a request to the GitLab API"""
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(ERROR_REQUEST_FAILED.format(str(e)))

    def get_projects(self, params=None):
        """Get list of projects"""
        return self._make_request("GET", PROJECTS_ENDPOINT, params=params)

    def get_project(self, project_id):
        """Get specific project by ID"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}"
        return self._make_request("GET", url)

    def create_project(self, name, description=None):
        """Create a new project"""
        data = {"name": name, "description": description}
        return self._make_request("POST", PROJECTS_ENDPOINT, data=data)

    def get_users(self, params=None):
        """Get list of users"""
        return self._make_request("GET", USERS_ENDPOINT, params=params)

    def get_user(self, user_id):
        """Get specific user by ID"""
        url = f"{USERS_ENDPOINT}/{user_id}"
        return self._make_request("GET", url)

    def get_groups(self, params=None):
        """Get list of groups"""
        return self._make_request("GET", GROUPS_ENDPOINT, params=params)

    def get_group(self, group_id):
        """Get specific group by ID"""
        url = f"{GROUPS_ENDPOINT}/{group_id}"
        return self._make_request("GET", url)

    def get_project_branches(self, project_id):
        """Get list of branches for a project"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/repository/branches"
        return self._make_request("GET", url)

    def get_project_commits(self, project_id):
        """Get list of commits for a project"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/repository/commits"
        return self._make_request("GET", url)

    def get_project_issues(self, project_id, params=None):
        """Get list of issues for a project"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/issues"
        return self._make_request("GET", url, params=params)

    def get_project_issue(self, project_id, issue_iid):
        """Get a specific issue by project ID and issue IID

        Returns issue data if found, None if not found or on error
        """
        try:
            url = f"{PROJECTS_ENDPOINT}/{project_id}/issues/{issue_iid}"
            return self._make_request("GET", url)
        except Exception as e:
            # Instead of raising an exception, return None on HTTP errors
            print(f"Error retrieving issue: {str(e)}")
            return None

    def create_project_issue(
        self,
        project_id,
        title,
        description=None,
        labels=None,
        assignee_ids=None,
        milestone_id=None,
        due_date=None,
        confidential=False,
        weight=None,
    ):
        """Create a new issue in a project with extended options"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/issues"
        data = {"title": title, "description": description}

        # Add optional parameters if provided
        if labels:
            data["labels"] = labels
        if assignee_ids:
            data["assignee_ids"] = assignee_ids
        if milestone_id:
            data["milestone_id"] = milestone_id
        if due_date:
            data["due_date"] = due_date
        if confidential:
            data["confidential"] = confidential
        if weight is not None:
            data["weight"] = weight

        return self._make_request("POST", url, data=data)

    def update_project_issue(self, project_id, issue_iid, **kwargs):
        """Update an existing issue

        Allowed kwargs: title, description, state_event, labels, assignee_ids,
        milestone_id, due_date, confidential, weight, etc.
        """
        url = f"{PROJECTS_ENDPOINT}/{project_id}/issues/{issue_iid}"
        return self._make_request("PUT", url, data=kwargs)

    def delete_project_issue(self, project_id, issue_iid):
        """Delete an issue (actually closes it as GitLab doesn't allow true deletion via API)"""
        return self.update_project_issue(project_id, issue_iid, state_event="close")

    def create_issue_relationship(
        self,
        project_id,
        issue_iid,
        target_project_id,
        target_issue_iid,
        link_type="relates_to",
    ):
        """Create a relationship between issues

        link_type can be: relates_to, blocks, is_blocked_by, etc.
        """
        url = f"{PROJECTS_ENDPOINT}/{project_id}/issues/{issue_iid}/links"
        data = {
            "target_project_id": target_project_id,
            "target_issue_iid": target_issue_iid,
            "link_type": link_type,
        }
        return self._make_request("POST", url, data=data)

    def get_issue_links(self, project_id, issue_iid):
        """Get all issues related to the given issue"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/issues/{issue_iid}/links"
        return self._make_request("GET", url)

    def remove_issue_link(self, project_id, issue_iid, issue_link_id):
        """Remove a link between two issues"""
        url = (
            f"{PROJECTS_ENDPOINT}/{project_id}/issues/{issue_iid}/links/{issue_link_id}"
        )
        return self._make_request("DELETE", url)

    def get_project_merge_requests(self, project_id, params=None):
        """Get list of merge requests for a project"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/merge_requests"
        return self._make_request("GET", url, params=params)

    def create_merge_request(self, project_id, source_branch, target_branch, title):
        """Create a new merge request"""
        url = f"{PROJECTS_ENDPOINT}/{project_id}/merge_requests"
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
        }
        return self._make_request("POST", url, data=data)

    def get_current_user(self):
        """Get information about the current authenticated user."""
        return self._make_request("GET", CURRENT_USER_ENDPOINT)
