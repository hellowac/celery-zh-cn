.. _internals-guide:

================================
代码贡献指南
================================

Contributors Guide to the Code


哲学
==========

Philosophy

API > RCP 优先级规则
---------------------------

The API>RCP Precedence Rule

.. tab:: 中文

    - API 比可读性更重要
    - 可读性比编码约定更重要
    - 编码约定比性能更重要
        - ……除非这段代码已被证明是性能热点。

    最重要的是最终用户的 API。
    编码约定必须为更好的 API 让路；即便因此带来一些痛苦，只要最终结果是更好的 API，这些痛苦就都是值得的。

.. tab:: 英文

    - The API is more important than Readability
    - Readability is more important than Convention
    - Convention is more important than Performance
        - …unless the code is a proven hot-spot.

    More important than anything else is the end-user API.
    Conventions must step aside, and any suffering is always alleviated
    if the end result is a better API.

使用的约定和惯用语
===========================

Conventions and Idioms Used

类
-------

Classes

命名
~~~~~~

Naming

.. tab:: 中文

    - 遵循 :pep:`8`。

    - 类名必须使用 `CamelCase` （驼峰式命名法）。
    - 但如果类名是动词，则必须使用 `lower_case` （下划线小写命名）：

      .. code-block:: python

          # - 针对类的测试用例
          class TestMyClass(Case):                # 不推荐
              pass

          class test_MyClass(Case):               # 推荐
              pass

          # - 针对函数的测试用例
          class TestMyFunction(Case):             # 不推荐
              pass

          class test_my_function(Case):           # 推荐
              pass

          # - “动作类”（动词）
          class UpdateTwitterStatus:    # 不推荐
              pass

          class update_twitter_status:    # 推荐
              pass

      .. note::

          有时候让类伪装成函数是合理的，Python 标准库中也有类似先例（如
          :class:`~contextlib.contextmanager`）。Celery 中的示例包括
          :class:`~celery.signature`、:class:`~celery.chord`、``inspect``、
          :class:`~kombu.utils.functional.promise` 等。

    - 工厂函数与方法必须使用 `CamelCase` 命名（动词除外）：

      .. code-block:: python

          class Celery:
              def consumer_factory(self):     # 不推荐
                  ...
              def Consumer(self):             # 推荐
                  ...

.. tab:: 英文

    - Follows :pep:`8`.

    - Class names must be `CamelCase`.
    - but not if they're verbs, verbs shall be `lower_case`:

        .. code-block:: python

            # - test case for a class
            class TestMyClass(Case):                # BAD
                pass

            class test_MyClass(Case):               # GOOD
                pass

            # - test case for a function
            class TestMyFunction(Case):             # BAD
                pass

            class test_my_function(Case):           # GOOD
                pass

            # - "action" class (verb)
            class UpdateTwitterStatus:    # BAD
                pass

            class update_twitter_status:    # GOOD
                pass

        .. note::

            Sometimes it makes sense to have a class mask as a function,
            and there's precedence for this in the Python standard library (e.g.,
            :class:`~contextlib.contextmanager`). Celery examples include
            :class:`~celery.signature`, :class:`~celery.chord`,
            ``inspect``, :class:`~kombu.utils.functional.promise` and more..

    - Factory functions and methods must be `CamelCase` (excluding verbs):

        .. code-block:: python

            class Celery:

                def consumer_factory(self):     # BAD
                    ...

                def Consumer(self):             # GOOD
                    ...

默认值
~~~~~~~~~~~~~~

Default values

.. tab:: 中文

    类属性用作实例的默认值，
    这样可以在实例化或继承时进行设置。

    **示例：**

    .. code-block:: python

        class Producer:
            active = True
            serializer = 'json'

            def __init__(self, serializer=None, active=None):
                self.serializer = serializer or self.serializer

                # 如果值可能为假值，必须检查 None
                self.active = active if active is not None else self.active

    子类可以修改默认值：

    .. code-block:: python

        TaskProducer(Producer):
            serializer = 'pickle'

    同时也可以在实例化时设置值：

    .. code-block:: pycon

        >>> producer = TaskProducer(serializer='msgpack')


.. tab:: 英文

    Class attributes serve as default values for the instance,
    as this means that they can be set by either instantiation or inheritance.

    **Example:**

    .. code-block:: python

        class Producer:
            active = True
            serializer = 'json'

            def __init__(self, serializer=None, active=None):
                self.serializer = serializer or self.serializer

                # must check for None when value can be false-y
                self.active = active if active is not None else self.active

    A subclass can change the default value:

    .. code-block:: python

        TaskProducer(Producer):
            serializer = 'pickle'

    and the value can be set at instantiation:

    .. code-block:: pycon

        >>> producer = TaskProducer(serializer='msgpack')

异常
~~~~~~~~~~

Exceptions

.. tab:: 中文

    对象的方法与属性所抛出的自定义异常应作为属性提供，并在
    抛出异常的方法或属性的文档中加以说明。

    这样，用户无需去查找异常类的导入路径，而是可以通过 ``help(obj)``
    直接从实例访问异常类。

    **示例**：

    .. code-block:: python

        class Empty(Exception):
            pass

        class Queue:
            Empty = Empty

            def get(self):
                """从队列中获取下一个元素。

                :raises Queue.Empty: 如果队列中已无元素。

                """
                try:
                    return self.queue.popleft()
                except IndexError:
                    raise self.Empty()

.. tab:: 英文

    Custom exceptions raised by an objects methods and properties
    should be available as an attribute and documented in the
    method/property that throw.

    This way a user doesn't have to find out where to import the
    exception from, but rather use ``help(obj)`` and access
    the exception class from the instance directly.

    **Example**:

    .. code-block:: python

        class Empty(Exception):
            pass

        class Queue:
            Empty = Empty

            def get(self):
                """Get the next item from the queue.

                :raises Queue.Empty: if there are no more items left.

                """
                try:
                    return self.queue.popleft()
                except IndexError:
                    raise self.Empty()

复合类
~~~~~~~~~~

Composites

.. tab:: 中文

    与异常类似，组合类也应该支持通过继承和/或实例化进行覆盖。
    在选择要包含哪些类时可以根据常识进行判断，但通常宁可包含多一点：
    预测用户将要覆盖的内容是困难的（我们因此避免了许多猴子补丁）。

    **示例**：

    .. code-block:: python

        class Worker:
            Consumer = Consumer

            def __init__(self, connection, consumer_cls=None):
                self.Consumer = consumer_cls or self.Consumer

            def do_work(self):
                with self.Consumer(self.connection) as consumer:
                    self.connection.drain_events()

.. tab:: 英文

    Similarly to exceptions, composite classes should be override-able by
    inheritance and/or instantiation. Common sense can be used when
    selecting what classes to include, but often it's better to add one
    too many: predicting what users need to override is hard (this has
    saved us from many a monkey patch).

    **Example**:

    .. code-block:: python

        class Worker:
            Consumer = Consumer

            def __init__(self, connection, consumer_cls=None):
                self.Consumer = consumer_cls or self.Consumer

            def do_work(self):
                with self.Consumer(self.connection) as consumer:
                    self.connection.drain_events()

应用程序 vs. “单一模式”
==============================

Applications vs. "single mode"

.. tab:: 中文

    Celery 起初是为 Django 开发的，仅仅是因为这样可以快速启动项目，
    同时也能接触到一个潜在的庞大用户群体。

    在 Django 中有一个全局的设置对象，因此多个 Django 项目无法在
    同一个进程空间中共存，这在后期对将 Celery 与无此限制的框架结合使用时
    造成了问题。

    因此引入了 app 的概念。当使用 app 时，你会使用 'celery' 对象，
    而不是从 Celery 的子模块中直接导入内容，这也（不幸地）意味着
    Celery 实际上存在两套 API。

    以下是使用单实例模式的 Celery 示例：

    .. code-block:: python

        from celery import task
        from celery.task.control import inspect

        from .models import CeleryStats

        @task
        def write_stats_to_db():
            stats = inspect().stats(timeout=1)
            for node_name, reply in stats:
                CeleryStats.objects.update_stat(node_name, stats)

    以下是使用 Celery app 对象的同一示例：

    .. code-block:: python

        from .celery import celery
        from .models import CeleryStats

        @app.task
        def write_stats_to_db():
            stats = celery.control.inspect().stats(timeout=1)
            for node_name, reply in stats:
                CeleryStats.objects.update_stat(node_name, stats)

    在上面的示例中，实际的应用实例是从项目中的一个模块中导入的，
    这个模块可能如下所示：

    .. code-block:: python

        from celery import Celery

        app = Celery(broker='amqp://')

.. tab:: 英文

    In the beginning Celery was developed for Django, simply because
    this enabled us get the project started quickly, while also having
    a large potential user base.

    In Django there's a global settings object, so multiple Django projects
    can't co-exist in the same process space, this later posed a problem
    for using Celery with frameworks that don't have this limitation.

    Therefore the app concept was introduced. When using apps you use 'celery'
    objects instead of importing things from Celery sub-modules, this
    (unfortunately) also means that Celery essentially has two API's.

    Here's an example using Celery in single-mode:

    .. code-block:: python

        from celery import task
        from celery.task.control import inspect

        from .models import CeleryStats

        @task
        def write_stats_to_db():
            stats = inspect().stats(timeout=1)
            for node_name, reply in stats:
                CeleryStats.objects.update_stat(node_name, stats)


    and here's the same using Celery app objects:

    .. code-block:: python

        from .celery import celery
        from .models import CeleryStats

        @app.task
        def write_stats_to_db():
            stats = celery.control.inspect().stats(timeout=1)
            for node_name, reply in stats:
                CeleryStats.objects.update_stat(node_name, stats)


    In the example above the actual application instance is imported
    from a module in the project, this module could look something like this:

    .. code-block:: python

        from celery import Celery

        app = Celery(broker='amqp://')


模块概述
===============

Module Overview

.. tab:: 中文

    - celery.app  
        这是 Celery 的核心：所有功能的入口点。

    - celery.loaders  
        每个应用都必须有一个 loader。Loader 决定了如何读取配置；
        Worker 启动时发生什么；任务开始与结束时发生什么；
        等等。

        包含的 loader 有：

        - app
            自定义的 Celery 应用实例默认使用此 loader。

        - default
            “单实例模式”（single-mode）默认使用此 loader。

        也存在扩展的 loader，例如 :pypi:`celery-pylons`。

    - celery.worker  
        这是 Worker 的具体实现。

    - celery.backends  
        任务结果的后端实现位于此模块中。

    - celery.apps  
        主要的用户应用：worker 与 beat。  
        它们的命令行包装器位于 celery.bin 中（见下）。

    - celery.bin  
        命令行应用。  
        :file:`setup.py` 会为这些应用创建 setuptools 的 entry-point。

    - celery.concurrency  
        执行池实现（prefork、eventlet、gevent、solo、thread）。

    - celery.db  
        用于 SQLAlchemy 结果后端的数据库模型。  
        （应当迁移到 :mod:`celery.backends.database` 中）

    - celery.events  
        用于发送与消费监控事件，还包含 curses 监控器、事件转储器、
        以及与内存中集群状态协同使用的工具。

    - celery.execute.trace  
        描述 Worker 如何执行与追踪任务，以及 eager 模式下的行为。

    - celery.security  
        与安全相关的功能，目前包括一个使用加密摘要的序列化器。

    - celery.task  
        单实例模式下用于创建任务和控制 worker 的接口。

    - t.unit（内部发布）  
        单元测试套件。

    - celery.utils  
        Celery 代码库中使用的实用函数。  
        其中很多是为了跨 Python 版本的兼容性。

    - celery.contrib  
        其他不适合放入任何命名空间的公共附加代码。

.. tab:: 英文

    - celery.app
        This is the core of Celery: the entry-point for all functionality.

    - celery.loaders
        Every app must have a loader. The loader decides how configuration
        is read; what happens when the worker starts; when a task starts and ends;
        and so on.

        The loaders included are:

            - app

                Custom Celery app instances uses this loader by default.

            - default

                "single-mode" uses this loader by default.

        Extension loaders also exist, for example :pypi:`celery-pylons`.

    - celery.worker
        This is the worker implementation.

    - celery.backends
        Task result backends live here.

    - celery.apps
        Major user applications: worker and beat.
        The command-line wrappers for these are in celery.bin (see below)

    - celery.bin
        Command-line applications.
        :file:`setup.py` creates setuptools entry-points for these.

    - celery.concurrency
        Execution pool implementations (prefork, eventlet, gevent, solo, thread).

    - celery.db
        Database models for the SQLAlchemy database result backend.
        (should be moved into :mod:`celery.backends.database`)

    - celery.events
        Sending and consuming monitoring events, also includes curses monitor,
        event dumper and utilities to work with in-memory cluster state.

    - celery.execute.trace
        How tasks are executed and traced by the worker, and in eager mode.

    - celery.security
        Security related functionality, currently a serializer using
        cryptographic digests.

    - celery.task
        single-mode interface to creating tasks, and controlling workers.

    - t.unit (int distribution)
        The unit test suite.

    - celery.utils
        Utility functions used by the Celery code base.
        Much of it is there to be compatible across Python versions.

    - celery.contrib
        Additional public code that doesn't fit into any other name-space.

Worker 概述
===============

Worker overview

.. tab:: 中文

    * `celery.bin.worker:Worker`  
        这是 Worker 的命令行接口。

        主要职责：
            * 当设置了 :option:`--detach <celery worker --detach>` 时执行守护进程化
            * 当使用 :option:`--uid <celery worker --uid>` /
                :option:`--gid <celery worker --gid>` 参数时降权运行
            * 安装“并发补丁”（eventlet/gevent 的 monkey patch）

        ``app.worker_main(argv)`` 实际调用：

        ``instantiate('celery.bin.worker:Worker')(app).execute_from_commandline(argv)``

    * `app.Worker` -> `celery.apps.worker:Worker`  
        主要职责：
        
        * 设置日志记录并重定向标准输出
        * 安装信号处理器（支持 `TERM` / `HUP` / `STOP` / `USR1` (cry)/ `USR2` （rdb））
        * 打印横幅与警告（如 pickle 警告）
        * 处理 :option:`celery worker --purge` 参数

    * `app.WorkController` -> `celery.worker.WorkController`  
        这是实际的 Worker，实现基于 bootstep 模型构建。


.. tab:: 英文

    * `celery.bin.worker:Worker`
        This is the command-line interface to the worker.

        Responsibilities:
            
            * Daemonization when :option:`--detach <celery worker --detach>` set,
            * dropping privileges when using :option:`--uid <celery worker --uid>`/
                :option:`--gid <celery worker --gid>` arguments
            * Installs "concurrency patches" (eventlet/gevent monkey patches).

        ``app.worker_main(argv)`` calls
        ``instantiate('celery.bin.worker:Worker')(app).execute_from_commandline(argv)``

    * `app.Worker` -> `celery.apps.worker:Worker`
        Responsibilities:
        * sets up logging and redirects standard outs
        * installs signal handlers (`TERM`/`HUP`/`STOP`/`USR1` (cry)/`USR2` (rdb))
        * prints banner and warnings (e.g., pickle warning)
        * handles the :option:`celery worker --purge` argument

    * `app.WorkController` -> `celery.worker.WorkController`
        This is the real worker, built up around bootsteps.
