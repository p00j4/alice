import jenkins
import requests
from datetime import datetime
from alice.helper.log_utils import LOG
import traceback

class JenkinsHelper(object):

    def __init__(self, pr):
        self.pr = pr
        self.token = self.pr.config.jenkinsToken
        LOG.debug("Form Jenkins Connection")
        self.jenkins = jenkins.Jenkins(self.pr.config.ci_jenkins_domain, username=self.pr.config.ci_jenkins_username,
                                       password=self.token)



    def build_job(self, job_name, files_modified):
        LOG.debug("**Hitting Job {0} on PR link {1}".format(job_name, self.pr.link_pretty))

        statuses_url = self.pr.status_url
        sha = statuses_url.rsplit("/", 1)[1]
        parameters = dict(repo=self.pr.head_repo, head_branch=self.pr.head_branch,
                                              base_branch=self.pr.base_branch,
                                              pr_no=self.pr.link_pretty, checker_tool="pylint", lint_path=files_modified,
                                              additional_flags="", msg="", machine="", sha=sha,
                                              author=self.pr.opened_by_slack)
        LOG.debug("*** job parameters=%s" %parameters)

        a = datetime.now()
        try:
            print "Jenkins token="+self.token
            #import pdb; pdb.set_trace()
            build_response = self.jenkins.build_job(job_name,parameters,{'token': self.token})
            print "*** triggered the job", build_response
            b = datetime.now()
            c = b - a
            print int(c.total_seconds()), " seconds"
            msg = "@{0} started tests, PR will be updated after tests are finished, check bottom for more details PR={1}".format(
                self.pr.opened_by_slack, self.pr.link_pretty)
            print msg
        except Exception, e:
            print e
            traceback.print_exc()

