
django-bridgekeeper
===================

    He who answers the five questions--three questions--may cross in safety.

    https://youtu.be/cV0tCphFMr8


A private beta app for Django 1.10+ and Python 3.5+.

Any "traveler" who "answers the questions" may pass ``BridgekeeperMiddleware``
and "cross in safety" to the beta views.

Questions are pluggable via ``BRIDGEKEEPER_QUESTIONS`` setting.

Unlike other private beta apps, immediate user sign up is not required. With
default ``BRIDGEKEEPER_QUESTIONS`` an invited ``AnonymousUser`` may browse the
beta views before--or without ever--signing up as long as their ``Invite`` is
valid.


Installation
============

During soft release of django-bridgekeeper, install directly from git repo:

.. code-block:: bash

    $ pip install git+https://github.com/brettstil/django-bridgekeeper.git#egg=django-bridgekeeper


Usage
=====

Add to ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS = [
        # ...
        'bridgekeeper.apps.BridgekeeperConfig',
    ]

Add ``BridgekeeperMiddleware`` to ``MIDDLEWARE`` settings after Django's authentication middleware:

.. code:: python

    MIDDDLEWARE = [
        # ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'bridgekeeper.middleware.BridgekeeperMiddleware',
    ]

For default ``valid_invite`` question, add bridgekeeper urls to root urls:

.. code:: python

    urlpatterns = [
        # ...
        url(r'^bridgekeeper/', include(
            'bridgekeeper.urls', namespace='bridgekeeper')),
    ]

Configure settings, especially redirect urls and allowed modules and views.


Questions
=========

Just like the Monty Python sketch, ``BridgekeeperMiddleware`` asks a list of
questions to determine whether the traveler may pass.

Questions are defined in ``BRIDGEKEEPER_QUESTIONS`` setting.

Each question has three possible results:

* ``return True`` for explicit yes, traveler may pass.
  ``BridgekeeperMiddleware.process_view`` returns immedate ``None`` and skips
  remaining questions in ``BRIDGEKEEPER_QUESTIONS``.

  For example, in default question ``enable`` explicit yes is returned if
  ``BRIDGEKEEPER_ENABLE`` setting is ``False``.

* ``return False`` for explicit no, traveler may not pass and traveler cast
  into the gorge. ``BridgekeeperMiddleware.process_view`` returns immediate
  ``HttpResponseRedirect`` to ``BRIDGEKEEPER_URL_GORGE`` and skips remaining
  questions in ``BRIDGEKEEPER_QUESTIONS``.

  For example, in default question ``valid_invite`` explicit no is returned if
  an existing invite code is expired. Remember, order of
  ``BRIDGEKEEPER_QUESTIONS`` is important!

* ``return None``, or just ``return``, for no opinion.
  ``BridgekeeperMiddleware`` continues to the next question, if any, in
  ``BRIDGEKEEPER_QUESTIONS``.

  If all questions return ``None``, then
  ``BridgekeeperMiddleware.process_view`` also simply returns ``None`` and
  traveler may pass.


Settings
========

Available settings are:

``BRIDGEKEEPER_INVITE_EXPIRED_SECONDS``
    Default: ``None``

    With default ``None`` setting, created invite does not expire at
    predetermined ``expired`` datetime.

    With integer setting, created invite ``expired`` set to ``timezone.now()``
    + the setting number of seconds.

    Created invite with manually set ``expired`` ignores the setting.

``BRIDGEKEEPER_URL_GORGE``
    Default: ``'/'``

    Redirect url after a middleware question explicitly casts traveler into
    gorge.

``BRIDGEKEEPER_URL_INVITED_OK``
    Default: ``'/'``

    Redirect url after traveler successfully visits ``'invited'`` url and has
    invite code cookie set.

``BRIDGEKEEPER_URL_INVITED_INVALID``
    Default: ``'/'``

    Redirect url after traveler visits ``'invited'`` url with invalid or
    expired invite code.

``BRIDGEKEEPER_COOKIE_NAME``
    Default: ``'bridgekeeper_invite_code'``

``BRIDGEKEEPER_QUESTIONS``
    Default: ``['bridgekeeper.middleware.authenticated',
    'bridgekeeper.middleware.enable',
    'bridgekeeper.middleware.allowed_module',
    'bridgekeeper.middleware.allowed_view',
    'bridgekeeper.middleware.valid_invite']``

    Order of questions is important!

``BRIDGEKEEPER_ENABLE``
    Default: ``True``

    Setting for ``'bridgekeeper.middleware.enable'`` question.

    Completely disable bridgekeeper with a single setting.

``BRIDGEKEEPER_ALLOWED_MODULES``
    Default: ``[]``

    Setting for ``'bridgekeeper.middleware.allowed_module'`` question.

    Always allow views from these modules, for example ``'welcome.views'``.

    These modules are always allowed: ``['django.contrib.admin.sites',
    'django.contrib.auth.views', 'django.contrib.staticfiles.views',
    'django.views.static']``.

``BRIDGEKEEPER_ALLOWED_VIEWS``
    Default: ``[]``

    Setting for ``'bridgekeeper.middleware.allowed_view'`` question.

    Always allow these views, for example ``'landing.views.hello'``.


Similar Projects
================

Inspired by unmaintained https://github.com/pragmaticbadger/django-privatebeta
and https://github.com/joshuakarjala/django-hunger

https://djangopackages.org/grids/g/private-beta/

https://github.com/mgrouchy/django-stronghold

