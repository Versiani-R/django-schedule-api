# Built-in documentation built by django rest framework and openapi.
**Note:** This file is the preview of the 'docs/' url.

HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/vnd.oai.openapi
Vary: Accept

openapi: 3.0.2
info:
  title: Schedule Api
  version: ''
  description: A simple-core, well documented api, for schedules.
paths:
  /register/:
    get:
      operationId: listRegisterViewSets
      description: Return the register template.
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items: {}
          description: ''
      tags:
      - register
    post:
      operationId: createRegisterViewSet
      description: Handle the register.
      parameters: []
      requestBody:
        content:
          application/json:
            schema: {}
          application/x-www-form-urlencoded:
            schema: {}
          multipart/form-data:
            schema: {}
      responses:
        '201':
          content:
            application/json:
              schema: {}
          description: ''
      tags:
      - register
  /api/:
    get:
      operationId: listScheduleApiViewSets
      description: List all the schedule meetings to the day.
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items: {}
          description: ''
      tags:
      - api
    post:
      operationId: createScheduleApiViewSet
      description: Create a new schedule meeting  to the day.
      parameters: []
      requestBody:
        content:
          application/json:
            schema: {}
          application/x-www-form-urlencoded:
            schema: {}
          multipart/form-data:
            schema: {}
      responses:
        '201':
          content:
            application/json:
              schema: {}
          description: ''
      tags:
      - api
  /calls/:
    get:
      operationId: listApiCallsViewSets
      description: List  the number of api calls of a certain account
      parameters: []
      responses:
        '200':
          content:
            application/json:
              schema:
                type: array
                items: {}
          description: ''
      tags:
      - calls
    post:
      operationId: createApiCallsViewSet
      description: Reset the number of api calls of a certain account
      parameters: []
      requestBody:
        content:
          application/json:
            schema: {}
          application/x-www-form-urlencoded:
            schema: {}
          multipart/form-data:
            schema: {}
      responses:
        '201':
          content:
            application/json:
              schema: {}
          description: ''
      tags:
      - calls