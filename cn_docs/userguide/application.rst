.. _guide-app:

=============
应用程序
=============

Application

.. tab:: 中文

    在使用 Celery 库之前，必须先实例化它，这个实例被称为应用（或简称 *app*）。

    该应用是线程安全的，因此多个具有不同配置、组件和任务的 Celery 应用可以共存于同一个进程空间中。

    现在我们来创建一个：

    .. code-block:: pycon

        >>> from celery import Celery
        >>> app = Celery()
        >>> app
        <Celery __main__:0x100469fd0>

    最后一行展示了该应用的文本表示形式：包括应用类的名称（ ``Celery`` ）、当前主模块的名称（ ``__main__`` ）以及对象的内存地址（ ``0x100469fd0`` ）。

.. tab:: 英文

    The Celery library must be instantiated before use, this instance
    is called an application (or *app* for short).

    The application is thread-safe so that multiple Celery applications
    with different configurations, components, and tasks can co-exist in the
    same process space.

    Let's create one now:

    .. code-block:: pycon

        >>> from celery import Celery
        >>> app = Celery()
        >>> app
        <Celery __main__:0x100469fd0>

    The last line shows the textual representation of the application:
    including the name of the app class (``Celery``), the name of the
    current main module (``__main__``), and the memory address of the object
    (``0x100469fd0``).

主名称
=========

Main Name

.. tab:: 中文

    这三者中，只有一个是重要的，那就是主模块名称。我们来看一下原因。
    
    当你在 Celery 中发送一个任务消息时，该消息不会包含任何源代码，只包含你想执行的任务名称。这类似于互联网中的主机名工作原理：每个 worker 维护着一个任务名称与其实际函数的映射，称为 *任务注册表* （task registry）。
    
    每当你定义一个任务时，该任务也会被添加到本地注册表中：
    
    .. code-block:: pycon
    
        >>> @app.task
        ... def add(x, y):
        ...     return x + y
    
        >>> add
        <@task: __main__.add>
    
        >>> add.name
        __main__.add
    
        >>> app.tasks['__main__.add']
        <@task: __main__.add>
    
    你再次看到 ``__main__``；当 Celery 无法检测函数所属模块时，它会使用主模块名来生成任务名称的开头部分。
    
    这种情况只在一小部分使用场景中才会造成问题：
    
    #. 如果定义任务的模块作为程序运行；
    #. 如果在 Python 解释器（REPL）中创建应用；
    
    比如下面这个例子，其中 `tasks` 模块也用于通过 :meth:`@worker_main` 启动一个 worker：
    
    :file:`tasks.py`:
    
    .. code-block:: python
    
        from celery import Celery
        app = Celery()
    
        @app.task
        def add(x, y): return x + y
    
        if __name__ == '__main__':
            args = ['worker', '--loglevel=INFO']
            app.worker_main(argv=args)
    
    当该模块被执行时，任务的名称将以 "``__main__``" 开头，但当该模块被另一个进程导入（例如为了调用一个任务）时，任务名称将以 "``tasks``" 开头（也就是模块的实际名称）：
    
    .. code-block:: pycon
    
        >>> from tasks import add
        >>> add.name
        tasks.add
    
    你也可以为主模块指定一个其他名称：
    
    .. code-block:: pycon
    
        >>> app = Celery('tasks')
        >>> app.main
        'tasks'
    
        >>> @app.task
        ... def add(x, y):
        ...     return x + y
    
        >>> add.name
        tasks.add
    
    .. seealso:: :ref:`task-names`

.. tab:: 英文

    Only one of these is important, and that's the main module name.
    Let's look at why that is.
    
    When you send a task message in Celery, that message won't contain
    any source code, but only the name of the task you want to execute.
    This works similarly to how host names work on the internet: every worker
    maintains a mapping of task names to their actual functions, called the *task
    registry*.
    
    Whenever you define a task, that task will also be added to the local registry:
    
    .. code-block:: pycon
    
        >>> @app.task
        ... def add(x, y):
        ...     return x + y
    
        >>> add
        <@task: __main__.add>
    
        >>> add.name
        __main__.add
    
        >>> app.tasks['__main__.add']
        <@task: __main__.add>
    
    and there you see that ``__main__`` again; whenever Celery isn't able
    to detect what module the function belongs to, it uses the main module
    name to generate the beginning of the task name.
    
    This is only a problem in a limited set of use cases:
    
    #. If the module that the task is defined in is run as a program.
    #. If the application is created in the Python shell (REPL).
    
    For example here, where the tasks module is also used to start a worker
    with :meth:`@worker_main`:
    
    :file:`tasks.py`:
    
    .. code-block:: python
    
        from celery import Celery
        app = Celery()
    
        @app.task
        def add(x, y): return x + y
    
        if __name__ == '__main__':
            args = ['worker', '--loglevel=INFO']
            app.worker_main(argv=args)
    
    When this module is executed the tasks will be named starting with "``__main__``",
    but when the module is imported by another process, say to call a task,
    the tasks will be named starting with "``tasks``" (the real name of the module):
    
    .. code-block:: pycon
    
        >>> from tasks import add
        >>> add.name
        tasks.add
    
    You can specify another name for the main module:
    
    .. code-block:: pycon
    
        >>> app = Celery('tasks')
        >>> app.main
        'tasks'
    
        >>> @app.task
        ... def add(x, y):
        ...     return x + y
    
        >>> add.name
        tasks.add
    
    .. seealso:: :ref:`task-names`

配置
=============

Configuration

.. tab:: 中文

    Celery 提供了若干配置选项来调整其行为。这些选项可以直接设置在应用实例上，或通过一个专门的配置模块进行设置。
    
    配置对象可通过 :attr:`@conf` 访问：
    
    .. code-block:: pycon
    
        >>> app.conf.timezone
        'Europe/London'
    
    你也可以直接设置配置值：
    
    .. code-block:: pycon
    
        >>> app.conf.enable_utc = True
    
    或者使用 ``update`` 方法一次更新多个配置项：
    
    .. code-block:: python
    
        >>> app.conf.update(
        ...     enable_utc=True,
        ...     timezone='Europe/London',
        ...)
    
    配置对象由多个字典组成，按以下优先顺序查找：

    #. 运行时所做的更改；
    #. 配置模块（如果有）；
    #. 默认配置（:mod:`celery.app.defaults`）。
    
    你甚至可以使用 :meth:`@add_defaults` 方法添加新的默认配置来源。
    
    .. seealso::
    
        请参阅 :ref:`Configuration reference <configuration>` 获取所有可用配置项及其默认值的完整列表。


.. tab:: 英文

    There are several options you can set that'll change how
    Celery works. These options can be set directly on the app instance,
    or you can use a dedicated configuration module.
    
    The configuration is available as :attr:`@conf`:
    
    .. code-block:: pycon
    
        >>> app.conf.timezone
        'Europe/London'
    
    where you can also set configuration values directly:
    
    .. code-block:: pycon
    
        >>> app.conf.enable_utc = True
    
    or update several keys at once by using the ``update`` method:
    
    .. code-block:: python
    
        >>> app.conf.update(
        ...     enable_utc=True,
        ...     timezone='Europe/London',
        ...)
    
    The configuration object consists of multiple dictionaries
    that are consulted in order:
    
        #. Changes made at run-time.
        #. The configuration module (if any)
        #. The default configuration (:mod:`celery.app.defaults`).
    
    You can even add new default sources by using the :meth:`@add_defaults`
    method.
    
    .. seealso::
    
        Go to the :ref:`Configuration reference <configuration>` for a complete
        listing of all the available settings, and their default values.
    
``config_from_object``
----------------------

``config_from_object``

.. tab:: 中文

    :meth:`@config_from_object` 方法用于从配置对象中加载配置。

    该对象可以是一个配置模块，也可以是任意具有配置属性的对象。

    请注意，当调用 :meth:`~@config_from_object` 方法时，之前设置的所有配置将会被重置。如果你还想设置其他配置项，应在调用之后再进行设置。

.. tab:: 英文

    The :meth:`@config_from_object` method loads configuration
    from a configuration object.

    This can be a configuration module, or any object with configuration attributes.

    Note that any configuration that was previously set will be reset when
    :meth:`~@config_from_object` is called. If you want to set additional
    configuration you should do so after.

示例 1：使用模块名称
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example 1: Using the name of a module

.. tab:: 中文

    :meth:`@config_from_object` 方法可以接受一个 Python 模块的全限定名称，甚至可以是某个 Python 属性的名称，例如： ``"celeryconfig"`` 、 ``"myproj.config.celery"`` ，或 ``"myproj.config:CeleryConfig"`` ：

    .. code-block:: python

        from celery import Celery

        app = Celery()
        app.config_from_object('celeryconfig')

    此时， ``celeryconfig`` 模块可以如下所示：

    :file:`celeryconfig.py`:

    .. code-block:: python

        enable_utc = True
        timezone = 'Europe/London'

    只要可以导入 ``celeryconfig``，应用就能够使用它。

.. tab:: 英文

    The :meth:`@config_from_object` method can take the fully qualified
    name of a Python module, or even the name of a Python attribute,
    for example: ``"celeryconfig"``, ``"myproj.config.celery"``, or
    ``"myproj.config:CeleryConfig"``:

    .. code-block:: python

        from celery import Celery

        app = Celery()
        app.config_from_object('celeryconfig')

    The ``celeryconfig`` module may then look like this:

    :file:`celeryconfig.py`:

    .. code-block:: python

        enable_utc = True
        timezone = 'Europe/London'

    and the app will be able to use it as long as ``import celeryconfig`` is
    possible.

示例 2：传递实际模块对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example 2: Passing an actual module object

.. tab:: 中文

    你也可以传入一个已经导入的模块对象，但通常不推荐这样做。

    .. tip::

        建议使用模块名称的方式，因为这意味着在使用 prefork 进程池时不需要对模块进行序列化。如果你遇到了配置问题或 pickle 错误，请尝试改用模块名称。

    .. code-block:: python

        import celeryconfig

        from celery import Celery

        app = Celery()
        app.config_from_object(celeryconfig)


.. tab:: 英文

    You can also pass an already imported module object, but this
    isn't always recommended.

    .. tip::

        Using the name of a module is recommended as this means the module does
        not need to be serialized when the prefork pool is used. If you're
        experiencing configuration problems or pickle errors then please
        try using the name of a module instead.

    .. code-block:: python

        import celeryconfig

        from celery import Celery

        app = Celery()
        app.config_from_object(celeryconfig)


示例 3：使用配置类/对象
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example 3:  Using a configuration class/object

.. tab:: 中文

    .. code-block:: python

        from celery import Celery

        app = Celery()

        class Config:
            enable_utc = True
            timezone = 'Europe/London'

        app.config_from_object(Config)
        # 或使用对象的完全限定名称：
        #   app.config_from_object('module:Config')

.. tab:: 英文

    .. code-block:: python

        from celery import Celery

        app = Celery()

        class Config:
            enable_utc = True
            timezone = 'Europe/London'

        app.config_from_object(Config)
        # or using the fully qualified name of the object:
        #   app.config_from_object('module:Config')

``config_from_envvar``
----------------------

``config_from_envvar``

.. tab:: 中文

    :meth:`@config_from_envvar` 方法通过读取环境变量来获取配置模块的名称。

    例如 —— 若要从环境变量 :envvar:`CELERY_CONFIG_MODULE` 指定的模块中加载配置：

    .. code-block:: python

        import os
        from celery import Celery

        #: 设置默认的配置模块名
        os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

        app = Celery()
        app.config_from_envvar('CELERY_CONFIG_MODULE')

    然后你可以通过环境变量指定要使用的配置模块：

    .. code-block:: console

        $ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l INFO

.. tab:: 英文

    The :meth:`@config_from_envvar` takes the configuration module name
    from an environment variable

    For example -- to load configuration from a module specified in the
    environment variable named :envvar:`CELERY_CONFIG_MODULE`:

    .. code-block:: python

        import os
        from celery import Celery

        #: Set default configuration module name
        os.environ.setdefault('CELERY_CONFIG_MODULE', 'celeryconfig')

        app = Celery()
        app.config_from_envvar('CELERY_CONFIG_MODULE')

    You can then specify the configuration module to use via the environment:

    .. code-block:: console

        $ CELERY_CONFIG_MODULE="celeryconfig.prod" celery worker -l INFO

.. _app-censored-config:

审查配置
----------------------

Censored configuration

.. tab:: 中文

    如果你希望打印出配置信息（例如用于调试），你可能还希望过滤掉敏感信息，比如密码或 API 密钥。

    Celery 提供了一些用于展示配置信息的实用工具，其中一个是 :meth:`~celery.app.utils.Settings.humanize`：

    .. code-block:: pycon

        >>> app.conf.humanize(with_defaults=False, censored=True)

    此方法将配置以表格字符串的形式返回。默认情况下它只包含变更项，但你可以通过启用 ``with_defaults`` 参数来包含内建的默认键值对。

    如果你希望以字典形式处理配置数据，可以使用 :meth:`~celery.app.utils.Settings.table` 方法：

    .. code-block:: pycon

        >>> app.conf.table(with_defaults=False, censored=True)

    请注意，Celery 无法完全过滤所有敏感信息，它仅通过正则表达式搜索常见的键名模式。如果你添加了自定义的包含敏感信息的配置项，请确保使用 Celery 能识别为机密的键名。

    若配置项名称包含以下子字符串之一，将被视为敏感并被遮蔽处理：
    
    ``API``, ``TOKEN``, ``KEY``, ``SECRET``, ``PASS``, ``SIGNATURE``, ``DATABASE``

.. tab:: 英文

    If you ever want to print out the configuration, as debugging information
    or similar, you may also want to filter out sensitive information like
    passwords and API keys.
    
    Celery comes with several utilities useful for presenting the configuration,
    one is :meth:`~celery.app.utils.Settings.humanize`:
    
    .. code-block:: pycon
    
        >>> app.conf.humanize(with_defaults=False, censored=True)
    
    This method returns the configuration as a tabulated string. This will
    only contain changes to the configuration by default, but you can include the
    built-in default keys and values by enabling the ``with_defaults`` argument.
    
    If you instead want to work with the configuration as a dictionary, you
    can use the :meth:`~celery.app.utils.Settings.table` method:
    
    .. code-block:: pycon
    
        >>> app.conf.table(with_defaults=False, censored=True)
    
    Please note that Celery won't be able to remove all sensitive information,
    as it merely uses a regular expression to search for commonly named keys.
    If you add custom settings containing sensitive information you should name
    the keys using a name that Celery identifies as secret.
    
    A configuration setting will be censored if the name contains any of
    these sub-strings:
    
    ``API``, ``TOKEN``, ``KEY``, ``SECRET``, ``PASS``, ``SIGNATURE``, ``DATABASE``

惰性
========

Laziness

.. tab:: 中文

    应用实例是惰性加载的，即只有在真正需要时才会进行初始化。
    
    创建一个 :class:`@Celery` 实例时只会执行以下操作：
    
    #. 创建逻辑时钟实例，用于事件系统。
    #. 创建任务注册表。
    #. 将自身设置为当前应用（除非禁用了 ``set_as_current`` 参数）。
    #. 调用 :meth:`@on_init` 回调（默认无操作）。
    
    :meth:`@task` 装饰器在任务被定义时不会立即创建任务，而是将任务的创建延迟到任务被使用，或应用被 *finalize* 之后。
    
    下面的示例展示了任务在实际使用前并未真正创建：
    
    .. code-block:: pycon
    
        >>> @app.task
        >>> def add(x, y):
        ...    return x + y
    
        >>> type(add)
        <class 'celery.local.PromiseProxy'>
    
        >>> add.__evaluated__()
        False
    
        >>> add        # <-- 导致调用 repr(add)
        <@task: __main__.add>
    
        >>> add.__evaluated__()
        True
    
    应用的 *finalization* 可以显式通过调用 :meth:`@finalize` 方法完成，或者隐式通过访问 :attr:`@tasks` 属性来触发。
    
    完成 finalization 会执行以下操作：
    
    #. 复制需要在多个应用间共享的任务。
    
       默认情况下任务是共享的，但如果在 task 装饰器中禁用了 ``shared`` 参数，那么该任务将仅绑定于其所归属的应用实例中。
    
    #. 执行所有待处理的任务装饰器。
    
    #. 确保所有任务都绑定到当前应用上。
    
       任务之所以需要绑定到应用，是为了从配置中读取默认值等信息。
    
    .. _default-app:
    
    .. topic:: “默认应用（default app）”
    
        Celery 并不总是支持应用实例机制，早期版本中只有基于模块的 API。
        在 Celery 5.0 之前，这种旧的兼容性 API 仍可使用，但已被移除。
    
        Celery 始终会创建一个特殊的应用 —— “默认应用（default app）”，
        若未实例化任何自定义应用，则使用该默认应用。
    
        现在 :mod:`celery.task` 模块已不可用。应使用应用实例上的方法，而非模块级 API：
    
        .. code-block:: python
    
            from celery.task import Task   # << 旧的 Task 基类。
    
            from celery import Task        # << 新的基类。


.. tab:: 英文

    The application instance is lazy, meaning it won't be evaluated
    until it's actually needed.
    
    Creating a :class:`@Celery` instance will only do the following:
    
    #. Create a logical clock instance, used for events.
    #. Create the task registry.
    #. Set itself as the current app (but not if the ``set_as_current`` argument was disabled)
    #. Call the :meth:`@on_init` callback (does nothing by default).
    
    The :meth:`@task` decorators don't create the tasks at the point when
    the task is defined, instead it'll defer the creation
    of the task to happen either when the task is used, or after the
    application has been *finalized*,
    
    This example shows how the task isn't created until
    you use the task, or access an attribute (in this case :meth:`repr`):
    
    .. code-block:: pycon
    
        >>> @app.task
        >>> def add(x, y):
        ...    return x + y
    
        >>> type(add)
        <class 'celery.local.PromiseProxy'>
    
        >>> add.__evaluated__()
        False
    
        >>> add        # <-- causes repr(add) to happen
        <@task: __main__.add>
    
        >>> add.__evaluated__()
        True
    
    *Finalization* of the app happens either explicitly by calling
    :meth:`@finalize` -- or implicitly by accessing the :attr:`@tasks`
    attribute.
    
    Finalizing the object will:
    
    #. Copy tasks that must be shared between apps
    
       Tasks are shared by default, but if the ``shared`` argument to the task decorator is disabled, then the task will be private to the app it's bound to.
    
    #. Evaluate all pending task decorators.
    
    #. Make sure all tasks are bound to the current app.
       
       Tasks are bound to an app so that they can read default values from the configuration.
    
    .. topic:: The "default app"
    
        Celery didn't always have applications, it used to be that
        there was only a module-based API. A compatibility API was
        available at the old location until the release of Celery 5.0,
        but has been removed.
    
        Celery always creates a special app - the "default app",
        and this is used if no custom application has been instantiated.
    
        The :mod:`celery.task` module is no longer available. Use the
        methods on the app instance, not the module based API:
    
        .. code-block:: python
    
            from celery.task import Task   # << OLD Task base class.
    
            from celery import Task        # << NEW base class.
    

打破链条
==================

Breaking the chain

.. tab:: 中文

    尽管依赖当前应用被设置是可行的，但最佳实践是始终将应用实例作为参数传递给需要它的地方。
    
    我将此称为 “应用链（app chain）” ，因为它会形成一个依赖于显式传递 app 的实例链。
    
    以下示例被认为是不良实践：
    
    .. code-block:: python
    
        from celery import current_app
    
        class Scheduler:
    
            def run(self):
                app = current_app
    
    正确的做法是将 ``app`` 作为参数传入：
    
    .. code-block:: python
    
        class Scheduler:
    
            def __init__(self, app):
                self.app = app
    
    Celery 内部使用 :func:`celery.app.app_or_default` 函数，以确保模块兼容性 API 中一切也能正常工作：
    
    .. code-block:: python
    
        from celery.app import app_or_default
    
        class Scheduler:
            def __init__(self, app=None):
                self.app = app_or_default(app)
    
    在开发过程中，你可以设置 :envvar:`CELERY_TRACE_APP` 环境变量，当“应用链”断裂时抛出异常：
    
    .. code-block:: console
    
        $ CELERY_TRACE_APP=1 celery worker -l INFO
    
    
    .. topic:: API 的演化
    
        自 2009 年 Celery 最初创建以来，其 API 已经发生了很大变化。
    
        例如，最初可以将任意可调用对象作为任务使用：
    
        .. code-block:: pycon
    
            def hello(to):
                return 'hello {0}'.format(to)
    
            >>> from celery.execute import apply_async
    
            >>> apply_async(hello, ('world!',))
    
        也可以通过创建 ``Task`` 类来设置特定选项，或重写某些行为：
    
        .. code-block:: python
    
            from celery import Task
            from celery.registry import tasks
    
            class Hello(Task):
                queue = 'hipri'
    
                def run(self, to):
                    return 'hello {0}'.format(to)
            tasks.register(Hello)
    
            >>> Hello.delay('world!')
    
        后来，Celery 团队认为传递任意可调用对象是反模式，
        因为这会导致难以使用除 pickle 之外的序列化器。
        这一特性在 2.0 中被移除，并由 task 装饰器取而代之：
    
        .. code-block:: python
    
            from celery import app
    
            @app.task(queue='hipri')
            def hello(to):
                return 'hello {0}'.format(to)

.. tab:: 英文

    While it's possible to depend on the current app
    being set, the best practice is to always pass the app instance
    around to anything that needs it.
    
    I call this the "app chain", since it creates a chain
    of instances depending on the app being passed.
    
    The following example is considered bad practice:
    
    .. code-block:: python
    
        from celery import current_app
    
        class Scheduler:
    
            def run(self):
                app = current_app
    
    Instead it should take the ``app`` as an argument:
    
    .. code-block:: python
    
        class Scheduler:
    
            def __init__(self, app):
                self.app = app
    
    Internally Celery uses the :func:`celery.app.app_or_default` function
    so that everything also works in the module-based compatibility API
    
    .. code-block:: python
    
        from celery.app import app_or_default
    
        class Scheduler:
            def __init__(self, app=None):
                self.app = app_or_default(app)
    
    In development you can set the :envvar:`CELERY_TRACE_APP`
    environment variable to raise an exception if the app
    chain breaks:
    
    .. code-block:: console
    
        $ CELERY_TRACE_APP=1 celery worker -l INFO
    
    
    .. topic:: Evolving the API
    
        Celery has changed a lot from 2009 since it was initially
        created.
    
        For example, in the beginning it was possible to use any callable as
        a task:
    
        .. code-block:: pycon
    
            def hello(to):
                return 'hello {0}'.format(to)
    
            >>> from celery.execute import apply_async
    
            >>> apply_async(hello, ('world!',))
    
        or you could also create a ``Task`` class to set
        certain options, or override other behavior
    
        .. code-block:: python
    
            from celery import Task
            from celery.registry import tasks
    
            class Hello(Task):
                queue = 'hipri'
    
                def run(self, to):
                    return 'hello {0}'.format(to)
            tasks.register(Hello)
    
            >>> Hello.delay('world!')
    
        Later, it was decided that passing arbitrary call-able's
        was an anti-pattern, since it makes it very hard to use
        serializers other than pickle, and the feature was removed
        in 2.0, replaced by task decorators:
    
        .. code-block:: python
    
            from celery import app
    
            @app.task(queue='hipri')
            def hello(to):
                return 'hello {0}'.format(to)

抽象任务
==============

Abstract Tasks

.. tab:: 中文

    所有使用 :meth:`@task` 装饰器创建的任务都会继承应用的基类 :attr:`~@Task`。
    
    你可以通过 ``base`` 参数指定不同的基类：
    
    .. code-block:: python
    
        @app.task(base=OtherTask):
        def add(x, y):
            return x + y
    
    若要创建自定义任务类，应从中性基类 :class:`celery.Task` 继承：
    
    .. code-block:: python
    
        from celery import Task
    
        class DebugTask(Task):
    
            def __call__(self, *args, **kwargs):
                print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
                return self.run(*args, **kwargs)
    
    
    .. tip::
    
        如果你重写了任务的 ``__call__`` 方法，务必要调用 ``self.run`` 来执行任务主体。
        不要调用 ``super().__call__``。中性基类 :class:`celery.Task` 的 ``__call__`` 方法仅供参考。
        出于优化目的，该方法在内部被展开为 ``celery.app.trace.build_tracer.trace_task``，
        如果未定义 ``__call__`` 方法，Celery 会直接在自定义任务类上调用 ``run``。
    
    中性基类的特殊之处在于它尚未绑定到任何特定的 app。
    一旦任务绑定到某个 app，它就会读取配置来设置默认值等。
    
    要实现一个基类，需通过 :meth:`@task` 装饰器创建任务：
    
    .. code-block:: python
    
        @app.task(base=DebugTask)
        def add(x, y):
            return x + y
    
    你甚至可以通过修改应用的 :meth:`@Task` 属性来改变应用的默认基类：
    
    .. code-block:: pycon
    
        >>> from celery import Celery, Task
    
        >>> app = Celery()
    
        >>> class MyBaseTask(Task):
        ...    queue = 'hipri'
    
        >>> app.Task = MyBaseTask
        >>> app.Task
        <unbound MyBaseTask>
    
        >>> @app.task
        ... def add(x, y):
        ...     return x + y
    
        >>> add
        <@task: __main__.add>
    
        >>> add.__class__.mro()
        [<class add of <Celery __main__:0x1012b4410>>,
         <unbound MyBaseTask>,
         <unbound Task>,
         <type 'object'>]


.. tab:: 英文

    All tasks created using the :meth:`@task` decorator
    will inherit from the application's base :attr:`~@Task` class.

    You can specify a different base class using the ``base`` argument:

    .. code-block:: python

        @app.task(base=OtherTask):
        def add(x, y):
            return x + y

    To create a custom task class you should inherit from the neutral base
    class: :class:`celery.Task`.

    .. code-block:: python

        from celery import Task

        class DebugTask(Task):

            def __call__(self, *args, **kwargs):
                print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
                return self.run(*args, **kwargs)


    .. tip::

        If you override the task's ``__call__`` method, then it's very important
        that you also call ``self.run`` to execute the body of the task.  Do not
        call ``super().__call__``.  The ``__call__`` method of the neutral base
        class :class:`celery.Task` is only present for reference.  For optimization,
        this has been unrolled into ``celery.app.trace.build_tracer.trace_task``
        which calls ``run`` directly on the custom task class if no ``__call__``
        method is defined.

    The neutral base class is special because it's not bound to any specific app
    yet. Once a task is bound to an app it'll read configuration to set default
    values, and so on.

    To realize a base class you need to create a task using the :meth:`@task`
    decorator:

    .. code-block:: python

        @app.task(base=DebugTask)
        def add(x, y):
            return x + y

    It's even possible to change the default base class for an application
    by changing its :meth:`@Task` attribute:

    .. code-block:: pycon

        >>> from celery import Celery, Task

        >>> app = Celery()

        >>> class MyBaseTask(Task):
        ...    queue = 'hipri'

        >>> app.Task = MyBaseTask
        >>> app.Task
        <unbound MyBaseTask>

        >>> @app.task
        ... def add(x, y):
        ...     return x + y

        >>> add
        <@task: __main__.add>

        >>> add.__class__.mro()
        [<class add of <Celery __main__:0x1012b4410>>,
         <unbound MyBaseTask>,
         <unbound Task>,
         <type 'object'>]
