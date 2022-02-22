'''
Created on Feb 8, 2022

@author: spirzad
'''

import requests
import json
import time
import argparse
import base64

class GitHubClass:
    
    def __init__(self, auth_token):
        self.auth_token = auth_token
        
    def generate_header(self):
        self.header = {
            'Authorization': 'token '+self.get_auth_token()
        }
        self.proxies = {
            "http":"http://proxy-dmz.intel.com:912",
            "https":"http://proxy-dmz.intel.com:912",
        }
        
    def get_repositories_by_tag(self, tag):
        
        # Github API by Default returns only 30 results so we need to loop through every page until we reach [].
        page_number = 1
        json_result = []
        result = {"items": "Temp"}
        
        while result["items"] != []:
            self.url = "https://api.github.com/search/repositories?q="+tag+"+org:intel-innersource&page="+str(page_number)
            print(self.url)
            response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
            result   = response.text
            result = json.loads(result)
            for data in result['items']:
                json_result.append(data)
            
            page_number +=1
        return json_result
    
    # This can be used to fetch data from repos.yml/ teams.yml/ 
    def get_file_content(self, url):
        
        self.url = url
        print("INFO - ",self.url)
        error = True
        try:
            response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
            result   = response.text
            result = json.loads(result)
            
            print("INFO - Fetching file content..")
            print("Result : ", result)
            file_content = result['content']
            file_content_encoding = result.get('encoding')
            
            if file_content_encoding == 'base64':
                print("INFO - Decoding file content..")
                file_content = str(base64.b64decode(file_content).decode())
                error = False
        except Exception as e:
            print("ERR - Problem in fetching data from the URL - ",e)
            file_content = "Couldn't fetch File content."
            
            
        return (file_content,error)
        
        
    def get_pulls_allstate_by_repo(self, org, repo_name, pull_type):
        
        # Github API by Default returns only 30 results so we need to loop through every page until we reach [].
        page_number = 1
        json_result = []
        result = ["Temp"]
        
        if pull_type == "per_page":
            self.url = "https://api.github.com/repos/"+org+"/"+repo_name+"/pulls?state=all&per_page=100"
            print(self.url)
            response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
            result   = response.text
            result = json.loads(result)
            json_result = result
            
        else:
            while result != []:
                self.url = "https://api.github.com/repos/"+org+"/"+repo_name+"/pulls?state=all&page="+str(page_number)
                print(self.url)
                response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
                result   = response.text
                result = json.loads(result)
                
                for data in result:
                    json_result.append(data)
            
                page_number +=1
                
        return json_result
    
    def get_pulls_per_pullnumber(self, org, repo_name, number):
        
        self.url = "https://api.github.com/repos/"+org+"/"+repo_name+"/pulls/"+str(number)
        print(self.url)
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = response.text
        result = json.loads(result)
        
        return result
    
    def get_reviews_by_pullnumber(self, org, repo_name, pull_number):
        
        result_list = {}
        result_list.__setitem__("Repo Name", repo_name)
        result_list.__setitem__("Pull Number", pull_number)
        
        self.url = "https://api.github.com/repos/"+org+"/"+repo_name+"/pulls/"+str(pull_number)+"/reviews"
        print(self.url)
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = response.text
        result = json.loads(result)
        
        if result == []:
            result_list.__setitem__("Reviews", [{"state":"Required"}])
        else:
            result_list.__setitem__("Reviews", result)
        
        return result_list
        
    def get_reviews_by_repo(self, repo_name, state, review_type):
        # Either open, closed, or all to filter by state. Default: open
        
        result_list = {}
        result_list.__setitem__("Repo Name", repo_name)
        result_list.__setitem__("Review_Type", review_type)
        
        self.url = "https://api.github.com/search/issues?q=repo:intel-innersource/"+repo_name+"+is:pr+is:"+state+"+review:"+review_type
        print(self.url)
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = response.text
        result = json.loads(result)
            
        result_list.__setitem__("Reviews", result)
        return result_list
    
    def get_commits_per_pullnumber(self, org, repo_name, pull_number):
        
        result_list = {}
        result_list.__setitem__("Repo Name", repo_name)
        result_list.__setitem__("Pull Number", pull_number)
        
        self.url = "https://api.github.com/repos/"+org+"/"+repo_name+"/pulls/"+str(pull_number)+"/commits"
        print(self.url)
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = response.text
        result = json.loads(result)
        
        result_list.__setitem__("Commits", result)
        
        return result_list
    
    def get_collaborators_by_repo(self, repo_name):
        
        result_list = {}
        result_list.__setitem__("Repo Name", repo_name)
        
        self.url = "https://api.github.com/repos/intel-innersource/"+repo_name+"/collaborators"
        print(self.url)
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = response.text
        result = json.loads(result)
        
        if str(response) == "<Response [404]>":
            
            result_list.__setitem__("Collaborators", [])
        
        elif str(response) == "<Response [200]>":
            
            
            #result_list.__setitem__("Collaborators", result)
            
            all_data = []
           
            for row in result:
                collaborator_info = {}
                collaborator_info.__setitem__("Login", row["login"])
                collaborator_info.__setitem__("Permissions", row["permissions"])
                collaborator_info.__setitem__("Role_Name", row["role_name"])
                
                userID = row["login"]
                self.url = "https://api.github.com/users/"+userID
                print("INFO: ",self.url)
                response_user = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
                result_user   = response_user.text
                result_user = json.loads(result_user)
                
                collaborator_info.__setitem__("Name", result_user["name"])
                collaborator_info.__setitem__("Location", result_user["location"])
                collaborator_info.__setitem__("email", result_user["email"])
                
                all_data.append(collaborator_info)
            
                
            result_list.__setitem__("Collaborators", all_data)
            
        return result_list
    
    def get_permission_by_user(self, repo_name, user, type):
        
        self.url = "https://api.github.com/repos/intel-innersource/"+repo_name+"/collaborators/"+user+"/permission"
        print("INFO : Getting permission for - ", type,self.url)
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = response.text
        result = json.loads(result)
        
        if str(response) == "<Response [404]>":
            result = {"permission": "Not_Specified"}
            
        return result
        
    
    def get_contributors_by_repo(self, repo_name):
        try:
            self.url = "https://api.github.com/repos/intel-innersource/"+repo_name+"/contributors"
            response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
            result   = response.text
            result = json.loads(result)
            
            data = []
            for row in result:
                temp = {}
                login = row["login"]
                contributions = row["contributions"]
                
                temp.__setitem__("Repo_Name", repo_name)
                temp.__setitem__("Login", login)
                temp.__setitem__("Contribution", contributions)
                
                data.append(temp)
        except:
            print("Repo - ", repo_name, " err: Contribution list too large for API to support it.")
        
        return data
    
    def get_contributors_by_date(self, repo_name):
        try:
            self.url = "https://api.github.com/repos/intel-innersource/"+repo_name+"/stats/contributors"
            response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
            result   = response.text
            result = json.loads(result)
            
            
            data = []
            
            for row in result:
                total_commits = row["total"]
                total_weeks = row["weeks"]
                total_author = row["author"]
                
                print(row)
                temp = {}
                temp.__setitem__("Repo_Name", repo_name)
                temp.__setitem__("Total_Commits", total_commits)
                temp.__setitem__("Total_Weeks", total_weeks)
                temp.__setitem__("Total_Authors", total_author)
                
                data.append(temp)
            
        except:
            print("Repo - ", repo_name, " err: Can't get contribution stats.")
        
        return data
        
    
    def get_maintainers_from_project(self, team, project):
        self.url = "https://api.github.com/orgs/intel-innersource/teams/"+team+"/members"
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = str(response.text)
        result = json.loads(result)
        
        temp = {}
        temp.__setitem__("Project", project)
        temp.__setitem__("Team", team)
        temp.__setitem__("Members", result)
        
        return temp
        
    
    def get_languages_by_repo(self, repo_name):
        self.url = "https://api.github.com/repos/intel-innersource/"+repo_name+"/languages"
        response = requests.request("GET", url=self.get_restAPI(), headers=self.get_header(), proxies=self.get_proxy(), verify=True)
        result   = str(response.text)
        
        data = []
        temp = {}
        temp.__setitem__("Repo_Name", repo_name)
        temp.__setitem__("Languages", result)
        data.append(temp)
        
        return data
        
    def get_auth_token(self): return self.auth_token
    def get_proxy(self): return self.proxies
    def get_header(self): return self.header
    def get_restAPI(self): return self.url
    def get_total_repos(self): return self.total_repositories
    
