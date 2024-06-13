# BOOTCON SFTS PROJECT

### SFTS: Secure File Transfer System

> This project was developed on Ubutunu on WSL. If you are using Windows you may need to adjust the steps. For example, on Windows you would use `python` instead of `python3`

## SETUP

1. Clone this repository.
2. Check that python is installed by running `python3 --version`
3. Check that node is installed by running `node --version`
4. Check that pip is installed by running `pip --version`
5. Check that npm is installed by running `npm --version`
6. To create the virtual environment run `python3 -m venv env`
7. To activate the virtual environment run `source env/bin/activate`

> What is the point of a virtual environment? A virtual environment is crucial for isolating project-specific dependencies from the system-wide Python packages.

## SETUP BACKEND

1. `cd bootcon/backend`
2. `pip install -r requirements.txt`
3. `python3 manage.py runserver`

Now you can make requests to the API endpoints on the server.

## SETUP FRONTEND

1. `cd bootcon/frontend`
2. `npm install`
3. `npm run dev`

Now you can use the client UI to make requests to the server.

## USAGE

1. To register a user navigate to /register by manually editing the url.
2. Login as the user you just created.
3. Create a file by filling in the necessary form information followed by pressing Submit.
4. Delete the file by clicking the delete button on the file.
5. Download the file by clicking the download button on the file.

## TESTING

- To run the tests I made in the api app, run `python3 manage.py test api`
- To reset the database run `python3 manage.py flush`

## INTUTION
### Program Flow

1. User passes credentials to frontend,
2. frontend passes credentials to backend,
3. backend grants token based on the credentials,
4. if credentials are valid the backend then passes an access token and refresh token to the frontend
5. Access token is used for requests, refresh token is used to refresh the access token
6. Frontend stores both tokens (localStorage)
7. If access token expires then frontend submits refresh token to a specific route on the backend and if the token is valid a new access token is passed to the frontend
   - REASON FOR REFRESH: Access tokens should expire fast because if the access token is leaked then the unauthorized party cannot maintain access on the account.


### JWT

Acts as the permissions or authentication every time we access a website.
Every time the frontend makes a request to the backend, the backend:
- needs to know who we are,
- what we have permissions to do

We include a token with every request to the backend. Then it can be decoded and understood to represent a certain set of permissions.\
For example, user dylan signs in, user is granted a token, token is then used for all future requests to tell backend who is interacting with it and what permissions they have.


### Interceptor with axios in api.js


Interceptor: Intercepts requests frontend sends and automatically adds the correct headers so that we do not need to write them manually.\
With axios interceptor anytime the frontend sends a request, it checks if you have an access token and if you do it will automatically add it to the request.


### Protected Route Component

Wrapper for protected route: need auth token before being able to access the route.
Theoretically could be bypassed but not on the frontend.
This prevents unauthorized users from accessing the route until they have logged in.

### AES Encryption and RSA Encryption
1. AES Encryption
- When the file arrives on the server encrypt it using a AES key.
- Store the key in the database.
2. RSA Encryption
- Encrypt the AES key using the RSA public key on the server.
3. Decryption
- When the client sends a request to download the file decrypt the AES key with the RSA private key.
- Use the AES key to decrypt the file
- Send the file in the response to the client.

SECURE DATA AT REST


