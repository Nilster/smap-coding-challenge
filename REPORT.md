==Django Models==  
Before uploading the data files, first create the models for 'User' and 'Usage' inside the consumption app. This will create all the necessary tables beforehand and then we can upload the data into those tables.  

Create the models by running the following:  
-Make migration  
    python manage.py makemigrations consumption  
-View sql generated  
    python manage.py sqlmigrate consumption 0001  
-Actually apply the migration  
    python manage.py migrate  

==Data Upload==  
Then upload the data using:  
    python manage.py import  
This should upload the data into previously created tables. This script checks for the duplicate users but it doesn't check for the same usage file uploaded twice. It uses sqlite3 library to upload the data to sqlite db.  

==Views==  
In addition to 'summary' and 'detail', two additional views are created which return requested data as json.  
1)overall_summary_half_hour: This returns json of total and average consumption of all users grouped by half hour time interval.  
2)user_summary_half_hour: This returns json of all the consumption values for a given user.  
summary and detail views serve the webpages using the predefined templates. They provide context information for all_users which gets rendered as tables using templates.  

==Front-end==  
The charts are displated on the webpage using javascript library D3. It recieves data from django using the views that serve json.(eg.http://127.0.0.1:8000/api/overall_summary_half_hour)
The charts drawn are interactive and connected to each other. Chart1 is the focus view which can be zoomed and dragged. Chart2 is the overview focus.
The 'detail' page refreshes the chart when clicked on the hyperlink for a given user. It does not load in the whole page from the server. It only reads user specific usage as json from the views created earlier and then redraws the svg on the same page.  

==Issues==  
The overview graph on both pages does not contain data preview (blue line in Graph2). It needs investigating.  
The timestamp is taking into account timezone and BST related changes. Not sure how the timestamp in files is formatted. The data upload script will need to changed accordingly. Also, either django or D3 is compensating for day light savings. It needs investigating.
eg For user 3069, the peak consumption (5366) is at 2016-08-23 17:00:00 but D3 shows it at 2016-08-23 18:00:00  

==Testing==  
The test cases are not defined for all views, only a handful to you give you gist.  

==Improvements==  
The javascript code summary and detail template is very similar. It needs refactoring.  