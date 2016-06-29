.. _api:

Contributing
------------

OpenGB is an Open Source project and all contributions are gratefully appreciated.

By donating your time and skills you are helping to build a platform used by 3D printing enthusiasts around the globe!

Repositories
^^^^^^^^^^^^

OpenGB
======

* OpenGB is written in Python and hosted in the Github repository `re-3D/opengb`_. 

OpenGB Web
==========

The OpenGB web frontend is written in `Vue.js`_, a Javascript framework. It is hosted separately in the Github repository `re-3D/opengb-web`.

Changes to the frontend trigger a build which outputs to `re-3D/opengb-web/dist`_. This directory is periodically pulled into the OpenGB repo using `git read-tree` as described in the `OpenGB README`_.

Bug Reports
^^^^^^^^^^^

Report bugs as `OpenGB Github issues`_ using the label `bug`.

Be sure to check existing issues for duplicates.

Feature Requests
^^^^^^^^^^^^^^^^

Request features as `OpenGB Github issues`_ using the label `enhancement`.

Be sure to check existing issues for duplicates.

Submitting Code
^^^^^^^^^^^^^^^

#. Create an `OpenGB Github issue`_ for the bug/feature in question (if one does not already exist).
#. Fork the OpenGB repository.
#. Create a topic branch off `develop`.
#. Make changes, being aware of:
   * Logical commits
   * Whitespace
   * PEP8
* Update the `CHANGELOG`_ following the instructions therein.
* Push changes to your topic branch.
* Submit a PR.
* Wait for feedback from a project maintainer.

.. _`re-3D/opengb`: https://github.com/re-3D/opengb
.. _`re-3D/opengb-web`: https://github.com/re-3D/opengb-web
.. _`OpenGB Repository`: https://github.com/re-3D/opengb-web
.. _`re-3D/opengb-web/dist`: https://github.com/re-3D/opengb-web/tree/master/dist
.. _`Vue.js`: https://vuejs.org
.. _`OpenGB README`: https://github.com/re-3D/opengb/blob/master/README.md
.. _`CHANGELOG`: https://github.com/re-3D/opengb/blob/master/CHANGELOG.md
.. _`OpenGB Github issue`: https://github.com/re-3D/opengb/issues
.. _`OpenGB Github issues`: https://github.com/re-3D/opengb/issues
.. _`PEP8`: http://www.python.org/dev/peps/pep-0008/
