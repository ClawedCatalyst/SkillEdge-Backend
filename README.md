# SkillEdge-Backend


### Backend Hosted link ----->

https://skilledge.herokuapp.com/


## Video



https://user-images.githubusercontent.com/62144720/218805519-4f2cf368-f32a-4da6-a20a-9e291da3159e.mp4


## ScreenShots


<p align="center">
      <img src="https://i.ibb.co/KG9b8rQ/photo-2023-02-14-21-47-24.jpg" width="150" />
  <img src="https://i.ibb.co/6P76Fjn/photo-2023-02-14-21-47-25.jpg" width="150" />
  <img src="https://i.ibb.co/sgypy0q/photo-2023-02-14-21-47-26.jpg" width="150" />
  <img src="https://i.ibb.co/09LsncF/photo-2023-02-14-21-47-27.jpg" width="150" />
</p>

<p align="center">
  <img src="https://i.ibb.co/PFD7SxC/photo-2023-02-14-21-47-16.jpg" width="150" />
  <img src="https://i.ibb.co/Bq0spSY/photo-2023-02-14-21-47-18.jpg" width="150" />
  <img src="https://i.ibb.co/Z6BXkSR/photo-2023-02-14-21-47-20.jpg" width="150" />
  <img src="https://i.ibb.co/rpQvdwp/photo-2023-02-14-21-47-21.jpg" width="150" />
  <img src="https://i.ibb.co/mBSGmgR/photo-2023-02-14-21-47-22.jpg" width="150" />
</p>
<p align="center">

  <img src="https://i.ibb.co/wzfMx1h/photo-2023-02-14-21-47-09.jpg" width="150" />
  <img src="https://i.ibb.co/v1BMM2x/photo-2023-02-14-21-47-12.jpg" width="150" />
  <img src="https://i.ibb.co/RT67Jdm/photo-2023-02-14-21-47-13.jpg" width="150" />
  <img src="https://i.ibb.co/N263Xcp/photo-2023-02-14-21-47-14.jpg" width="150" />
  
</p>

## RUNNING THE SERVER

1. Clone the repository:

```CMD
git clone https://github.com/suhaillahmad/SkillEdge-Backend.git
```

To run the server, you need to have Python installed on your machine. If you don't have it installed, you can follow the instructions [here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) to install it.

2. Install, Create and activate a virtual environment:

```CMD
pip install virtualenv
virtualenv venv
```

Activate the virtual environment

```CMD
source venv/bin/activate
```

3. Install the dependencies:

```CMD
pip install -r requirements.txt
```

4. Setup .env file in Bulk-Mailer-Backend/bulkmailer

```
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

DATABASE_NAME=''
DATABASE_USER=''
DATABASE_PASSWORD=''

CLOUD_NAME: ''
API_KEY: ''
API_SECRET: ''

PUBLIC_KEY = 
SECRET_KEY = 

```

5. Create a PostgreSQL database and connect it by entering credentials in .env file, once connected run the migrate command

```CMD
python manage.py migrate
```

6. Run the backend server on localhost:

```CMD
python manage.py runserver
```

You can access the endpoints from your web browser following this url

```url
http://127.0.0.1:8000
```

7. You can create a superuser executing the following commands

```CMD
python manage.py createsuperuer
```

A prompt will appear asking for email followed by password.
To access the django admin panel follow this link and login through superuser credentials

```url
http://127.0.0.1:8000/admin/
```

8. Start the Celery worker (On a separate terminal with activated virtual environment):

```CMD
celery -A bulkmailer.celery worker --pool=solo -l info
```

9. Run celerybeat (On a separate terminal with activated virtual environment):

```CMD
celery -A bulkmailer beat -l info
```


### Contributors ----->

https://github.com/suhaillahmad (Suhail Ahmad)

https://github.com/Tech-Shreyansh (Shreyansh Agrawal)
