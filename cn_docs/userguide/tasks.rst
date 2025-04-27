.. _guide-tasks:

=====================================================================
任务/Tasks
=====================================================================

Tasks

.. tab:: 中文

.. tab:: 英文

Tasks are the building blocks of Celery applications.

A task is a class that can be created out of any callable. It performs
dual roles in that it defines both what happens when a task is
called (sends a message), and what happens when a worker receives that message.

Every task class has a unique name, and this name is referenced in messages
so the worker can find the right function to execute.

A task message is not removed from the queue
until that message has been :term:`acknowledged` by a worker. A worker can reserve
many messages in advance and even if the worker is killed -- by power failure
or some other reason -- the message will be redelivered to another worker.

Ideally task functions should be :term:`idempotent`: meaning
the function won't cause unintended effects even if called
multiple times with the same arguments.
Since the worker cannot detect if your tasks are idempotent, the default
behavior is to acknowledge the message in advance, just before it's executed,
so that a task invocation that already started is never executed again.

If your task is idempotent you can set the :attr:`~Task.acks_late` option
to have the worker acknowledge the message *after* the task returns
instead. See also the FAQ entry :ref:`faq-acks_late-vs-retry`.

Note that the worker will acknowledge the message if the child process executing
the task is terminated (either by the task calling :func:`sys.exit`, or by signal)
even when :attr:`~Task.acks_late` is enabled.  This behavior is intentional
as...

#. We don't want to rerun tasks that forces the kernel to send
   a :sig:`SIGSEGV` (segmentation fault) or similar signals to the process.
#. We assume that a system administrator deliberately killing the task
   does not want it to automatically restart.
#. A task that allocates too much memory is in danger of triggering the kernel
   OOM killer, the same may happen again.
#. A task that always fails when redelivered may cause a high-frequency
   message loop taking down the system.

If you really want a task to be redelivered in these scenarios you should
consider enabling the :setting:`task_reject_on_worker_lost` setting.

.. warning::

    A task that blocks indefinitely may eventually stop the worker instance
    from doing any other work.

    If your task does I/O then make sure you add timeouts to these operations,
    like adding a timeout to a web request using the :pypi:`requests` library:

    .. code-block:: python

        connect_timeout, read_timeout = 5.0, 30.0
        response = requests.get(URL, timeout=(connect_timeout, read_timeout))

    :ref:`Time limits <worker-time-limits>` are convenient for making sure all
    tasks return in a timely manner, but a time limit event will actually kill
    the process by force so only use them to detect cases where you haven't
    used manual timeouts yet.

    In previous versions, the default prefork pool scheduler was not friendly
    to long-running tasks, so if you had tasks that ran for minutes/hours, it
    was advised to enable the :option:`-Ofair <celery worker -O>` command-line
    argument to the :program:`celery worker`. However, as of version 4.0,
    -Ofair is now the default scheduling strategy. See :ref:`optimizing-prefetch-limit`
    for more information, and for the best performance route long-running and
    short-running tasks to dedicated workers (:ref:`routing-automatic`).

    If your worker hangs then please investigate what tasks are running
    before submitting an issue, as most likely the hanging is caused
    by one or more tasks hanging on a network operation.

--

In this chapter you'll learn all about defining tasks,
and this is the **table of contents**:




.. _task-basics:

基础知识
======

Basics

.. tab:: 中文

.. tab:: 英文

You can easily create a task from any callable by using
the :meth:`@task` decorator:

.. code-block:: python

    from .models import User

    @app.task
    def create_user(username, password):
        User.objects.create(username=username, password=password)


There are also many :ref:`options <task-options>` that can be set for the task,
these can be specified as arguments to the decorator:

.. code-block:: python

    @app.task(serializer='json')
    def create_user(username, password):
        User.objects.create(username=username, password=password)


如何导入任务装饰器？
-----------------------------------

How do I import the task decorator?

.. tab:: 中文

.. tab:: 英文

    The task decorator is available on your :class:`@Celery` application instance,
    if you don't know what this is then please read :ref:`first-steps`.

    If you're using Django (see :ref:`django-first-steps`), or you're the author
    of a library then you probably want to use the :func:`@shared_task` decorator:

    .. code-block:: python

        from celery import shared_task

        @shared_task
        def add(x, y):
            return x + y

多个装饰器
-------------------

Multiple decorators

.. tab:: 中文

.. tab:: 英文

    When using multiple decorators in combination with the task
    decorator you must make sure that the `task`
    decorator is applied last (oddly, in Python this means it must
    be first in the list):

    .. code-block:: python

        @app.task
        @decorator2
        @decorator1
        def add(x, y):
            return x + y

绑定任务
-----------

Bound tasks

.. tab:: 中文

.. tab:: 英文

A task being bound means the first argument to the task will always
be the task instance (``self``), just like Python bound methods:

.. code-block:: python

    logger = get_task_logger(__name__)

    @app.task(bind=True)
    def add(self, x, y):
        logger.info(self.request.id)

Bound tasks are needed for retries (using :meth:`Task.retry() <@Task.retry>`),
for accessing information about the current task request, and for any
additional functionality you add to custom task base classes.

任务继承
----------------

Task inheritance

.. tab:: 中文

.. tab:: 英文

The ``base`` argument to the task decorator specifies the base class of the task:

.. code-block:: python

    import celery

    class MyTask(celery.Task):

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            print('{0!r} failed: {1!r}'.format(task_id, exc))

    @app.task(base=MyTask)
    def add(x, y):
        raise KeyError()

.. _task-names:

名称
=====

Names

.. tab:: 中文

.. tab:: 英文

Every task must have a unique name.

If no explicit name is provided the task decorator will generate one for you,
and this name will be based on 1) the module the task is defined in, and 2)
the name of the task function.

Example setting explicit name:

.. code-block:: pycon

    >>> @app.task(name='sum-of-two-numbers')
    >>> def add(x, y):
    ...     return x + y

    >>> add.name
    'sum-of-two-numbers'

A best practice is to use the module name as a name-space,
this way names won't collide if there's already a task with that name
defined in another module.

.. code-block:: pycon

    >>> @app.task(name='tasks.add')
    >>> def add(x, y):
    ...     return x + y

You can tell the name of the task by investigating its ``.name`` attribute:

.. code-block:: pycon

    >>> add.name
    'tasks.add'

The name we specified here (``tasks.add``) is exactly the name that would've
been automatically generated for us if the task was defined in a module
named :file:`tasks.py`:

:file:`tasks.py`:

.. code-block:: python

    @app.task
    def add(x, y):
        return x + y

.. code-block:: pycon

    >>> from tasks import add
    >>> add.name
    'tasks.add'

.. note::

   You can use the `inspect` command in a worker to view the names of
   all registered tasks. See the `inspect registered` command in the
   :ref:`monitoring-control` section of the User Guide.

.. _task-name-generator-info:

更改自动命名行为
--------------------------------------

Changing the automatic naming behavior

.. tab:: 中文

.. tab:: 英文

.. versionadded:: 4.0

There are some cases when the default automatic naming isn't suitable.
Consider having many tasks within many different modules::

    project/
           /__init__.py
           /celery.py
           /moduleA/
                   /__init__.py
                   /tasks.py
           /moduleB/
                   /__init__.py
                   /tasks.py

Using the default automatic naming, each task will have a generated name
like `moduleA.tasks.taskA`, `moduleA.tasks.taskB`, `moduleB.tasks.test`,
and so on. You may want to get rid of having `tasks` in all task names.
As pointed above, you can explicitly give names for all tasks, or you
can change the automatic naming behavior by overriding
:meth:`@gen_task_name`. Continuing with the example, `celery.py`
may contain:

.. code-block:: python

    from celery import Celery

    class MyCelery(Celery):

        def gen_task_name(self, name, module):
            if module.endswith('.tasks'):
                module = module[:-6]
            return super().gen_task_name(name, module)

    app = MyCelery('main')

So each task will have a name like `moduleA.taskA`, `moduleA.taskB` and
`moduleB.test`.

.. warning::

    Make sure that your :meth:`@gen_task_name` is a pure function: meaning
    that for the same input it must always return the same output.

.. _task-request-info:

任务请求
============

Task Request

.. tab:: 中文

.. tab:: 英文

:attr:`Task.request <@Task.request>` contains information and state
related to the currently executing task.

The request defines the following attributes:

:id: The unique id of the executing task.

:group: The unique id of the task's :ref:`group <canvas-group>`, if this task is a member.

:chord: The unique id of the chord this task belongs to (if the task
        is part of the header).

:correlation_id: Custom ID used for things like de-duplication.

:args: Positional arguments.

:kwargs: Keyword arguments.

:origin: Name of host that sent this task.

:retries: How many times the current task has been retried.
          An integer starting at `0`.

:is_eager: Set to :const:`True` if the task is executed locally in
           the client, not by a worker.

:eta: The original ETA of the task (if any).
      This is in UTC time (depending on the :setting:`enable_utc`
      setting).

:expires: The original expiry time of the task (if any).
          This is in UTC time (depending on the :setting:`enable_utc`
          setting).

:hostname: Node name of the worker instance executing the task.

:delivery_info: Additional message delivery information. This is a mapping
                containing the exchange and routing key used to deliver this
                task. Used by for example :meth:`Task.retry() <@Task.retry>`
                to resend the task to the same destination queue.
                Availability of keys in this dict depends on the
                message broker used.

:reply-to: Name of queue to send replies back to (used with RPC result
           backend for example).

:called_directly: This flag is set to true if the task wasn't
                  executed by the worker.

:timelimit: A tuple of the current ``(soft, hard)`` time limits active for
            this task (if any).

:callbacks: A list of signatures to be called if this task returns successfully.

:errbacks: A list of signatures to be called if this task fails.

:utc: Set to true the caller has UTC enabled (:setting:`enable_utc`).


.. versionadded:: 3.1

:headers:  Mapping of message headers sent with this task message
           (may be :const:`None`).

:reply_to:  Where to send reply to (queue name).

:correlation_id: Usually the same as the task id, often used in amqp
                 to keep track of what a reply is for.

.. versionadded:: 4.0

:root_id: The unique id of the first task in the workflow this task
          is part of (if any).

:parent_id: The unique id of the task that called this task (if any).

:chain: Reversed list of tasks that form a chain (if any).
        The last item in this list will be the next task to succeed the
        current task.  If using version one of the task protocol the chain
        tasks will be in ``request.callbacks`` instead.

.. versionadded:: 5.2

:properties: Mapping of message properties received with this task message
             (may be :const:`None` or :const:`{}`)

:replaced_task_nesting: How many times the task was replaced, if at all.
                        (may be :const:`0`)

示例
-------

Example

.. tab:: 中文

.. tab:: 英文

An example task accessing information in the context is:

.. code-block:: python

    @app.task(bind=True)
    def dump_context(self, x, y):
        print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
                self.request))


The ``bind`` argument means that the function will be a "bound method" so
that you can access attributes and methods on the task type instance.

.. _task-logging:

日志记录
=======

Logging

.. tab:: 中文

.. tab:: 英文

The worker will automatically set up logging for you, or you can
configure logging manually.

A special logger is available named "celery.task", you can inherit
from this logger to automatically get the task name and unique id as part
of the logs.

The best practice is to create a common logger
for all of your tasks at the top of your module:

.. code-block:: python

    from celery.utils.log import get_task_logger

    logger = get_task_logger(__name__)

    @app.task
    def add(x, y):
        logger.info('Adding {0} + {1}'.format(x, y))
        return x + y

Celery uses the standard Python logger library,
and the documentation can be found :mod:`here <logging>`.

You can also use :func:`print`, as anything written to standard
out/-err will be redirected to the logging system (you can disable this,
see :setting:`worker_redirect_stdouts`).

.. note::

    The worker won't update the redirection if you create a logger instance
    somewhere in your task or task module.

    If you want to redirect ``sys.stdout`` and ``sys.stderr`` to a custom
    logger you have to enable this manually, for example:

    .. code-block:: python

        import sys

        logger = get_task_logger(__name__)

        @app.task(bind=True)
        def add(self, x, y):
            old_outs = sys.stdout, sys.stderr
            rlevel = self.app.conf.worker_redirect_stdouts_level
            try:
                self.app.log.redirect_stdouts_to_logger(logger, rlevel)
                print('Adding {0} + {1}'.format(x, y))
                return x + y
            finally:
                sys.stdout, sys.stderr = old_outs


.. note::

    If a specific Celery logger you need is not emitting logs, you should
    check that the logger is propagating properly. In this example
    "celery.app.trace" is enabled so that "succeeded in" logs are emitted:

    .. code-block:: python


        import celery
        import logging

        @celery.signals.after_setup_logger.connect
        def on_after_setup_logger(**kwargs):
            logger = logging.getLogger('celery')
            logger.propagate = True
            logger = logging.getLogger('celery.app.trace')
            logger.propagate = True


.. note::

    If you want to completely disable Celery logging configuration,
    use the :signal:`setup_logging` signal:

    .. code-block:: python

        import celery

        @celery.signals.setup_logging.connect
        def on_setup_logging(**kwargs):
            pass


.. _task-argument-checking:

参数检查
-----------------

Argument checking

.. tab:: 中文

.. tab:: 英文

.. versionadded:: 4.0

Celery will verify the arguments passed when you call the task, just
like Python does when calling a normal function:

.. code-block:: pycon

    >>> @app.task
    ... def add(x, y):
    ...     return x + y

    # Calling the task with two arguments works:
    >>> add.delay(8, 8)
    <AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

    # Calling the task with only one argument fails:
    >>> add.delay(8)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "celery/app/task.py", line 376, in delay
        return self.apply_async(args, kwargs)
      File "celery/app/task.py", line 485, in apply_async
        check_arguments(*(args or ()), **(kwargs or {}))
    TypeError: add() takes exactly 2 arguments (1 given)

You can disable the argument checking for any task by setting its
:attr:`~@Task.typing` attribute to :const:`False`:

.. code-block:: pycon

    >>> @app.task(typing=False)
    ... def add(x, y):
    ...     return x + y

    # Works locally, but the worker receiving the task will raise an error.
    >>> add.delay(8)
    <AsyncResult: f59d71ca-1549-43e0-be41-4e8821a83c0c>

.. _task-hiding-sensitive-information:

在参数中隐藏敏感信息
-----------------------------------------

Hiding sensitive information in arguments

.. tab:: 中文

.. tab:: 英文

.. versionadded:: 4.0

When using :setting:`task_protocol` 2 or higher (default since 4.0), you can
override how positional arguments and keyword arguments are represented in logs
and monitoring events using the ``argsrepr`` and ``kwargsrepr`` calling
arguments:

.. code-block:: pycon

    >>> add.apply_async((2, 3), argsrepr='(<secret-x>, <secret-y>)')

    >>> charge.s(account, card='1234 5678 1234 5678').set(
    ...     kwargsrepr=repr({'card': '**** **** **** 5678'})
    ... ).delay()


.. warning::

    Sensitive information will still be accessible to anyone able
    to read your task message from the broker, or otherwise able intercept it.

    For this reason you should probably encrypt your message if it contains
    sensitive information, or in this example with a credit card number
    the actual number could be stored encrypted in a secure store that you retrieve
    and decrypt in the task itself.

.. _task-retry:

重试
========

Retrying

.. tab:: 中文

.. tab:: 英文

:meth:`Task.retry() <@Task.retry>` can be used to re-execute the task,
for example in the event of recoverable errors.

When you call ``retry`` it'll send a new message, using the same
task-id, and it'll take care to make sure the message is delivered
to the same queue as the originating task.

When a task is retried this is also recorded as a task state,
so that you can track the progress of the task using the result
instance (see :ref:`task-states`).

Here's an example using ``retry``:

.. code-block:: python

    @app.task(bind=True)
    def send_twitter_status(self, oauth, tweet):
        try:
            twitter = Twitter(oauth)
            twitter.update_status(tweet)
        except (Twitter.FailWhaleError, Twitter.LoginError) as exc:
            raise self.retry(exc=exc)

.. note::

    The :meth:`Task.retry() <@Task.retry>` call will raise an exception so any
    code after the retry won't be reached. This is the :exc:`~@Retry`
    exception, it isn't handled as an error but rather as a semi-predicate
    to signify to the worker that the task is to be retried,
    so that it can store the correct state when a result backend is enabled.

    This is normal operation and always happens unless the
    ``throw`` argument to retry is set to :const:`False`.

The bind argument to the task decorator will give access to ``self`` (the
task type instance).

The ``exc`` argument is used to pass exception information that's
used in logs, and when storing task results.
Both the exception and the traceback will
be available in the task state (if a result backend is enabled).

If the task has a ``max_retries`` value the current exception
will be re-raised if the max number of retries has been exceeded,
but this won't happen if:

- An ``exc`` argument wasn't given.

    In this case the :exc:`~@MaxRetriesExceededError`
    exception will be raised.

- There's no current exception

    If there's no original exception to re-raise the ``exc``
    argument will be used instead, so:

    .. code-block:: python

        self.retry(exc=Twitter.LoginError())

    will raise the ``exc`` argument given.

.. _task-retry-custom-delay:

使用自定义重试延迟
--------------------------

Using a custom retry delay

.. tab:: 中文

.. tab:: 英文

When a task is to be retried, it can wait for a given amount of time
before doing so, and the default delay is defined by the
:attr:`~@Task.default_retry_delay`
attribute. By default this is set to 3 minutes. Note that the
unit for setting the delay is in seconds (int or float).

You can also provide the `countdown` argument to :meth:`~@Task.retry` to
override this default.

.. code-block:: python

    @app.task(bind=True, default_retry_delay=30 * 60)  # retry in 30 minutes.
    def add(self, x, y):
        try:
            something_raising()
        except Exception as exc:
            # overrides the default delay to retry after 1 minute
            raise self.retry(exc=exc, countdown=60)

.. _task-autoretry:

已知异常的自动重试
------------------------------------

Automatic retry for known exceptions

.. tab:: 中文

.. tab:: 英文

.. versionadded:: 4.0

Sometimes you just want to retry a task whenever a particular exception
is raised.

Fortunately, you can tell Celery to automatically retry a task using
`autoretry_for` argument in the :meth:`@task` decorator:

.. code-block:: python

    from twitter.exceptions import FailWhaleError

    @app.task(autoretry_for=(FailWhaleError,))
    def refresh_timeline(user):
        return twitter.refresh_timeline(user)

If you want to specify custom arguments for an internal :meth:`~@Task.retry`
call, pass `retry_kwargs` argument to :meth:`@task` decorator:

.. code-block:: python

    @app.task(autoretry_for=(FailWhaleError,),
              retry_kwargs={'max_retries': 5})
    def refresh_timeline(user):
        return twitter.refresh_timeline(user)

This is provided as an alternative to manually handling the exceptions,
and the example above will do the same as wrapping the task body
in a :keyword:`try` ... :keyword:`except` statement:

.. code-block:: python

    @app.task
    def refresh_timeline(user):
        try:
            twitter.refresh_timeline(user)
        except FailWhaleError as exc:
            raise refresh_timeline.retry(exc=exc, max_retries=5)

If you want to automatically retry on any error, simply use:

.. code-block:: python

    @app.task(autoretry_for=(Exception,))
    def x():
        ...

.. versionadded:: 4.2

If your tasks depend on another service, like making a request to an API,
then it's a good idea to use `exponential backoff`_ to avoid overwhelming the
service with your requests. Fortunately, Celery's automatic retry support
makes it easy. Just specify the :attr:`~Task.retry_backoff` argument, like this:

.. code-block:: python

    from requests.exceptions import RequestException

    @app.task(autoretry_for=(RequestException,), retry_backoff=True)
    def x():
        ...

By default, this exponential backoff will also introduce random jitter_ to
avoid having all the tasks run at the same moment. It will also cap the
maximum backoff delay to 10 minutes. All these settings can be customized
via options documented below.

.. versionadded:: 4.4

You can also set `autoretry_for`, `max_retries`, `retry_backoff`, `retry_backoff_max` and `retry_jitter` options in class-based tasks:

.. code-block:: python

    class BaseTaskWithRetry(Task):
        autoretry_for = (TypeError,)
        max_retries = 5
        retry_backoff = True
        retry_backoff_max = 700
        retry_jitter = False

.. attribute:: Task.autoretry_for

    A list/tuple of exception classes. If any of these exceptions are raised
    during the execution of the task, the task will automatically be retried.
    By default, no exceptions will be autoretried.

.. attribute:: Task.max_retries

    A number. Maximum number of retries before giving up. A value of ``None``
    means task will retry forever. By default, this option is set to ``3``.

.. attribute:: Task.retry_backoff

    A boolean, or a number. If this option is set to ``True``, autoretries
    will be delayed following the rules of `exponential backoff`_. The first
    retry will have a delay of 1 second, the second retry will have a delay
    of 2 seconds, the third will delay 4 seconds, the fourth will delay 8
    seconds, and so on. (However, this delay value is modified by
    :attr:`~Task.retry_jitter`, if it is enabled.)
    If this option is set to a number, it is used as a
    delay factor. For example, if this option is set to ``3``, the first retry
    will delay 3 seconds, the second will delay 6 seconds, the third will
    delay 12 seconds, the fourth will delay 24 seconds, and so on. By default,
    this option is set to ``False``, and autoretries will not be delayed.

.. attribute:: Task.retry_backoff_max

    A number. If ``retry_backoff`` is enabled, this option will set a maximum
    delay in seconds between task autoretries. By default, this option is set to ``600``,
    which is 10 minutes.

.. attribute:: Task.retry_jitter

    A boolean. `Jitter`_ is used to introduce randomness into
    exponential backoff delays, to prevent all tasks in the queue from being
    executed simultaneously. If this option is set to ``True``, the delay
    value calculated by :attr:`~Task.retry_backoff` is treated as a maximum,
    and the actual delay value will be a random number between zero and that
    maximum. By default, this option is set to ``True``.

.. versionadded:: 5.3.0

.. attribute:: Task.dont_autoretry_for

    A list/tuple of exception classes.  These exceptions won't be autoretried.
	This allows to exclude some exceptions that match `autoretry_for
	<Task.autoretry_for>`:attr: but for which you don't want a retry.

.. _task-pydantic:

使用 Pydantic 进行参数验证
=================================

Argument validation with Pydantic

.. tab:: 中文

.. tab:: 英文

.. versionadded:: 5.5.0

You can use Pydantic_ to validate and convert arguments as well as serializing
results based on typehints by passing ``pydantic=True``.

.. NOTE::

   Argument validation only covers arguments/return values on the task side. You still have
   serialize arguments yourself when invoking a task with ``delay()`` or ``apply_async()``.

For example:

.. code-block:: python

    from pydantic import BaseModel

    class ArgModel(BaseModel):
        value: int

    class ReturnModel(BaseModel):
        value: str

    @app.task(pydantic=True)
    def x(arg: ArgModel) -> ReturnModel:
        # args/kwargs type hinted as Pydantic model will be converted
        assert isinstance(arg, ArgModel)

        # The returned model will be converted to a dict automatically
        return ReturnModel(value=f"example: {arg.value}")

The task can then be called using a dict matching the model, and you'll receive
the returned model "dumped" (serialized using ``BaseModel.model_dump()``):

.. code-block:: python

   >>> result = x.delay({'value': 1})
   >>> result.get(timeout=1)
   {'value': 'example: 1'}

联合类型、泛型参数
----------------------------------

Union types, arguments to generics

.. tab:: 中文

.. tab:: 英文

Union types (e.g. ``Union[SomeModel, OtherModel]``) or arguments to generics (e.g.
``list[SomeModel]``) are **not** supported.

In case you want to support a list or similar types, it is recommended to use
``pydantic.RootModel``.


可选参数/返回值
---------------------------------

Optional parameters/return values

.. tab:: 中文

.. tab:: 英文

Optional parameters or return values are also handled properly. For example, given this task:

.. code-block:: python

    from typing import Optional

    # models are the same as above

    @app.task(pydantic=True)
    def x(arg: Optional[ArgModel] = None) -> Optional[ReturnModel]:
        if arg is None:
            return None
        return ReturnModel(value=f"example: {arg.value}")

You'll get the following behavior:

.. code-block:: python

    >>> result = x.delay()
   >>> result.get(timeout=1) is None
   True
   >>> result = x.delay({'value': 1})
   >>> result.get(timeout=1)
   {'value': 'example: 1'}

返回值处理
---------------------

Return value handling

.. tab:: 中文

.. tab:: 英文

Return values will only be serialized if the returned model matches the annotation. If you pass a
model instance of a different type, it will *not* be serialized. ``mypy`` should already catch such
errors and you should fix your typehints then.


Pydantic 参数
-------------------

Pydantic parameters

.. tab:: 中文

.. tab:: 英文

There are a few more options influencing Pydantic behavior:

.. attribute:: Task.pydantic_strict

   By default, `strict mode <https://docs.pydantic.dev/dev/concepts/strict_mode/>`_
   is disabled. You can pass ``True`` to enable strict model validation.

.. attribute:: Task.pydantic_context

   Pass `additional validation context
   <https://docs.pydantic.dev/dev/concepts/validators/#validation-context>`_ during
   Pydantic model validation. The context already includes the application object as
   ``celery_app`` and the task name as ``celery_task_name`` by default.

.. attribute:: Task.pydantic_dump_kwargs

   When serializing a result, pass these additional arguments to ``dump_kwargs()``.
   By default, only ``mode='json'`` is passed.


.. _task-options:

选项列表
===============

List of Options

.. tab:: 中文

.. tab:: 英文

The task decorator can take a number of options that change the way
the task behaves, for example you can set the rate limit for a task
using the :attr:`rate_limit` option.

Any keyword argument passed to the task decorator will actually be set
as an attribute of the resulting task class, and this is a list
of the built-in attributes.

常规
-------

General

.. tab:: 中文

.. tab:: 英文

.. _task-general-options:

.. attribute:: Task.name

    The name the task is registered as.

    You can set this name manually, or a name will be
    automatically generated using the module and class name.

    See also :ref:`task-names`.

.. attribute:: Task.request

    If the task is being executed this will contain information
    about the current request. Thread local storage is used.

    See :ref:`task-request-info`.

.. attribute:: Task.max_retries

    Only applies if the task calls ``self.retry`` or if the task is decorated
    with the :ref:`autoretry_for <task-autoretry>` argument.

    The maximum number of attempted retries before giving up.
    If the number of retries exceeds this value a :exc:`~@MaxRetriesExceededError`
    exception will be raised.

    .. note::

        You have to call :meth:`~@Task.retry`
        manually, as it won't automatically retry on exception..

    The default is ``3``.
    A value of :const:`None` will disable the retry limit and the
    task will retry forever until it succeeds.

.. attribute:: Task.throws

    Optional tuple of expected error classes that shouldn't be regarded
    as an actual error.

    Errors in this list will be reported as a failure to the result backend,
    but the worker won't log the event as an error, and no traceback will
    be included.

    Example:

    .. code-block:: python

        @task(throws=(KeyError, HttpNotFound)):
        def get_foo():
            something()

    Error types:

    - Expected errors (in ``Task.throws``)

        Logged with severity ``INFO``, traceback excluded.

    - Unexpected errors

        Logged with severity ``ERROR``, with traceback included.

.. attribute:: Task.default_retry_delay

    Default time in seconds before a retry of the task
    should be executed. Can be either :class:`int` or :class:`float`.
    Default is a three minute delay.

.. attribute:: Task.rate_limit

    Set the rate limit for this task type (limits the number of tasks
    that can be run in a given time frame). Tasks will still complete when
    a rate limit is in effect, but it may take some time before it's allowed to
    start.

    If this is :const:`None` no rate limit is in effect.
    If it is an integer or float, it is interpreted as "tasks per second".

    The rate limits can be specified in seconds, minutes or hours
    by appending `"/s"`, `"/m"` or `"/h"` to the value. Tasks will be evenly
    distributed over the specified time frame.

    Example: `"100/m"` (hundred tasks a minute). This will enforce a minimum
    delay of 600ms between starting two tasks on the same worker instance.

    Default is the :setting:`task_default_rate_limit` setting:
    if not specified means rate limiting for tasks is disabled by default.

    Note that this is a *per worker instance* rate limit, and not a global
    rate limit. To enforce a global rate limit (e.g., for an API with a
    maximum number of  requests per second), you must restrict to a given
    queue.

.. attribute:: Task.time_limit

    The hard time limit, in seconds, for this task.
    When not set the workers default is used.

.. attribute:: Task.soft_time_limit

    The soft time limit for this task.
    When not set the workers default is used.

.. attribute:: Task.ignore_result

    Don't store task state. Note that this means you can't use
    :class:`~celery.result.AsyncResult` to check if the task is ready,
    or get its return value.

    Note: Certain features will not work if task results are disabled.
    For more details check the Canvas documentation.

.. attribute:: Task.store_errors_even_if_ignored

    If :const:`True`, errors will be stored even if the task is configured
    to ignore results.

.. attribute:: Task.serializer

    A string identifying the default serialization
    method to use. Defaults to the :setting:`task_serializer`
    setting. Can be `pickle`, `json`, `yaml`, or any custom
    serialization methods that have been registered with
    :mod:`kombu.serialization.registry`.

    Please see :ref:`calling-serializers` for more information.

.. attribute:: Task.compression

    A string identifying the default compression scheme to use.

    Defaults to the :setting:`task_compression` setting.
    Can be `gzip`, or `bzip2`, or any custom compression schemes
    that have been registered with the :mod:`kombu.compression` registry.

    Please see :ref:`calling-compression` for more information.

.. attribute:: Task.backend

    The result store backend to use for this task. An instance of one of the
    backend classes in `celery.backends`. Defaults to `app.backend`,
    defined by the :setting:`result_backend` setting.

.. attribute:: Task.acks_late

    If set to :const:`True` messages for this task will be acknowledged
    **after** the task has been executed, not *just before* (the default
    behavior).

    Note: This means the task may be executed multiple times should the worker
    crash in the middle of execution.  Make sure your tasks are
    :term:`idempotent`.

    The global default can be overridden by the :setting:`task_acks_late`
    setting.

.. _task-track-started:

.. attribute:: Task.track_started

    If :const:`True` the task will report its status as "started"
    when the task is executed by a worker.
    The default value is :const:`False` as the normal behavior is to not
    report that level of granularity. Tasks are either pending, finished,
    or waiting to be retried. Having a "started" status can be useful for
    when there are long running tasks and there's a need to report what
    task is currently running.

    The host name and process id of the worker executing the task
    will be available in the state meta-data (e.g., `result.info['pid']`)

    The global default can be overridden by the
    :setting:`task_track_started` setting.


.. seealso::

    The API reference for :class:`~@Task`.

.. _task-states:

状态
======

States

.. tab:: 中文

    Celery 可以跟踪任务的当前状态。状态信息中还包含了
    成功任务的返回结果，或者失败任务的异常与回溯（traceback）信息。

    Celery 提供了多种 *结果后端*（result backend）供选择，
    每种后端都有其各自的优缺点（参见 :ref:`task-result-backends`）。

    在任务的生命周期中，它将经历多个可能的状态变迁，
    且每个状态都可以附加任意的元数据（meta-data）。
    当任务进入一个新的状态时，之前的状态将被遗忘，
    但某些状态变迁可以被推断出来（例如，
    如果一个任务当前处于 :state:`FAILED` 状态，
    可以推断出它之前曾处于 :state:`STARTED` 状态）。

    同时，Celery 还定义了一些状态集合，
    比如 :state:`FAILURE_STATES` 集合和 :state:`READY_STATES` 集合。

    客户端可以通过判断任务状态是否属于这些集合来决定后续行为，
    例如，是否需要重新抛出异常（如果任务状态属于 :state:`PROPAGATE_STATES`），
    或者是否可以缓存该任务状态（如果任务已准备就绪，则可以缓存）。

    此外，你也可以定义 :ref:`custom-states` 来扩展状态管理。

.. tab:: 英文

    Celery can keep track of the tasks current state. The state also contains the
    result of a successful task, or the exception and traceback information of a
    failed task.

    There are several *result backends* to choose from, and they all have
    different strengths and weaknesses (see :ref:`task-result-backends`).

    During its lifetime a task will transition through several possible states,
    and each state may have arbitrary meta-data attached to it. When a task
    moves into a new state the previous state is
    forgotten about, but some transitions can be deduced, (e.g., a task now
    in the :state:`FAILED` state, is implied to have been in the
    :state:`STARTED` state at some point).

    There are also sets of states, like the set of
    :state:`FAILURE_STATES`, and the set of :state:`READY_STATES`.

    The client uses the membership of these sets to decide whether
    the exception should be re-raised (:state:`PROPAGATE_STATES`), or whether
    the state can be cached (it can if the task is ready).

    You can also define :ref:`custom-states`.

.. _task-result-backends:

结果后端
---------------

Result Backends

.. tab:: 中文

    如果你希望跟踪任务或需要获取返回值，那么 Celery 必须将状态存储或发送到某个地方，以便之后能够检索。
    Celery 提供了多种内置的结果后端供选择：SQLAlchemy/Django ORM、Memcached、RabbitMQ/QPid（``rpc``）和 Redis —— 当然你也可以自定义自己的后端。

    没有任何一个后端能在所有使用场景中都表现良好。
    你应当了解每种后端的优缺点，并根据自己的需求选择最合适的方案。

    .. warning::

        后端在存储和传输结果时会占用资源。为了确保资源能够及时释放，
        你必须在调用任务之后，对每一个返回的 :class:`~@AsyncResult` 实例，
        最终调用一次 :meth:`~@AsyncResult.get` 或 :meth:`~@AsyncResult.forget` 方法。

    .. seealso::

        :ref:`conf-result-backend`

.. tab:: 英文

    If you want to keep track of tasks or need the return values, then Celery
    must store or send the states somewhere so that they can be retrieved later.
    There are several built-in result backends to choose from: SQLAlchemy/Django ORM,
    Memcached, RabbitMQ/QPid (``rpc``), and Redis -- or you can define your own.
    
    No backend works well for every use case.
    You should read about the strengths and weaknesses of each backend, and choose
    the most appropriate for your needs.
    
    .. warning::
    
        Backends use resources to store and transmit results. To ensure
        that resources are released, you must eventually call
        :meth:`~@AsyncResult.get` or :meth:`~@AsyncResult.forget` on
        EVERY :class:`~@AsyncResult` instance returned after calling
        a task.
    
    .. seealso::
    
        :ref:`conf-result-backend`

RPC 结果后端 (RabbitMQ/QPid)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RPC Result Backend (RabbitMQ/QPid)

.. tab:: 中文

    RPC 结果后端（ ``rpc://`` ）比较特殊，因为它实际上并不 *存储* 状态，
    而是将其作为消息发送出去。这一点非常重要，因为它意味着：

    - 一个结果 *只能被检索一次*。
    - *只能由发起该任务的客户端* 进行检索。

    两个不同的进程无法同时等待同一个结果。

    尽管有这些限制，如果你需要实时接收状态变更信息，RPC 后端依然是一个非常优秀的选择。
    使用消息传递机制意味着客户端无需轮询即可接收新状态。

    默认情况下，消息是瞬时（非持久化）的，因此如果代理（broker）重启，结果将会丢失。
    你可以通过设置 :setting:`result_persistent` 来配置后端发送持久化消息。

.. tab:: 英文

    The RPC result backend (`rpc://`) is special as it doesn't actually *store*
    the states, but rather sends them as messages. This is an important difference as it
    means that a result *can only be retrieved once*, and *only by the client
    that initiated the task*. Two different processes can't wait for the same result.

    Even with that limitation, it is an excellent choice if you need to receive
    state changes in real-time. Using messaging means the client doesn't have to
    poll for new states.

    The messages are transient (non-persistent) by default, so the results will
    disappear if the broker restarts. You can configure the result backend to send
    persistent messages using the :setting:`result_persistent` setting.

数据库结果后端
~~~~~~~~~~~~~~~~~~~~~~~

Database Result Backend

.. tab:: 中文

    将状态存储在数据库中对许多人来说非常方便，特别是当已有数据库基础设施（例如 Web 应用）时，
    但这种方式也存在一些局限性：
    
    * 轮询数据库以获取新状态的代价很高，因此你应当增加操作的轮询间隔，比如在调用 `result.get()` 时。
    
    * 有些数据库的默认事务隔离级别并不适合用于轮询数据表以检测变化。
    
      以 MySQL 为例，其默认的事务隔离级别是 `REPEATABLE-READ`：
      这意味着在当前事务提交之前，该事务无法看到其他事务所做的更改。
    
      因此，推荐将事务隔离级别修改为 `READ-COMMITTED`。


.. tab:: 英文

    Keeping state in the database can be convenient for many, especially for
    web applications with a database already in place, but it also comes with
    limitations.
    
    * Polling the database for new states is expensive, and so you should
      increase the polling intervals of operations, such as `result.get()`.
    
    * Some databases use a default transaction isolation level that
      isn't suitable for polling tables for changes.
    
      In MySQL the default transaction isolation level is `REPEATABLE-READ`:
      meaning the transaction won't see changes made by other transactions until
      the current transaction is committed.
    
      Changing that to the `READ-COMMITTED` isolation level is recommended.

.. _task-builtin-states:

内置状态
---------------

Built-in States

.. state:: PENDING

PENDING
~~~~~~~

.. tab:: 中文

    任务正在等待执行或未知.
    任何未知的任务 ID 都暗示处于待处理状态.

.. tab:: 英文

    Task is waiting for execution or unknown.
    Any task id that's not known is implied to be in the pending state.

.. state:: STARTED

STARTED
~~~~~~~

.. tab:: 中文

    任务已开始.
    默认情况下不报告，要启用请参阅 :attr:`@Task.track_started` 。

    :meta-data: 执行任务的工作进程的 `pid` 和 `hostname` 。

.. tab:: 英文

    Task has been started.
    Not reported by default, to enable please see :attr:`@Task.track_started`.

    :meta-data: `pid` and `hostname` of the worker process executing the task.

.. state:: SUCCESS

SUCCESS
~~~~~~~

.. tab:: 中文

    任务已成功执行。

    :meta-data: `result` 包含任务的返回值。
    :propagates: Yes
    :ready: Yes

.. tab:: 英文

    Task has been successfully executed.

    :meta-data: `result` contains the return value of the task.
    :propagates: Yes
    :ready: Yes

.. state:: FAILURE

FAILURE
~~~~~~~

.. tab:: 中文

    任务执行失败.

    :meta-data: `result` 包含发生的异常， `traceback` 包含引发异常时堆栈的回溯。
    :propagates: Yes

.. tab:: 英文

    Task execution resulted in failure.

    :meta-data: `result` contains the exception occurred, and `traceback` contains the backtrace of the stack at the point when the exception was raised.
    :propagates: Yes

.. state:: RETRY

RETRY
~~~~~

.. tab:: 中文

    任务正在重试.

    :meta-data: `result` 包含导致重试的异常， `traceback` 包含引发异常时堆栈的回溯。
    :propagates: No

.. tab:: 英文

    Task is being retried.

    :meta-data: `result` contains the exception that caused the retry, and `traceback` contains the backtrace of the stack at the point when the exceptions was raised.
    :propagates: No

.. state:: REVOKED

REVOKED
~~~~~~~

.. tab:: 中文

    任务已被撤销.

    :propagates: Yes

.. tab:: 英文

    Task has been revoked.

    :propagates: Yes

.. _custom-states:

自定义状态
-------------

Custom states

.. tab:: 中文

    你可以轻松地定义自己的任务状态，只需要一个唯一的名称即可。
    状态名通常是一个大写字符串。例如，你可以参考 :mod:`可中止任务 <~celery.contrib.abortable>` ，
    其中定义了一个自定义的 :state:`ABORTED` 状态。

    使用 :meth:`~@Task.update_state` 方法可以更新任务的状态：

    .. code-block:: python

        @app.task(bind=True)
        def upload_files(self, filenames):
            for i, file in enumerate(filenames):
                if not self.request.called_directly:
                    self.update_state(state='PROGRESS',
                        meta={'current': i, 'total': len(filenames)})

    在上面的例子中，我创建了状态 `"PROGRESS"`，
    用于告知了解此状态的应用程序当前任务正在进行中，
    并通过 `current` 和 `total` 这两个计数值来表示任务的进度。
    例如，可以基于这些元数据来创建进度条显示。

.. tab:: 英文

    You can easily define your own states, all you need is a unique name.
    The name of the state is usually an uppercase string. As an example
    you could have a look at the :mod:`abortable tasks <~celery.contrib.abortable>`
    which defines a custom :state:`ABORTED` state.

    Use :meth:`~@Task.update_state` to update a task's state:.

    .. code-block:: python

        @app.task(bind=True)
        def upload_files(self, filenames):
            for i, file in enumerate(filenames):
                if not self.request.called_directly:
                    self.update_state(state='PROGRESS',
                        meta={'current': i, 'total': len(filenames)})


    Here I created the state `"PROGRESS"`, telling any application
    aware of this state that the task is currently in progress, and also where
    it is in the process by having `current` and `total` counts as part of the
    state meta-data. This can then be used to create progress bars for example.

.. _pickling_exceptions:

创建可 pickle 的异常
------------------------------

Creating pickleable exceptions

.. tab:: 中文

    一个鲜为人知的 Python 事实是：异常要能被 `pickle` 模块序列化，必须遵循一些简单的规则。

    如果任务抛出了无法被 pickle 序列化的异常，那么在使用 Pickle 作为序列化器时，任务将无法正常工作。

    为了确保异常对象可以被 pickle 正确序列化，
    异常类 *必须* 在其 ``.args`` 属性中保存创建实例时的原始参数。
    最简单的方式就是在自定义异常的构造函数中调用 ``Exception.__init__`` 方法。

    下面是一些可以正常工作的示例，以及一个错误示例：

    .. code-block:: python

        # 正确示例：
        class HttpError(Exception):
            pass

        # 错误示例：
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code

        # 正确示例：
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code
                Exception.__init__(self, status_code)  # <-- 必须调用

    因此，规则总结如下：
    如果异常类支持自定义参数 ``*args``，
    则必须在构造函数中调用 ``Exception.__init__(self, *args)``。

    需要注意的是：
    目前对于 *关键字参数（keyword arguments）* 并没有特别的支持，
    因此如果希望在反序列化（unpickle）时保留关键字参数，
    必须将它们作为普通的位置参数（args）传递：

    .. code-block:: python

        class HttpError(Exception):

            def __init__(self, status_code, headers=None, body=None):
                self.status_code = status_code
                self.headers = headers
                self.body = body

                super(HttpError, self).__init__(status_code, headers, body)


.. tab:: 英文

    A rarely known Python fact is that exceptions must conform to some
    simple rules to support being serialized by the pickle module.

    Tasks that raise exceptions that aren't pickleable won't work
    properly when Pickle is used as the serializer.

    To make sure that your exceptions are pickleable the exception
    *MUST* provide the original arguments it was instantiated
    with in its ``.args`` attribute. The simplest way
    to ensure this is to have the exception call ``Exception.__init__``.

    Let's look at some examples that work, and one that doesn't:

    .. code-block:: python


        # OK:
        class HttpError(Exception):
            pass

        # BAD:
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code

        # OK:
        class HttpError(Exception):

            def __init__(self, status_code):
                self.status_code = status_code
                Exception.__init__(self, status_code)  # <-- REQUIRED


    So the rule is:
    For any exception that supports custom arguments ``*args``,
    ``Exception.__init__(self, *args)`` must be used.

    There's no special support for *keyword arguments*, so if you
    want to preserve keyword arguments when the exception is unpickled
    you have to pass them as regular args:

    .. code-block:: python

        class HttpError(Exception):

            def __init__(self, status_code, headers=None, body=None):
                self.status_code = status_code
                self.headers = headers
                self.body = body

                super(HttpError, self).__init__(status_code, headers, body)

.. _task-semipredicates:

任务半谓词
==============

Semipredicates

.. tab:: 中文

    worker 将任务包装在一个跟踪函数中，用于记录任务的最终状态。可以使用多种异常来通知此函数，以改变其处理任务返回的方式。

    .. admonition:: 译注: Semipredicates
       :class: toggle

       在 Celery 的上下文中，"task semipredicates" 是一个相对专业的术语，其翻译需要结合技术语义和中文表达习惯。以下是针对该术语的详细解析和推荐译法：

       ----

       1. **术语解析**

       - **Semipredicate（半谓词）**：

         - **计算机科学中的原意**：指既返回结果又返回状态（如成功/失败）的函数，例如 C 语言的 ``fopen()`` 在失败时返回 ``NULL`` 同时设置 ``errno``。

         - **在 Celery 中的延伸**：可能指任务（task）在执行时既产生返回值，又隐含状态信息（如 ``SUCCESS``、``FAILURE`` 或重试状态）。

       - **Task Semipredicates**：

         - 指 Celery 任务设计中同时承载业务逻辑结果和自身执行状态的特性，例如：

           .. code-block:: python
    
                @app.task(bind=True)
                def my_task(self, x, y):
                    try:
                        return x / y  # 业务结果
                    except ZeroDivisionError:
                        self.retry(countdown=60)  # 状态控制

       ----

       2. **推荐翻译方案**

       根据上下文可选择以下译法：

       .. list-table::
          
          * - 英文术语
            - 推荐中文翻译
            - 适用场景
          * - Task Semipredicates
            - 任务半谓词
            - 强调技术实现（学术/底层文档）
          * - 
            - 任务状态复合体
            - 强调状态与结果的结合（设计文档）
          * - 
            - 双态任务
            - 简洁表达（非正式场合）

       ----

       3. **使用示例**

       **(1) 技术文档中的翻译**

       原文：

           Celery tasks act as semipredicates, returning both computed values and their own execution status.

       译文：

           Celery 任务作为任务半谓词，既返回计算结果，又携带自身执行状态。

       **(2) 设计文档中的翻译**

       原文：

           The semipredicate nature of tasks allows for robust error handling.

       译文：

           任务的状态复合体特性使其支持健壮的错误处理。

       ----

       4. **注意事项**

       - **一致性**：在同一个项目中保持术语翻译统一。

       - **注释说明**：首次出现时可添加英文原词和简要解释，例如：

       任务半谓词（Task Semipredicates，指同时返回结果和状态的任务）

       - **受众适配**：面向开发者可直接用英文术语，面向非技术读者建议意译。

       ----

       5. **相关术语对照表**

       .. list-table::
          
          * - 英文术语
            - 中文翻译
          * - Task
            - 任务
          * - Predicate Function
            - 谓词函数
          * - Stateful Task
            - 有状态任务
          * - Idempotent Task
            - 幂等任务

       通过以上方式，可以准确传达 "task semipredicates" 在 Celery 中的技术内涵。


.. tab:: 英文

    The worker wraps the task in a tracing function that records the final state of the task. There are a number of exceptions that can be used to signal this function to change how it treats the return of the task.

.. _task-semipred-ignore:

忽略
------

Ignore

.. tab:: 中文

.. tab:: 英文

The task may raise :exc:`~@Ignore` to force the worker to ignore the
task. This means that no state will be recorded for the task, but the
message is still acknowledged (removed from queue).

This can be used if you want to implement custom revoke-like
functionality, or manually store the result of a task.

Example keeping revoked tasks in a Redis set:

.. code-block:: python

    from celery.exceptions import Ignore

    @app.task(bind=True)
    def some_task(self):
        if redis.ismember('tasks.revoked', self.request.id):
            raise Ignore()

Example that stores results manually:

.. code-block:: python

    from celery import states
    from celery.exceptions import Ignore

    @app.task(bind=True)
    def get_tweets(self, user):
        timeline = twitter.get_timeline(user)
        if not self.request.called_directly:
            self.update_state(state=states.SUCCESS, meta=timeline)
        raise Ignore()

.. _task-semipred-reject:

拒绝
------

Reject

.. tab:: 中文

.. tab:: 英文

The task may raise :exc:`~@Reject` to reject the task message using
AMQPs ``basic_reject`` method. This won't have any effect unless
:attr:`Task.acks_late` is enabled.

Rejecting a message has the same effect as acking it, but some
brokers may implement additional functionality that can be used.
For example RabbitMQ supports the concept of `Dead Letter Exchanges`_
where a queue can be configured to use a dead letter exchange that rejected
messages are redelivered to.

.. _`Dead Letter Exchanges`: http://www.rabbitmq.com/dlx.html

Reject can also be used to re-queue messages, but please be very careful
when using this as it can easily result in an infinite message loop.

Example using reject when a task causes an out of memory condition:

.. code-block:: python

    import errno
    from celery.exceptions import Reject

    @app.task(bind=True, acks_late=True)
    def render_scene(self, path):
        file = get_file(path)
        try:
            renderer.render_scene(file)

        # if the file is too big to fit in memory
        # we reject it so that it's redelivered to the dead letter exchange
        # and we can manually inspect the situation.
        except MemoryError as exc:
            raise Reject(exc, requeue=False)
        except OSError as exc:
            if exc.errno == errno.ENOMEM:
                raise Reject(exc, requeue=False)

        # For any other error we retry after 10 seconds.
        except Exception as exc:
            raise self.retry(exc, countdown=10)

Example re-queuing the message:

.. code-block:: python

    from celery.exceptions import Reject

    @app.task(bind=True, acks_late=True)
    def requeues(self):
        if not self.request.delivery_info['redelivered']:
            raise Reject('no reason', requeue=True)
        print('received two times')

Consult your broker documentation for more details about the ``basic_reject``
method.


.. _task-semipred-retry:

重试
-----

Retry

.. tab:: 中文

.. tab:: 英文

The :exc:`~@Retry` exception is raised by the ``Task.retry`` method
to tell the worker that the task is being retried.

.. _task-custom-classes:

自定义任务类
===================

Custom task classes

.. tab:: 中文

.. tab:: 英文

All tasks inherit from the :class:`@Task` class.
The :meth:`~@Task.run` method becomes the task body.

As an example, the following code,

.. code-block:: python

    @app.task
    def add(x, y):
        return x + y


will do roughly this behind the scenes:

.. code-block:: python

    class _AddTask(app.Task):

        def run(self, x, y):
            return x + y
    add = app.tasks[_AddTask.name]


实例化
-------------

Instantiation

.. tab:: 中文

.. tab:: 英文

A task is **not** instantiated for every request, but is registered
in the task registry as a global instance.

This means that the ``__init__`` constructor will only be called
once per process, and that the task class is semantically closer to an
Actor.

If you have a task,

.. code-block:: python

    from celery import Task

    class NaiveAuthenticateServer(Task):

        def __init__(self):
            self.users = {'george': 'password'}

        def run(self, username, password):
            try:
                return self.users[username] == password
            except KeyError:
                return False

And you route every request to the same process, then it
will keep state between requests.

This can also be useful to cache resources,
For example, a base Task class that caches a database connection:

.. code-block:: python

    from celery import Task

    class DatabaseTask(Task):
        _db = None

        @property
        def db(self):
            if self._db is None:
                self._db = Database.connect()
            return self._db

每个任务的使用
~~~~~~~~~~~~~~

Per task usage

.. tab:: 中文

.. tab:: 英文

The above can be added to each task like this:

.. code-block:: python


    from celery.app import task

    @app.task(base=DatabaseTask, bind=True)
    def process_rows(self: task):
        for row in self.db.table.all():
            process_row(row)

The ``db`` attribute of the ``process_rows`` task will then
always stay the same in each process.

.. _custom-task-cls-app-wide:

应用范围的使用
~~~~~~~~~~~~~~

App-wide usage

.. tab:: 中文

.. tab:: 英文

You can also use your custom class in your whole Celery app by passing it as
the ``task_cls`` argument when instantiating the app. This argument should be
either a string giving the python path to your Task class or the class itself:

.. code-block:: python

    from celery import Celery

    app = Celery('tasks', task_cls='your.module.path:DatabaseTask')

This will make all your tasks declared using the decorator syntax within your
app to use your ``DatabaseTask`` class and will all have a ``db`` attribute.

The default value is the class provided by Celery: ``'celery.app.task:Task'``.

处理程序
--------

Handlers

.. tab:: 中文

.. tab:: 英文

.. method:: before_start(self, task_id, args, kwargs)

    Run by the worker before the task starts executing.

    .. versionadded:: 5.2

    :param task_id: Unique id of the task to execute.
    :param args: Original arguments for the task to execute.
    :param kwargs: Original keyword arguments for the task to execute.

    The return value of this handler is ignored.

.. method:: after_return(self, status, retval, task_id, args, kwargs, einfo)

    Handler called after the task returns.

    :param status: Current task state.
    :param retval: Task return value/exception.
    :param task_id: Unique id of the task.
    :param args: Original arguments for the task that returned.
    :param kwargs: Original keyword arguments for the task
                   that returned.

    :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                    instance, containing the traceback (if any).

    The return value of this handler is ignored.

.. method:: on_failure(self, exc, task_id, args, kwargs, einfo)

    This is run by the worker when the task fails.

    :param exc: The exception raised by the task.
    :param task_id: Unique id of the failed task.
    :param args: Original arguments for the task that failed.
    :param kwargs: Original keyword arguments for the task
                       that failed.

    :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                           instance, containing the traceback.

    The return value of this handler is ignored.

.. method:: on_retry(self, exc, task_id, args, kwargs, einfo)

    This is run by the worker when the task is to be retried.

    :param exc: The exception sent to :meth:`~@Task.retry`.
    :param task_id: Unique id of the retried task.
    :param args: Original arguments for the retried task.
    :param kwargs: Original keyword arguments for the retried task.

    :keyword einfo: :class:`~billiard.einfo.ExceptionInfo`
                    instance, containing the traceback.

    The return value of this handler is ignored.

.. method:: on_success(self, retval, task_id, args, kwargs)

    Run by the worker if the task executes successfully.

    :param retval: The return value of the task.
    :param task_id: Unique id of the executed task.
    :param args: Original arguments for the executed task.
    :param kwargs: Original keyword arguments for the executed task.

    The return value of this handler is ignored.

.. _task-requests-and-custom-requests:

请求和自定义请求
----------------------------

Requests and custom requests

.. tab:: 中文

.. tab:: 英文

Upon receiving a message to run a task, the `worker <guide-workers>`:ref:
creates a `request <celery.worker.request.Request>`:class: to represent such
demand.

Custom task classes may override which request class to use by changing the
attribute `celery.app.task.Task.Request`:attr:.  You may either assign the
custom request class itself, or its fully qualified name.

The request has several responsibilities.  Custom request classes should cover
them all -- they are responsible to actually run and trace the task.  We
strongly recommend to inherit from `celery.worker.request.Request`:class:.

When using the `pre-forking worker <worker-concurrency>`:ref:, the methods
`~celery.worker.request.Request.on_timeout`:meth: and
`~celery.worker.request.Request.on_failure`:meth: are executed in the main
worker process.  An application may leverage such facility to detect failures
which are not detected using `celery.app.task.Task.on_failure`:meth:.

As an example, the following custom request detects and logs hard time
limits, and other failures.

.. code-block:: python

   import logging
   from celery import Task
   from celery.worker.request import Request

   logger = logging.getLogger('my.package')

   class MyRequest(Request):
       'A minimal custom request to log failures and hard time limits.'

       def on_timeout(self, soft, timeout):
           super(MyRequest, self).on_timeout(soft, timeout)
           if not soft:
              logger.warning(
                  'A hard timeout was enforced for task %s',
                  self.task.name
              )

       def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
           super().on_failure(
               exc_info,
               send_failed_event=send_failed_event,
               return_ok=return_ok
           )
           logger.warning(
               'Failure detected for task %s',
               self.task.name
           )

   class MyTask(Task):
       Request = MyRequest  # you can use a FQN 'my.package:MyRequest'

   @app.task(base=MyTask)
   def some_longrunning_task():
       # use your imagination


.. _task-how-they-work:

工作原理
============

How it works

.. tab:: 中文

.. tab:: 英文

Here come the technical details. This part isn't something you need to know,
but you may be interested.

All defined tasks are listed in a registry. The registry contains
a list of task names and their task classes. You can investigate this registry
yourself:

.. code-block:: pycon

    >>> from proj.celery import app
    >>> app.tasks
    {'celery.chord_unlock':
        <@task: celery.chord_unlock>,
     'celery.backend_cleanup':
        <@task: celery.backend_cleanup>,
     'celery.chord':
        <@task: celery.chord>}

This is the list of tasks built into Celery. Note that tasks
will only be registered when the module they're defined in is imported.

The default loader imports any modules listed in the
:setting:`imports` setting.

The :meth:`@task` decorator is responsible for registering your task
in the applications task registry.

When tasks are sent, no actual function code is sent with it, just the name
of the task to execute. When the worker then receives the message it can look
up the name in its task registry to find the execution code.

This means that your workers should always be updated with the same software
as the client. This is a drawback, but the alternative is a technical
challenge that's yet to be solved.

.. _task-best-practices:

技巧和最佳实践
=======================

Tips and Best Practices

.. tab:: 中文

.. tab:: 英文

.. _task-ignore_results:

忽略不需要的结果
-----------------------------

Ignore results you don't want

.. tab:: 中文

.. tab:: 英文

If you don't care about the results of a task, be sure to set the
:attr:`~@Task.ignore_result` option, as storing results
wastes time and resources.

.. code-block:: python

    @app.task(ignore_result=True)
    def mytask():
        something()

Results can even be disabled globally using the :setting:`task_ignore_result`
setting.

.. versionadded::4.2

Results can be enabled/disabled on a per-execution basis, by passing the ``ignore_result`` boolean parameter,
when calling ``apply_async``.

.. code-block:: python

    @app.task
    def mytask(x, y):
        return x + y

    # No result will be stored
    result = mytask.apply_async((1, 2), ignore_result=True)
    print(result.get()) # -> None

    # Result will be stored
    result = mytask.apply_async((1, 2), ignore_result=False)
    print(result.get()) # -> 3

By default tasks will *not ignore results* (``ignore_result=False``) when a result backend is configured.


The option precedence order is the following:

1. Global :setting:`task_ignore_result`
2. :attr:`~@Task.ignore_result` option
3. Task execution option ``ignore_result``

更多优化技巧
----------------------

More optimization tips

.. tab:: 中文

.. tab:: 英文

You find additional optimization tips in the
:ref:`Optimizing Guide <guide-optimizing>`.

.. _task-synchronous-subtasks:

避免启动同步子任务
------------------------------------

Avoid launching synchronous subtasks

.. tab:: 中文

.. tab:: 英文

Having a task wait for the result of another task is really inefficient,
and may even cause a deadlock if the worker pool is exhausted.

Make your design asynchronous instead, for example by using *callbacks*.

**Bad**:

.. code-block:: python

    @app.task
    def update_page_info(url):
        page = fetch_page.delay(url).get()
        info = parse_page.delay(page).get()
        store_page_info.delay(url, info)

    @app.task
    def fetch_page(url):
        return myhttplib.get(url)

    @app.task
    def parse_page(page):
        return myparser.parse_document(page)

    @app.task
    def store_page_info(url, info):
        return PageInfo.objects.create(url, info)


**Good**:

.. code-block:: python

    def update_page_info(url):
        # fetch_page -> parse_page -> store_page
        chain = fetch_page.s(url) | parse_page.s() | store_page_info.s(url)
        chain()

    @app.task()
    def fetch_page(url):
        return myhttplib.get(url)

    @app.task()
    def parse_page(page):
        return myparser.parse_document(page)

    @app.task(ignore_result=True)
    def store_page_info(info, url):
        PageInfo.objects.create(url=url, info=info)


Here I instead created a chain of tasks by linking together
different :func:`~celery.signature`'s.
You can read about chains and other powerful constructs
at :ref:`designing-workflows`.

By default Celery will not allow you to run subtasks synchronously within a task,
but in rare or extreme cases you might need to do so.
**WARNING**:
enabling subtasks to run synchronously is not recommended!

.. code-block:: python

    @app.task
    def update_page_info(url):
        page = fetch_page.delay(url).get(disable_sync_subtasks=False)
        info = parse_page.delay(page).get(disable_sync_subtasks=False)
        store_page_info.delay(url, info)

    @app.task
    def fetch_page(url):
        return myhttplib.get(url)

    @app.task
    def parse_page(page):
        return myparser.parse_document(page)

    @app.task
    def store_page_info(url, info):
        return PageInfo.objects.create(url, info)


.. _task-performance-and-strategies:

性能和策略
==========================

Performance and Strategies

.. tab:: 中文

.. tab:: 英文

.. _task-granularity:

粒度
-----------

Granularity

.. tab:: 中文

.. tab:: 英文

The task granularity is the amount of computation needed by each subtask.
In general it is better to split the problem up into many small tasks rather
than have a few long running tasks.

With smaller tasks you can process more tasks in parallel and the tasks
won't run long enough to block the worker from processing other waiting tasks.

However, executing a task does have overhead. A message needs to be sent, data
may not be local, etc. So if the tasks are too fine-grained the
overhead added probably removes any benefit.

.. seealso::

    The book `Art of Concurrency`_ has a section dedicated to the topic
    of task granularity [AOC1]_.

.. _`Art of Concurrency`: http://oreilly.com/catalog/9780596521547

.. [AOC1] Breshears, Clay. Section 2.2.1, "The Art of Concurrency".
   O'Reilly Media, Inc. May 15, 2009. ISBN-13 978-0-596-52153-0.

.. _task-data-locality:

数据本地性
-------------

Data locality

.. tab:: 中文

.. tab:: 英文

The worker processing the task should be as close to the data as
possible. The best would be to have a copy in memory, the worst would be a
full transfer from another continent.

If the data is far away, you could try to run another worker at location, or
if that's not possible - cache often used data, or preload data you know
is going to be used.

The easiest way to share data between workers is to use a distributed cache
system, like `memcached`_.

.. seealso::

    The paper `Distributed Computing Economics`_ by Jim Gray is an excellent
    introduction to the topic of data locality.

.. _`Distributed Computing Economics`:
    http://research.microsoft.com/pubs/70001/tr-2003-24.pdf

.. _`memcached`: http://memcached.org/

.. _task-state:

状态
-----

State

.. tab:: 中文

.. tab:: 英文

Since Celery is a distributed system, you can't know which process, or
on what machine the task will be executed. You can't even know if the task will
run in a timely manner.

The ancient async sayings tells us that “asserting the world is the
responsibility of the task”. What this means is that the world view may
have changed since the task was requested, so the task is responsible for
making sure the world is how it should be;  If you have a task
that re-indexes a search engine, and the search engine should only be
re-indexed at maximum every 5 minutes, then it must be the tasks
responsibility to assert that, not the callers.

Another gotcha is Django model objects. They shouldn't be passed on as
arguments to tasks. It's almost always better to re-fetch the object from
the database when the task is running instead,  as using old data may lead
to race conditions.

Imagine the following scenario where you have an article and a task
that automatically expands some abbreviations in it:

.. code-block:: python

    class Article(models.Model):
        title = models.CharField()
        body = models.TextField()

    @app.task
    def expand_abbreviations(article):
        article.body.replace('MyCorp', 'My Corporation')
        article.save()

First, an author creates an article and saves it, then the author
clicks on a button that initiates the abbreviation task:

.. code-block:: pycon

    >>> article = Article.objects.get(id=102)
    >>> expand_abbreviations.delay(article)

Now, the queue is very busy, so the task won't be run for another 2 minutes.
In the meantime another author makes changes to the article, so
when the task is finally run, the body of the article is reverted to the old
version because the task had the old body in its argument.

Fixing the race condition is easy, just use the article id instead, and
re-fetch the article in the task body:

.. code-block:: python

    @app.task
    def expand_abbreviations(article_id):
        article = Article.objects.get(id=article_id)
        article.body.replace('MyCorp', 'My Corporation')
        article.save()

.. code-block:: pycon

    >>> expand_abbreviations.delay(article_id)

There might even be performance benefits to this approach, as sending large
messages may be expensive.

.. _task-database-transactions:

数据库事务
---------------------

Database transactions

.. tab:: 中文

.. tab:: 英文

Let's have a look at another example:

.. code-block:: python

    from django.db import transaction
    from django.http import HttpResponseRedirect

    @transaction.atomic
    def create_article(request):
        article = Article.objects.create()
        expand_abbreviations.delay(article.pk)
        return HttpResponseRedirect('/articles/')

This is a Django view creating an article object in the database,
then passing the primary key to a task. It uses the `transaction.atomic`
decorator, that will commit the transaction when the view returns, or
roll back if the view raises an exception.

There is a race condition because transactions are atomic. This means the article object is not persisted to the database until after the view function returns a response. If the asynchronous task starts executing before the transaction is committed, it may attempt to query the article object before it exists. To prevent this, we need to ensure that the transaction is committed before triggering the task.

The solution is to use
:meth:`~celery.contrib.django.task.DjangoTask.delay_on_commit` instead:

.. code-block:: python

    from django.db import transaction
    from django.http import HttpResponseRedirect

    @transaction.atomic
    def create_article(request):
        article = Article.objects.create()
        expand_abbreviations.delay_on_commit(article.pk)
        return HttpResponseRedirect('/articles/')

This method was added in Celery 5.4. It's a shortcut that uses Django's
``on_commit`` callback to launch your Celery task once all transactions
have been committed successfully.

使用 Celery 5.4 及以下版本
~~~~~~~~~~~~~~~~

With Celery <5.4

.. tab:: 中文

.. tab:: 英文

If you're using an older version of Celery, you can replicate this behaviour
using the Django callback directly as follows:

.. code-block:: python

    import functools
    from django.db import transaction
    from django.http import HttpResponseRedirect

    @transaction.atomic
    def create_article(request):
        article = Article.objects.create()
        transaction.on_commit(
            functools.partial(expand_abbreviations.delay, article.pk)
        )
        return HttpResponseRedirect('/articles/')

.. note::
    ``on_commit`` is available in Django 1.9 and above, if you are using a
    version prior to that then the `django-transaction-hooks`_ library
    adds support for this.

.. _`django-transaction-hooks`: https://github.com/carljm/django-transaction-hooks

.. _task-example:

示例
=======

Example

.. tab:: 中文

.. tab:: 英文

Let's take a real world example: a blog where comments posted need to be
filtered for spam. When the comment is created, the spam filter runs in the
background, so the user doesn't have to wait for it to finish.

I have a Django blog application allowing comments
on blog posts. I'll describe parts of the models/views and tasks for this
application.

``blog/models.py``
------------------

The comment model looks like this:

.. code-block:: python

    from django.db import models
    from django.utils.translation import ugettext_lazy as _


    class Comment(models.Model):
        name = models.CharField(_('name'), max_length=64)
        email_address = models.EmailField(_('email address'))
        homepage = models.URLField(_('home page'),
                                   blank=True, verify_exists=False)
        comment = models.TextField(_('comment'))
        pub_date = models.DateTimeField(_('Published date'),
                                        editable=False, auto_add_now=True)
        is_spam = models.BooleanField(_('spam?'),
                                      default=False, editable=False)

        class Meta:
            verbose_name = _('comment')
            verbose_name_plural = _('comments')


In the view where the comment is posted, I first write the comment
to the database, then I launch the spam filter task in the background.

.. _task-example-blog-views:

``blog/views.py``
-----------------

.. code-block:: python

    from django import forms
    from django.http import HttpResponseRedirect
    from django.template.context import RequestContext
    from django.shortcuts import get_object_or_404, render_to_response

    from blog import tasks
    from blog.models import Comment


    class CommentForm(forms.ModelForm):

        class Meta:
            model = Comment


    def add_comment(request, slug, template_name='comments/create.html'):
        post = get_object_or_404(Entry, slug=slug)
        remote_addr = request.META.get('REMOTE_ADDR')

        if request.method == 'post':
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                comment = form.save()
                # Check spam asynchronously.
                tasks.spam_filter.delay(comment_id=comment.id,
                                        remote_addr=remote_addr)
                return HttpResponseRedirect(post.get_absolute_url())
        else:
            form = CommentForm()

        context = RequestContext(request, {'form': form})
        return render_to_response(template_name, context_instance=context)


To filter spam in comments I use `Akismet`_, the service
used to filter spam in comments posted to the free blog platform
`Wordpress`. `Akismet`_ is free for personal use, but for commercial use you
need to pay. You have to sign up to their service to get an API key.

To make API calls to `Akismet`_ I use the `akismet.py`_ library written by
`Michael Foord`_.

.. _task-example-blog-tasks:

``blog/tasks.py``
-----------------

.. code-block:: python

    from celery import Celery

    from akismet import Akismet

    from django.core.exceptions import ImproperlyConfigured
    from django.contrib.sites.models import Site

    from blog.models import Comment


    app = Celery(broker='amqp://')


    @app.task
    def spam_filter(comment_id, remote_addr=None):
        logger = spam_filter.get_logger()
        logger.info('Running spam filter for comment %s', comment_id)

        comment = Comment.objects.get(pk=comment_id)
        current_domain = Site.objects.get_current().domain
        akismet = Akismet(settings.AKISMET_KEY, 'http://{0}'.format(domain))
        if not akismet.verify_key():
            raise ImproperlyConfigured('Invalid AKISMET_KEY')


        is_spam = akismet.comment_check(user_ip=remote_addr,
                            comment_content=comment.comment,
                            comment_author=comment.name,
                            comment_author_email=comment.email_address)
        if is_spam:
            comment.is_spam = True
            comment.save()

        return is_spam

.. _`Akismet`: http://akismet.com/faq/
.. _`akismet.py`: http://www.voidspace.org.uk/downloads/akismet.py
.. _`Michael Foord`: http://www.voidspace.org.uk/
.. _`exponential backoff`: https://en.wikipedia.org/wiki/Exponential_backoff
.. _`jitter`: https://en.wikipedia.org/wiki/Jitter
.. _`Pydantic`: https://docs.pydantic.dev/
