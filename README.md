# SIRS-Project

## Environment
* Ubuntu 20.04 LTS
* Python 3.8
* Pipenv version 2022.12.19
* PostgreSQL 15.1 (Ubuntu 15.1-1.pgdg20.04+1)

## Running
Change the password for the postgres user with `postgres`
And create the databases and tables
* `sudo -u postgres psql`
* `\password postgres` use `postgres` as a password
* `CREATE DATABASE sirs`
* `\c sirs`
* Copy and paste the tables in the `schema.sql`
* Copy and paste the rows in the `populate.sql`

Setup the libraries (these can be found in the Pipfile)
* `pipenv sync` to install the libraries
* `pipenv shell` to use the libraries

Then run one of these commands
* `bash start_regular_client.sh` to start the client for the Secure Communications part
* `bash start_flask.sh` to start the application server for the Secure Communications part
* `bash start_auth_client.sh` to start the client for the Secure Protocol
* `bash start_auth_server.sh` to start the server for the Secure Protocol

## Command line

### Secure Communications
The client app sends a warning for each message complaining about missing `subjectAltName`  
in the certificate but still works properly.

You can also check the test results for a given client with the signature.

### Secure Protocol
The server prints the session key and nounce being used, and the json message with the data and
the signature in base64

When the server for the Secure Protocol asks
`continue to receive requests? [y/n]`
If you enter `n` the server will get all of the rows in the tests_results table and check if all the
signatures still match.
