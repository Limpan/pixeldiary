Pixel Diary
===========

An example application that implements a small REST API. This is made as the
Pixel Diary, a diary where every day is one pixel.
To run, do a `docker-compose up`.

Accounts are registered via the web browser. To use the API first authenticate
with HTTP Basic Auth at `/api/token`, you will then receive a token that can
be used with further requests.
