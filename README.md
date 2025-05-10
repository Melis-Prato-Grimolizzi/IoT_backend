# Backend IoT

# API Documentation not yet finished and I don't know when it will be. (Probably never)

The API exposes multiple HTTP routes.

In this documentation, if there are parameters in the route's path, they will be surrounded by angle brackets, because
that's how it's specified in Flask code, so we're doing it this way in the docs as well.

The API can be divided into two sections:

1. [Users](#users), which is the section that deals with user management.
2. [Slots](#slots), which is the section that deals with slot management.


## Users

The API uses HTTP Bearer authentication, more specifically requests are authorized using JWTs with no expiration date
provided by the API after a successful login to an existing user account.

Here is a table of contents with all the routes in this section:


1. [GET `/users`](#get-users)
2. [GET `/users/user/<user_id>`](#get-usersuseruser_id)
3. [GET `/users/verify`](#get-usersverify)
4. [POST `/users/signup`](#post-userssignup)
5. [POST `/users/login`](#post-userslogin)



### GET `/users/`

Returns a list of all users in the database.
The response will be something like this:

~~~json
[
  {
    "id": 1,
    "username": "user1",
  },
  {
    "id": 2,
    "username": "user2",
  }
]
~~~

### POST `/users/signup`

This route takes a POST request body in `application/x-www-form-urlencoded`
or `multipart/form-data` format containing two parameters:

* the `username` of the user to create;
* the `password` for the user.

and creates an user accordingly.

It returns:

* `OK` with status code 201 if the request body is valid and the user has been created;
* `missing form` with status code 400, if no valid form in the supported formats is sent along with the request;
* `missing fields [<list_of_missing_stuff>]` with status code 400 if there are missing fields in the form;
* `invalid fields [<list_of_invalid_stuff>]` with status code 400 if the username and/or password does not align with
  the [requirements](#username-and-password-requirements);
* `username conflict` with status code 409 if there is another user in the database with the same username.

### POST `/users/login`

This route takes a POST request body in `application/x-www-form-urlencoded`
or `multipart/form-data` format containing two parameters:

* the `username` of an existing user;
* the user's`password`.

and attempts to log into that user's account.

It returns:

* a newly generated JWT, as per the [RFC 7519](https://tools.ietf.org/html/rfc7519)
  standard for the user with status code 200 if the login attempt was successful
  (the user exists and the password is correct).
* `missing form` with status code 400, if no valid form in the supported formats is sent along with the request;
* `missing fields [<list_of_missing_stuff>]` with status code 400 if there are missing fields in the form;
* `invalid fields [<list_of_invalid_stuff>]` with status code 400 if the username and/or password does not align with
  the [requirements](#username-and-password-requirements);
* `bad credentials` with status code 401 if the login attempt failed either because the user doesn't exist or the password is wrong.