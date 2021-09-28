# WebScrapersPython

**Project Description**

A set of webscrapers that output data pulled from various newspaoers and inserts them into a locally hosted database

Currently available:

- National Post
- Toronto Sun


## Notes 

if you're setting up a db to store the files that will be input, be mindful of the datatype/chartype. The body text column functions much better as a UTF8mb4 rather than utf8

**Sept 27**

<<<<<<< HEAD
The National Post has updated their pages to include multiple links for ELECTION 2021. These links will be removed from the array in future iterations, but for now these links are added to the columnlinks list.

**To Do**

The next logical step is to have these scripts hosted on a server to run every 24 hours. There are always a few column links that cause problems and are currently being fixed by user prompts. This can be done later by setting the column values causing issues to "please review". Human review of data scraped from the web should be done daily to ensure the integrity of the database
=======
The National Post has updated their pages to include multiple links for ELECTION 2021. These links will be removed from the array in future iterations, but for now these links are added to the columnlinks list. 

** To Do **

The next logical step is to have these scripts hosted on a server to run every 24 hours. 
There are always a few column links that cause problems and are currently being fixed by user prompts. This can be done later by setting the column values causing issues to "please review". Human review of data scraped from the web should be done daily to ensure the integrity of the database
>>>>>>> 176bcd34ae2d987976f997943a007feb31e3e093
