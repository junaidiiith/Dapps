# Dapps

#Rental Agreement Manager for Blockchain

#### Technologies required


Dependencies

Install MySql, IPFSClient, Ganache
Remaining dependencies are present in the virtual environment.

Download Mysql and start the Mysql Server
Login to Mysql client
Create a user named "dapp" with password "dapp" --  

**create user 'dapp'@localhost' identified by 'dapp';
grant all privileges on dapp.* to 'dapp'@'localhost';**
Exit
Login using new user "dapp" and create database dapp
**create database dapp**

Download ganache software from [here](https://github.com/trufflesuite/ganache/releases/download/v2.3.0-beta.2/Ganache-2.3.0-beta.2-win-setup.exe)
Open ganache and start the server

Download the setup file for go-ipfs from [here](https://dist.ipfs.io/#go-ipfs)

Clone the repository and activate the virutal environment by using the command

**source venv/bin/activate**

Now to create the database tables and starting the application server run the following commands

**python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manager.py runserver**
