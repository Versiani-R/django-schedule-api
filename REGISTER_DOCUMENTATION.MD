# Welcome to the register documentation of the Django Schedule Api (DSA for short).

# Introduction
The goal of the register api is to make sure every request to the schedule api is validated.  
With that being said, every user that actively uses the schedule api, must have a token id.  
The way to obtain the token id is through a proper registration.  

# Overview
The promise of the register api is quite simple.  
It requires:
* A valid email
* A valid and strong password

# Authentication
To authenticate, you have two options:
* Go to the register/ url
* Send a post request to the register/ url

### Sending a post request to the register/ url
The post validation requires two fields:
* Email
* Password

# Error codes
## Error code 1:
Invalid or Incorrect data on the post request.

## Error code 2:
Invalid or Incorrect credentials. Email already registered.

## Error code 3:
Invalid or Incorrect credentials. Weak credentials.

# Rate Limit
There is no rate limit since it's a register page, and it does not make sense asking for a token id, since the user is trying to get one in the first place.

# Success
If the register was successfull, the api returns a response like this:
```json
{
    "success": "true",
    "data": {
        "email": "registered-email@example.com",
        "token-id": "32321h5443j42h31hasf198f34d6788y203jw98kl5jh8ladh5fa87u29yhhfjkadh891y22h1221"
    },
    "error": {}
}
```
