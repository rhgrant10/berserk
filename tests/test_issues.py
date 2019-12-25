'''
Created on 2019-12-25

@author: wf
'''
from berserk.clients import Client
from berserk.session import TokenSession
import requests
import os
import yaml

def getToken(self,tokenname="token"):
        home=os.getenv("HOME")
        #print(home)
        configPath=home+"/.berserk/config.yaml"
        if not os.path.isfile(configPath):
            print ("%s is missing please create it" % (configPath))
            return None
        config=yaml.load(open(configPath),Loader=yaml.FullLoader)
        if not tokenname in config:
            print ("no token found in %s please add it" % (configPath))
            return None
        return config[tokenname]

def test_Issue6_400_return():
    token=getToken("token")
    token_session = TokenSession(token)
    client=Client(token_session)
    error=False
    try:
        client.bots.abort_game("Ul3SHlm9")
    except requests.exceptions.HTTPError as httpError:
        error=True
        assert "This game can no longer be aborted" in str(httpError)
    assert error    
    
#test_Issue6_400_return()    
