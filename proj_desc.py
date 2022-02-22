import sys
sys.path.append('modules')
from GitHubClass import GitHubClass
import argparse

if __name__ == "__main__":
    
  parser = argparse.ArgumentParser()
  parser.add_argument("--auth_token", "-a", help="You need to provide auth token.",type=str, required=True)
  args = parser.parse_args()
  
  # Getting auth token.
  auth_token = str(args.auth_token)
  
  # Github Class Instantiation.
  go = GitHubClass(auth_token=auth_token)
  go.generate_header()
  
  repo_names = ["python-application"]
  
  for repo in repo_names:
      repo_data = go.get_pulls_allstate_by_repo("spirzad" ,repo, pull_type="per_page")
      
      for data in repo_data:
          pull_number = data["number"]
          state = data["state"]
          message = data["body"]
          
          print("PR - ",pull_number," state - ", state ," message - ", message)
