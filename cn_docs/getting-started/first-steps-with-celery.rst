.. _tut-celery:
.. _first-steps:

=========================
使用 Celery 的第一步
=========================

First Steps with Celery

.. tab:: 中文

    Celery 是一个“电池齐全”的任务队列系统。  
    它易于上手，可以让你在不了解其解决问题的全部复杂性的情况下快速开始使用。  
    它围绕最佳实践进行设计，能够让你的产品具备良好的可扩展性，并能够与其他语言集成，  
    同时还提供了运行生产系统所需的工具与支持。

    在本教程中，你将学习使用 Celery 的最基础知识。

    学习内容包括：

    - 选择并安装消息传输组件（broker）；
    - 安装 Celery 并创建你的第一个任务；
    - 启动 worker 并调用任务；
    - 跟踪任务在不同状态之间的转换，并检查其返回值。

    Celery 初看可能让人望而生畏 —— 但别担心 —— 本教程会帮你迅速入门。  
    教程内容有意保持简洁，以避免高级功能带来的困扰。  
    在你完成本教程后，建议继续阅读其余文档，例如 :ref:`next-steps` 教程将展示 Celery 更强大的能力。

.. tab:: 英文

    Celery is a task queue with batteries included.
    It's easy to use so that you can get started without learning
    the full complexities of the problem it solves. It's designed
    around best practices so that your product can scale
    and integrate with other languages, and it comes with the
    tools and support you need to run such a system in production.

    In this tutorial you'll learn the absolute basics of using Celery.

    Learn about:

    - Choosing and installing a message transport (broker).
    - Installing Celery and creating your first task.
    - Starting the worker and calling tasks.
    - Keeping track of tasks as they transition through different states,
    and inspecting return values.

    Celery may seem daunting at first - but don't worry - this tutorial
    will get you started in no time. It's deliberately kept simple, so
    as to not confuse you with advanced features.
    After you have finished this tutorial,
    it's a good idea to browse the rest of the documentation.
    For example the :ref:`next-steps` tutorial will
    showcase Celery's capabilities.



.. _celerytut-broker:

选择 Broker
=================

Choosing a Broker

.. tab:: 中文

    Celery 需要一个用于发送与接收消息的解决方案；  
    这通常表现为一个独立的服务，称为 *消息中间件（message broker）*。

    你可以从以下几种方案中选择：

.. tab:: 英文

    Celery requires a solution to send and receive messages; usually this
    comes in the form of a separate service called a *message broker*.

    There are several choices available, including:

RabbitMQ
--------

RabbitMQ

.. tab:: 中文

    `RabbitMQ`_ 功能完备、稳定可靠、持久性强且易于安装。  
    它是生产环境中的优秀选择。  
    关于如何将 RabbitMQ 与 Celery 配合使用的详细信息：

        :ref:`broker-rabbitmq`

    如果你使用的是 Ubuntu 或 Debian，可以执行以下命令安装 RabbitMQ：

    .. code-block:: console

        $ sudo apt-get install rabbitmq-server

    或者，如果你想使用 Docker 运行它，可以执行：

    .. code-block:: console

        $ docker run -d -p 5672:5672 rabbitmq

    命令执行完成后，broker 会在后台运行，准备好为你传递消息：  
    ``Starting rabbitmq-server: SUCCESS``。

    如果你不是使用 Ubuntu 或 Debian，也不必担心，  
    你可以访问以下网址，查找适用于其他平台（包括 Microsoft Windows）的安装指南：

        http://www.rabbitmq.com/download.html

.. tab:: 英文

    `RabbitMQ`_ is feature-complete, stable, durable and easy to install.
    It's an excellent choice for a production environment.
    Detailed information about using RabbitMQ with Celery:

        :ref:`broker-rabbitmq`

    If you're using Ubuntu or Debian install RabbitMQ by executing this
    command:

    .. code-block:: console

        $ sudo apt-get install rabbitmq-server

    Or, if you want to run it on Docker execute this:

    .. code-block:: console

        $ docker run -d -p 5672:5672 rabbitmq

    When the command completes, the broker will already be running in the background,
    ready to move messages for you: ``Starting rabbitmq-server: SUCCESS``.

    Don't worry if you're not running Ubuntu or Debian, you can go to this
    website to find similarly simple installation instructions for other
    platforms, including Microsoft Windows:

        http://www.rabbitmq.com/download.html

.. _`RabbitMQ`: http://www.rabbitmq.com/

Redis
-----

Redis

.. tab:: 中文

    `Redis`_ 也是一个功能完备的解决方案，  
    但在遇到异常终止或断电的情况下更容易出现数据丢失。  
    关于使用 Redis 的详细信息：

    :ref:`broker-redis`

    如果你想在 Docker 中运行 Redis，可以执行以下命令：

    .. code-block:: console

        $ docker run -d -p 6379:6379 redis

.. tab:: 英文

    `Redis`_ is also feature-complete, but is more susceptible to data loss in
    the event of abrupt termination or power failures. Detailed information about using Redis:

    :ref:`broker-redis`

    If you want to run it on Docker execute this:

    .. code-block:: console

        $ docker run -d -p 6379:6379 redis

.. _`Redis`: https://redis.io/

其他 broker
-------------

Other brokers

.. tab:: 中文

    除了上述方案外，还有一些实验性的传输实现可供选择，  
    包括 :ref:`Amazon SQS <broker-sqs>` 等。

    完整列表请参见 :ref:`broker-overview`。

.. tab:: 英文

    In addition to the above, there are other experimental transport implementations
    to choose from, including :ref:`Amazon SQS <broker-sqs>`.

    See :ref:`broker-overview` for a full list.

.. _celerytut-installation:

安装 Celery
=================

Installing Celery

.. tab:: 中文

    Celery 已发布至 Python 软件包索引（PyPI），因此可以使用标准的 Python 工具（如 ``pip`` ）进行安装:

    .. code-block:: console

        $ pip install celery

.. tab:: 英文

    Celery is on the Python Package Index (PyPI), so it can be installed
    with standard Python tools like ``pip``:

    .. code-block:: console

        $ pip install celery

Application
===========

Application

.. tab:: 中文

    你首先需要一个 Celery 实例。我们称之为 *Celery 应用*，简称 *app*。由于该实例是你在 Celery 中执行所有操作的入口点（如创建任务、管理 Worker 等），它必须能被其他模块导入。

    本教程将所有内容集中在一个模块中，但在较大的项目中，建议创建一个 :ref:`专用模块 <project-layout>`。

    我们来创建一个 :file:`tasks.py` 文件：

    .. code-block:: python

        from celery import Celery

        app = Celery('tasks', broker='pyamqp://guest@localhost//')

        @app.task
        def add(x, y):
            return x + y

    :class:`~celery.app.Celery` 的第一个参数是当前模块的名称，这样在任务定义于 `__main__` 模块时可以自动生成名称。

    第二个参数是 ``broker`` 关键字参数，用于指定你想使用的消息中间件的 URL。这里我们使用的是 RabbitMQ（也是默认选项）。

    更多中间件选项参见 :ref:`celerytut-broker` —— 如果你使用 RabbitMQ，可以写成 ``amqp://localhost``，使用 Redis 则可以写成 ``redis://localhost``。

    你定义了一个简单的任务 ``add``，用于返回两个数的和。

.. tab:: 英文

    The first thing you need is a Celery instance.  We call this the *Celery
    application* or just *app* for short. As this instance is used as
    the entry-point for everything you want to do in Celery, like creating tasks and
    managing workers, it must be possible for other modules to import it.

    In this tutorial we keep everything contained in a single module,
    but for larger projects you want to create
    a :ref:`dedicated module <project-layout>`.

    Let's create the file :file:`tasks.py`:

    .. code-block:: python

        from celery import Celery

        app = Celery('tasks', broker='pyamqp://guest@localhost//')

        @app.task
        def add(x, y):
            return x + y

    The first argument to :class:`~celery.app.Celery` is the name of the current module.
    This is only needed so that names can be automatically generated when the tasks are
    defined in the `__main__` module.

    The second argument is the broker keyword argument, specifying the URL of the
    message broker you want to use. Here we are using RabbitMQ (also the default option).

    See :ref:`celerytut-broker` above for more choices --
    for RabbitMQ you can use ``amqp://localhost``, or for Redis you can
    use ``redis://localhost``.

    You defined a single task, called ``add``, returning the sum of two numbers.

.. _celerytut-running-the-worker:

运行 Celery Worker 服务
================================

Running the Celery worker server

.. tab:: 中文

    你现在可以通过在程序中加入 ``worker`` 参数来运行 worker 进程：

    .. code-block:: console

        $ celery -A tasks worker --loglevel=INFO

    .. note::

        如果 worker 无法启动，请参考 :ref:`celerytut-troubleshooting` 部分进行排查。

    在生产环境中，你可能希望将 worker 作为后台守护进程运行。  
    要实现这一点，你需要使用你的操作系统所提供的工具，或者使用像 `supervisord`_ 这样的进程管理器（参见 :ref:`daemonizing` 了解更多信息）。

    若要查看所有可用的命令行选项，可运行：

    .. code-block:: console

        $ celery worker --help

    此外 Celery 还有许多其他可用的命令，也可以通过以下方式查看帮助信息：

    .. code-block:: console

        $ celery --help

.. tab:: 英文

    You can now run the worker by executing our program with the ``worker``
    argument:

    .. code-block:: console

        $ celery -A tasks worker --loglevel=INFO

    .. note::

        See the :ref:`celerytut-troubleshooting` section if the worker
        doesn't start.

    In production you'll want to run the worker in the
    background as a daemon. To do this you need to use the tools provided
    by your platform, or something like `supervisord`_ (see :ref:`daemonizing`
    for more information).

    For a complete listing of the command-line options available, do:

    .. code-block:: console

        $  celery worker --help

    There are also several other commands available, and help is also available:

    .. code-block:: console

        $ celery --help

.. _`supervisord`: http://supervisord.org

.. _celerytut-calling:

调用任务
================

Calling the task

.. tab:: 中文

    要调用我们的任务，可以使用 :meth:`~@Task.delay` 方法。

    这是 :meth:`~@Task.apply_async` 方法的便捷快捷方式，后者提供了更强大的任务执行控制（见 :ref:`guide-calling`）：

    .. code-block:: python

        >>> from tasks import add
        >>> add.delay(4, 4)

    此时任务已经由之前启动的 worker 处理。  
    你可以通过查看 worker 控制台的输出，验证任务是否已被处理。

    调用任务会返回一个 :class:`~@AsyncResult` 实例。  
    可以使用该实例检查任务的状态、等待任务完成，或者获取任务的返回值（如果任务失败，还可以获取异常和回溯信息）。

    默认情况下，结果功能是禁用的。  
    如果你希望进行远程过程调用或跟踪任务结果到数据库中，你需要配置 Celery 使用一个结果后端（Result Backend）。  
    有关这方面的配置，请参考下一节。

.. tab:: 英文

    To call our task you can use the :meth:`~@Task.delay` method.

    This is a handy shortcut to the :meth:`~@Task.apply_async`
    method that gives greater control of the task execution (see
    :ref:`guide-calling`)::

        >>> from tasks import add
        >>> add.delay(4, 4)

    The task has now been processed by the worker you started earlier.
    You can verify this by looking at the worker's console output.

    Calling a task returns an :class:`~@AsyncResult` instance.
    This can be used to check the state of the task, wait for the task to finish,
    or get its return value (or if the task failed, to get the exception and traceback).

    Results are not enabled by default. In order to do remote procedure calls
    or keep track of task results in a database, you will need to configure Celery to use a result
    backend.  This is described in the next section.

.. _celerytut-keeping-results:

保存结果
===============

Keeping Results

.. tab:: 中文

    如果你希望跟踪任务的状态，Celery 需要将这些状态存储或发送到某个地方。你可以选择多个内置的结果后端： `SQLAlchemy`_ / `Django`_ ORM、 `MongoDB`_ 、 `Memcached`_ 、 `Redis`_ 、:ref:`RPC <conf-rpc-result-backend>` （ `RabbitMQ`_ / AMQP），或者你也可以定义自己的后端。

    在这个示例中，我们使用 `rpc` 结果后端，它将状态作为瞬时消息发送回来。后端通过 `backend` 参数传递给 :class:`@Celery`（如果你选择使用配置模块，则通过 :setting:`result_backend` 设置）。因此，你可以修改 `tasks.py` 文件中的这一行来启用 `rpc://` 后端：

    .. code-block:: python

        app = Celery('tasks', backend='rpc://', broker='pyamqp://')

    或者，如果你想使用 Redis 作为结果后端，但仍然使用 RabbitMQ 作为消息代理（这是一个常见的组合）：

    .. code-block:: python

        app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')

    要了解有关结果后端的更多信息，请参阅 :ref:`task-result-backends`。

    现在，配置了结果后端后，重新启动 worker，关闭当前的 Python 会话，然后再次导入 `tasks` 模块以使更改生效。此时，当你调用任务时，你将持有返回的 :class:`~@AsyncResult` 实例：

    .. code-block:: pycon

        >>> from tasks import add    # 关闭并重新打开以获取更新的 'app'
        >>> result = add.delay(4, 4)

    :meth:`~@AsyncResult.ready` 方法返回任务是否已完成处理：

    .. code-block:: pycon

        >>> result.ready()
        False

    你可以等待结果完成，但这很少使用，因为它将异步调用转化为同步调用：

    .. code-block:: pycon

        >>> result.get(timeout=1)
        8

    如果任务引发了异常，:meth:`~@AsyncResult.get` 将重新引发该异常，但你可以通过指定 `propagate` 参数来覆盖这一行为：

    .. code-block:: pycon

        >>> result.get(propagate=False)

    如果任务引发了异常，你还可以访问原始的回溯信息：

    .. code-block:: pycon

        >>> result.traceback

    .. warning::

        后端使用资源来存储和传输结果。为了确保资源被释放，你必须最终对每个通过调用任务返回的 :class:`~@AsyncResult` 实例调用 :meth:`~@AsyncResult.get` 或 :meth:`~@AsyncResult.forget`。

    请参见 :mod:`celery.result` 获取完整的结果对象参考。

.. tab:: 英文

    If you want to keep track of the tasks' states, Celery needs to store or send
    the states somewhere. There are several
    built-in result backends to choose from: `SQLAlchemy`_/`Django`_ ORM,
    `MongoDB`_, `Memcached`_, `Redis`_, :ref:`RPC <conf-rpc-result-backend>` (`RabbitMQ`_/AMQP),
    and -- or you can define your own.

    For this example we use the `rpc` result backend, that sends states
    back as transient messages. The backend is specified via the ``backend`` argument to
    :class:`@Celery`, (or via the :setting:`result_backend` setting if
    you choose to use a configuration module). So, you can modify this line in the `tasks.py`
    file to enable the `rpc://` backend:

    .. code-block:: python

        app = Celery('tasks', backend='rpc://', broker='pyamqp://')

    Or if you want to use Redis as the result backend, but still use RabbitMQ as
    the message broker (a popular combination):

    .. code-block:: python

        app = Celery('tasks', backend='redis://localhost', broker='pyamqp://')

    To read more about result backends please see :ref:`task-result-backends`.

    Now with the result backend configured, restart the worker, close the current python session and import the
    ``tasks`` module again to put the changes into effect. This time you'll hold on to the
    :class:`~@AsyncResult` instance returned when you call a task:

    .. code-block:: pycon

        >>> from tasks import add    # close and reopen to get updated 'app'
        >>> result = add.delay(4, 4)

    The :meth:`~@AsyncResult.ready` method returns whether the task
    has finished processing or not:

    .. code-block:: pycon

        >>> result.ready()
        False

    You can wait for the result to complete, but this is rarely used
    since it turns the asynchronous call into a synchronous one:

    .. code-block:: pycon

        >>> result.get(timeout=1)
        8

    In case the task raised an exception, :meth:`~@AsyncResult.get` will
    re-raise the exception, but you can override this by specifying
    the ``propagate`` argument:

    .. code-block:: pycon

        >>> result.get(propagate=False)


    If the task raised an exception, you can also gain access to the
    original traceback:

    .. code-block:: pycon

        >>> result.traceback

    .. warning::

        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        :meth:`~@AsyncResult.get` or :meth:`~@AsyncResult.forget` on
        EVERY :class:`~@AsyncResult` instance returned after calling
        a task.

    See :mod:`celery.result` for the complete result object reference.

.. _`Memcached`: http://memcached.org
.. _`MongoDB`: http://www.mongodb.org
.. _`SQLAlchemy`: http://www.sqlalchemy.org/
.. _`Django`: http://djangoproject.com

.. _celerytut-configuration:

Celery 配置
=============

Configuration

.. tab:: 中文

    Celery 像一台消费型电器一样，不需要复杂的配置即可运行。
    它有输入和输出。输入必须连接到一个代理（broker），输出可以选择性地连接到结果后端。然而，如果你仔细观察后部，你会发现有很多滑块、旋钮和按钮：这些就是配置项。

    默认配置对于大多数用例应该足够了，但有许多选项可以进行配置，以使 Celery 完全按照需要的方式工作。阅读可用的配置选项是一个好主意，这样可以帮助你了解哪些内容是可以配置的。你可以在 :ref:`configuration` 参考中阅读这些选项。

    配置可以直接在应用程序中设置，也可以通过使用专门的配置模块来设置。作为示例，你可以通过更改 :setting:`task_serializer` 设置来配置默认的任务有效负载序列化器：

    .. code-block:: python

        app.conf.task_serializer = 'json'

    如果你一次配置多个设置，可以使用 ``update`` 方法：

    .. code-block:: python

        app.conf.update(
            task_serializer='json',
            accept_content=['json'],  # 忽略其他内容
            result_serializer='json',
            timezone='Europe/Oslo',
            enable_utc=True,
        )

    对于较大的项目，推荐使用专门的配置模块。避免将周期性任务间隔和任务路由选项硬编码在代码中。将这些设置集中存放更好，尤其是在库中，这样可以让用户控制他们的任务行为。集中配置也能让系统管理员在发生系统故障时轻松进行调整。

    你可以通过调用 :meth:`@config_from_object` 方法让 Celery 实例使用配置模块：

    .. code-block:: python

        app.config_from_object('celeryconfig')

    这个模块通常被命名为 "``celeryconfig``"，但你可以使用任何模块名。

    在上面的例子中，必须提供一个名为 ``celeryconfig.py`` 的模块，该模块可以从当前目录或 Python 路径中加载。它可能如下所示：

    :file:`celeryconfig.py`:

    .. code-block:: python

        broker_url = 'pyamqp://'
        result_backend = 'rpc://'

        task_serializer = 'json'
        result_serializer = 'json'
        accept_content = ['json']
        timezone = 'Europe/Oslo'
        enable_utc = True

    为了验证你的配置文件是否正常工作，并且不包含任何语法错误，你可以尝试导入它：

    .. code-block:: console

        $ python -m celeryconfig

    有关完整的配置选项参考，请参阅 :ref:`configuration`。

    为了展示配置文件的强大功能，下面是如何将一个表现不佳的任务路由到专门的队列：

    :file:`celeryconfig.py`:

    .. code-block:: python

        task_routes = {
            'tasks.add': 'low-priority',
        }

    或者，你也可以选择限制该任务的处理速率，而不是路由它，这样每分钟只允许处理 10 个此类任务（10/m）：

    :file:`celeryconfig.py`:

    .. code-block:: python

        task_annotations = {
            'tasks.add': {'rate_limit': '10/m'}
        }

    如果你使用的是 RabbitMQ 或 Redis 作为代理，你也可以在运行时指示 worker 为任务设置新的速率限制：

    .. code-block:: console

        $ celery -A tasks control rate_limit tasks.add 10/m
        worker@example.com: OK
            new rate limit set successfully

    参见 :ref:`guide-routing` 了解更多关于任务路由的信息，和 :setting:`task_annotations` 设置了解更多关于注释的内容，或者查看 :ref:`guide-monitoring` 了解更多关于远程控制命令以及如何监控 worker 的运行情况。

.. tab:: 英文

    Celery, like a consumer appliance, doesn't need much configuration to operate.
    It has an input and an output. The input must be connected to a broker, and the output can
    be optionally connected to a result backend. However, if you look closely at the back,
    there's a lid revealing loads of sliders, dials, and buttons: this is the configuration.

    The default configuration should be good enough for most use cases, but there are
    many options that can be configured to make Celery work exactly as needed.
    Reading about the options available is a good idea to familiarize yourself with what
    can be configured. You can read about the options in the
    :ref:`configuration` reference.

    The configuration can be set on the app directly or by using a dedicated
    configuration module.
    As an example you can configure the default serializer used for serializing
    task payloads by changing the :setting:`task_serializer` setting:

    .. code-block:: python

        app.conf.task_serializer = 'json'

    If you're configuring many settings at once you can use ``update``:

    .. code-block:: python

        app.conf.update(
            task_serializer='json',
            accept_content=['json'],  # Ignore other content
            result_serializer='json',
            timezone='Europe/Oslo',
            enable_utc=True,
        )

    For larger projects, a dedicated configuration module is recommended.
    Hard coding periodic task intervals and task routing options is discouraged.
    It is much better to keep these in a centralized location. This is especially
    true for libraries, as it enables users to control how their tasks behave.
    A centralized configuration will also allow your SysAdmin to make simple changes
    in the event of system trouble.

    You can tell your Celery instance to use a configuration module
    by calling the :meth:`@config_from_object` method:

    .. code-block:: python

        app.config_from_object('celeryconfig')

    This module is often called "``celeryconfig``", but you can use any
    module name.

    In the above case, a module named ``celeryconfig.py`` must be available to load from the
    current directory or on the Python path. It could look something like this:

    :file:`celeryconfig.py`:

    .. code-block:: python

        broker_url = 'pyamqp://'
        result_backend = 'rpc://'

        task_serializer = 'json'
        result_serializer = 'json'
        accept_content = ['json']
        timezone = 'Europe/Oslo'
        enable_utc = True

    To verify that your configuration file works properly and doesn't
    contain any syntax errors, you can try to import it:

    .. code-block:: console

        $ python -m celeryconfig

    For a complete reference of configuration options, see :ref:`configuration`.

    To demonstrate the power of configuration files, this is how you'd
    route a misbehaving task to a dedicated queue:

    :file:`celeryconfig.py`:

    .. code-block:: python

        task_routes = {
            'tasks.add': 'low-priority',
        }

    Or instead of routing it you could rate limit the task
    instead, so that only 10 tasks of this type can be processed in a minute
    (10/m):

    :file:`celeryconfig.py`:

    .. code-block:: python

        task_annotations = {
            'tasks.add': {'rate_limit': '10/m'}
        }

    If you're using RabbitMQ or Redis as the
    broker then you can also direct the workers to set a new rate limit
    for the task at runtime:

    .. code-block:: console

        $ celery -A tasks control rate_limit tasks.add 10/m
        worker@example.com: OK
            new rate limit set successfully

    See :ref:`guide-routing` to read more about task routing,
    and the :setting:`task_annotations` setting for more about annotations,
    or :ref:`guide-monitoring` for more about remote control commands
    and how to monitor what your workers are doing.

进一步学习
=====================

Where to go from here

.. tab:: 中文

    如果你想深入了解，应该继续阅读 :ref:`Next Steps <next-steps>` 教程，之后可以阅读 :ref:`User Guide <guide>`。

.. tab:: 英文

    If you want to learn more you should continue to the
    :ref:`Next Steps <next-steps>` tutorial, and after that you
    can read the :ref:`User Guide <guide>`.

.. _celerytut-troubleshooting:

问题排查
===============

Troubleshooting

.. tab:: 中文

    另外，在 :ref:`faq` 中还有故障排除部分。

.. tab:: 英文

    There's also a troubleshooting section in the :ref:`faq`.

worker 没有开始执行: Permission Error
--------------------------------------

Worker doesn't start: Permission Error

.. tab:: 中文

    - 如果你使用的是 Debian、Ubuntu 或其他基于 Debian 的发行版：

        Debian 最近将 :file:`/dev/shm` 特殊文件重命名为 :file:`/run/shm`。

        一个简单的解决方法是创建一个符号链接：

        .. code-block:: console

            # ln -s /run/shm /dev/shm

    - 其他情况：

        如果你提供了 :option:`--pidfile <celery worker --pidfile>`、:option:`--logfile <celery worker --logfile>` 或 :option:`--statedb <celery worker --statedb>` 参数，那么你必须确保它们指向一个可写且可读的文件或目录，并且该目录对启动 worker 的用户是可访问的。

.. tab:: 英文

    - If you're using Debian, Ubuntu or other Debian-based distributions:

        Debian recently renamed the :file:`/dev/shm` special file
        to :file:`/run/shm`.

        A simple workaround is to create a symbolic link:

        .. code-block:: console

            # ln -s /run/shm /dev/shm

    - Others:

        If you provide any of the :option:`--pidfile <celery worker --pidfile>`,
        :option:`--logfile <celery worker --logfile>` or
        :option:`--statedb <celery worker --statedb>` arguments, then you must
        make sure that they point to a file or directory that's writable and
        readable by the user starting the worker.

结果后端没有工作或者任务总是处在 ``PENDING`` 状态
--------------------------------------------------------------------

Result backend doesn't work or tasks are always in ``PENDING`` state

.. tab:: 中文

    所有任务默认状态为 :state:`PENDING`，因此其状态本应更准确地命名为“未知”。Celery 在发送任务时不会更新状态，任何没有历史记录的任务都被认为是待处理的（毕竟你知道任务 ID）。

    1) 确保任务没有启用 ``ignore_result``。

        启用此选项会强制 worker 跳过更新状态。

    2) 确保 :setting:`task_ignore_result` 设置未启用。

    3) 确保没有任何旧的 worker 仍在运行。

        很容易不小心启动多个 worker，因此请确保在启动新 worker 之前，先正确关闭旧的 worker。

        一个未配置为使用预期结果后端的旧 worker 可能仍在运行，并劫持了任务。

        可以将 :option:`--pidfile <celery worker --pidfile>` 参数设置为绝对路径，以确保不会发生这种情况。

    4) 确保客户端配置了正确的后端。

        如果由于某种原因，客户端配置为使用与 worker 不同的后端，则无法接收结果。确保正确配置了后端：

        .. code-block:: pycon

            >>> result = task.delay()
            >>> print(result.backend)

.. tab:: 英文

    All tasks are :state:`PENDING` by default, so the state would've been
    better named "unknown". Celery doesn't update the state when a task
    is sent, and any task with no history is assumed to be pending (you know
    the task id, after all).

    1) Make sure that the task doesn't have ``ignore_result`` enabled.

        Enabling this option will force the worker to skip updating
        states.

    2) Make sure the :setting:`task_ignore_result` setting isn't enabled.

    3) Make sure that you don't have any old workers still running.

        It's easy to start multiple workers by accident, so make sure
        that the previous worker is properly shut down before you start a new one.

        An old worker that isn't configured with the expected result backend
        may be running and is hijacking the tasks.

        The :option:`--pidfile <celery worker --pidfile>` argument can be set to
        an absolute path to make sure this doesn't happen.

    4) Make sure the client is configured with the right backend.

        If, for some reason, the client is configured to use a different backend
        than the worker, you won't be able to receive the result.
        Make sure the backend is configured correctly:

        .. code-block:: pycon

            >>> result = task.delay()
            >>> print(result.backend)
