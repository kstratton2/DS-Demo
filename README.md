The purpose of this repository is to create and share the Drive Spotter coding evaluation. The scope of the project contains a few main points.

1. Creating a web application with basic authentication using Python 2.7
2. Store user data in a Postgresql database with a few required fields
3. Passwords for each user should NEVER be stored in plaintext
4. Authenticated users should be able to view and create users

The application has 2 routes that are currently in use, '/' and '/register'.

The '/register' route's main functionality is to gather a users information, clean the user input, verify the cleaned input meets the requirements, and register the user in the database.

The '/' route serves 2 functions. This route is both the login route, as well as the view users route. If a user attempts to access this route, they will first be met with the login page. Upon providing matching credentials, their data will be stored in the session, and the page will be reloaded, alowing them to view a list of all users.

Problems faced:
5/22/17: Project assigned	
	Change OS on laptop (Win 10 -> Ubuntu 16.04) (for better dev env, as well as personal choice):
		-Windows computer with Intel processor apparently uses AMD version of Ubuntu - Solved by trying different versions.
		-Wrote new OS over ENTIRE drive -> no OEM partition -> 'no' wifi driver - Solved by reasearching the problem, solution was disabling an additional wifi driver that was running first, but failing for specific computer models
5/23/17: Project Started
	VERY basic knowledge of Python:
		-Started by researching and working through tutorials that were based on the same technologies (flask and python 2.7) - Used tutorials to establish routing and basic views
5/24/17: Database Dev Env issues
	Installing Postgresql to host database:
		-Reading documentation on installing database from source -> cascading dependency errors - Solved by looking up error codes and finding solutions.
5/25/17: Database Creation/Connection
	Creating Database:
		-Syntax errors with PSQL specifics (ex. SERIAL vs AUTO_INCREMENT) - Solved by researching differences
		-Created DB in wrong location ('psql') - researched problem to find that app uses the localhost version of the DB not the local version('psql -h localhost'), and created DB there.
	Connecting Application to Database:
		-Getting application to talk to database to query data or insert data - Issues with how the URL for the database was written, fixed through tutorials as well as researching resulting errors.
5/26/17: Registration / Login - Safe Passwords
	Hashing and salting passwords:
		-Hashing passwords prior to storage - Solved by researching easy hashing methods for Python
		-Retrieving hashed passwords / salts to login users -> bad data errors, concatenating str and None - Solved by debugging code to find the source of the problem (limited test data had salt = None somehow, re-registered test users to give them non-null salts)
5/27/17: Testing
5/30/17: Git deployment / Final Documentation
	Git deployment:
		-First tried to create a local repo, then push it to a remote github repo - FAILED due to the local repo not being properly set up before attempting to push to remote, subsequent attempts to correct repo failed
		-Second created a remote repo, cloned it locally, and filled it with code to push back to remote.
	Documentation:
		-Reviewing requirements / desired outcomes of the project and writing documentation specifically to meet those needs