.. _testing:

================================================================
使用 Celery 进行测试
================================================================

Testing with Celery

.. tab:: 中文

    使用 Celery 进行测试分为两部分：

    * 单元测试与集成测试：使用 ``celery.contrib.pytest``。
    * 烟雾测试 / 生产环境测试：使用 :pypi:`pytest-celery <pytest-celery>` >= 1.0.0

    安装 pytest-celery 插件时，还会同时安装 ``celery.contrib.pytest`` 基础设施，
    以及 pytest 插件基础设施。它们的区别在于使用方式。

    .. warning::

        两个 API 之间是不兼容的。pytest-celery 插件基于 Docker，
        而 ``celery.contrib.pytest`` 则基于 mock。

    要使用 ``celery.contrib.pytest`` 基础设施，请按照以下说明进行操作。

    pytest-celery 插件有其 `独立文档 <https://pytest-celery.readthedocs.io/>`_。

.. tab:: 英文

    Testing with Celery is divided into two parts:

    * Unit & Integration: Using ``celery.contrib.pytest``.
    * Smoke / Production: Using :pypi:`pytest-celery <pytest-celery>` >= 1.0.0

    Installing the pytest-celery plugin will install the ``celery.contrib.pytest`` infrastructure as well,
    alongside the pytest plugin infrastructure. The difference is how you use it.

    .. warning::

        Both APIs are NOT compatible with each other. The pytest-celery plugin is Docker based
        and the ``celery.contrib.pytest`` is mock based.

    To use the ``celery.contrib.pytest`` infrastructure, follow the instructions below.

    The pytest-celery plugin has its `own documentation <https://pytest-celery.readthedocs.io/>`_.

任务和单元测试
====================

Tasks and unit tests

.. tab:: 中文

    在单元测试中测试任务行为时，推荐的方法是使用 mock。

    .. admonition:: 急切模式

        :setting:`task_always_eager` 设置启用的急切模式
        定义上并不适合单元测试。

        使用急切模式测试时，实际上你仅仅是在测试一个
        仿真环境与工作进程之间的差异，而仿真与实际工作中
        所发生的行为之间存在许多不一致。

        注意，急切执行的任务默认不会将结果写入后端。
        如果你想启用此功能，可以查看 :setting:`task_store_eager_result`。

    Celery 任务很像 Web 视图，它应该只定义如何在作为任务调用时执行操作。

    这意味着，理想情况下，任务只处理诸如序列化、消息头、
    重试等事项，实际的逻辑应在其他地方实现。

    假设我们有一个任务如下：

    .. code-block:: python

        from .models import Product


        @app.task(bind=True)
        def send_order(self, product_pk, quantity, price):
            price = Decimal(price)  # json 序列化为字符串。

            # 模型通过 ID 传递，而非序列化。
            product = Product.objects.get(product_pk)

            try:
                product.order(quantity, price)
            except OperationalError as exc:
                raise self.retry(exc=exc)


    ``Note``: 任务被 `绑定 <https://docs.celeryq.dev/en/latest/userguide/tasks.html#bound-tasks>`_ 意味着任务的第一个
    参数将始终是任务实例（self）。这意味着你会得到一个 self 参数作为
    第一个参数，可以使用 Task 类的方法和属性。

    你可以为此任务编写单元测试，使用像下面这样的 mock：

    .. code-block:: python

        from pytest import raises

        from celery.exceptions import Retry

        # 对于 Python 2：使用 mock.patch 从 `pip install mock`。
        from unittest.mock import patch

        from proj.models import Product
        from proj.tasks import send_order

        class test_send_order:

            @patch('proj.tasks.Product.order')  # < 在上面模块中对 Product 进行 patch
            def test_success(self, product_order):
                product = Product.objects.create(
                    name='Foo',
                )
                send_order(product.pk, 3, Decimal(30.3))
                product_order.assert_called_with(3, Decimal(30.3))

            @patch('proj.tasks.Product.order')
            @patch('proj.tasks.send_order.retry')
            def test_failure(self, send_order_retry, product_order):
                product = Product.objects.create(
                    name='Foo',
                )

                # 设置 patch 方法的副作用
                # 使它们抛出我们需要的错误。
                send_order_retry.side_effect = Retry()
                product_order.side_effect = OperationalError()

                with raises(Retry):
                    send_order(product.pk, 3, Decimal(30.6))


.. tab:: 英文

    To test task behavior in unit tests the preferred method is mocking.

    .. admonition:: Eager mode

        The eager mode enabled by the :setting:`task_always_eager` setting
        is by definition not suitable for unit tests.

        When testing with eager mode you are only testing an emulation
        of what happens in a worker, and there are many discrepancies
        between the emulation and what happens in reality.

        Note that eagerly executed tasks don't write results to backend by default.
        If you want to enable this functionality, have a look at :setting:`task_store_eager_result`.

    A Celery task is much like a web view, in that it should only
    define how to perform the action in the context of being called as a task.

    This means optimally tasks only handle things like serialization, message headers,
    retries, and so on, with the actual logic implemented elsewhere.

    Say we had a task like this:

    .. code-block:: python

        from .models import Product


        @app.task(bind=True)
        def send_order(self, product_pk, quantity, price):
            price = Decimal(price)  # json serializes this to string.

            # models are passed by id, not serialized.
            product = Product.objects.get(product_pk)

            try:
                product.order(quantity, price)
            except OperationalError as exc:
                raise self.retry(exc=exc)


    ``Note``: A task being `bound <https://docs.celeryq.dev/en/latest/userguide/tasks.html#bound-tasks>`_ means the first
    argument to the task will always be the task instance (self). which means you do get a self argument as the
    first argument and can use the Task class methods and attributes.

    You could write unit tests for this task, using mocking like
    in this example:

    .. code-block:: python

        from pytest import raises

        from celery.exceptions import Retry

        # for python 2: use mock.patch from `pip install mock`.
        from unittest.mock import patch

        from proj.models import Product
        from proj.tasks import send_order

        class test_send_order:

            @patch('proj.tasks.Product.order')  # < patching Product in module above
            def test_success(self, product_order):
                product = Product.objects.create(
                    name='Foo',
                )
                send_order(product.pk, 3, Decimal(30.3))
                product_order.assert_called_with(3, Decimal(30.3))

            @patch('proj.tasks.Product.order')
            @patch('proj.tasks.send_order.retry')
            def test_failure(self, send_order_retry, product_order):
                product = Product.objects.create(
                    name='Foo',
                )

                # Set a side effect on the patched methods
                # so that they raise the errors we want.
                send_order_retry.side_effect = Retry()
                product_order.side_effect = OperationalError()

                with raises(Retry):
                    send_order(product.pk, 3, Decimal(30.6))

.. _pytest_plugin:

pytest
======

.. versionadded:: 4.0

.. tab:: 中文

    Celery 还提供了一个 :pypi:`pytest` 插件，添加了一些 fixture，可以
    在集成测试（或单元测试）中使用。

.. tab:: 英文

    Celery also makes a :pypi:`pytest` plugin available that adds fixtures that you can
    use in your integration (or unit) test suites.

启用
--------

Enabling

.. tab:: 中文

    Celery 默认将插件以禁用状态发布，要启用它，你可以选择以下任意方法：

    * ``pip install celery[pytest]``
    * ``pip install pytest-celery``
    * 或者添加环境变量 ``PYTEST_PLUGINS=celery.contrib.pytest``
    * 或者在根目录的 conftest.py 中添加 ``pytest_plugins = ("celery.contrib.pytest", )``

.. tab:: 英文

    Celery initially ships the plugin in a disabled state, to enable it you can either:

    * ``pip install celery[pytest]``
    * ``pip install pytest-celery``
    * or add an environment variable ``PYTEST_PLUGINS=celery.contrib.pytest``
    * or add ``pytest_plugins = ("celery.contrib.pytest", )`` to your root conftest.py


标记
-----

Marks

``celery`` - 设置测试应用配置。
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``celery`` - Set test app configuration.

.. tab:: 中文

    ``celery`` 标记使你能够覆盖单个测试用例使用的配置：

    .. code-block:: python

        @pytest.mark.celery(result_backend='redis://')
        def test_something():
            ...


    或者为类中的所有测试用例配置：

    .. code-block:: python

        @pytest.mark.celery(result_backend='redis://')
        class test_something:

            def test_one(self):
                ...

            def test_two(self):
                ...

.. tab:: 英文

    The ``celery`` mark enables you to override the configuration
    used for a single test case:

    .. code-block:: python

        @pytest.mark.celery(result_backend='redis://')
        def test_something():
            ...


    or for all the test cases in a class:

    .. code-block:: python

        @pytest.mark.celery(result_backend='redis://')
        class test_something:

            def test_one(self):
                ...

            def test_two(self):
                ...

Fixtures
--------

Fixtures

函数作用域
^^^^^^^^^^^^^^

Function scope

``celery_app`` - 用于测试的 Celery 应用。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_app`` - Celery app used for testing.

.. tab:: 中文

    这个 fixture 返回一个 Celery 应用，你可以在测试中使用它。

    示例：

    .. code-block:: python

        def test_create_task(celery_app, celery_worker):
            @celery_app.task
            def mul(x, y):
                return x * y
            
            celery_worker.reload()
            assert mul.delay(4, 4).get(timeout=10) == 16

.. tab:: 英文

    This fixture returns a Celery app you can use for testing.

    Example:

    .. code-block:: python

        def test_create_task(celery_app, celery_worker):
            @celery_app.task
            def mul(x, y):
                return x * y
            
            celery_worker.reload()
            assert mul.delay(4, 4).get(timeout=10) == 16

``celery_worker`` - 嵌入实时工作线程。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_worker`` - Embed live worker.

.. tab:: 中文

    这个 fixture 启动一个 Celery 工作进程实例，你可以在集成测试中使用它。
    工作进程将在 *独立线程* 中启动，并在测试返回后关闭。

    默认情况下，fixture 会等待最多 10 秒钟，直到工作进程完成
    所有待处理任务，如果超时则会抛出异常。
    超时时间可以通过设置 :func:`celery_worker_parameters` fixture 返回的字典中的
    ``shutdown_timeout`` 键来定制。

    示例：

    .. code-block:: python

        # 在你的 conftest.py 中添加
        @pytest.fixture(scope='session')
        def celery_config():
            return {
                'broker_url': 'amqp://',
                'result_backend': 'redis://'
            }

        def test_add(celery_worker):
            mytask.delay()


        # 如果你只想在某个测试用例中覆盖某些设置
        # - 可以使用 ``celery`` 标记：
        @pytest.mark.celery(result_backend='rpc')
        def test_other(celery_worker):
            ...

    默认情况下，心跳被禁用，这意味着测试工作进程不会
    发送 ``worker-online``、``worker-offline`` 和 ``worker-heartbeat`` 事件。
    要启用心跳，可以修改 :func:`celery_worker_parameters` fixture：

    .. code-block:: python

        # 在你的 conftest.py 中添加
        @pytest.fixture(scope="session")
        def celery_worker_parameters():
            return {"without_heartbeat": False}
            ...


.. tab:: 英文

    This fixture starts a Celery worker instance that you can use
    for integration tests.  The worker will be started in a *separate thread*
    and will be shutdown as soon as the test returns.

    By default the fixture will wait up to 10 seconds for the worker to complete
    outstanding tasks and will raise an exception if the time limit is exceeded.
    The timeout can be customized by setting the ``shutdown_timeout`` key in the
    dictionary returned by the :func:`celery_worker_parameters` fixture.

    Example:

    .. code-block:: python

        # Put this in your conftest.py
        @pytest.fixture(scope='session')
        def celery_config():
            return {
                'broker_url': 'amqp://',
                'result_backend': 'redis://'
            }

        def test_add(celery_worker):
            mytask.delay()


        # If you wish to override some setting in one test cases
        # only - you can use the ``celery`` mark:
        @pytest.mark.celery(result_backend='rpc')
        def test_other(celery_worker):
            ...

    Heartbeats are disabled by default which means that the test worker doesn't
    send events for ``worker-online``, ``worker-offline`` and ``worker-heartbeat``.
    To enable heartbeats modify the :func:`celery_worker_parameters` fixture:

    .. code-block:: python

        # Put this in your conftest.py
        @pytest.fixture(scope="session")
        def celery_worker_parameters():
            return {"without_heartbeat": False}
            ...



会话作用域
^^^^^^^^^^^^^

Session scope

``celery_config`` - 覆盖该函数以设置 Celery 测试应用配置。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_config`` - Override to setup Celery test app configuration.

.. tab:: 中文

    你可以重新定义这个 fixture 来配置测试用的 Celery 应用。

    由你的 fixture 返回的配置将用于配置 :func:`celery_app` 和 :func:`celery_session_app` fixtures。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_config():
            return {
                'broker_url': 'amqp://',
                'result_backend': 'rpc',
            }

.. tab:: 英文

    You can redefine this fixture to configure the test Celery app.

    The config returned by your fixture will then be used
    to configure the :func:`celery_app`, and :func:`celery_session_app` fixtures.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_config():
            return {
                'broker_url': 'amqp://',
                'result_backend': 'rpc',
            }


``celery_parameters`` - 覆盖该函数以设置 Celery 测试应用参数。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_parameters`` - Override to setup Celery test app parameters.

.. tab:: 中文

    你可以重新定义这个 fixture 来改变测试 Celery 应用的 ``__init__`` 参数。
    与 :func:`celery_config` 不同，这些参数在实例化 :class:`~celery.Celery` 时直接传递。

    由你的 fixture 返回的配置将用于配置 :func:`celery_app` 和 :func:`celery_session_app` fixtures。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_parameters():
            return {
                'task_cls':  my.package.MyCustomTaskClass,
                'strict_typing': False,
            }

.. tab:: 英文

    You can redefine this fixture to change the ``__init__`` parameters of test
    Celery app. In contrast to :func:`celery_config`, these are directly passed to
    when instantiating :class:`~celery.Celery`.

    The config returned by your fixture will then be used
    to configure the :func:`celery_app`, and :func:`celery_session_app` fixtures.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_parameters():
            return {
                'task_cls':  my.package.MyCustomTaskClass,
                'strict_typing': False,
            }

``celery_worker_parameters`` - 覆盖该函数以设置 Celery 工作线程参数。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_worker_parameters`` - Override to setup Celery worker parameters.

.. tab:: 中文

    你可以重新定义这个 fixture 来改变测试 Celery 工作进程的 ``__init__`` 参数。这些参数在实例化 :class:`~celery.worker.WorkController` 时直接传递。

    由你的 fixture 返回的配置将用于配置 :func:`celery_worker` 和 :func:`celery_session_worker` fixtures。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_worker_parameters():
            return {
                'queues':  ('high-prio', 'low-prio'),
                'exclude_queues': ('celery'),
            }

.. tab:: 英文

    You can redefine this fixture to change the ``__init__`` parameters of test
    Celery workers. These are directly passed to
    :class:`~celery.worker.WorkController` when it is instantiated.

    The config returned by your fixture will then be used
    to configure the :func:`celery_worker`, and :func:`celery_session_worker`
    fixtures.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_worker_parameters():
            return {
                'queues':  ('high-prio', 'low-prio'),
                'exclude_queues': ('celery'),
            }


``celery_enable_logging`` - 覆盖该函数以启用嵌入式工作线程的日志记录。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_enable_logging`` - Override to enable logging in embedded workers.

.. tab:: 中文

    这是一个你可以重写的 fixture，用来启用嵌入式工作进程的日志记录。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_enable_logging():
            return True

.. tab:: 英文

    This is a fixture you can override to enable logging in embedded workers.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_enable_logging():
            return True

``celery_includes`` - 为嵌入式工作线程添加额外的导入。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_includes`` - Add additional imports for embedded workers.

.. tab:: 中文

    你可以重写这个 fixture 来在嵌入式工作进程启动时包含模块。

    你可以让它返回一个模块名称的列表进行导入，
    这些模块可以是任务模块、注册信号的模块等。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_includes():
            return [
                'proj.tests.tasks',
                'proj.tests.celery_signal_handlers',
            ]

.. tab:: 英文

    You can override fixture to include modules when an embedded worker starts.

    You can have this return a list of module names to import,
    which can be task modules, modules registering signals, and so on.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_includes():
            return [
                'proj.tests.tasks',
                'proj.tests.celery_signal_handlers',
            ]

``celery_worker_pool`` - 覆盖用于嵌入式工作线程的池。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_worker_pool`` - Override the pool used for embedded workers.

.. tab:: 中文

    你可以重写这个 fixture 来配置嵌入式工作进程使用的执行池。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_worker_pool():
            return 'prefork'

    .. warning::

        你不能使用 gevent/eventlet 池，除非你的整个测试套件在启用猴子补丁的情况下运行。

.. tab:: 英文

    You can override fixture to configure the execution pool used for embedded
    workers.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def celery_worker_pool():
            return 'prefork'

    .. warning::

        You cannot use the gevent/eventlet pools, that is unless your whole test
        suite is running with the monkeypatches enabled.

``celery_session_worker`` - 在整个会话期间都处于活动状态的嵌入式工作线程。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_session_worker`` - Embedded worker that lives throughout the session.

.. tab:: 中文

    这个 fixture 启动一个在整个测试会话期间存在的工作进程
    （它不会为每个测试启动/停止）。

    示例：

    .. code-block:: python

        # 将此添加到你的 conftest.py 中
        @pytest.fixture(scope='session')
        def celery_config():
            return {
                'broker_url': 'amqp://',
                'result_backend': 'rpc',
            }

        # 在你的测试中这样做。
        def test_add_task(celery_session_worker):
            assert add.delay(2, 2).get() == 4

    .. warning::

        混合使用会话和临时工作进程可能不是一个好主意...

.. tab:: 英文

    This fixture starts a worker that lives throughout the testing session
    (it won't be started/stopped for every test).

    Example:

    .. code-block:: python

        # Add this to your conftest.py
        @pytest.fixture(scope='session')
        def celery_config():
            return {
                'broker_url': 'amqp://',
                'result_backend': 'rpc',
            }

        # Do this in your tests.
        def test_add_task(celery_session_worker):
            assert add.delay(2, 2).get() == 4

    .. warning::

        It's probably a bad idea to mix session and ephemeral workers...

``celery_session_app`` - 用于测试的 Celery 应用（会话范围）。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``celery_session_app`` - Celery app used for testing (session scope).

.. tab:: 中文

    当其他以 session 为作用域的 fixture 需要引用 Celery 应用实例时，可以使用此 fixture。

.. tab:: 英文

    This can be used by other session scoped fixtures when they need to refer
    to a Celery app instance.

``use_celery_app_trap`` - 回退到默认应用时引发异常。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``use_celery_app_trap`` - Raise exception on falling back to default app.

.. tab:: 中文

    你可以在 ``conftest.py`` 中重写这个 fixture，以启用 “app trap” 机制：
    如果某些代码尝试访问默认应用（default_app）或当前应用（current_app），则会抛出异常。

    示例：

    .. code-block:: python

        @pytest.fixture(scope='session')
        def use_celery_app_trap():
            return True


    如果某个测试确实需要访问默认应用，你必须通过 ``depends_on_current_app`` fixture 来标记它：

    .. code-block:: python

        @pytest.mark.usefixtures('depends_on_current_app')
        def test_something():
            something()

.. tab:: 英文

    This is a fixture you can override in your ``conftest.py``, to enable the "app trap":
    if something tries to access the default or current_app, an exception
    is raised.

    Example:

    .. code-block:: python

        @pytest.fixture(scope='session')
        def use_celery_app_trap():
            return True

    If a test wants to access the default app, you would have to mark it using
    the ``depends_on_current_app`` fixture:

    .. code-block:: python

        @pytest.mark.usefixtures('depends_on_current_app')
        def test_something():
            something()
