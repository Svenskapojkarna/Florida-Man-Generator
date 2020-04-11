# Meetings notes

## Meeting 1.
* **DATE:** 13.06.2020
* **ASSISTANTS:** Marta Cortés Orduña

### Minutes

Probems in the wiki:
Our overview is not about "selling" our API, it should focus on those aspects.
Our main concepts and relations -part also needs some tuning...
API uses -part is "okay", also related work is "ok".

The main problem is, that there is not enough resources in our API.
We need to add more.

### Action points

Find some more resources to add to the API.
Fix the wiki.


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE:** 19.2.2020
* **ASSISTANTS:** Ivan Sanchez Milara

### Minutes
Discussion about the database and API.

Why did we choose a number instead of nickname as unique?
-We maybe should change nickname to be unique string, instead of number
Change the month tables to just one, with month column?
-Date is an unique attribute then in the table?
Discussion about the changes, and what are needed...

Ivan checked our populated database.
Users and stuff are not populated yet.
Only the monthly tables.

We could use an excel file for example to populate the database instead of
using row by row -python fill. CSV.
Create a dictionary and call the .csv etc...

We need to populate the users and added articles too, 4-5 users...

Define what happens when user is deleted?
Check what happens if unique field is tried to add with same value?
That was already implemented in the tests...

Checked running the pytest from our repo.

### Action points
Change users to be identified with unique string.

Month-tables to just one table instead, with datetime or similar unique identifier.

Populate users and added articles, 4-5 examples.
Also in headlines-links a few examples is enough.

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE:** 18.3.2020
* **ASSISTANTS:** Ivan Sanchez Milara

### Minutes
Zoom meeting because of the coronavirus episode.
We could have used URIs like /api/users?date=12.02.2019 instead of /api/articles/{date}/.
It's not wrong though.
Same with the addedarticles/{id}/ and addedarticles/{owner}/ -> addedarticles?owner="myself"...
 --> this date was ok, those others not
 
Link the 2 parts of the api-diagram, if it's done with a entry point draw it to the diagram.

Remove added article-by-date or some other unnecessary links.
Those arrows are not needed.

In the GET-patch-post diagram...
Added article by owner -> only GET?

Remember to add the entry point to the diagram.

We are missing the profiles from the Apiary.
One of the @controls can be profile.

We are using collection in article-item instead of articles-all.
Don't use both, use only one. Fix drawing or the Apiary.

Some confusion with {} and ? in the Apiary.

Be consistent with the names of the links.

How the API meets REST:
 give examples how

 Stateless: No exception with the adding.
 
 Connectedness: Example.

Client-server: Client can command.. Not "user" because it's not user...

Code-on-demand:;
 Actually telling the client how to create the new URI can be said to be Code-on-demand.
 
Dont round the hours used down...

### Action points
*List here the actions points discussed with assistants*

Think about changing URIs to the ?-format

Draw the Entry point to the diagram (box and 2 arrows).

Remove unnecessary links (arrows) in the diagram (article-collection...)

In the GET-patch-post diagram...
Added article by owner -> only GET?

Add the profiles to Apiary.

We are using collection in article-item instead of articles-all.
Don't use both, use only one. Fix drawing or the Apiary.

Article-by-date, get article had problems.


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE:** 9.4.2020
* **ASSISTANTS:** Mika Oja

### Minutes
*Summary of what was discussed during the meeting*
Articles, added articles:
a bit confusing...
Could have used one, with maybe unique owner+date...


URLs are hard-coded, could have used url_for...
url_for("api.user", user="uo-user-1")
That avoids circular imports

Added article, should POST new be inside user instead of collection or...?
Better way: use optional part of url?
Use 2 different url, one with owner one, without, so you can post with user coded in the url as a parameter. 
/api/{user}/added-articles/
def post(self, owner=None)

Building id to items is not necessary, because it's not a data that client can modify with PUT, but it then still has to send it back. Use self instead.

Builder-schema: for date we could use:
    "type":"string",
    "format":"date"
For url "format":"uri".
Is python schema module updated for that, thats not sure...

Installing package things (__init__.py, setup.py) should be implemented, so that 
pip install -e should install it into library.
Folders dont have __init__.py
That could help imports in python.

Comment "borrowed" lines in to the codes...

### Action points
*List here the actions points discussed with assistants*
Change url hard coding to url_for()
Build more tests, check coverage.

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

