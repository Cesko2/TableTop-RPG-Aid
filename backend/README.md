# BACKEND FOLDER
# SUMMARY:
The back end folder is expected to hold any and all files pertaining to the back end of the webapp.
The back end will handle all critical thinking and calculations done by the program, the frontend is designed
only to send user input to the back end, whereas the main back end file will route said information into the 
appropriate file. With this setup the intention is that if anyone part in the link fails, we can easily isolate
and solve the issue. That is, if the back end is divided into many small pieces, then when a part of it breaks,
only that one part is effected, which will cause the ensuing debugging and fixing to be much easier as we can
narrow our scope of where the problem might lie. 
Examples of files that will be in the back end folder include:
- database interface
- user authentication
- sheet manager
- entry manager

and likely several more to come.
