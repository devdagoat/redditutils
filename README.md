# redditutils
Reddit utility for Python that basically puts PRAW on steroids if applied correctly.
It's by no means perfect but it works efficient enough.

## Installation

Put this script in your project directory.

## Usage

```python
  from redditutils import LoginUtils
  
  login_utility = LoginUtils("username","password")
  
  # appealing
  appeal_str = "explain here why you got your account suspended/shadowbaned and why it should be reinstated"
  resp = login_utility.appeal(appeal_str) # returns response object, do this if debug is needed:
  print(resp.json())
  
  # creating application
  client_id, client_secret = login_utility.create_app("My new app", app_type="script", desc="Some description", about_url="example.com", redir_uri="some redirect uri") #redir_uri is defaulted to localhost:8080
  # passing args is optional, script app with name "Test" and localhost redirect uri is created if nothing is passed
  
```
