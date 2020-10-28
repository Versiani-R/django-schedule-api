# Welcome to the documentation of the Django Schedule Api (DSA for short).

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
    * **NOTE: Day and Month must be 2 characters long, and Year must be 4 characters long.**
    * **CORRECT:** 20-10-2020 (Oct 20th, 2020)
    * **INCORRECT:** 2-5-2020 (May 2nd, 2020) 
    * **NOTE: Day and Month are not 0 index**
1. Time **(Hours:Minutes)**
    * **NOTE: Hours and Minutes must be both 2 characters long.**
    * **NOTE: Hours cannot be greater than 23 or smaller than 1. Minutes cannot be greater than 59 or smaller than 1.**
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
    "minutes": "20",
    "company_name": "Dr4kk0nnys Inc.",
    "token-id": "186a87fda690d7fb5bc66a963875968b5d31f771751f6b5f0f5602f135dc9225"
}
```
**NOTE: To register and get a token-id, go to the 'register/' page**

## More
The links used to create this documentation, and api in general are the following:
* https://stackoverflow.com/questions/12806386/is-there-any-standard-for-json-api-response-format
* https://stackoverflow.blog/2020/03/02/best-practices-for-rest-api-design/
* https://jsonapi.org/
* https://github.com/omniti-labs/jsend
* https://google.github.io/styleguide/jsoncstyleguide.xml