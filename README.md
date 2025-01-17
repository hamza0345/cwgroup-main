## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment

2. Download this repo as a zip and add the files to your own private repo.

3. Install Pyhton dependencies (main folder):

    ```console
    $ pip install -r requirements.txt
    ```

4. Create a development database:

    ```console
    $ python manage.py migrate
    ```

5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    $ npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    $ python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    $ npm run dev
    ```

8. Make sure your localhost link is http://localhost:5173

9. Open your browser and go to http://localhost:8000/login

## OpenShift deployment

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' (on Mac and Linux) the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

    If using Windows run

    ```console
    $ npm run build-windows
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).

## Contributions

### Muhammed Fahim Miah
- **Expected Tasks**:  
  - Selenium Testing  
  - `models.py`  
  - Templates  
- **Completed**: All  

---

### Hamza Ahmed
- **Expected Tasks**:  
  - `views.api`  
  - `serializers.py`  
  - Views for REST API  
- **Completed**: All  

---

### Ibrahim Kharim
- **Expected Tasks**:  
  - User Stores  
  - Deployment
  - OpenShift Deployments  
- **Completed**: All  

---

### Lamain Islam
- **Expected Tasks**:  
  - `urls.py` (Routing)  
  - Vue Pages  
  - Global CSS  
- **Completed**: All  

---

## Deployment Link
[https://group47-web-apps-ec22656.apps.a.comp-teach.qmul.ac.uk/]

---

## Admin Credentials
- **Username**:  
  `Admin`  
- **Password**:  
  `wqa12344`

---

## Test User's Credential

### Test User1 Credentials
- **Username**:  
  `User1`  
- **Password**:  
  `re112345`

### Test User2 Credentials
- **Username**:  
  `User2`  
- **Password**:  
  `ht122345`

### Test User3 Credentials
- **Username**:  
  `User3`  
- **Password**:  
  `xp112243`

### Test User4 Credentials
- **Username**:  
  `User4`  
- **Password**:  
  `fda12334`

### Test User5 Credentials
- **Username**:  
  `User5`  
- **Password**:  
  `jfq12234`
