import sys
sys.path.append('modules')


if __name__ == "__main__":
    import json
    import glob
    import os.path
    from Onboarding_Checklist_Module import Onboarding_Checklist
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth_token", "-a", help="You need to provide auth token.",type=str, required=True)
    args = parser.parse_args()
    
    auth_token = str(args.auth_token)
    checklist = Onboarding_Checklist(auth_token=auth_token)
    type = "yaml"
    
    if type == "yaml":
        checklist.check_for_yaml()
        data = checklist.get_maintainers()
    
    for d in data:
        print(d)
