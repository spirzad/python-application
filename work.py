import sys
sys.path.append('./modules')


if __name__ == "__main__":
    import json
    import glob
    import os.path
    from Onboarding_Checklist_Module import Onboarding_Checklist        
        
    checklist = Onboarding_Checklist(auth_token="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")
    type = "yaml"
    
    if type == "yaml":
        checklist.check_for_yaml()
        data = checklist.get_maintainers()
    
    for d in data:
        print(d)
