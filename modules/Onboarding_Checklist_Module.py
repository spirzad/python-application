'''
Created on Feb 15, 2022

@author: spirzad
'''

import sys
sys.path.append('/home/runner/work/python-application/python-application/modules')

import json
import requests
from GitHubClass import GitHubClass

class Onboarding_Checklist:
    
    def __init__(self, auth_token):
        self.auth_token = auth_token
        
    def check_for_yaml(self):
        
        # Github Class Instantiation.
        go = GitHubClass(auth_token=self.auth_token)
        go.generate_header()
    
        print("***-- Checking repos.yml/teams.yml file --***")
        
        # Setting repos.yaml for all projects.
        yamls = {
            "linux-kernel": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/os/linux/kernel/repos.yml",
            "sbl": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/firmware/boot/bootloader/sbl/repos.yml",
            "manageability": "",
            "security-ovsa": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/frameworks/ai/openvino/ovsa/repos.yml",
            "driver-tcc": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/drivers/tgpio/repos.yml",
            "robotics-slam": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/applications/robotics/mobile/repos.yml",
            "star": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/frameworks/automation/star1.0/repos.yml",
            "devcloud": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/applications/services/devcloud/repos.yml",
            "edge-industrial": "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/applications/industrial/edge-insights/repos.yml",
            "edge-peak" : "",
            "devops-auto" : "https://api.github.com/repos/intel-innersource/inventory/contents/organizations/intel-innersource/repos/applications/devops/jenkins/repos.yml",
            "rbhe-edtech" : "",
            "rbhe-openamt": ""
        }
        
        maintainer_dist = []
        
        # Loop through every yaml url.
        for yaml in yamls:
            project = yaml
            project_url = yamls[yaml]
            
            print("INFO - Project : ", project)
            # If the project_url is empty or it exists.
            if project_url == "":
                print("ERR : URL is empty.")
            else:
                data,errors = go.get_file_content(project_url)
                # If error exists because of file doesn't exist or
                if errors:
                    print("ERR : File doesn't exist/connection with github couldn't be established.")
                else:
                    # Marking every maintain area in every repos.yml/teams.yml file 
                    data_split = data.replace("maintain:", "$tart").splitlines()
                    maintainer_name = []
                    
                    list_len = len(data_split)
                    
                    for i in range(0, list_len):
                        if "$tart" in data_split[i]:
                            start = i+1
                            while "- " in data_split[start]:
                                temp = {}
                                temp.__setitem__("Project", project)
                                temp.__setitem__("Maintainer Team", data_split[start].replace("- ","").strip())
                                maintainer_name.append(temp)
                                start+=1
                            
                            # Setting i=start to make list index not go through the same maintainer names.     
                            i = start
                    
                                        
                    # Remove Duplicates and put into maintainer_dist list
                    seen = set()
                    for entry in maintainer_name:
                        t = tuple(entry.items())
                        if t not in seen:
                            seen.add(t)
                            maintainer_dist.append(entry)
                            
        self.maintainers = maintainer_dist
    
    
    def check_for_codeowner_file(self):
        
        # Github Class Instantiation.
        go = GitHubClass(auth_token=self.auth_token)
        go.generate_header()
        
        print("***-- Checking codeowner file --***")
    
        # Define all the codeowner urls.
        code_owner_url = {
            "manageability" : ["https://api.github.com/repos/intel-innersource/applications.manageability.inband-manageability.iotg-manageability/contents/CODEOWNERS"],
            "sbl" : ["https://api.github.com/repos/intel-innersource/firmware.boot.bootloader.sbl.sblplatform/contents/.github/CODEOWNERS"],
            "linux-kernel" : ["https://api.github.com/repos/intel-innersource/os.linux.kernel.kernel-mlt-for-upstream/contents/.github/CODEOWNERS"],
            "star" : [
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.star/contents/.github/CODEOWNERS",
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.media-tests/contents/.github/CODEOWNERS",
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.manageability-tests/contents/.github/CODEOWNERS",
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.iotg-windows-tests/contents/.github/CODEOWNERS",
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.rt-kpi-tests/contents/.github/CODEOWNERS",
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.std-kpi-tests/contents/.github/CODEOWNERS",
                    "https://api.github.com/repos/intel-innersource/frameworks.automation.star.star-1-0.vision-kpi/contents/.github/CODEOWNERS"
                    ],
            "driver-tcc" : ["https://api.github.com/repos/intel-innersource/drivers.tgpio.linux-tgpio/contents/CODEOWNERS"],
            "edge-industrial" : ["https://api.github.com/repos/intel-innersource/applications.industrial.edge-insights.open-edge-insights-github-io/contents/.github/CODEOWNERS"],
            "robotics-slam" : ["https://api.github.com/repos/intel-innersource/applications.robotics.mobile.collaborative-slam/contents/.github/CODEOWNERS"],
            "security-ovsa" : ["https://api.github.com/repos/intel-innersource/frameworks.ai.openvino.ovsa.openvino-security/contents/CODEOWNERS"],
            "devops-auto" : ["https://github.com/intel-innersource/applications.devops.jenkins.jenkins-common-pipelines/blob/master/.github/CODEOWNERS"],
            "edge-peak" : [""],
            "devcloud" : [""],
            "rbhe-edtech" : ["https://api.github.com/repos/intel-collab/applications.iot.education.edtech/contents/.github/CODEOWNERS"],
            "rbhe-openamt" : [""]
        }
        
        codeowner_results = []
        
        # Looping through codeowner urls
        for url in code_owner_url:
            project = url
            c_url = code_owner_url[url]
            
            print("INFO - Project : ", project)
            
            # If url is empty 
            if c_url == "":
                print("ERR : URL is empty.")
                temp = {}
                temp.__setitem__("Project", project)
                temp.__setitem__("File_Exist", False)
                temp.__setitem__("Team", "")
                codeowner_results.append(temp)
            else:
                print(c_url)
                
                for url in c_url:
                    data,errors = go.get_file_content(url)
                    if errors:
                        print("ERR : No file Content/Couldn't establish connection with Github")
                        temp = {}
                        temp.__setitem__("Project", project)
                        temp.__setitem__("File_Exist", False)
                        temp.__setitem__("Team", "")
                        codeowner_results.append(temp)
                    else:
                        # Marking every maintain area in every repos.yml/teams.yml file 
                        data_split = data.splitlines()
                        
                        for line in data_split:
                            if "*" in line:
                                temp = {}
                                temp.__setitem__("Project", project)
                                temp.__setitem__("File_Exist", True)
                                temp.__setitem__("Team", line)
                                codeowner_results.append(temp)
    
        self.codeowner_list = codeowner_results
    
    def check_for_codecontribution_file(self):
        
        # Github Class Instantiation.
        go = GitHubClass(auth_token=self.auth_token)
        go.generate_header()
        
        print("***-- Checking codecontribution.md file --***")
        
        # Listing all the code_contribution Urls
        code_contribution_url = {
                "manageability" : "https://api.github.com/repos/intel-innersource/applications.manageability.inband-manageability.iotg-manageability/contents/CONTRIBUTING.md",
                "sbl" : "",
                "linux-kernel" : "https://api.github.com/repos/intel-innersource/os.linux.kernel.kernel-mlt-for-upstream/contents/.github/contributions.md",
                "security-ovsa" : "",
                "driver-tcc" : "https://api.github.com/repos/intel-innersource/drivers.tgpio.linux-tgpio/contents/contributions.md" ,
                "edge-peak" : "",
                "robotics-slam" : "https://api.github.com/repos/intel-innersource/applications.robotics.mobile.collaborative-slam/contents/.github/CONTRIBUTING.md",
                "star" : "https://api.github.com/repos/intel-innersource/frameworks.automation.star1.0.star/contents/.github/contributing.md",
                "devcloud" : "https://api.github.com/repos/intel-innersource/applications.services.devcloud.openshift-int-ms/contents/.github/CONTRIBUTING.md",
                "edge-industrial" : "https://api.github.com/repos/intel-innersource/applications.industrial.edge-insights.open-edge-insights-github-io/contents/.github/CONTRIBUTING.md",
                "devops-auto" : "",
                "rbhe-edtech" : "https://api.github.com/repos/intel-collab/applications.iot.education.edtech/contents/.github/CONTRIBUTING.md",
                "rbhe-openamt" : ""
        }
        
        cc_md = []
        
        # Looping through code contribution urls.
        for url in code_contribution_url:
            project = url
            c_url = code_contribution_url[url]
            
            print("\nINFO - Project : ", project)
            if c_url == "":
                print("ERR : URL is empty.")
                temp={}
                temp.__setitem__("Project", project)
                temp.__setitem__("contribution_md", False)
                cc_md.append(temp)
                
            else:
                data,errors = go.get_file_content(c_url)
                
                # If result has error than it means that the file doesn't exist or connection issue.
                if errors:
                    print("ERR : No file Content")
                    temp={}
                    temp.__setitem__("Project", project)
                    temp.__setitem__("contribution_md", False)
                    cc_md.append(temp)
                    
                else:
                    data_split = data.splitlines()
                    lines = int(len(data_split))
                    
                    if lines > 0:
                        temp={}
                        temp.__setitem__("Project", project)
                        temp.__setitem__("contribution_md", True)
                        cc_md.append(temp)
                    
            self.code_contribution_list = cc_md
        
    
    def get_maintainers(self):
        return self.maintainers
        
    def get_codeowners(self):
        return self.codeowner_list
        
    def get_codecontributions(self):
        return self.code_contribution_list
        
        
