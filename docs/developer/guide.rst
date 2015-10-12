Development guidelines
======================

1. Use `git flow <http://danielkummer.github.io/git-flow-cheatsheet/>`_
2. Follow `PEP8 <http://python.org/dev/peps/pep-0008/>`_
3. Cover code with tests.
4. Document important functionality.


Setup work environment
----------------------

- Clone project repository:

.. code-block:: bash

    git clone https://github.com/crypotex/taas.git

- Go to the project root folder:

.. code-block:: bash

    cd taas

- Create separated python environment and activate it (recommended):

.. code-block:: bash

    virtualenv -p /usr/bin/python3 venv
    source venv/bin/activate

- Install project requirements:

.. code-block:: bash

    pip setup.py develop

- Migrate database:

.. code-block:: bash

    python manage.py migrate

- Run server:

.. code-block:: bash

    python manage.py runserver


Flow for tasks
--------------

- Create a new branch from develop.

.. code-block:: bash

    git checkout develop
    git pull origin develop
    git checkout -b feature/task-id (task-id is number of the issue in github. For example 7.)

- Write code.
- Create tests.
- Verify that tests are passing.
- If some important functionality is implemented, add documentation for it with screenshots if necessary.
- After work on the task is completed:

.. code-block:: bash

    git push origin feature/task-id

- Go to the github and make **Pull request** to the develop branch.
- Assign Pull request to the team member.
- Add **Done** label to the Github issue.

Commit rules
------------
- Commit message should be 50 characters or less.
- Do not make large commits.
- At the end of the commit specify task number using `Issue #task-id`
- Example of proper commit message:

.. code-block:: bash

    Create initial project structure
    
    Issue #7

