import requests
import json
import time
from alice.helper.constants  import GITHUB_REVIEW_ACCEPT_KEY, EP_REVIEWS, GITHUB_REPO_MEMBER
from alice.helper.decorators.retry import Retry
from alice.helper.api_manager import ApiManager

class PRFilesNotFoundException(Exception):
    def __init__(self, pr_response):
        self.pr_response = pr_response
        super(PRFilesNotFoundException, self).__init__(str(self.pr_response))


class GithubHelper:

    def __init__(self, org, repo, github_token, pr_api_link):
        self.pr_api_link = pr_api_link
        self.GITHUB_TOKEN = github_token
        self.headers = {"Authorization": "token " + self.GITHUB_TOKEN}

        url = GITHUB_REPO_MEMBER.format(org=org, repo=repo)
        response = ApiManager.get(url=url, headers=self.headers)
        if response["status_code"] != 200:
            raise Exception(response["content"], "Please check the provided Github Token, "
                               "either user doesn't have permission to the organisation or the repository")


    def comment_pr(self, comment_section, comment):
        resp = requests.post(comment_section, headers={"Authorization": "token " + self.GITHUB_TOKEN},
                             data=json.dumps(comment))
        print resp.content

    def modify_pr(self, msg, state):
        data = {
            "title": msg,
            "state": state
        }
        resp = requests.post(pr_api_link, json.dumps(data), headers={"Authorization": "token " + self.GITHUB_TOKEN})
        print resp.content

    def get_reviews(self):
        url = self.pr_api_link + "/" + EP_REVIEWS
        self.headers["Accept"] = GITHUB_REVIEW_ACCEPT_KEY
        reviews = requests.get(url, headers=self.headers)
        print "********** REVIEW ********************"
        return reviews

    def get_files_requests(self):
        url = self.pr_api_link + "/files"
        files = ApiManager.get(url, headers=self.headers)
        return files["response"].json()

    def is_pr_file_content_available(self, response):
        return not (isinstance(response, dict) and 'message' in response and response['message'] == "Not Found")


    @Retry(PRFilesNotFoundException, max_retries=20,
           default_value={"message": "Not Found", "documentation_url": "https://developer.github.com/v3"})
    def get_files(self):
        #import pdb; pdb.set_trace()
        files_content = self.get_files_requests()
        if not self.is_pr_file_content_available(files_content):
            raise PRFilesNotFoundException(files_content)
        print "********** FILE CONTENT ********************"
        #print files_content
        return files_content

