.. _django-first-steps:

=========================
使用 Django 的第一步
=========================

First steps with Django

将 Celery 与 Django 结合使用
============================

Using Celery with Django

.. tab:: 中文

    .. note::

        旧版本的 Celery 需要单独的库才能与 Django 一起使用，
        但从 3.1 版本开始不再需要。Celery 现在原生支持 Django，
        因此本教程仅介绍 Celery 与 Django 集成的基础方法。
        你将使用与非 Django 用户相同的 API，因此推荐你首先阅读 :ref:`first-steps` 教程，
        然后再回来阅读本教程。当你有了一个可运行的示例之后，
        可以继续阅读 :ref:`next-steps` 指南。

    .. note::

        Celery 5.5.x 支持 Django 2.2 LTS 或更新版本。
        如果你的 Django 版本低于 2.2，请使用 Celery 5.2.x；
        如果低于 1.11，请使用 Celery 4.4.x。

    要在你的 Django 项目中使用 Celery，首先需要定义
    一个 Celery 库的实例（称为“app”）。

    如果你有一个现代的 Django 项目结构，例如::

        - proj/
        - manage.py
        - proj/
            - __init__.py
            - settings.py
            - urls.py

    推荐的做法是在 `proj/proj/celery.py` 中创建一个新模块，
    用于定义 Celery 实例：

    :file:`proj/proj/celery.py`

    .. literalinclude:: ../../examples/django/proj/celery.py

    然后你需要在 :file:`proj/proj/__init__.py` 模块中导入此 app。
    这确保了 Django 启动时 app 被加载，
    以便稍后提到的 ``@shared_task`` 装饰器能够使用它：

    :file:`proj/proj/__init__.py`:

    .. literalinclude:: ../../examples/django/proj/__init__.py

    注意，这种项目结构适用于较大的项目，
    对于简单项目，你也可以使用一个包含 app 和任务定义的单一模块，
    如 :ref:`tut-celery` 教程所示。

    我们来分解第一个模块中的内容，
    首先我们为 :program:`celery` 命令行程序设置默认的
    :envvar:`DJANGO_SETTINGS_MODULE` 环境变量：

    .. code-block:: python

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

    这行并不是必须的，但它能省去每次都要给 ``celery`` 程序传递
    settings 模块的麻烦。它必须放在创建 app 实例之前，就像我们接下来所做的那样：

    .. code-block:: python

        app = Celery('proj')

    这是我们定义的 Celery 实例。你可以定义多个实例，
    但在使用 Django 时通常没必要这样做。

    我们还将 Django 的 settings 模块添加为 Celery 的配置来源。
    这意味着你不需要使用多个配置文件，
    可以直接从 Django 的设置中配置 Celery；
    当然你也可以将其分离配置。

    .. code-block:: python

        app.config_from_object('django.conf:settings', namespace='CELERY')

    这个大写的命名空间意味着所有的
    :ref:`Celery 配置选项 <configuration>`
    必须以大写字母书写，并以 ``CELERY_`` 开头，
    例如 :setting:`task_always_eager` 设置对应为 ``CELERY_TASK_ALWAYS_EAGER``，
    :setting:`broker_url` 设置对应为 ``CELERY_BROKER_URL``。
    这也适用于 worker 的设置，例如 :setting:`worker_concurrency` 设置对应为 ``CELERY_WORKER_CONCURRENCY``。

    例如，一个 Django 项目的配置文件可能包含如下内容：

    .. code-block:: python
        :caption: settings.py

        ...

        # Celery 配置选项
        CELERY_TIMEZONE = "Australia/Tasmania"
        CELERY_TASK_TRACK_STARTED = True
        CELERY_TASK_TIME_LIMIT = 30 * 60

    你也可以直接传递设置对象，但使用字符串更好，
    因为 worker 不必序列化该对象。
    命名空间 ``CELERY_`` 是可选的，但推荐使用（以防与其他 Django 设置冲突）。

    接下来，一个可重用 app 的通用做法是将所有任务
    定义在一个独立的 ``tasks.py`` 模块中，而 Celery 提供了
    自动发现这些模块的功能：

    .. code-block:: python

        app.autodiscover_tasks()

    有了上述这一行，Celery 将自动从所有已安装的 app 中发现任务，
    只要这些模块遵循 ``tasks.py`` 的命名规范::

        - app1/
            - tasks.py
            - models.py
        - app2/
            - tasks.py
            - models.py

    这样你就不需要手动将每个模块添加到 :setting:`CELERY_IMPORTS <imports>` 设置中。

    最后，``debug_task`` 示例是一个用于输出
    当前请求信息的任务。这使用了 Celery 3.1 中引入的新选项 ``bind=True``，
    用于方便地引用当前任务实例。


.. tab:: 英文

    .. note::

        Previous versions of Celery required a separate library to work with Django,
        but since 3.1 this is no longer the case. Django is supported out of the
        box now so this document only contains a basic way to integrate Celery and
        Django. You'll use the same API as non-Django users so you're recommended
        to read the :ref:`first-steps` tutorial
        first and come back to this tutorial. When you have a working example you can
        continue to the :ref:`next-steps` guide.

    .. note::

        Celery 5.5.x supports Django 2.2 LTS or newer versions.
        Please use Celery 5.2.x for versions older than Django 2.2 or Celery 4.4.x if your Django version is older than 1.11.

    To use Celery with your Django project you must first define
    an instance of the Celery library (called an "app")

    If you have a modern Django project layout like::

        - proj/
        - manage.py
        - proj/
            - __init__.py
            - settings.py
            - urls.py

    then the recommended way is to create a new `proj/proj/celery.py` module
    that defines the Celery instance:

    :file: `proj/proj/celery.py`

    .. literalinclude:: ../../examples/django/proj/celery.py

    Then you need to import this app in your :file:`proj/proj/__init__.py`
    module. This ensures that the app is loaded when Django starts
    so that the ``@shared_task`` decorator (mentioned later) will use it:

    :file:`proj/proj/__init__.py`:

    .. literalinclude:: ../../examples/django/proj/__init__.py

    Note that this example project layout is suitable for larger projects,
    for simple projects you may use a single contained module that defines
    both the app and tasks, like in the :ref:`tut-celery` tutorial.

    Let's break down what happens in the first module,
    first, we set the default :envvar:`DJANGO_SETTINGS_MODULE` environment
    variable for the :program:`celery` command-line program:

    .. code-block:: python

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

    You don't need this line, but it saves you from always passing in the
    settings module to the ``celery`` program. It must always come before
    creating the app instances, as is what we do next:

    .. code-block:: python

        app = Celery('proj')

    This is our instance of the library, you can have many instances
    but there's probably no reason for that when using Django.

    We also add the Django settings module as a configuration source
    for Celery. This means that you don't have to use multiple
    configuration files, and instead configure Celery directly
    from the Django settings; but you can also separate them if wanted.

    .. code-block:: python

        app.config_from_object('django.conf:settings', namespace='CELERY')

    The uppercase name-space means that all
    :ref:`Celery configuration options <configuration>`
    must be specified in uppercase instead of lowercase, and start with
    ``CELERY_``, so for example the :setting:`task_always_eager` setting
    becomes ``CELERY_TASK_ALWAYS_EAGER``, and the :setting:`broker_url`
    setting becomes ``CELERY_BROKER_URL``. This also applies to the
    workers settings, for instance, the :setting:`worker_concurrency`
    setting becomes ``CELERY_WORKER_CONCURRENCY``.

    For example, a Django project's configuration file might include:

    .. code-block:: python
        :caption: settings.py

        ...

        # Celery Configuration Options
        CELERY_TIMEZONE = "Australia/Tasmania"
        CELERY_TASK_TRACK_STARTED = True
        CELERY_TASK_TIME_LIMIT = 30 * 60

    You can pass the settings object directly instead, but using a string
    is better since then the worker doesn't have to serialize the object.
    The ``CELERY_`` namespace is also optional, but recommended (to
    prevent overlap with other Django settings).

    Next, a common practice for reusable apps is to define all tasks
    in a separate ``tasks.py`` module, and Celery does have a way to
    auto-discover these modules:

    .. code-block:: python

        app.autodiscover_tasks()

    With the line above Celery will automatically discover tasks from all
    of your installed apps, following the ``tasks.py`` convention::

        - app1/
            - tasks.py
            - models.py
        - app2/
            - tasks.py
            - models.py


    This way you don't have to manually add the individual modules
    to the :setting:`CELERY_IMPORTS <imports>` setting.

    Finally, the ``debug_task`` example is a task that dumps
    its own request information. This is using the new ``bind=True`` task option
    introduced in Celery 3.1 to easily refer to the current task instance.

使用 ``@shared_task`` 装饰器
------------------------------------

Using the ``@shared_task`` decorator

.. tab:: 中文

    你编写的任务通常会放在可重用的应用中，而可重用应用不能依赖于项目本身，
    因此你也不能直接导入项目中的 app 实例。

    ``@shared_task`` 装饰器允许你在没有具体 app 实例的情况下定义任务：

    :file:`demoapp/tasks.py`:

    .. literalinclude:: ../../examples/django/demoapp/tasks.py


    .. seealso::

        你可以在以下地址找到 Django 示例项目的完整源代码：
        https://github.com/celery/celery/tree/main/examples/django/

.. tab:: 英文

    The tasks you write will probably live in reusable apps, and reusable
    apps cannot depend on the project itself, so you also cannot import your app
    instance directly.

    The ``@shared_task`` decorator lets you create tasks without having any
    concrete app instance:

    :file:`demoapp/tasks.py`:

    .. literalinclude:: ../../examples/django/demoapp/tasks.py


    .. seealso::

        You can find the full source code for the Django example project at:
        https://github.com/celery/celery/tree/main/examples/django/

在数据库事务结束时触发任务
----------------------------------------------------

Trigger tasks at the end of the database transaction

.. tab:: 中文

    在 Django 中的一个常见陷阱是：在数据库事务提交之前立即触发任务，
    这意味着 Celery 任务可能会在所有更改被持久化到数据库之前运行。例如：

    .. code-block:: python

        # views.py
        def create_user(request):
            # 注意：这是一个简化示例，实际应使用表单来验证输入
            user = User.objects.create(username=request.POST['username'])
            send_email.delay(user.pk)
            return HttpResponse('User created')

        # task.py
        @shared_task
        def send_email(user_pk):
            user = User.objects.get(pk=user_pk)
            # 发送邮件...

    在这种情况下，``send_email`` 任务可能会在视图函数提交事务之前启动，
    从而导致任务无法查找到该用户。

    一种常见的解决方案是使用 Django 的 `on_commit`_ 钩子，
    在事务提交之后再触发任务：

    .. code-block:: diff

        - send_email.delay(user.pk)
        + transaction.on_commit(lambda: send_email.delay(user.pk))

    .. versionadded:: 5.4

    由于这是一个非常常见的模式，Celery 5.4 引入了一个便捷的快捷方式，
    通过 :class:`~celery.contrib.django.task.DjangoTask` 实现。你可以不再调用
    :meth:`~celery.app.task.Task.delay`，而是使用
    :meth:`~celery.contrib.django.task.DjangoTask.delay_on_commit`：

    .. code-block:: diff

        - send_email.delay(user.pk)
        + send_email.delay_on_commit(user.pk)

    该 API 会自动将任务封装在 `on_commit`_ 钩子中。
    如果你确实需要立即触发任务，仍然可以使用原有的
    :meth:`~celery.app.task.Task.delay` 方法。

    与 ``delay`` 方法相比，``delay_on_commit`` 的一个关键区别在于：
    该方法不会立即返回任务 ID。任务只有在 Django 事务完成后才会被发送到消息代理。
    如果你需要获取任务 ID，建议继续使用 :meth:`~celery.app.task.Task.delay`。

    如果你已经按照前述步骤进行设置，
    那么该任务类将会自动启用此行为。
    但如果你的 app :ref:`使用了自定义的任务基类 <task-custom-classes>`，
    那么你需要继承 :class:`~celery.contrib.django.task.DjangoTask`，
    而不是 :class:`~celery.app.task.Task`，以获得这一行为。

.. tab:: 英文

    A common pitfall with Django is triggering a task immediately and not wait until
    the end of the database transaction, which means that the Celery task may run
    before all changes are persisted to the database. For example:

    .. code-block:: python

        # views.py
        def create_user(request):
            # Note: simplified example, use a form to validate input
            user = User.objects.create(username=request.POST['username'])
            send_email.delay(user.pk)
            return HttpResponse('User created')

        # task.py
        @shared_task
        def send_email(user_pk):
            user = User.objects.get(pk=user_pk)
            # send email ...

    In this case, the ``send_email`` task could start before the view has committed
    the transaction to the database, and therefore the task may not be able to find
    the user.

    A common solution is to use Django's `on_commit`_ hook to trigger the task
    after the transaction has been committed:

    .. code-block:: diff

        - send_email.delay(user.pk)
        + transaction.on_commit(lambda: send_email.delay(user.pk))

    .. versionadded:: 5.4

    Since this is such a common pattern, Celery 5.4 introduced a handy shortcut for this,
    using a :class:`~celery.contrib.django.task.DjangoTask`. Instead of calling
    :meth:`~celery.app.task.Task.delay`, you should call
    :meth:`~celery.contrib.django.task.DjangoTask.delay_on_commit`:

    .. code-block:: diff

        - send_email.delay(user.pk)
        + send_email.delay_on_commit(user.pk)


    This API takes care of wrapping the call into the `on_commit`_ hook for you.
    In rare cases where you want to trigger a task without waiting, the existing
    :meth:`~celery.app.task.Task.delay` API is still available.

    One key difference compared to the ``delay`` method, is that ``delay_on_commit``
    will NOT return the task ID back to the caller. The task is not sent to the broker
    when you call the method, only when the Django transaction finishes. If you need the
    task ID, best to stick to :meth:`~celery.app.task.Task.delay`.

    This task class should be used automatically if you've follow the setup steps above.
    However, if your app :ref:`uses a custom task base class <task-custom-classes>`,
    you'll need inherit from :class:`~celery.contrib.django.task.DjangoTask` instead of
    :class:`~celery.app.task.Task` to get this behaviour.

.. _on_commit: https://docs.djangoproject.com/en/stable/topics/db/transactions/#django.db.transaction.on_commit

扩展
==========

Extensions

.. _django-celery-results:

``django-celery-results`` - 使用 Django ORM/Cache 作为结果后端
--------------------------------------------------------------------------

``django-celery-results`` - Using the Django ORM/Cache as a result backend

.. tab:: 中文

    :pypi:`django-celery-results` 扩展提供了使用 Django ORM 或 Django 缓存框架作为结果后端的能力。

    要在你的项目中使用该扩展，请按照以下步骤操作：

    #. 安装 :pypi:`django-celery-results` 库：
        .. code-block:: console

            $ pip install django-celery-results

    #. 在 Django 项目的 :file:`settings.py` 文件中将 ``django_celery_results`` 添加到 ``INSTALLED_APPS`` 中
        .. code-block::
            
            INSTALLED_APPS = (
                ...,
                'django_celery_results',
            )

    注意：模块名中使用的是下划线而不是连字符。

    #. 执行数据库迁移以创建 Celery 所需的数据库表：
        .. code-block:: console

            $ python manage.py migrate django_celery_results

    #. 配置 Celery 使用 :pypi:`django-celery-results` 作为结果后端。
        假设你也在使用 Django 的 :file:`settings.py` 来配置 Celery，添加如下配置：

        .. code-block:: python

            CELERY_RESULT_BACKEND = 'django-db'

        如果使用缓存后端，你可以指定一个在 Django 的 CACHES 设置中定义的缓存：

        .. code-block:: python

            CELERY_RESULT_BACKEND = 'django-cache'

            # 从 CACHES 设置中选择要使用的缓存
            CELERY_CACHE_BACKEND = 'default'

            # Django 中的缓存设置
            CACHES = {
                'default': {
                    'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                    'LOCATION': 'my_cache_table',
                }
            }

        有关更多配置选项，请参阅 :ref:`conf-result-backend` 参考文档。

.. tab:: 英文

    The :pypi:`django-celery-results` extension provides result backends
    using either the Django ORM, or the Django Cache framework.

    To use this with your project you need to follow these steps:

    #. Install the :pypi:`django-celery-results` library:
        .. code-block:: console

            $ pip install django-celery-results

    #. Add ``django_celery_results`` to ``INSTALLED_APPS`` in your Django project's :file:`settings.py`
        .. code-block::
            
            INSTALLED_APPS = (
                ...,
                'django_celery_results',
            )

    Note that there is no dash in the module name, only underscores.

    #. Create the Celery database tables by performing a database migrations:
        .. code-block:: console

            $ python manage.py migrate django_celery_results

    #. Configure Celery to use the :pypi:`django-celery-results` backend.
        Assuming you are using Django's :file:`settings.py` to also configure
        Celery, add the following settings:

        .. code-block:: python

            CELERY_RESULT_BACKEND = 'django-db'

        When using the cache backend, you can specify a cache defined within
        Django's CACHES setting.

        .. code-block:: python

            CELERY_RESULT_BACKEND = 'django-cache'

            # pick which cache from the CACHES setting.
            CELERY_CACHE_BACKEND = 'default'

            # django setting.
            CACHES = {
                'default': {
                    'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                    'LOCATION': 'my_cache_table',
                }
            }

        For additional configuration options, view the
        :ref:`conf-result-backend` reference.


``django-celery-beat`` - 带有管理界面的数据库支持的周期性任务。
-----------------------------------------------------------------------------

``django-celery-beat`` - Database-backed Periodic Tasks with Admin interface.

.. tab:: 中文

    更多信息请参考 :ref:`beat-custom-schedulers`。

.. tab:: 英文

    See :ref:`beat-custom-schedulers` for more information.

启动工作进程
===========================

Starting the worker process

.. tab:: 中文

    在生产环境中，你应该将 worker 作为后台守护进程运行 —— 参见 :ref:`daemonizing`。
    但在测试和开发阶段，你可以使用 :program:`celery worker` 管理命令启动一个 worker 实例，
    这与使用 Django 的 :command:`manage.py runserver` 命令类似：

    .. code-block:: console

        $ celery -A proj worker -l INFO

    如需查看所有可用的命令行选项，请使用 help 命令：

    .. code-block:: console

        $ celery --help

.. tab:: 英文

    In a production environment you'll want to run the worker in the background
    as a daemon - see :ref:`daemonizing` - but for testing and
    development it is useful to be able to start a worker instance by using the
    :program:`celery worker` manage command, much as you'd use Django's
    :command:`manage.py runserver`:

    .. code-block:: console

        $ celery -A proj worker -l INFO

    For a complete listing of the command-line options available,
    use the help command:

    .. code-block:: console

        $ celery --help

下一步
=====================

Where to go from here

.. tab:: 中文

    如果你希望进一步了解 Celery，建议继续阅读 :ref:`Next Steps <next-steps>` 教程，
    之后可以深入学习 :ref:`User Guide <guide>`。

.. tab:: 英文

    If you want to learn more you should continue to the
    :ref:`Next Steps <next-steps>` tutorial, and after that you
    can study the :ref:`User Guide <guide>`.
