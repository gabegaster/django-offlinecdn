.. warning::

    This package is a work in progress and is not yet available on pypi. This
    documentation should be considered more of a design document for what
    offlinecdn will do someday rather than a specification of what it can do
    today.

offlinecdn
===================================================

A nice way to allow for online-offline development, but also use cdn's
for package dependencies.

problem
-------

Using `CDN's <http://en.wikipedia.org/wiki/Content_delivery_network>`_
is a best practice -- it distributes load across servers. Using it in
development, though, requires you have internet access while you're
developing. Modern web browsers cache CDN's, but at this time,
`browsers need to be online for this to work
<http://stackoverflow.com/questions/29704811/why-isnt-the-browser-loading-cdn-file-from-cache>`_. That
leaves one option: download all dependencies and serve files locally
AND THEN remember to change everything back before you deply.


solution
--------

Enter ``offlinecdn``, a custom template tag in django to cache sourced
javascript and css locally.

To keep code `DRY
<http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`_, and avoid
manually downloading dependencies and serving them locally,
``offlinecdn`` is a `custom template tag
<https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/>`_
that, when ``DEBUG=True``, caches all javascript and css dependencies
and templates the link to serve them locally. Once the page has been
loaded once, you will no longer download files from cdn and can
develop your site offline.


example
-------

With ``offlinecdn``, sourcing javascript and css from cdn's is easy!
You do exactly what you would normally do -- just wrap any ``link`` s or
``source`` s in the ``offlinecdn`` tag.

 ::

   {% offlinecdn %}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/js/bootstrap.min.js"></script>
   {% endofflinecdn %}

With ``DEBUG=True``, or with ``OFFLINECDN_MODE=True``, any sourced
files get cached locally and the links set to:

::

    <link href="/static/cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/css/bootstrap.min.css">
    <script src="/static/cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/js/bootstrap.min.js"></script>
 
   
quick start
-----------

Getting started with ``offlinecdn`` is as simple as:

- ``pip install django-offlinecdn``, 
- include ``offlinecdn`` as an ``INSTALLED_APP`` in ``settings.py``

::

    INSTALLED_APPS = (
        'django.contrib.staticfiles',
        'offlinecdn',
	...
	)


- incorporating the ``offlinecdn`` tag into your templates like this:

.. code:: html

   {% offlinecdn %}
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.4/js/bootstrap.min.js"></script>
    ...
   {% endofflinecdn %}


Contents:

.. toctree::
   :maxdepth: 2

   changelog


