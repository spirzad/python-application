import sys
sys.path.append('modules')
from GitHubClass import GitHubClass
import argparse

if __name__ == "__main__":
    
  parser = argparse.ArgumentParser()
  parser.add_argument("--auth_token", "-a", help="You need to provide auth token",type=str, required=True)
  parser.add_argument("--pull_number", "-pr", help="You need to provide pull_number",type=str, required=True)
  parser.add_argument("--repo_org", "-ro", help="You need to provide repo org",type=str, required=True)
  parser.add_argument("--repo_name", "-rn", help="You need to provide repo name",type=str, required=True)
  args = parser.parse_args()
  
  # Getting auth token.
  auth_token = str(args.auth_token)
  pr_number = str(args.pull_number)
  repo_org = str(args.repo_org)
  repo_name = str(args.repo_name)
  
  # Github Class Instantiation.
  go = GitHubClass(auth_token=auth_token)
  go.generate_header()
  
  repo_names = repo_name.split()
  pr_desc = ""

  for repo in repo_names:
      repo_data = go.get_pulls_allstate_by_repo(repo_org ,repo, pull_type="per_page")
      
      for data in repo_data:
          pull_number = data["number"]
          state = data["state"]
          message = data["body"]
          
          if int(pull_number) == int(pr_number):
                pr_desc = message
                break
print("INFO - PR : ", pr_number)
print("INFO - PR_Desc", pr_desc)

if "AUTHOR" in pr_desc:
    response = go.post_comment_by_pr(org=repo_org, repo_name=repo_name, pull_number=pr_number, comment="Author is present in PR Description.")
else:
    response = go.post_comment_by_pr(org=repo_org, repo_name=repo_name, pull_number=pr_number, comment="This is crazy comment.")
