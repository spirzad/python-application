import sys
sys.path.insert(0, "..\\modules")


if __name__ == "__main__":
    import json
    import glob
    import os.path
    import pandas as pd
    from Onboarding_Checklist_Module import Onboarding_Checklist
        
    # Parsing argument in the API.
    parser = reqparse.RequestParser()   #/isdm_onboarding?type=yaml
    parser.add_argument("type", type=str)
    args = parser.parse_args() 
        
        
    checklist = Onboarding_Checklist(auth_token="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")
    type = args["type"]
        
    if type == "yaml":
        checklist.check_for_yaml()
        data = checklist.get_maintainers()
    
    for d in data:
        print(d)