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
4. In `seev/settings.py`, modify database and Django secret key settings with appropriate environmental variables (or hard-code them if only want to run a local test, and ensure instant client is available for Oracle connection).
5. Obtain a working API key from Google Cloud Platform and enable Maps & Places API. Then, set the environmental variable "SEEV_GOOG_KEY" to the API key (*optional, but Google Map will not work if not set up*).
6. Install Sass (may require NPM), and compile all Sass files into minified CSS files (create a directory named "css" in all four static folders where you find a scss directory, and the css file will have the same name with `.min.css` extension).
7. Verify your database connection and run `python manage.py migrate` to create the schema for the application (migration files are included in the repository).

### Run Local Server
### Production Deployment Notes