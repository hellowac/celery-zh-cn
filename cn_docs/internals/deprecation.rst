.. _deprecation-timeline:

==============================
Celery 弃用时间表
==============================

Celery Deprecation Time-line


.. _deprecations-v5.0:

5.0 版移除内容
========================

Removals for version 5.0

旧版任务 API
------------

Old Task API

.. _deprecate-compat-task-modules:

兼容任务模块
~~~~~~~~~~~~~~~~~~~

Compat Task Modules

.. tab:: 中文

    - 模块 ``celery.decorators`` 将被移除：  
      这意味着你需要将如下代码：

      .. code-block:: python

          from celery.decorators import task

      修改为：

      .. code-block:: python

          from celery import task

    - 模块 ``celery.task`` 将被移除  
      这意味着你应该将如下代码：

      .. code-block:: python

          from celery.task import task

      修改为：

      .. code-block:: python

          from celery import shared_task

      —— 以及：

      .. code-block:: python

          from celery import task

      修改为：

      .. code-block:: python

          from celery import shared_task

      —— 还有：

      .. code-block:: python

          from celery.task import Task

      修改为：

      .. code-block:: python

          from celery import Task

    请注意，新的 :class:`~celery.Task` 类不再使用 :func:`classmethod` 修饰以下方法：

    - delay
    - apply_async
    - retry
    - apply
    - AsyncResult
    - subtask

    这也意味着你不能再直接通过类调用这些方法，而是需要先实例化任务：

    .. code-block:: pycon

        >>> MyTask.delay()          # 不再可用

        >>> MyTask().delay()        # 正确用法！

.. tab:: 英文

    - Module ``celery.decorators`` will be removed:
        This means you need to change:

        .. code-block:: python

            from celery.decorators import task

        Into:

        .. code-block:: python

            from celery import task

    - Module ``celery.task`` will be removed
        This means you should change:

        .. code-block:: python

            from celery.task import task

        into:

        .. code-block:: python

            from celery import shared_task

        -- and:

        .. code-block:: python

            from celery import task

        into:

        .. code-block:: python

            from celery import shared_task

        -- and:

        .. code-block:: python

            from celery.task import Task

        into:

        .. code-block:: python

            from celery import Task


    Note that the new :class:`~celery.Task` class no longer
    uses :func:`classmethod` for these methods:

    - delay
    - apply_async
    - retry
    - apply
    - AsyncResult
    - subtask

    This also means that you can't call these methods directly
    on the class, but have to instantiate the task first:

    .. code-block:: pycon

        >>> MyTask.delay()          # NO LONGER WORKS


        >>> MyTask().delay()        # WORKS!


任务属性
---------------

Task attributes

.. tab:: 中文
    
    以下任务属性已弃用，必须通过 :setting:`task_routes` 来设置：
    
    - ``queue``
    - ``exchange``
    - ``exchange_type``
    - ``routing_key``
    - ``delivery_mode``
    - ``priority``

.. tab:: 英文

    The task attributes:

    - ``queue``
    - ``exchange``
    - ``exchange_type``
    - ``routing_key``
    - ``delivery_mode``
    - ``priority``

    is deprecated and must be set by :setting:`task_routes` instead.


待移除模块
-----------------

Modules to Remove

.. tab:: 中文
    
    - ``celery.execute``  
      
      此模块仅包含 ``send_task``：应改为使用 :attr:`@send_task`。
    
    - ``celery.decorators``  
      
      参见 :ref:`deprecate-compat-task-modules`
    
    - ``celery.log``  
      
      改为使用 :attr:`@log`
    
    - ``celery.messaging``  
      
      改为使用 :attr:`@amqp`
    
    - ``celery.registry``  
      
      改为使用 :mod:`celery.app.registry`
    
    - ``celery.task.control``  
      
      改为使用 :attr:`@control`
    
    - ``celery.task.schedules``  
      
      改为使用 :mod:`celery.schedules`
    
    - ``celery.task.chords``  
      
      改为使用 :func:`celery.chord`

.. tab:: 英文

    - ``celery.execute``

      This module only contains ``send_task``: this must be replaced with
      :attr:`@send_task` instead.

    - ``celery.decorators``

      See :ref:`deprecate-compat-task-modules`

    - ``celery.log``

      Use :attr:`@log` instead.

    - ``celery.messaging``

      Use :attr:`@amqp` instead.

    - ``celery.registry``

      Use :mod:`celery.app.registry` instead.

    - ``celery.task.control``

      Use :attr:`@control` instead.

    - ``celery.task.schedules``

      Use :mod:`celery.schedules` instead.

    - ``celery.task.chords``

      Use :func:`celery.chord` instead.

设置
--------

Settings

``BROKER`` 设置
~~~~~~~~~~~~~~~~~~~

``BROKER`` Settings

=====================================  =====================================
**Setting name**                       **Replace with**
=====================================  =====================================
``BROKER_HOST``                        :setting:`broker_url`
``BROKER_PORT``                        :setting:`broker_url`
``BROKER_USER``                        :setting:`broker_url`
``BROKER_PASSWORD``                    :setting:`broker_url`
``BROKER_VHOST``                       :setting:`broker_url`
=====================================  =====================================

``REDIS`` 结果后端设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``REDIS`` Result Backend Settings

=====================================  =====================================
**Setting name**                       **Replace with**
=====================================  =====================================
``CELERY_REDIS_HOST``                  :setting:`result_backend`
``CELERY_REDIS_PORT``                  :setting:`result_backend`
``CELERY_REDIS_DB``                    :setting:`result_backend`
``CELERY_REDIS_PASSWORD``              :setting:`result_backend`
``REDIS_HOST``                         :setting:`result_backend`
``REDIS_PORT``                         :setting:`result_backend`
``REDIS_DB``                           :setting:`result_backend`
``REDIS_PASSWORD``                     :setting:`result_backend`
=====================================  =====================================


Task_sent 信号
----------------

Task_sent signal

.. tab:: 中文

    :signal:`task_sent` 信号将在 4.0 版本中移除。  
    请改用 :signal:`before_task_publish` 和 :signal:`after_task_publish` 信号。

.. tab:: 英文

    The :signal:`task_sent` signal will be removed in version 4.0.
    Please use the :signal:`before_task_publish` and :signal:`after_task_publish`
    signals instead.

结果
------

Result

.. tab:: 中文

    适用于：:class:`~celery.result.AsyncResult`,  
    :class:`~celery.result.EagerResult`：

    - ``Result.wait()`` -> ``Result.get()``

    - ``Result.task_id()`` -> ``Result.id``

    - ``Result.status`` -> ``Result.state``

.. tab:: 英文

    Apply to: :class:`~celery.result.AsyncResult`, :class:`~celery.result.EagerResult`:

    - ``Result.wait()`` -> ``Result.get()``

    - ``Result.task_id()`` -> ``Result.id``

    - ``Result.status`` -> ``Result.state``.

.. _deprecations-v3.1:


设置
~~~~~~~~

Settings

=====================================  =====================================
**Setting name**                       **Replace with**
=====================================  =====================================
``CELERY_AMQP_TASK_RESULT_EXPIRES``    :setting:`result_expires`
=====================================  =====================================



.. _deprecations-v2.0:

2.0 版移除内容
========================

Removals for version 2.0

.. tab:: 中文

    * 以下配置项将被移除：

    =====================================  =====================================
    **配置项名称**                         **替代项**
    =====================================  =====================================
    `CELERY_AMQP_CONSUMER_QUEUES`          `task_queues`
    `CELERY_AMQP_CONSUMER_QUEUES`          `task_queues`
    `CELERY_AMQP_EXCHANGE`                 `task_default_exchange`
    `CELERY_AMQP_EXCHANGE_TYPE`            `task_default_exchange_type`
    `CELERY_AMQP_CONSUMER_ROUTING_KEY`     `task_queues`
    `CELERY_AMQP_PUBLISHER_ROUTING_KEY`    `task_default_routing_key`
    =====================================  =====================================

    * 未包含类名的 :envvar:`CELERY_LOADER` 定义

      例如：`celery.loaders.default`，必须包含类名： `celery.loaders.default.Loader`

    * :meth:`TaskSet.run`。请改为使用 :meth:`celery.task.base.TaskSet.apply_async`。


.. tab:: 英文

    * The following settings will be removed:

    =====================================  =====================================
    **Setting name**                       **Replace with**
    =====================================  =====================================
    `CELERY_AMQP_CONSUMER_QUEUES`          `task_queues`
    `CELERY_AMQP_CONSUMER_QUEUES`          `task_queues`
    `CELERY_AMQP_EXCHANGE`                 `task_default_exchange`
    `CELERY_AMQP_EXCHANGE_TYPE`            `task_default_exchange_type`
    `CELERY_AMQP_CONSUMER_ROUTING_KEY`     `task_queues`
    `CELERY_AMQP_PUBLISHER_ROUTING_KEY`    `task_default_routing_key`
    =====================================  =====================================

    * :envvar:`CELERY_LOADER` definitions without class name.

      For example,, `celery.loaders.default`, needs to include the class name: `celery.loaders.default.Loader`.

    * :meth:`TaskSet.run`. Use :meth:`celery.task.base.TaskSet.apply_async` instead.
