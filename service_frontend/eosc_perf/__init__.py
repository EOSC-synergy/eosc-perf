"""The root package.

Submodules of this package are related to the core app functionality, e.g. creating the Flask app object, launching the
application and loading the configuration.

The application is structured as Model-View-Controller, the packages are arranged as such. As summary:
 - the model wraps around the database and provides abstraction classes for the different datatypes,
 - the view exposes the HTTP endpoints used by end-users in their browsers, so it takes in requests, does a completeness
   check and then forwards queries or submissions to the model or the controller,
 - the controller handles specific types of requests requiring authentication, like data submission, and validates
   incoming data if possible.

"""
