=======
photodl
=======

Tools for downloading photos from social network site

1.	instagram - currently on progress
2.	facebook - future plan


notes :

1.	http://jelled.com/instagram/lookup-user-id
2.	https://github.com/Instagram/python-instagram
3.	http://instagram.com/developer/endpoints/relationships/


Authentication
-----
photodl app uses Instagram OAuth2 protocol for authentication.


Guide to run the App
-----

  * Create a new virtualenv, and activate it
  * Run `pip install -Ur requirements.txt`
  * Create `photodl/settings.yml` or environment variable based on default config on `photodl/defaults.yml`
      * Make sure to update instagram setting with you personal `client_id` and `client_secret`
        get it from `http://instagram.com/developer/`
  * If you use env variable use all UPPERCASE separated by UNDERLINE(_), ie `PHOTODL_INSTAGRAM_CLIENT_ID`
  * Do `python run_app.py` to run the app and which get hosted on local server on port 5001
  * Try visiting `http://localhost:5001` in your browser
