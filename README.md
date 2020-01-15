# SE Eon Venture
[![Language](https://img.shields.io/badge/Python-v3.7.3-2b5b84)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Django-v3.01-20AA76)](https://www.djangoproject.com/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Preview](https://img.shields.io/badge/Preview-Available-brightgreen)](http://35.226.171.164:8081/)

SE Eon Venture is a conceptual prototype of an ordering platform for enterprise level products and services. It is built to be used by both service providers and their potential customers. Due to business complexity and the fact that the application is general-purpose, some training is required in order for any user to operate on the site effectively.

## Build Project
### Prerequisites
* [Python 3](https://www.python.org/)
* [Virtualenv](https://virtualenv.pypa.io/en/latest/)
* [Oracle Database](https://www.oracle.com/database/12c-database/)
* [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client.html)
* [Sass](https://sass-lang.com/)
* [Nginx](https://www.nginx.com/) (Recommended for production)
* [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) (Recommended for nginx deployment)

*Django supports other database implementations such as MySQL and PostgreSQL. A few settings and environmental variables need to be modified if you choose to not use Oracle.*

### Setup
1. Clone or download the repository and change into the project's root directory (where `manage.py` is located).
2. Make sure Python 3 is installed and create/activate a virtual environment for this project.
3. Run `pip install -r requirements.txt` to install all required dependencies.
4. In `seev/settings.py`, modify database and Django secret key settings with appropriate environmental variables (or hard-code them if you only want to run a local test, and ensure instant client is available for Oracle connection).
5. Obtain a working API key from Google Cloud Platform and enable Maps & Places API. Then, set the environmental variable "SEEV_GOOG_KEY" to the API key (*optional, but Google Maps will not work if not set up*).
6. Install Sass (may require NPM), and compile all Sass files into minified CSS files (create a directory named "css" in all four static folders where you find a scss directory, and the css file will have the same name with `.min.css` extension).
7. Verify your database connection and run `python manage.py migrate` to create the schema for the application (migration files are included in the repository).
8. To enable administrator access, open `seev/apps/utils/generators.py` file and replace "credentials" list within the function `getAdminCredentials` with the SHA-224 hashes of a username and password.

### Run Local Server
1. After completing the setup steps, run `python manage.py runserver` from the project's root directory, and the development server will be running on port 8000 by default.
2. Open any browser and navigate to `http://127.0.0.1:8000/`, application's home page should be displayed.

### Production Deployment Notes
1. Please carefully review the [documentation](https://docs.djangoproject.com/en/3.0/howto/deployment/) for Django deployment before you move the application to a production server (if you wish to enable https, follow the guidelines from the Django website).
2. Connect to the deployment server and repeat the steps in the setup.
3. Run `git checkout release` and then `python manage.py collectstatic` after which all static files will be grouped in the `static/` folder in the project's root directory.
4. If you decide to use Nginx, make sure it is installed and then run `sudo service nginx start` to start the server (feel free to use `seev_nginx.conf` as a base template for Nginx configuration).
5. Review and edit both Nginx configuration file as well as `uwsgi.yaml` so that all location variables are pointing to viable paths on your server.
6. From the project's root directory, run `uwsgi -y uwsgi.yaml`, and the Nginx server should be able to communicate with the Django application.
7. Open a browser and navigate to your server's public domain or IP address with the correct port, verify the application is running without issues.

*At the time of this writing, the latest version of Django available on a Debian distribution is 2.9.9, and therefore the dependency file on the "release" branch does not specify version 3.0.1.*

## Usage
Due to multiple levels of complexity, the user manual will be on a separate document.

## Credits
* [Marek Polakovic](https://thenounproject.com/marekpolakovic/)
* [Flaticon](https://www.flaticon.com/home)