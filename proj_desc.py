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
  go = GitHubClass(auth_token=self.auth_token)
  go.generate_header()
  
  repo_names = ["python-application"]
  
  for repo in repo_names:
      repo_data = go.get_pulls_allstate_by_repo("spirzad" ,repo, pull_type="per_page")
      
      for data in repo_data:
          print("INFO - ",data)