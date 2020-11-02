# Welcome to the documentation of the Django Schedule Api (DSA for short).

# Introduction
The main goal of the api is to be as easy to use as it can possibly be.  
The overall goal is to be precise, and easy to understand.  
The project has a simple core: You call the api, and it returns an object.  
Within this object, you can see if it failed or if it succeed.  
If it succeed, then you should be able to clearly see the object body, with well thought parameter names, and values.  
If it failed, then you should be able to see the code of the error, and understand it's cause reading the message body.

# Overview
Although it has a simple promise. It does has it's rules:  
For example, the date object is always in the day-month-year format.  
The api has a limit call of 15, and this number is reset every 15 minutes, giving a limit of 1 api call every minute.  
Other key-points are also presented in the rest of the documentation.    

# Authentication
In order to authenticate to the api, go to the /register/ page or on the index of the application, and click on the 'Register now' button.

# Error codes
There are a bunch of errors that can occur while using the api, to understand more of them, I have a separate file called CODES_ERRORS.md.  
There you can not only see the code of the error and what it means, but also a message displaying a human-readable info.  

# Rate Limit
As previously said, the api has a limit of 15 calls per 15 minutes.  
That being said, you can:
* Do 15 calls in 1 minute
* Do 1 call per minutes, for 15 minutes.  
The api calls values gets reset every fifteen minutes. So you should be able to call the api 60 times an hour.  

## Json Value Return
This is very important, this is the data you will receive every time you do an api call.  
First, the standardized way.  
Every time you do an api call, you will receive this same object.  
```json
{  
    "success": "boolean_value",  
    "data": {},
    "error": {}
}
```

## Success
Will be true if the return succeed.  
Will be false if it didn't.  
Boolean value.  

### Example:
```json
{
    "success": "true",  
    "data": {  
        "date": "18-10-2020",  
        "time": "16:20",  
        "company_name": "Dr4kk0nnys Inc."   
    },  
    "error": {}  
}
```

```json
{
    "success": "false",
    "data": {},
    "error": {
        "code": 3,
        "message": "You cannot schedule a meeting to the past."
    }
}
```

## Data
Will always be an object.  
Will always contain:
1. Date **(Day-Month-Year)**
    * **NOTE: Day and Month are always 2 characters long, and Year is always 4 characters long.**
        * **Example:** 20-10-2020 (Oct 20th, 2020)
    * **NOTE: Day and Month are not 0 index**
1. Time **(Hours:Minutes)**
    * **NOTE: Hours and Minutes are always 2 characters long.**
    * **NOTE: Hours cannot be greater than 19 or smaller than 7. Minutes can be either 0 or 30.**
        * **Examples:** 16:30, 17:00, 19:00, 08:30, 10:00, 7:00, 19:30
1. Company Name

#### Example

```json
{
    "success": "true",  
    "data": {  
        "date": "18-10-2020",  
        "time": "16:20",  
        "company_name": "Dr4kk0nnys Inc."   
    },  
    "error": {}  
}
```

```json
{
    "success": "true",  
    "data": {  
        "date": "11-11-2021",  
        "time": "08:30",  
        "company_name": "Dr4kk0nnys Inc."   
    },  
    "error": {}  
}
```

## Error
Will always be an object.  
Will always contain:
1. Code: **(number)**
1. Message: **(string)**

```json
{
    "success": "false",
    "data": {},
    "error": {
        "code": 3,
        "message": "You cannot schedule a meeting to the past."
    }
}
```

```json
{
    "success": "false",
    "data": {},
    "error": {
        "code": 2,
        "message": "You cannot schedule a meeting to a saturday or sunday."
    }
}
```

**Read more about the codes on the CODE_ERRORS.md file**

## How to send a post request
The api will always be expecting the same object:
```json
{
    "day": "20",
    "month": "10",
    "year": "2020",
    "hours": "16",
    "minutes": "00",
    "company_name": "Dr4kk0nnys Inc.",
    "token-id": "186a87fda690d7fb5bc66a963875968b5d31f771751f6b5f0f5602f135dc9225"
}
```
**NOTE: To register and get a token-id, go to the 'register/' page**  
# Time
While scheduling, it's really important to know which times are available.  
Otherwise, you would've been just guessing which times are not fully scheduled yet.  
Luckily the api takes care of it.  
Doing a post request to the ***api/time/*** url with the following parameters, returns
the times that are already scheduled.  
**To do a time request, you must first be authenticated**  

### Api call
The time api call will be expecting the following parameters:  
* Day
* Month
* Year
    * **NOTE:** Day and month must be 2 characters long. Year must be 4 characters long.
* Token ID  
    
### Example
```json
{
    "day": "20",
    "month": "06",
    "year": "2020",
    "token-id": "jh32jkh43jh23jh3j1h3jk21hj3asj3dha3c8zx7c87vxb7bgf97fss1ab2ja1"
}
```

### Return
The time-availability will always return the same object with the same parameters:
```json
{
    "success": "boolean_value",
    "data": {},
    "error": {}
}
```
**NOTE:** This same values also are returned on the main post call above, so I won't be reiterating those.

### Data
The only difference between the two objects ( time-availability and api-schedule ) is the data object.
The data object in the time-availability return is an object that holds an array of QuerySet.  

### Example
Calling the api
```json
{
    "day": "30",
    "month": "10",
    "year": "2020",
    "token-id": "423h234j2h34kj234jkh24329s8dsa97das89d1sad1hb12hb"
}
```
Api response
```json
{
    "success": "true",
    "data": [
        "2020-10-30 19:30:00: 1",
        "2020-10-30 19:00:00: 2"
    ],
    "error": {}
}
```  
**NOTE:** The value after the ':' is the amount of schedules to that day and time.  
The amount of schedules is 3 if the time is greater than 11:30.  
The amount of schedules is 5 if the time is smaller than 11:30.  


## More
The links used to create this documentation, and api in general are the following:
* https://stackoverflow.com/questions/12806386/is-there-any-standard-for-json-api-response-format
* https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/
* https://jsonapi.org/
* https://github.com/omniti-labs/jsend
* https://google.github.io/styleguide/jsoncstyleguide.xml
* https://learning.postman.com/docs/publishing-your-api/documenting-your-api/
