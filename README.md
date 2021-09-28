# WebScrapersPython

**Project Description**

A set of webscrapers that output data pulled from various newspaoers and inserts them into a locally hosted database

Currently available:

- National Post
- Toronto Sun


## Notes 

if you're setting up a db to store the files that will be input, be mindful of the datatype/chartype. The body text column functions much better as a UTF8mb4 rather than utf8

**Sept 27**

The National Post has updated their pages to include multiple links for ELECTION 2021. These links will be removed from the array in future iterations, but for now these links are added to the columnlinks list. 
