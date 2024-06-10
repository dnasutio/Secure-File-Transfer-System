# BOOTCON SFTS PROJECT
### SFTS: Secure File Transfer System

==This project was developed on Ubutunu on WSL. If you are using Windows you may need to adjust the steps.==

## SETUP
1. Clone this repository.

## SETUP BACKEND
1. cd backend
2. pip install -r requirements.txt
3. python3 manage.py runserver

Now you can make requests to the API endpoints on the server.

## SETUP FRONTEND
1. cd frontend
2. npm install
3. npm run dev

Now you can use the client UI to make requests to the server.

## USAGE
1. To register a user navigate to /register by manually editing the url.
2. Login as the user you just created.
3. Create a file by filling in the necessary form information followed by pressing Submit.
4. Delete the file by clicking the delete button on the file.
5. Download the file by clickin the download button on the file.
