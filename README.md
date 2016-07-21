# astroApp
In Progress
MSSQL Server + Rest API (python) + Client (angular.js)

This application is a concept application. The puropse is to check ability of rest service to consume big data.
It consists of following elements:

DB 'Astro' consists of:

Tables

    1. stg.stagingObservations 
    2. bi.observations 
    3. bi.uPhotometry 
    4. bi.vPhotometry 
    5. bi.bPhotometry 
    6. bi.uPhotometryTime 
    7. bi.vPhotometryTime 
    8. bi.bPhotometryTime 
    9. bi.hrDiagram
    10.log.log 
    11.data.fileNames
    12.data.TestData
    13.data.users
    14.util.testStatus
    15.util.metadataCounts
    16.util.metadataComparison
    

Views

    1. bi.observationsSorted
    2. bi.uPhotometrySorted
    3. bi.vPhotometrySorted
    4. bi.bPhotometrySorted
    5. bi.hrDiagramAvg

Stored Procedures

    1. bi.observationsDelta
    2. data.insertTestData
    3. test.observationsCounts
    4. test.observationsComparison
    
    
Queries

    1. metadata.sql
    2. DB.sql
    3. FullList.sql
    

Test Data

    1. SYEqu-bPhotometry.csv
    2. SYEqu-uPhotometry.csv
    3. SYEqu-vPhotometry.csv
    4. TestData.csv
    5. ../Stars folder with FullList.sql and single .csv files
       


Rest API consists of following modules:

    1. jsonBuilder.py
    2. jsonParser.py
    3. api.py
    4. procRunner.py
    5. ../uploads area


Client consists of following:

    1. app.css
    2. app.js
    3. controller.js
    4. directives.js
    5. services.js
    6. admin.html
    7. hr-diagram.html
    9. main.html
    10.table-list.html
    11.index.html


  
More info you can find in Installation.txt.

# Thinking about the future

Frontend features

    1. User should be able to choose date from date picker
    2. UVB data should be pre-populated in Edit modal
    3. CMD diagram dots should be colorized
    4. Diagram should be described in a better way
    5. Logged in User details should be displayed
    6. Remove # tag from the address

    
Release 2

    1. Observations should be personalized - when user log in only his observations should be displayed.
    2. Notifications should be sent to logged in user when adding, updating, removing and processing data
    3. New page with Stars Catalogues search option 
    4. Mail server should be configured
    5. New HR diagrams should be present - this includes personal diagrams
    6. Custom filter option in observations should be available

Release 3

    1. Spectroscopic observations
    2. Observations of Sun
    3. Observations of planetoids and comets
    4. New diagrams - Periodograms, Light curves, Sun's activity

