.. _configuration:

============================
配置和默认值
============================

Configuration and defaults

.. tab:: 中文

    本文档描述了可用的配置选项。

    如果你正在使用默认的加载器，则必须创建一个 :file:`celeryconfig.py` 模块，
    并确保该模块在 Python 路径上可用。

.. tab:: 英文

    This document describes the configuration options available.

    If you're using the default loader, you must create the :file:`celeryconfig.py`
    module and make sure it's available on the Python path.




.. _conf-example:

示例配置文件
==========================

Example configuration file

.. tab:: 中文

    以下是一个配置文件示例，供你入门使用。
    它应当包含运行一个基础 Celery 设置所需的全部内容。

    .. code-block:: python

        ## Broker 设置。
        broker_url = 'amqp://guest:guest@localhost:5672//'

        # 当 Celery worker 启动时要导入的模块列表。
        imports = ('myapp.tasks',)

        ## 使用数据库存储任务状态和结果。
        result_backend = 'db+sqlite:///results.db'

        task_annotations = {'tasks.add': {'rate_limit': '10/s'}}


.. tab:: 英文

    This is an example configuration file to get you started.
    It should contain all you need to run a basic Celery set-up.

    .. code-block:: python

        ## Broker settings.
        broker_url = 'amqp://guest:guest@localhost:5672//'

        # List of modules to import when the Celery worker starts.
        imports = ('myapp.tasks',)

        ## Using the database to store task state and results.
        result_backend = 'db+sqlite:///results.db'

        task_annotations = {'tasks.add': {'rate_limit': '10/s'}}


.. _conf-old-settings-map:

新的小写设置
======================

New lowercase settings

.. tab:: 中文

    在 4.0 版本中，引入了新的小写配置项及配置结构。

    与早期版本相比，主要的区别在于配置项名称从大写变为小写，
    以及一些前缀被重命名，例如 ``celery_beat_`` 改为 ``beat_``，
    ``celeryd_`` 改为 ``worker_``，并且大多数顶层的 ``celery_`` 配置项
    都被移动到了新的 ``task_`` 前缀下。

    .. warning::

        Celery 仍然能够读取旧版的配置文件，直到 Celery 6.0。
        此后将不再支持旧的配置方式。
        我们提供了 ``celery upgrade`` 命令，用于处理大量的升级情况
        （包括 :ref:`Django <latentcall-django-admonition>`）。

        请尽快迁移到新的配置结构。

.. tab:: 英文

    Version 4.0 introduced new lower case settings and setting organization.

    The major difference between previous versions, apart from the lower case
    names, are the renaming of some prefixes, like ``celery_beat_`` to ``beat_``,
    ``celeryd_`` to ``worker_``, and most of the top level ``celery_`` settings
    have been moved into a new  ``task_`` prefix.

    .. warning::

        Celery will still be able to read old configuration files until Celery 6.0.
        Afterwards, support for the old configuration files will be removed.
        We provide the ``celery upgrade`` command that should handle
        plenty of cases (including :ref:`Django <latentcall-django-admonition>`).

        Please migrate to the new configuration scheme as soon as possible.


============================================= ==============================================
**Setting name**                              **Replace with**
============================================= ==============================================
``CELERY_ACCEPT_CONTENT``                     :setting:`accept_content`
``CELERY_ENABLE_UTC``                         :setting:`enable_utc`
``CELERY_IMPORTS``                            :setting:`imports`
``CELERY_INCLUDE``                            :setting:`include`
``CELERY_TIMEZONE``                           :setting:`timezone`
``CELERYBEAT_MAX_LOOP_INTERVAL``              :setting:`beat_max_loop_interval`
``CELERYBEAT_SCHEDULE``                       :setting:`beat_schedule`
``CELERYBEAT_SCHEDULER``                      :setting:`beat_scheduler`
``CELERYBEAT_SCHEDULE_FILENAME``              :setting:`beat_schedule_filename`
``CELERYBEAT_SYNC_EVERY``                     :setting:`beat_sync_every`
``BROKER_URL``                                :setting:`broker_url`
``BROKER_TRANSPORT``                          :setting:`broker_transport`
``BROKER_TRANSPORT_OPTIONS``                  :setting:`broker_transport_options`
``BROKER_CONNECTION_TIMEOUT``                 :setting:`broker_connection_timeout`
``BROKER_CONNECTION_RETRY``                   :setting:`broker_connection_retry`
``BROKER_CONNECTION_MAX_RETRIES``             :setting:`broker_connection_max_retries`
``BROKER_FAILOVER_STRATEGY``                  :setting:`broker_failover_strategy`
``BROKER_HEARTBEAT``                          :setting:`broker_heartbeat`
``BROKER_LOGIN_METHOD``                       :setting:`broker_login_method`
``BROKER_NATIVE_DELAYED_DELIVERY_QUEUE_TYPE`` :setting:`broker_native_delayed_delivery_queue_type`
``BROKER_POOL_LIMIT``                         :setting:`broker_pool_limit`
``BROKER_USE_SSL``                            :setting:`broker_use_ssl`
``CELERY_CACHE_BACKEND``                      :setting:`cache_backend`
``CELERY_CACHE_BACKEND_OPTIONS``              :setting:`cache_backend_options`
``CASSANDRA_COLUMN_FAMILY``                   :setting:`cassandra_table`
``CASSANDRA_ENTRY_TTL``                       :setting:`cassandra_entry_ttl`
``CASSANDRA_KEYSPACE``                        :setting:`cassandra_keyspace`
``CASSANDRA_PORT``                            :setting:`cassandra_port`
``CASSANDRA_READ_CONSISTENCY``                :setting:`cassandra_read_consistency`
``CASSANDRA_SERVERS``                         :setting:`cassandra_servers`
``CASSANDRA_WRITE_CONSISTENCY``               :setting:`cassandra_write_consistency`
``CASSANDRA_OPTIONS``                         :setting:`cassandra_options`
``S3_ACCESS_KEY_ID``                          :setting:`s3_access_key_id`
``S3_SECRET_ACCESS_KEY``                      :setting:`s3_secret_access_key`
``S3_BUCKET``                                 :setting:`s3_bucket`
``S3_BASE_PATH``                              :setting:`s3_base_path`
``S3_ENDPOINT_URL``                           :setting:`s3_endpoint_url`
``S3_REGION``                                 :setting:`s3_region`
``CELERY_COUCHBASE_BACKEND_SETTINGS``         :setting:`couchbase_backend_settings`
``CELERY_ARANGODB_BACKEND_SETTINGS``          :setting:`arangodb_backend_settings`
``CELERY_MONGODB_BACKEND_SETTINGS``           :setting:`mongodb_backend_settings`
``CELERY_EVENT_QUEUE_EXPIRES``                :setting:`event_queue_expires`
``CELERY_EVENT_QUEUE_TTL``                    :setting:`event_queue_ttl`
``CELERY_EVENT_QUEUE_PREFIX``                 :setting:`event_queue_prefix`
``CELERY_EVENT_SERIALIZER``                   :setting:`event_serializer`
``CELERY_REDIS_DB``                           :setting:`redis_db`
``CELERY_REDIS_HOST``                         :setting:`redis_host`
``CELERY_REDIS_MAX_CONNECTIONS``              :setting:`redis_max_connections`
``CELERY_REDIS_USERNAME``                     :setting:`redis_username`
``CELERY_REDIS_PASSWORD``                     :setting:`redis_password`
``CELERY_REDIS_PORT``                         :setting:`redis_port`
``CELERY_REDIS_BACKEND_USE_SSL``              :setting:`redis_backend_use_ssl`
``CELERY_RESULT_BACKEND``                     :setting:`result_backend`
``CELERY_MAX_CACHED_RESULTS``                 :setting:`result_cache_max`
``CELERY_MESSAGE_COMPRESSION``                :setting:`result_compression`
``CELERY_RESULT_EXCHANGE``                    :setting:`result_exchange`
``CELERY_RESULT_EXCHANGE_TYPE``               :setting:`result_exchange_type`
``CELERY_RESULT_EXPIRES``                     :setting:`result_expires`
``CELERY_RESULT_PERSISTENT``                  :setting:`result_persistent`
``CELERY_RESULT_SERIALIZER``                  :setting:`result_serializer`
``CELERY_RESULT_DBURI``                       Use :setting:`result_backend` instead.
``CELERY_RESULT_ENGINE_OPTIONS``              :setting:`database_engine_options`
``[...]_DB_SHORT_LIVED_SESSIONS``             :setting:`database_short_lived_sessions`
``CELERY_RESULT_DB_TABLE_NAMES``              :setting:`database_db_names`
``CELERY_SECURITY_CERTIFICATE``               :setting:`security_certificate`
``CELERY_SECURITY_CERT_STORE``                :setting:`security_cert_store`
``CELERY_SECURITY_KEY``                       :setting:`security_key`
``CELERY_SECURITY_KEY_PASSWORD``              :setting:`security_key_password`
``CELERY_ACKS_LATE``                          :setting:`task_acks_late`
``CELERY_ACKS_ON_FAILURE_OR_TIMEOUT``         :setting:`task_acks_on_failure_or_timeout`
``CELERY_TASK_ALWAYS_EAGER``                  :setting:`task_always_eager`
``CELERY_ANNOTATIONS``                        :setting:`task_annotations`
``CELERY_COMPRESSION``                        :setting:`task_compression`
``CELERY_CREATE_MISSING_QUEUES``              :setting:`task_create_missing_queues`
``CELERY_DEFAULT_DELIVERY_MODE``              :setting:`task_default_delivery_mode`
``CELERY_DEFAULT_EXCHANGE``                   :setting:`task_default_exchange`
``CELERY_DEFAULT_EXCHANGE_TYPE``              :setting:`task_default_exchange_type`
``CELERY_DEFAULT_QUEUE``                      :setting:`task_default_queue`
``CELERY_DEFAULT_QUEUE_TYPE``                 :setting:`task_default_queue_type`
``CELERY_DEFAULT_RATE_LIMIT``                 :setting:`task_default_rate_limit`
``CELERY_DEFAULT_ROUTING_KEY``                :setting:`task_default_routing_key`
``CELERY_EAGER_PROPAGATES``                   :setting:`task_eager_propagates`
``CELERY_IGNORE_RESULT``                      :setting:`task_ignore_result`
``CELERY_PUBLISH_RETRY``                      :setting:`task_publish_retry`
``CELERY_PUBLISH_RETRY_POLICY``               :setting:`task_publish_retry_policy`
``CELERY_QUEUES``                             :setting:`task_queues`
``CELERY_ROUTES``                             :setting:`task_routes`
``CELERY_SEND_SENT_EVENT``                    :setting:`task_send_sent_event`
``CELERY_TASK_SERIALIZER``                    :setting:`task_serializer`
``CELERYD_SOFT_TIME_LIMIT``                   :setting:`task_soft_time_limit`
``CELERY_TASK_TRACK_STARTED``                 :setting:`task_track_started`
``CELERY_TASK_REJECT_ON_WORKER_LOST``         :setting:`task_reject_on_worker_lost`
``CELERYD_TIME_LIMIT``                        :setting:`task_time_limit`
``CELERY_ALLOW_ERROR_CB_ON_CHORD_HEADER``     :setting:`task_allow_error_cb_on_chord_header`
``CELERYD_AGENT``                             :setting:`worker_agent`
``CELERYD_AUTOSCALER``                        :setting:`worker_autoscaler`
``CELERYD_CONCURRENCY``                       :setting:`worker_concurrency`
``CELERYD_CONSUMER``                          :setting:`worker_consumer`
``CELERY_WORKER_DIRECT``                      :setting:`worker_direct`
``CELERY_DISABLE_RATE_LIMITS``                :setting:`worker_disable_rate_limits`
``CELERY_ENABLE_REMOTE_CONTROL``              :setting:`worker_enable_remote_control`
``CELERYD_HIJACK_ROOT_LOGGER``                :setting:`worker_hijack_root_logger`
``CELERYD_LOG_COLOR``                         :setting:`worker_log_color`
``CELERY_WORKER_LOG_FORMAT``                  :setting:`worker_log_format`
``CELERYD_WORKER_LOST_WAIT``                  :setting:`worker_lost_wait`
``CELERYD_MAX_TASKS_PER_CHILD``               :setting:`worker_max_tasks_per_child`
``CELERYD_POOL``                              :setting:`worker_pool`
``CELERYD_POOL_PUTLOCKS``                     :setting:`worker_pool_putlocks`
``CELERYD_POOL_RESTARTS``                     :setting:`worker_pool_restarts`
``CELERYD_PREFETCH_MULTIPLIER``               :setting:`worker_prefetch_multiplier`
``CELERYD_ENABLE_PREFETCH_COUNT_REDUCTION``   :setting:`worker_enable_prefetch_count_reduction`
``CELERYD_REDIRECT_STDOUTS``                  :setting:`worker_redirect_stdouts`
``CELERYD_REDIRECT_STDOUTS_LEVEL``            :setting:`worker_redirect_stdouts_level`
``CELERY_SEND_EVENTS``                        :setting:`worker_send_task_events`
``CELERYD_STATE_DB``                          :setting:`worker_state_db`
``CELERY_WORKER_TASK_LOG_FORMAT``             :setting:`worker_task_log_format`
``CELERYD_TIMER``                             :setting:`worker_timer`
``CELERYD_TIMER_PRECISION``                   :setting:`worker_timer_precision`
``CELERYD_DETECT_QUORUM_QUEUES``              :setting:`worker_detect_quorum_queues`
============================================= ==============================================

配置指令
========================

Configuration Directives

.. _conf-datetime:

常规设置
----------------

General settings

.. setting:: accept_content

``accept_content``
~~~~~~~~~~~~~~~~~~

Default: ``{'json'}``  (set, list, or tuple).

.. tab:: 中文

    允许的内容类型/序列化器白名单。

    如果收到的消息不在此列表中，则
    该消息将被丢弃并产生错误。

    默认情况下，仅启用 json，但可以添加任何内容类型，
    包括 pickle 和 yaml；在这种情况下，确保
    未经授权的人员无法访问您的代理。
    有关更多信息，请参见 :ref:`guide-security`。

    示例::

        # 使用序列化器名称
        accept_content = ['json']

        # 或者使用实际的内容类型（MIME）
        accept_content = ['application/json']

.. tab:: 英文

    A white-list of content-types/serializers to allow.

    If a message is received that's not in this list then
    the message will be discarded with an error.

    By default only json is enabled but any content type can be added,
    including pickle and yaml; when this is the case make sure
    untrusted parties don't have access to your broker.
    See :ref:`guide-security` for more.

    Example::

        # using serializer name
        accept_content = ['json']

        # or the actual content-type (MIME)
        accept_content = ['application/json']

.. setting:: result_accept_content

``result_accept_content``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``None`` (can be set, list or tuple).

.. versionadded:: 4.3

.. tab:: 中文

    结果后端的内容类型/序列化器白名单。

    如果收到的消息不在此列表中，则
    该消息将被丢弃并产生错误。

    默认情况下，它与 ``accept_content`` 使用相同的序列化器。
    但是，可以为结果后端的接受内容指定不同的序列化器。
    通常，当使用签名消息且结果以未签名形式存储在结果后端时，
    需要这样做。
    有关更多信息，请参见 :ref:`guide-security`。

    示例::

        # 使用序列化器名称
        result_accept_content = ['json']

        # 或者使用实际的内容类型（MIME）
        result_accept_content = ['application/json']

.. tab:: 英文

    A white-list of content-types/serializers to allow for the result backend.

    If a message is received that's not in this list then
    the message will be discarded with an error.

    By default it is the same serializer as ``accept_content``.
    However, a different serializer for accepted content of the result backend
    can be specified.
    Usually this is needed if signed messaging is used and the result is stored
    unsigned in the result backend.
    See :ref:`guide-security` for more.

    Example::

        # using serializer name
        result_accept_content = ['json']

        # or the actual content-type (MIME)
        result_accept_content = ['application/json']

时间和日期设置
----------------------

Time and date settings

.. setting:: enable_utc

``enable_utc``
~~~~~~~~~~~~~~

.. versionadded:: 2.5

.. tab:: 中文

    默认值：自版本 3.0 起默认启用。

    如果启用，消息中的日期和时间将转换为使用
    UTC 时区。

    请注意，运行低于 2.5 版本的 Celery 的工作进程会将所有消息假设为本地
    时区，因此只有当所有工作进程都已升级时才启用此选项。


.. tab:: 英文

    Default: Enabled by default since version 3.0.

    If enabled dates and times in messages will be converted to use
    the UTC timezone.

    Note that workers running Celery versions below 2.5 will assume a local
    timezone for all messages, so only enable if all workers have been
    upgraded.

.. setting:: timezone

``timezone``
~~~~~~~~~~~~

.. versionadded:: 2.5

Default: ``"UTC"``.

.. tab:: 中文

    配置 Celery 使用自定义时区。
    时区值可以是 `ZoneInfo <https://docs.python.org/3/library/zoneinfo.html>`_
    库支持的任何时区。

    如果未设置，则使用 UTC 时区。为了向后兼容，
    还有一个 :setting:`enable_utc` 设置，当此设置为
    false 时，使用系统本地时区。

.. tab:: 英文

    Configure Celery to use a custom time zone.
    The timezone value can be any time zone supported by the `ZoneInfo <https://docs.python.org/3/library/zoneinfo.html>`_
    library.

    If not set the UTC timezone is used. For backwards compatibility
    there's also a :setting:`enable_utc` setting, and when this is set
    to false the system local timezone is used instead.

.. _conf-tasks:

任务设置
-------------

Task settings

.. setting:: task_annotations

``task_annotations``
~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.5

Default: :const:`None`.

.. tab:: 中文

    此设置可用于从配置中重写任何任务属性。该设置可以是一个字典，或是一个任务过滤器的注解对象列表，返回一个要更改的属性映射。

    这将更改 ``tasks.add`` 任务的 ``rate_limit`` 属性：

    .. code-block:: python

        task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

    或者更改所有任务的相同属性：

    .. code-block:: python

        task_annotations = {'*': {'rate_limit': '10/s'}}

    您还可以更改方法，例如 ``on_failure`` 处理器：

    .. code-block:: python

        def my_on_failure(self, exc, task_id, args, kwargs, einfo):
            print('哦，不！任务失败: {0!r}'.format(exc))

        task_annotations = {'*': {'on_failure': my_on_failure}}

    如果您需要更多灵活性，您可以使用对象而不是字典来选择要注解的任务：

    .. code-block:: python

        class MyAnnotate:

            def annotate(self, task):
                if task.name.startswith('tasks.'):
                    return {'rate_limit': '10/s'}

        task_annotations = (MyAnnotate(), {other,})

.. tab:: 英文

    This setting can be used to rewrite any task attribute from the
    configuration. The setting can be a dict, or a list of annotation
    objects that filter for tasks and return a map of attributes
    to change.

    This will change the ``rate_limit`` attribute for the ``tasks.add``
    task:

    .. code-block:: python

        task_annotations = {'tasks.add': {'rate_limit': '10/s'}}

    or change the same for all tasks:

    .. code-block:: python

        task_annotations = {'*': {'rate_limit': '10/s'}}

    You can change methods too, for example the ``on_failure`` handler:

    .. code-block:: python

        def my_on_failure(self, exc, task_id, args, kwargs, einfo):
            print('Oh no! Task failed: {0!r}'.format(exc))

        task_annotations = {'*': {'on_failure': my_on_failure}}

    If you need more flexibility then you can use objects
    instead of a dict to choose the tasks to annotate:

    .. code-block:: python

        class MyAnnotate:

            def annotate(self, task):
                if task.name.startswith('tasks.'):
                    return {'rate_limit': '10/s'}

        task_annotations = (MyAnnotate(), {other,})

.. setting:: task_compression

``task_compression``
~~~~~~~~~~~~~~~~~~~~

Default: :const:`None`

.. tab:: 中文

    任务消息的默认压缩格式。
    可以是 ``gzip``， ``bzip2`` （如果可用），或在 Kombu 压缩注册表中注册的任何自定义压缩方案。

    默认情况下，发送的是未压缩的消息。

.. tab:: 英文

    Default compression used for task messages.
    Can be ``gzip``, ``bzip2`` (if available), or any custom
    compression schemes registered in the Kombu compression registry.

    The default is to send uncompressed messages.

.. setting:: task_protocol

``task_protocol``
~~~~~~~~~~~~~~~~~

.. versionadded:: 4.0

Default: 2 (since 4.0).

.. tab:: 中文

    设置用于发送任务的默认任务消息协议版本。
    支持协议：1 和 2。

    协议 2 支持 3.1.24 和 4.x+。

.. tab:: 英文

    Set the default task message protocol version used to send tasks.
    Supports protocols: 1 and 2.

    Protocol 2 is supported by 3.1.24 and 4.x+.

.. setting:: task_serializer

``task_serializer``
~~~~~~~~~~~~~~~~~~~

Default: ``"json"`` (since 4.0, earlier: pickle).

.. tab:: 中文

    一个字符串，标识用于的默认序列化方法。可以是
    `json` （默认）， `pickle`， `yaml`， `msgpack`，或任何已注册的自定义序列化
    方法，注册在 :mod:`kombu.serialization.registry` 中。

    .. seealso::

        :ref:`calling-serializers`。

.. tab:: 英文

    A string identifying the default serialization method to use. Can be
    `json` (default), `pickle`, `yaml`, `msgpack`, or any custom serialization
    methods that have been registered with :mod:`kombu.serialization.registry`.

    .. seealso::

        :ref:`calling-serializers`.

.. setting:: task_publish_retry

``task_publish_retry``
~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.2

Default: Enabled.

.. tab:: 中文

    决定在发生连接丢失或其他连接错误的情况下，是否重试发布任务消息。
    另请参见 :setting:`task_publish_retry_policy`。

.. tab:: 英文

    Decides if publishing task messages will be retried in the case
    of connection loss or other connection errors.
    See also :setting:`task_publish_retry_policy`.

.. setting:: task_publish_retry_policy

``task_publish_retry_policy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.2

Default: See :ref:`calling-retry`.

.. tab:: 中文

    定义在连接丢失或其他连接错误的情况下重试发布任务消息时的默认策略。

.. tab:: 英文

    Defines the default policy when retrying publishing a task message in
    the case of connection loss or other connection errors.

.. _conf-task-execution:

任务执行设置
-----------------------

Task execution settings

.. setting:: task_always_eager

``task_always_eager``
~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    如果此项为 :const:`True`，所有任务将通过本地执行，直到
    任务返回为止。``apply_async()`` 和 ``Task.delay()`` 将返回
    一个 :class:`~celery.result.EagerResult` 实例，该实例模拟
    :class:`~celery.result.AsyncResult` 的 API
    和行为，但结果已经被评估。

    也就是说，任务将被本地执行，而不是发送到
    队列中。

.. tab:: 英文

    If this is :const:`True`, all tasks will be executed locally by blocking until
    the task returns. ``apply_async()`` and ``Task.delay()`` will return
    an :class:`~celery.result.EagerResult` instance, that emulates the API
    and behavior of :class:`~celery.result.AsyncResult`, except the result
    is already evaluated.

    That is, tasks will be executed locally instead of being sent to
    the queue.

.. setting:: task_eager_propagates

``task_eager_propagates``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    如果此项为 :const:`True`，则急切执行的任务（通过 `task.apply()` 应用，
    或启用了 :setting:`task_always_eager` 设置时），将
    传播异常。

    这相当于始终以 ``throw=True`` 运行 ``apply()``。

.. tab:: 英文

    If this is :const:`True`, eagerly executed tasks (applied by `task.apply()`,
    or when the :setting:`task_always_eager` setting is enabled), will
    propagate exceptions.

    It's the same as always running ``apply()`` with ``throw=True``.

.. setting:: task_store_eager_result

``task_store_eager_result``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.1

Default: Disabled.

.. tab:: 中文

    如果此项为 :const:`True`，且 :setting:`task_always_eager` 为 :const:`True`
    且 :setting:`task_ignore_result` 为 :const:`False`，
    急切执行任务的结果将被保存到后端。

    默认情况下，即使 :setting:`task_always_eager` 设置为 :const:`True`
    且 :setting:`task_ignore_result` 设置为 :const:`False`，
    结果也不会被保存。

.. tab:: 英文

    If this is :const:`True` and :setting:`task_always_eager` is :const:`True`
    and :setting:`task_ignore_result` is :const:`False`,
    the results of eagerly executed tasks will be saved to the backend.

    By default, even with :setting:`task_always_eager` set to :const:`True`
    and :setting:`task_ignore_result` set to :const:`False`,
    the result will not be saved.

.. setting:: task_remote_tracebacks

``task_remote_tracebacks``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    如果启用，任务结果将包含工作者的堆栈信息，以便在重新抛出任务错误时进行追踪。

    这需要 :pypi:`tblib` 库，可以通过
    :command:`pip` 安装：

    .. code-block:: console

        $ pip install celery[tblib]

    有关如何组合多个扩展要求的信息，请参见 :ref:`bundles`。

.. tab:: 英文

    If enabled task results will include the workers stack when re-raising
    task errors.

    This requires the :pypi:`tblib` library, that can be installed using
    :command:`pip`:

    .. code-block:: console

        $ pip install celery[tblib]

    See :ref:`bundles` for information on combining multiple extension
    requirements.

.. setting:: task_ignore_result

``task_ignore_result``
~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    是否存储任务返回值（墓碑/tombstones）。如果您仍然希望存储错误，而不是成功返回值，可以设置 :setting:`task_store_errors_even_if_ignored` 。

.. tab:: 英文

    Whether to store the task return values or not (tombstones). If you still want to store errors, just not successful return values, you can set :setting:`task_store_errors_even_if_ignored`.

.. setting:: task_store_errors_even_if_ignored

``task_store_errors_even_if_ignored``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    如果设置了此项，即使 :attr:`Task.ignore_result <celery.app.task.Task.ignore_result>` 已启用，工作者也会将所有任务错误存储在结果存储中。

.. tab:: 英文

    If set, the worker stores all task errors in the result store even if
    :attr:`Task.ignore_result <celery.app.task.Task.ignore_result>` is on.

.. setting:: task_track_started

``task_track_started``
~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    如果 :const:`True`，任务在被工作者执行时将报告其状态为“已开始”。默认值为 :const:`False`，因为正常行为是不报告如此细粒度的状态。任务通常是挂起、已完成或等待重试。拥有“已开始”状态对长时间运行的任务特别有用，因为需要报告当前正在运行的任务。

.. tab:: 英文

    If :const:`True` the task will report its status as 'started' when the
    task is executed by a worker. The default value is :const:`False` as
    the normal behavior is to not report that level of granularity. Tasks
    are either pending, finished, or waiting to be retried. Having a 'started'
    state can be useful for when there are long running tasks and there's a
    need to report what task is currently running.

.. setting:: task_time_limit

``task_time_limit``
~~~~~~~~~~~~~~~~~~~

Default: No time limit.

.. tab:: 中文

    任务硬时间限制，单位为秒。当任务处理超过此时间时，处理该任务的工作者将被终止，并由一个新的工作者替换。

.. tab:: 英文

    Task hard time limit in seconds. The worker processing the task will
    be killed and replaced with a new one when this is exceeded.

.. setting:: task_allow_error_cb_on_chord_header

``task_allow_error_cb_on_chord_header``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.3

Default: Disabled.

.. tab:: 中文

    启用此标志将允许将错误回调链接到一个 Chord 头部，默认情况下，使用 :code:`link_error()` 时不会进行链接，且如果头部中的任何任务失败，将阻止 Chord 的主体执行。

    考虑以下画布，在该标志禁用时（默认行为）：

    .. code-block:: python

        header = group([t1, t2])
        body = t3
        c = chord(header, body)
        c.link_error(error_callback_sig)

    如果 *任何* 头部任务失败（ :code:`t1` 或 :code:`t2` ），默认情况下，Chord 主体（:code:`t3`）将 **不执行**，并且 :code:`error_callback_sig` 将 **仅调用一次** （针对主体）。

    启用此标志将改变上述行为：

    1. :code:`error_callback_sig` 将被链接到 :code:`t1` 和 :code:`t2` （以及 :code:`t3`）。
    2. 如果 *任何* 头部任务失败，:code:`error_callback_sig` 将 **针对每个失败的头部任务调用一次**，并且也会针对 :code:`body` 调用一次（即使主体没有执行）。

    现在，考虑启用此标志后的画布：

    .. code-block:: python

        header = group([failingT1, failingT2])
        body = t3
        c = chord(header, body)
        c.link_error(error_callback_sig)

    如果 *所有* 头部任务失败（:code:`failingT1` 和 :code:`failingT2`），那么 Chord 主体（:code:`t3`）将 **不执行**，并且 :code:`error_callback_sig` 将被 **调用 3 次** （两次针对头部，一次针对主体）。

    最后，考虑启用此标志的画布：

    .. code-block:: python

        header = group([failingT1, failingT2])
        body = t3
        upgraded_chord = chain(header, body)
        upgraded_chord.link_error(error_callback_sig)

    此画布的行为将与之前的完全相同，因为 :code:`chain` 会在内部被升级为 :code:`chord`。

.. tab:: 英文

    Enabling this flag will allow linking an error callback to a chord header,
    which by default will not link when using :code:`link_error()`, and preventing
    from the chord's body to execute if any of the tasks in the header fails.

    Consider the following canvas with the flag disabled (default behavior):

    .. code-block:: python

        header = group([t1, t2])
        body = t3
        c = chord(header, body)
        c.link_error(error_callback_sig)

    If *any* of the header tasks failed (:code:`t1` or :code:`t2`), by default, the chord body (:code:`t3`) would **not execute**, and :code:`error_callback_sig` will be called **once** (for the body).

    Enabling this flag will change the above behavior by:

    1. :code:`error_callback_sig` will be linked to :code:`t1` and :code:`t2` (as well as :code:`t3`).
    2. If *any* of the header tasks failed, :code:`error_callback_sig` will be called **for each** failed header task **and** the :code:`body` (even if the body didn't run).

    Consider now the following canvas with the flag enabled:

    .. code-block:: python

        header = group([failingT1, failingT2])
        body = t3
        c = chord(header, body)
        c.link_error(error_callback_sig)

    If *all* of the header tasks failed (:code:`failingT1` and :code:`failingT2`), then the chord body (:code:`t3`) would **not execute**, and :code:`error_callback_sig` will be called **3 times** (two times for the header and one time for the body).

    Lastly, consider the following canvas with the flag enabled:

    .. code-block:: python

        header = group([failingT1, failingT2])
        body = t3
        upgraded_chord = chain(header, body)
        upgraded_chord.link_error(error_callback_sig)

    This canvas will behave exactly the same as the previous one, since the :code:`chain` will be upgraded to a :code:`chord` internally.

.. setting:: task_soft_time_limit

``task_soft_time_limit``
~~~~~~~~~~~~~~~~~~~~~~~~

Default: No soft time limit.

.. tab:: 中文

    任务软时间限制，单位为秒。

    当超过软时间限制时，将引发 :exc:`~@SoftTimeLimitExceeded` 异常。例如，任务可以捕获此异常并在硬时间限制到达之前进行清理：

    .. code-block:: python

        from celery.exceptions import SoftTimeLimitExceeded

        @app.task
        def mytask():
            try:
                return do_work()
            except SoftTimeLimitExceeded:
                cleanup_in_a_hurry()

.. tab:: 英文

    Task soft time limit in seconds.

    The :exc:`~@SoftTimeLimitExceeded` exception will be
    raised when this is exceeded. For example, the task can catch this to
    clean up before the hard time limit comes:

    .. code-block:: python

        from celery.exceptions import SoftTimeLimitExceeded

        @app.task
        def mytask():
            try:
                return do_work()
            except SoftTimeLimitExceeded:
                cleanup_in_a_hurry()

.. setting:: task_acks_late

``task_acks_late``
~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    延迟确认意味着任务消息将在任务执行 **后** 被确认，而不是 *在执行前* （默认行为）。

    .. seealso::

        FAQ: :ref:`faq-acks_late-vs-retry`。

.. tab:: 英文

    Late ack means the task messages will be acknowledged **after** the task
    has been executed, not *right before* (the default behavior).

    .. seealso::

        FAQ: :ref:`faq-acks_late-vs-retry`.

.. setting:: task_acks_on_failure_or_timeout

``task_acks_on_failure_or_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Enabled

.. tab:: 中文

    启用此项后，所有任务的消息即使失败或超时，也会被确认。

    此设置仅适用于在任务执行 **后** 被确认的任务，并且仅当 :setting:`task_acks_late` 启用时生效。

.. tab:: 英文

    When enabled messages for all tasks will be acknowledged even if they
    fail or time out.

    Configuring this setting only applies to tasks that are
    acknowledged **after** they have been executed and only if
    :setting:`task_acks_late` is enabled.

.. setting:: task_reject_on_worker_lost

``task_reject_on_worker_lost``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    即使 :setting:`task_acks_late` 启用，当执行任务的工作者进程突然退出或收到信号（例如 :sig:`KILL` / :sig:`INT` 等）时，工作者仍会确认任务。

    将此设置为 `true` 允许将消息重新排队，从而使任务由同一工作者或其他工作者重新执行。

    .. warning::

        启用此项可能会导致消息循环；确保了解你在做什么。

.. tab:: 英文

    Even if :setting:`task_acks_late` is enabled, the worker will
    acknowledge tasks when the worker process executing them abruptly
    exits or is signaled (e.g., :sig:`KILL`/:sig:`INT`, etc).

    Setting this to true allows the message to be re-queued instead,
    so that the task will execute again by the same worker, or another
    worker.

    .. warning::

        Enabling this can cause message loops; make sure you know
        what you're doing.

.. setting:: task_default_rate_limit

``task_default_rate_limit``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: No rate limit.

.. tab:: 中文

    任务的全局默认速率限制。

    该值用于没有自定义速率限制的任务。

    .. seealso::

        :setting:`worker_disable_rate_limits` 设置可以禁用所有速率限制。

.. tab:: 英文

    The global default rate limit for tasks.

    This value is used for tasks that doesn't have a custom rate limit

    .. seealso::

        The :setting:`worker_disable_rate_limits` setting can
        disable all rate limits.

.. _conf-result-backend:

任务结果后端设置
----------------------------

Task result backend settings

.. setting:: result_backend

``result_backend``
~~~~~~~~~~~~~~~~~~

Default: No result backend enabled by default.

.. tab:: 中文

    用于存储任务结果（墓碑）的后端。
    可以是以下之一：

    * ``rpc``
        通过 AMQP 消息返回结果。
        请参见 :ref:`conf-rpc-result-backend`。

    * ``database``
        使用 `SQLAlchemy`_ 支持的关系型数据库。
        请参见 :ref:`conf-database-result-backend`。

    * ``redis``
        使用 `Redis`_ 存储结果。
        请参见 :ref:`conf-redis-result-backend`。

    * ``cache``
        使用 `Memcached`_ 存储结果。
        请参见 :ref:`conf-cache-result-backend`。

    * ``mongodb``
        使用 `MongoDB`_ 存储结果。
        请参见 :ref:`conf-mongodb-result-backend`。

    * ``cassandra``
        使用 `Cassandra`_ 存储结果。
        请参见 :ref:`conf-cassandra-result-backend`。

    * ``elasticsearch``
        使用 `Elasticsearch`_ 存储结果。
        请参见 :ref:`conf-elasticsearch-result-backend`。

    * ``ironcache``
        使用 `IronCache`_ 存储结果。
        请参见 :ref:`conf-ironcache-result-backend`。

    * ``couchbase``
        使用 `Couchbase`_ 存储结果。
        请参见 :ref:`conf-couchbase-result-backend`。

    * ``arangodb``
        使用 `ArangoDB`_ 存储结果。
        请参见 :ref:`conf-arangodb-result-backend`。

    * ``couchdb``
        使用 `CouchDB`_ 存储结果。
        请参见 :ref:`conf-couchdb-result-backend`。

    * ``cosmosdbsql (experimental)``
        使用 `CosmosDB`_ PaaS 存储结果。
        请参见 :ref:`conf-cosmosdbsql-result-backend`。

    * ``filesystem``
        使用共享目录存储结果。
        请参见 :ref:`conf-filesystem-result-backend`。

    * ``consul``
        使用 `Consul`_ K/V 存储结果。
        请参见 :ref:`conf-consul-result-backend`。

    * ``azureblockblob``
        使用 `AzureBlockBlob`_ PaaS 存储结果。
        请参见 :ref:`conf-azureblockblob-result-backend`。

    * ``s3``
        使用 `S3`_ 存储结果。
        请参见 :ref:`conf-s3-result-backend`。

    * ``gcs``
        使用 `GCS`_ 存储结果。
        请参见 :ref:`conf-gcs-result-backend`。

    .. warning::

        虽然 AMQP 结果后端非常高效，但您必须确保只接收一次相同的结果。请参阅 :doc:`userguide/calling`。

.. tab:: 英文

    The backend used to store task results (tombstones).
    Can be one of the following:

    * ``rpc``
        Send results back as AMQP messages
        See :ref:`conf-rpc-result-backend`.

    * ``database``
        Use a relational database supported by `SQLAlchemy`_.
        See :ref:`conf-database-result-backend`.

    * ``redis``
        Use `Redis`_ to store the results.
        See :ref:`conf-redis-result-backend`.

    * ``cache``
        Use `Memcached`_ to store the results.
        See :ref:`conf-cache-result-backend`.

    * ``mongodb``
        Use `MongoDB`_ to store the results.
        See :ref:`conf-mongodb-result-backend`.

    * ``cassandra``
        Use `Cassandra`_ to store the results.
        See :ref:`conf-cassandra-result-backend`.

    * ``elasticsearch``
        Use `Elasticsearch`_ to store the results.
        See :ref:`conf-elasticsearch-result-backend`.

    * ``ironcache``
        Use `IronCache`_ to store the results.
        See :ref:`conf-ironcache-result-backend`.

    * ``couchbase``
        Use `Couchbase`_ to store the results.
        See :ref:`conf-couchbase-result-backend`.

    * ``arangodb``
        Use `ArangoDB`_ to store the results.
        See :ref:`conf-arangodb-result-backend`.

    * ``couchdb``
        Use `CouchDB`_ to store the results.
        See :ref:`conf-couchdb-result-backend`.

    * ``cosmosdbsql (experimental)``
        Use the `CosmosDB`_ PaaS to store the results.
        See :ref:`conf-cosmosdbsql-result-backend`.

    * ``filesystem``
        Use a shared directory to store the results.
        See :ref:`conf-filesystem-result-backend`.

    * ``consul``
        Use the `Consul`_ K/V store to store the results
        See :ref:`conf-consul-result-backend`.

    * ``azureblockblob``
        Use the `AzureBlockBlob`_ PaaS store to store the results
        See :ref:`conf-azureblockblob-result-backend`.

    * ``s3``
        Use the `S3`_ to store the results
        See :ref:`conf-s3-result-backend`.

    * ``gcs``
        Use the `GCS`_ to store the results
        See :ref:`conf-gcs-result-backend`.

    .. warning::

        While the AMQP result backend is very efficient, you must make sure
        you only receive the same result once. See :doc:`userguide/calling`).

.. _`SQLAlchemy`: http://sqlalchemy.org
.. _`Memcached`: http://memcached.org
.. _`MongoDB`: http://mongodb.org
.. _`Redis`: https://redis.io
.. _`Cassandra`: http://cassandra.apache.org/
.. _`Elasticsearch`: https://aws.amazon.com/elasticsearch-service/
.. _`IronCache`: http://www.iron.io/cache
.. _`CouchDB`: http://www.couchdb.com/
.. _`CosmosDB`: https://azure.microsoft.com/en-us/services/cosmos-db/
.. _`Couchbase`: https://www.couchbase.com/
.. _`ArangoDB`: https://www.arangodb.com/
.. _`Consul`: https://consul.io/
.. _`AzureBlockBlob`: https://azure.microsoft.com/en-us/services/storage/blobs/
.. _`S3`: https://aws.amazon.com/s3/
.. _`GCS`: https://cloud.google.com/storage/


.. setting:: result_backend_always_retry

``result_backend_always_retry``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`False`

.. tab:: 中文

    如果启用，后端将在可恢复异常发生时尝试重试，而不是传播异常。
    它将在两次重试之间使用指数退避的睡眠时间。

.. tab:: 英文

    If enable, backend will try to retry on the event of recoverable exceptions instead of propagating the exception.
    It will use an exponential backoff sleep time between 2 retries.


.. setting:: result_backend_max_sleep_between_retries_ms

``result_backend_max_sleep_between_retries_ms``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 10000

.. tab:: 中文

    此项指定两次后端操作重试之间的最大睡眠时间。

.. tab:: 英文

    This specifies the maximum sleep time between two backend operation retry.


.. setting:: result_backend_base_sleep_between_retries_ms

``result_backend_base_sleep_between_retries_ms``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 10

.. tab:: 中文

    此项指定两次后端操作重试之间的基础睡眠时间。

.. tab:: 英文

    This specifies the base amount of sleep time between two backend operation retry.


.. setting:: result_backend_max_retries

``result_backend_max_retries``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Inf

.. tab:: 中文

    这是在发生可恢复异常时的最大重试次数。

.. tab:: 英文

    This is the maximum of retries in case of recoverable exceptions.


.. setting:: result_backend_thread_safe

``result_backend_thread_safe``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: False

.. tab:: 中文

    如果为 True，则后端对象将在多个线程之间共享。
    这对于使用共享连接池而不是为每个线程创建一个连接可能很有用。

.. tab:: 英文

    If True, then the backend object is shared across threads.
    This may be useful for using a shared connection pool instead of creating
    a connection for every thread.


.. setting:: result_backend_transport_options

``result_backend_transport_options``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    一个传递给底层传输的附加选项字典。

    请参阅你的传输用户手册以了解支持的选项（如果有的话）。

    例如设置可见性超时（Redis 和 SQS 传输支持）：

    .. code-block:: python

        result_backend_transport_options = {'visibility_timeout': 18000}  # 5小时

.. tab:: 英文

    A dict of additional options passed to the underlying transport.

    See your transport user manual for supported options (if any).

    Example setting the visibility timeout (supported by Redis and SQS
    transports):

    .. code-block:: python

        result_backend_transport_options = {'visibility_timeout': 18000}  # 5 hours



.. setting:: result_serializer

``result_serializer``
~~~~~~~~~~~~~~~~~~~~~

Default: ``json`` since 4.0 (earlier: pickle).

.. tab:: 中文

    结果序列化格式。

    请参阅 :ref:`calling-serializers` 获取关于支持的序列化格式的更多信息。

.. tab:: 英文

    Result serialization format.

    See :ref:`calling-serializers` for information about supported
    serialization formats.

.. setting:: result_compression

``result_compression``
~~~~~~~~~~~~~~~~~~~~~~

Default: No compression.

.. tab:: 中文

    用于任务结果的可选压缩方法。
    支持与 :setting:`task_compression` 设置相同的选项。

.. tab:: 英文

    Optional compression method used for task results.
    Supports the same options as the :setting:`task_compression` setting.

.. setting:: result_extended

``result_extended``
~~~~~~~~~~~~~~~~~~~~~~

Default: ``False``

.. tab:: 中文

    启用后，可以将扩展的任务结果属性（名称、参数、关键字参数、工作者、重试次数、队列、投递信息）写入后端。

.. tab:: 英文

    Enables extended task result attributes (name, args, kwargs, worker,
    retries, queue, delivery_info) to be written to backend.

.. setting:: result_expires

``result_expires``
~~~~~~~~~~~~~~~~~~

Default: Expire after 1 day.

.. tab:: 中文

    存储的任务墓碑将在此时间（以秒为单位，或 :class:`~datetime.timedelta` 对象）后被删除。

    内建的定期任务将在此时间后删除结果（``celery.backend_cleanup``），前提是启用了 ``celery beat``。该任务每天早上4点运行。

    如果设置为 :const:`None` 或 0，表示结果永远不会过期（具体取决于后端的规范）。

    .. note::

        目前，这仅适用于 AMQP、数据库、缓存、Couchbase 和 Redis 后端。

        当使用数据库后端时，必须运行 ``celery beat``，以便结果能够过期。


.. tab:: 英文

    Time (in seconds, or a :class:`~datetime.timedelta` object) for when after
    stored task tombstones will be deleted.

    A built-in periodic task will delete the results after this time
    (``celery.backend_cleanup``), assuming that ``celery beat`` is
    enabled. The task runs daily at 4am.

    A value of :const:`None` or 0 means results will never expire (depending
    on backend specifications).

    .. note::

        For the moment this only works with the AMQP, database, cache, Couchbase,
        and Redis backends.

        When using the database backend, ``celery beat`` must be
        running for the results to be expired.

.. setting:: result_cache_max

``result_cache_max``
~~~~~~~~~~~~~~~~~~~~

Default: Disabled by default.

.. tab:: 中文

    启用客户端结果缓存。

    这对于旧版已弃用的 'amqp' 后端非常有用，因为当一个结果实例被消费后，结果将不再可用。

    这是在旧结果被逐出之前要缓存的结果总数。
    值为 0 或 None 表示没有限制，值为 :const:`-1` 将禁用缓存。

    默认情况下禁用。

.. tab:: 英文

    Enables client caching of results.

    This can be useful for the old deprecated
    'amqp' backend where the result is unavailable as soon as one result instance
    consumes it.

    This is the total number of results to cache before older results are evicted.
    A value of 0 or None means no limit, and a value of :const:`-1`
    will disable the cache.

    Disabled by default.

.. setting:: result_chord_join_timeout

``result_chord_join_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 3.0.

.. tab:: 中文

    在加入一个组的结果时的超时时间（秒，int/float）。

.. tab:: 英文

    The timeout in seconds (int/float) when joining a group's results within a chord.

.. setting:: result_chord_retry_interval

``result_chord_retry_interval``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 1.0.

.. tab:: 中文

    重试和弦任务的默认间隔。

.. tab:: 英文

    Default interval for retrying chord tasks.

.. setting:: override_backends

``override_backends``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled by default.

.. tab:: 中文

    实现后端的类的路径。

    允许覆盖后端实现。
    如果你需要存储执行任务的附加元数据、覆盖重试策略等，这可能会很有用。

    示例：

    .. code-block:: python

        override_backends = {"db": "custom_module.backend.class"}

.. tab:: 英文

    Path to class that implements backend.

    Allows to override backend implementation.
    This can be useful if you need to store additional metadata about executed tasks,
    override retry policies, etc.

    Example:

    .. code-block:: python

        override_backends = {"db": "custom_module.backend.class"}

.. _conf-database-result-backend:

数据库后端设置
-------------------------

Database backend settings

数据库 URL 示例
~~~~~~~~~~~~~~~~~~~~~

Database URL Examples

.. tab:: 中文

    要使用数据库后端，必须使用连接 URL 配置 :setting:`result_backend` 设置，并使用 ``db+`` 前缀：

    .. code-block:: python

        result_backend = 'db+scheme://user:password@host:port/dbname'

    示例::

        # sqlite（文件名）
        result_backend = 'db+sqlite:///results.sqlite'

        # mysql
        result_backend = 'db+mysql://scott:tiger@localhost/foo'

        # postgresql
        result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'

        # oracle
        result_backend = 'db+oracle://scott:tiger@127.0.0.1:1521/sidname'

    请参阅 `支持的数据库`_ 获取支持的数据库表格，
    并参阅 `连接字符串`_ 获取有关连接字符串的更多信息（即 URI 中 ``db+`` 前缀之后的部分）。


.. tab:: 英文

    To use the database backend you have to configure the
    :setting:`result_backend` setting with a connection URL and the ``db+``
    prefix:

    .. code-block:: python

        result_backend = 'db+scheme://user:password@host:port/dbname'

    Examples::

        # sqlite (filename)
        result_backend = 'db+sqlite:///results.sqlite'

        # mysql
        result_backend = 'db+mysql://scott:tiger@localhost/foo'

        # postgresql
        result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'

        # oracle
        result_backend = 'db+oracle://scott:tiger@127.0.0.1:1521/sidname'

    Please see `Supported Databases`_ for a table of supported databases,
    and `Connection String`_ for more information about connection
    strings (this is the part of the URI that comes after the ``db+`` prefix).

.. _`Supported Databases`:
    http://www.sqlalchemy.org/docs/core/engines.html#supported-databases

.. _`Connection String`:
    http://www.sqlalchemy.org/docs/core/engines.html#database-urls

.. _`支持的数据库`:
    https://hellowac.github.io/sqlalchemy-zh-cn/core/engines.html#supported-dbapis

.. _`连接字符串`:
    https://hellowac.github.io/sqlalchemy-zh-cn/core/engines.html#url

.. setting:: database_create_tables_at_setup

``database_create_tables_at_setup``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.5.0

Default: True by default.

.. tab:: 中文

    - 如果为 `True`，Celery 将在设置时创建数据库中的表。
    - 如果为 `False`，Celery 将延迟创建表，即等待第一个任务执行后再创建表。

    .. note::
        在 Celery 5.5 之前，表是延迟创建的，即相当于将 `database_create_tables_at_setup` 设置为 False。

.. tab:: 英文

    - If `True`, Celery will create the tables in the database during setup.
    - If `False`, Celery will create the tables lazily, i.e. wait for the first task to be executed before creating the tables.

    .. note::
        Before celery 5.5, the tables were created lazily i.e. it was equivalent to
        `database_create_tables_at_setup` set to False.

.. setting:: database_engine_options

``database_engine_options``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    要指定额外的 SQLAlchemy 数据库引擎选项，可以使用 :setting:`database_engine_options` 设置::

        # echo 启用 SQLAlchemy 的详细日志记录。
        app.conf.database_engine_options = {'echo': True}

.. tab:: 英文

    To specify additional SQLAlchemy database engine options you can use
    the :setting:`database_engine_options` setting::

        # echo enables verbose logging from SQLAlchemy.
        app.conf.database_engine_options = {'echo': True}

.. setting:: database_short_lived_sessions

``database_short_lived_sessions``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled by default.

.. tab:: 中文

    短生命周期会话默认情况下是禁用的。如果启用，它们可能会大幅降低性能，尤其是在处理大量任务的系统上。这个选项在低流量的 worker 上非常有用，特别是当因数据库连接由于不活跃而变得过时而导致错误时。例如，间歇性的错误如 `(OperationalError) (2006, 'MySQL server has gone away')` 可以通过启用短生命周期会话来修复。此选项仅影响数据库后端。

.. tab:: 英文

    Short lived sessions are disabled by default. If enabled they can drastically reduce
    performance, especially on systems processing lots of tasks. This option is useful
    on low-traffic workers that experience errors as a result of cached database connections
    going stale through inactivity. For example, intermittent errors like
    `(OperationalError) (2006, 'MySQL server has gone away')` can be fixed by enabling
    short lived sessions. This option only affects the database backend.

.. setting:: database_table_schemas

``database_table_schemas``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    当 SQLAlchemy 配置为结果后端时，Celery 会自动创建两个表来存储任务的结果元数据。此设置允许您自定义表的模式：

    .. code-block:: python

        # 为数据库结果后端使用自定义模式。
        database_table_schemas = {
            'task': 'celery',
            'group': 'celery',
        }

.. tab:: 英文

    When SQLAlchemy is configured as the result backend, Celery automatically
    creates two tables to store result meta-data for tasks. This setting allows
    you to customize the schema of the tables:

    .. code-block:: python

        # use custom schema for the database result backend.
        database_table_schemas = {
            'task': 'celery',
            'group': 'celery',
        }

.. setting:: database_table_names

``database_table_names``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    当 SQLAlchemy 配置为结果后端时，Celery 会自动创建两个表来存储任务的结果元数据。此设置允许您自定义表名：

    .. code-block:: python

        # 为数据库结果后端使用自定义表名。
        database_table_names = {
            'task': 'myapp_taskmeta',
            'group': 'myapp_groupmeta',
        }

.. tab:: 英文

    When SQLAlchemy is configured as the result backend, Celery automatically
    creates two tables to store result meta-data for tasks. This setting allows
    you to customize the table names:

    .. code-block:: python

        # use custom table names for the database result backend.
        database_table_names = {
            'task': 'myapp_taskmeta',
            'group': 'myapp_groupmeta',
        }

.. _conf-rpc-result-backend:

RPC 后段设置
--------------------

RPC backend settings

.. setting:: result_persistent

``result_persistent``
~~~~~~~~~~~~~~~~~~~~~

Default: Disabled by default (transient messages).

.. tab:: 中文

    如果设置为 :const:`True`，结果消息将是持久的。这意味着消息在代理重启后不会丢失。

.. tab:: 英文

    If set to :const:`True`, result messages will be persistent. This means the
    messages won't be lost after a broker restart.

示例配置
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    result_backend = 'rpc://'
    result_persistent = False

.. tab:: 中文

    **请注意**：使用此后端可能会触发 ``celery.backends.rpc.BacklogLimitExceeded`` 错误，如果任务墓碑太 *旧* 。

    例如：

    .. code-block:: python

        for i in range(10000):
            r = debug_task.delay()

        print(r.state)  # 这将引发 celery.backends.rpc.BacklogLimitExceeded

.. tab:: 英文

    **Please note**: using this backend could trigger the raise of ``celery.backends.rpc.BacklogLimitExceeded`` if the task tombstone is too *old*.

    E.g.

    .. code-block:: python

        for i in range(10000):
            r = debug_task.delay()

        print(r.state)  # this would raise celery.backends.rpc.BacklogLimitExceeded

.. _conf-cache-result-backend:

缓存后端设置
----------------------

Cache backend settings

.. tab:: 中文

    .. note::

        缓存后端支持 :pypi:`pylibmc` 和 :pypi:`python-memcached` 库。如果未安装 :pypi:`pylibmc`，则使用后者。

    使用单个 Memcached 服务器：

    .. code-block:: python

        result_backend = 'cache+memcached://127.0.0.1:11211/'

    使用多个 Memcached 服务器：

    .. code-block:: python

        result_backend = """
            cache+memcached://172.19.26.240:11211;172.19.26.242:11211/
        """.strip()

    "memory" 后端仅将缓存存储在内存中：

    .. code-block:: python

        result_backend = 'cache'
        cache_backend = 'memory'

.. tab:: 英文

    .. note::

        The cache backend supports the :pypi:`pylibmc` and :pypi:`python-memcached`
        libraries. The latter is used only if :pypi:`pylibmc` isn't installed.

    Using a single Memcached server:

    .. code-block:: python

        result_backend = 'cache+memcached://127.0.0.1:11211/'

    Using multiple Memcached servers:

    .. code-block:: python

        result_backend = """
            cache+memcached://172.19.26.240:11211;172.19.26.242:11211/
        """.strip()

    The "memory" backend stores the cache in memory only:

    .. code-block:: python

        result_backend = 'cache'
        cache_backend = 'memory'

.. setting:: cache_backend_options

``cache_backend_options``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    您可以使用 :setting:`cache_backend_options` 设置来配置 :pypi:`pylibmc` 选项：

    .. code-block:: python

        cache_backend_options = {
            'binary': True,
            'behaviors': {'tcp_nodelay': True},
        }

.. tab:: 英文

    You can set :pypi:`pylibmc` options using the :setting:`cache_backend_options`
    setting:

    .. code-block:: python

        cache_backend_options = {
            'binary': True,
            'behaviors': {'tcp_nodelay': True},
        }

.. setting:: cache_backend

``cache_backend``
~~~~~~~~~~~~~~~~~

.. tab:: 中文

    此设置不再用于 Celery 的内建后端，因为现在可以直接在 :setting:`result_backend` 设置中指定缓存后端。

    .. note::

        :ref:`django-celery-results` 库使用 ``cache_backend`` 来选择 Django 缓存。

.. tab:: 英文

    This setting is no longer used in celery's builtin backends as it's now possible to specify
    the cache backend directly in the :setting:`result_backend` setting.

    .. note::

        The :ref:`django-celery-results` library uses ``cache_backend`` for choosing django caches.

.. _conf-mongodb-result-backend:

MongoDB 后端设置
------------------------

MongoDB backend settings

.. tab:: 中文

    .. note::

        MongoDB 后端需要 :mod:`pymongo` 库：
        http://github.com/mongodb/mongo-python-driver/tree/master

.. tab:: 英文

    .. note::

        The MongoDB backend requires the :mod:`pymongo` library:
        http://github.com/mongodb/mongo-python-driver/tree/master

.. setting:: mongodb_backend_settings

mongodb_backend_settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mongodb_backend_settings

.. tab:: 中文

    这是一个支持以下键的字典：

    * database
        要连接的数据库名称。默认值为 ``celery``。

    * taskmeta_collection
        存储任务元数据的集合名称。默认值为 ``celery_taskmeta``。

    * max_pool_size
        传递给 PyMongo 的 Connection 或 MongoClient 构造函数的 max_pool_size。它是一次保持与 MongoDB 开放的最大 TCP 连接数。如果打开的连接数超过 max_pool_size，套接字将在释放时关闭。默认值为 10。

    * options
        传递给 MongoDB 连接构造函数的附加关键字参数。请参阅 :mod:`pymongo` 文档以查看支持的参数列表。

.. tab:: 英文

    This is a dict supporting the following keys:

    * database
        The database name to connect to. Defaults to ``celery``.

    * taskmeta_collection
        The collection name to store task meta data.
        Defaults to ``celery_taskmeta``.

    * max_pool_size
        Passed as max_pool_size to PyMongo's Connection or MongoClient
        constructor. It is the maximum number of TCP connections to keep
        open to MongoDB at a given time. If there are more open connections
        than max_pool_size, sockets will be closed when they are released.
        Defaults to 10.

    * options
        Additional keyword arguments to pass to the mongodb connection
        constructor.  See the :mod:`pymongo` docs to see a list of arguments
        supported.

.. _example-mongodb-result-config:

示例配置
~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. code-block:: python

    result_backend = 'mongodb://localhost:27017/'
    mongodb_backend_settings = {
        'database': 'mydb',
        'taskmeta_collection': 'my_taskmeta_collection',
    }

.. _conf-redis-result-backend:

Redis 后端设置
----------------------

Redis backend settings

配置后端 URL
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuring the backend URL

.. tab:: 中文

    .. note::

        Redis 后端需要 :pypi:`redis` 库。

        要安装此包，请使用 :command:`pip`：

        .. code-block:: console

            $ pip install celery[redis]

        请参见 :ref:`bundles` 了解有关组合多个扩展要求的信息。

    此后端要求将 :setting:`result_backend`
    设置为 Redis 或 `Redis over TLS`_ URL::

        result_backend = 'redis://username:password@host:port/db'

    例如::

        result_backend = 'redis://localhost/0'

    与此相同::

        result_backend = 'redis://'

    使用 ``rediss://`` 协议通过 TLS 连接 Redis::

        result_backend = 'rediss://username:password@host:port/db?ssl_cert_reqs=required'

    请注意，``ssl_cert_reqs`` 字符串应为 ``required``，
    ``optional`` 或 ``none`` 之一（尽管为了与旧版本的 Celery 向后兼容，该字符串
    也可以是 ``CERT_REQUIRED``、``CERT_OPTIONAL``、``CERT_NONE``，
    但这些值仅适用于 Celery，而不适用于 Redis 本身）。

    如果需要使用 Unix 套接字连接，URL 格式应为::

        result_backend = 'socket:///path/to/redis.sock'

    URL 的各个字段定义如下：

    #. ``username``
        .. versionadded:: 5.1.0

        用于连接数据库的用户名。

        请注意，这仅在 Redis>=6.0 且已安装 py-redis>=3.4.0 时支持。

        如果您使用的是较旧的数据库版本或较旧的客户端版本
        可以省略用户名::

            result_backend = 'redis://:password@host:port/db'

    #. ``password``
        用于连接数据库的密码。

    #. ``host``
        Redis 服务器的主机名或 IP 地址（例如，`localhost`）。

    #. ``port``
        Redis 服务器的端口。默认值为 6379。

    #. ``db``
        要使用的数据库编号。默认值为 0。
        数据库编号可以包括可选的前导斜杠。

    使用 TLS 连接时（协议为 ``rediss://``），可以将 :setting:`broker_use_ssl` 中的所有值作为查询参数传递。证书路径必须进行 URL 编码，且 ``ssl_cert_reqs`` 是必需的。示例：

    .. code-block:: python

        result_backend = 'rediss://:password@host:port/db?\
            ssl_cert_reqs=required\
            &ssl_ca_certs=%2Fvar%2Fssl%2Fmyca.pem\                  # /var/ssl/myca.pem
            &ssl_certfile=%2Fvar%2Fssl%2Fredis-server-cert.pem\     # /var/ssl/redis-server-cert.pem
            &ssl_keyfile=%2Fvar%2Fssl%2Fprivate%2Fworker-key.pem'   # /var/ssl/private/worker-key.pem

    请注意， ``ssl_cert_reqs`` 字符串应为 ``required``，
    ``optional`` 或 ``none`` 之一（尽管为了向后兼容，字符串
    也可以是 ``CERT_REQUIRED``、 ``CERT_OPTIONAL``、 ``CERT_NONE``）。

.. tab:: 英文

    .. note::

        The Redis backend requires the :pypi:`redis` library.

        To install this package use :command:`pip`:

        .. code-block:: console

            $ pip install celery[redis]

        See :ref:`bundles` for information on combining multiple extension
        requirements.

    This backend requires the :setting:`result_backend`
    setting to be set to a Redis or `Redis over TLS`_ URL::

        result_backend = 'redis://username:password@host:port/db'

    For example::

        result_backend = 'redis://localhost/0'

    is the same as::

        result_backend = 'redis://'

    Use the ``rediss://`` protocol to connect to redis over TLS::

        result_backend = 'rediss://username:password@host:port/db?ssl_cert_reqs=required'

    Note that the ``ssl_cert_reqs`` string should be one of ``required``,
    ``optional``, or ``none`` (though, for backwards compatibility with older Celery versions, the string
    may also be one of ``CERT_REQUIRED``, ``CERT_OPTIONAL``, ``CERT_NONE``, but those values
    only work for Celery, not for Redis directly).

    If a Unix socket connection should be used, the URL needs to be in the format:::

        result_backend = 'socket:///path/to/redis.sock'

    The fields of the URL are defined as follows:

    #. ``username``
        .. versionadded:: 5.1.0

        Username used to connect to the database.

        Note that this is only supported in Redis>=6.0 and with py-redis>=3.4.0
        installed.

        If you use an older database version or an older client version
        you can omit the username::

            result_backend = 'redis://:password@host:port/db'

    #. ``password``
        Password used to connect to the database.

    #. ``host``
        Host name or IP address of the Redis server (e.g., `localhost`).

    #. ``port``
        Port to the Redis server. Default is 6379.

    #. ``db``
        Database number to use. Default is 0.
        The db can include an optional leading slash.

    When using a TLS connection (protocol is ``rediss://``), you may pass in all values in :setting:`broker_use_ssl` as query parameters. Paths to certificates must be URL encoded, and ``ssl_cert_reqs`` is required. Example:

    .. code-block:: python

        result_backend = 'rediss://:password@host:port/db?\
            ssl_cert_reqs=required\
            &ssl_ca_certs=%2Fvar%2Fssl%2Fmyca.pem\                  # /var/ssl/myca.pem
            &ssl_certfile=%2Fvar%2Fssl%2Fredis-server-cert.pem\     # /var/ssl/redis-server-cert.pem
            &ssl_keyfile=%2Fvar%2Fssl%2Fprivate%2Fworker-key.pem'   # /var/ssl/private/worker-key.pem

    Note that the ``ssl_cert_reqs`` string should be one of ``required``,
    ``optional``, or ``none`` (though, for backwards compatibility, the string
    may also be one of ``CERT_REQUIRED``, ``CERT_OPTIONAL``, ``CERT_NONE``).

.. _`Redis over TLS`:
    https://www.iana.org/assignments/uri-schemes/prov/rediss


.. setting:: redis_backend_health_check_interval

.. versionadded:: 5.1.0

``redis_backend_health_check_interval``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Not configured

.. tab:: 中文

    Redis 后端支持健康检查。此值必须设置为整数，表示健康检查之间的秒数。如果在健康检查过程中遇到 ConnectionError 或 TimeoutError，
    连接将重新建立，并且命令将再次重试一次。

.. tab:: 英文

    The Redis backend supports health checks.  This value must be
    set as an integer whose value is the number of seconds between
    health checks.  If a ConnectionError or a TimeoutError is
    encountered during the health check, the connection will be
    re-established and the command retried exactly once.

.. setting:: redis_backend_use_ssl

``redis_backend_use_ssl``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    Redis 后端支持 SSL。此值必须以字典的形式设置。有效的键值对与
    在 :setting:`broker_use_ssl` 下的 ``redis`` 子部分中提到的键值对相同。

.. tab:: 英文

    The Redis backend supports SSL. This value must be set in
    the form of a dictionary. The valid key-value pairs are
    the same as the ones mentioned in the ``redis`` sub-section
    under :setting:`broker_use_ssl`.

.. setting:: redis_max_connections

``redis_max_connections``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: No limit.

.. tab:: 中文

    Redis 连接池中用于发送和接收结果的最大连接数。

    .. warning::
        如果并发连接数超过最大值，Redis 将引发 `ConnectionError`。

.. tab:: 英文

    Maximum number of connections available in the Redis connection
    pool used for sending and retrieving results.

    .. warning::
        Redis will raise a `ConnectionError` if the number of concurrent
        connections exceeds the maximum.

.. setting:: redis_socket_connect_timeout

``redis_socket_connect_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 4.0.1

Default: :const:`None`

.. tab:: 中文

    结果后端连接 Redis 的套接字超时（以秒为单位，int/float）。

.. tab:: 英文

    Socket timeout for connections to Redis from the result backend
    in seconds (int/float)

.. setting:: redis_socket_timeout

``redis_socket_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~

Default: 120.0 seconds.

.. tab:: 中文

    用于 Redis 服务器读/写操作的套接字超时时间（单位为秒，int/float），适用于 Redis 结果后端。

.. tab:: 英文

    Socket timeout for reading/writing operations to the Redis server
    in seconds (int/float), used by the redis result backend.

.. setting:: redis_retry_on_timeout

``redis_retry_on_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 4.4.1

Default: :const:`False`

.. tab:: 中文

    用于在遇到 TimeoutError 时重试 Redis 服务器的读/写操作，适用于 Redis 结果后端。如果使用 Unix 套接字连接 Redis，则不应设置该变量。

.. tab:: 英文

    To retry reading/writing operations on TimeoutError to the Redis server,
    used by the redis result backend. Shouldn't set this variable if using Redis
    connection by unix socket.

.. setting:: redis_socket_keepalive

``redis_socket_keepalive``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 4.4.1

Default: :const:`False`

.. tab:: 中文

    用于保持与 Redis 服务器连接健康状态的 Socket TCP keepalive，适用于 Redis 结果后端。

.. tab:: 英文

    Socket TCP keepalive to keep connections healthy to the Redis server,
    used by the redis result backend.

.. _conf-cassandra-result-backend:

Cassandra/AstraDB 后端设置
----------------------------------

Cassandra/AstraDB backend settings

.. tab:: 中文

    .. note::

        此 Cassandra 后端驱动依赖 :pypi:`cassandra-driver`。

        此后端既可用于常规的 Cassandra 部署，也可用于托管的 Astra DB 实例。根据所用的后端环境，必须在 :setting:`cassandra_servers` 和
        :setting:`cassandra_secure_bundle_path` 中选择其一进行配置（二者不可同时设置）。

        要安装，请使用 :command:`pip`：

        .. code-block:: console

            $ pip install celery[cassandra]

        请参见 :ref:`bundles` 了解有关组合多个扩展要求的信息。

    此后端需要配置以下参数：

.. tab:: 英文

    .. note::

        This Cassandra backend driver requires :pypi:`cassandra-driver`.

        This backend can refer to either a regular Cassandra installation
        or a managed Astra DB instance. Depending on which one, exactly one
        between the :setting:`cassandra_servers` and
        :setting:`cassandra_secure_bundle_path` settings must be provided
        (but not both).

        To install, use :command:`pip`:

        .. code-block:: console

            $ pip install celery[cassandra]

        See :ref:`bundles` for information on combining multiple extension
        requirements.

    This backend requires the following configuration directives to be set.

.. setting:: cassandra_servers

``cassandra_servers``
~~~~~~~~~~~~~~~~~~~~~

Default: ``[]`` (empty list).

.. tab:: 中文

    Cassandra 服务器的 ``host`` 列表。当连接 Cassandra 集群时必须提供该项。此项与 :setting:`cassandra_secure_bundle_path` 互斥。例如::

        cassandra_servers = ['localhost']

.. tab:: 英文

    List of ``host`` Cassandra servers. This must be provided when connecting to
    a Cassandra cluster. Passing this setting is strictly exclusive
    to :setting:`cassandra_secure_bundle_path`. Example::

        cassandra_servers = ['localhost']

.. setting:: cassandra_secure_bundle_path

``cassandra_secure_bundle_path``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    连接 Astra DB 实例所需的 secure-connect-bundle zip 文件的绝对路径。此项与 :setting:`cassandra_servers` 互斥。
    例如::

        cassandra_secure_bundle_path = '/home/user/bundles/secure-connect.zip'

    连接 Astra DB 时，必须指定明文认证提供程序（plain-text auth provider）以及相关的用户名和密码，
    其值分别为 Astra DB 实例所生成有效令牌的 Client ID 和 Client Secret。
    请参考下方 Astra DB 配置示例。

.. tab:: 英文

    Absolute path to the secure-connect-bundle zip file to connect
    to an Astra DB instance. Passing this setting is strictly exclusive
    to :setting:`cassandra_servers`.
    Example::

        cassandra_secure_bundle_path = '/home/user/bundles/secure-connect.zip'

    When connecting to Astra DB, it is necessary to specify
    the plain-text auth provider and the associated username and password,
    which take the value of the Client ID and the Client Secret, respectively,
    of a valid token generated for the Astra DB instance.
    See below for an Astra DB configuration example.

.. setting:: cassandra_port

``cassandra_port``
~~~~~~~~~~~~~~~~~~

Default: 9042.

.. tab:: 中文

    与 Cassandra 服务器通信所用的端口。

.. tab:: 英文

    Port to contact the Cassandra servers on.

.. setting:: cassandra_keyspace

``cassandra_keyspace``
~~~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    用于存储结果的 keyspace。例如::

        cassandra_keyspace = 'tasks_keyspace'

.. tab:: 英文

    The keyspace in which to store the results. For example::

        cassandra_keyspace = 'tasks_keyspace'

.. setting:: cassandra_table

``cassandra_table``
~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    用于存储结果的表（列族）。例如::

        cassandra_table = 'tasks'

.. tab:: 英文

    The table (column family) in which to store the results. For example::

        cassandra_table = 'tasks'

.. setting:: cassandra_read_consistency

``cassandra_read_consistency``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    读取一致性级别。可选值包括 ``ONE``, ``TWO``, ``THREE``, ``QUORUM``, ``ALL``,
    ``LOCAL_QUORUM``, ``EACH_QUORUM``, ``LOCAL_ONE``.

.. tab:: 英文

    The read consistency used. Values can be ``ONE``, ``TWO``, ``THREE``, ``QUORUM``, ``ALL``,
    ``LOCAL_QUORUM``, ``EACH_QUORUM``, ``LOCAL_ONE``.

.. setting:: cassandra_write_consistency

``cassandra_write_consistency``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    写入一致性级别。可选值包括 ``ONE``, ``TWO``, ``THREE``, ``QUORUM``, ``ALL``,
    ``LOCAL_QUORUM``, ``EACH_QUORUM``, ``LOCAL_ONE``.


.. tab:: 英文

    The write consistency used. Values can be ``ONE``, ``TWO``, ``THREE``, ``QUORUM``, ``ALL``,
    ``LOCAL_QUORUM``, ``EACH_QUORUM``, ``LOCAL_ONE``.

.. setting:: cassandra_entry_ttl

``cassandra_entry_ttl``
~~~~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    状态条目的存活时间（TTL），单位为秒。超过该时间后条目将过期并被移除。
    默认值为 :const:`None`，表示永不过期。

.. tab:: 英文

    Time-to-live for status entries. They will expire and be removed after that many seconds
    after adding. A value of :const:`None` (default) means they will never expire.

.. setting:: cassandra_auth_provider

``cassandra_auth_provider``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`None`.

.. tab:: 中文

    在 ``cassandra.auth`` 模块中用于认证的 AuthProvider 类。可选值包括
    ``PlainTextAuthProvider`` 或 ``SaslAuthProvider``。

.. tab:: 英文

    AuthProvider class within ``cassandra.auth`` module to use. Values can be
    ``PlainTextAuthProvider`` or ``SaslAuthProvider``.

.. setting:: cassandra_auth_kwargs

``cassandra_auth_kwargs``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    传递给认证提供程序的命名参数。例如：

    .. code-block:: python

        cassandra_auth_kwargs = {
            username: 'cassandra',
            password: 'cassandra'
        }

.. tab:: 英文

    Named arguments to pass into the authentication provider. For example:

    .. code-block:: python

        cassandra_auth_kwargs = {
            username: 'cassandra',
            password: 'cassandra'
        }

.. setting:: cassandra_options

``cassandra_options``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    传递给 ``cassandra.cluster`` 类的命名参数。

    .. code-block:: python

        cassandra_options = {
            'cql_version': '3.2.1'
            'protocol_version': 3
        }

.. tab:: 英文

    Named arguments to pass into the ``cassandra.cluster`` class.

.. code-block:: python

    cassandra_options = {
        'cql_version': '3.2.1'
        'protocol_version': 3
    }

示例配置 (Cassandra)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example configuration (Cassandra)

.. code-block:: python

    result_backend = 'cassandra://'
    cassandra_servers = ['localhost']
    cassandra_keyspace = 'celery'
    cassandra_table = 'tasks'
    cassandra_read_consistency = 'QUORUM'
    cassandra_write_consistency = 'QUORUM'
    cassandra_entry_ttl = 86400

示例配置 (Astra DB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example configuration (Astra DB)

.. code-block:: python

    result_backend = 'cassandra://'
    cassandra_keyspace = 'celery'
    cassandra_table = 'tasks'
    cassandra_read_consistency = 'QUORUM'
    cassandra_write_consistency = 'QUORUM'
    cassandra_auth_provider = 'PlainTextAuthProvider'
    cassandra_auth_kwargs = {
      'username': '<<CLIENT_ID_FROM_ASTRA_DB_TOKEN>>',
      'password': '<<CLIENT_SECRET_FROM_ASTRA_DB_TOKEN>>'
    }
    cassandra_secure_bundle_path = '/path/to/secure-connect-bundle.zip'
    cassandra_entry_ttl = 86400

其他配置
~~~~~~~~~~~~~~~~~~~~~~~~

Additional configuration

.. tab:: 中文

    在建立连接时，Cassandra 驱动程序会与服务器协商协议版本。
    同时，还会自动使用一个负载均衡策略（默认值为 ``DCAwareRoundRobinPolicy``，其含有一个由驱动自动确定的 ``local_dc`` 设置）。
    当可能时，应在配置中显式提供这些参数：
    此外，Cassandra 驱动的未来版本将要求至少指定负载均衡策略
    （可通过 `execution profiles <https://docs.datastax.com/en/developer/python-driver/3.25/execution_profiles/>`_ 进行配置，如下所示）。

    因此，一个完整的 Cassandra 后端配置将包含以下附加配置：

    .. code-block:: python

        from cassandra.policies import DCAwareRoundRobinPolicy
        from cassandra.cluster import ExecutionProfile
        from cassandra.cluster import EXEC_PROFILE_DEFAULT
        myEProfile = ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy(
            local_dc='datacenter1', # 替换为您的数据中心名称
        )
        )
        cassandra_options = {
        'protocol_version': 5,    # 适用于 Cassandra 4，如有需要可更改
        'execution_profiles': {EXEC_PROFILE_DEFAULT: myEProfile},
        }

    对于 Astra DB，配置方式类似：

    .. code-block:: python

        from cassandra.policies import DCAwareRoundRobinPolicy
        from cassandra.cluster import ExecutionProfile
        from cassandra.cluster import EXEC_PROFILE_DEFAULT
        myEProfile = ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy(
            local_dc='europe-west1',  # 对于 Astra DB，region 名即为 dc 名
        )
        )
        cassandra_options = {
        'protocol_version': 4,      # 适用于 Astra DB
        'execution_profiles': {EXEC_PROFILE_DEFAULT: myEProfile},
        }

.. tab:: 英文

    The Cassandra driver, when establishing the connection, undergoes a stage
    of negotiating the protocol version with the server(s). Similarly,
    a load-balancing policy is automatically supplied (by default
    ``DCAwareRoundRobinPolicy``, which in turn has a ``local_dc`` setting, also
    determined by the driver upon connection).
    When possible, one should explicitly provide these in the configuration:
    moreover, future versions of the Cassandra driver will require at least the
    load-balancing policy to be specified (using `execution profiles <https://docs.datastax.com/en/developer/python-driver/3.25/execution_profiles/>`_,
    as shown below).

    A full configuration for the Cassandra backend would thus have the
    following additional lines:

    .. code-block:: python

        from cassandra.policies import DCAwareRoundRobinPolicy
        from cassandra.cluster import ExecutionProfile
        from cassandra.cluster import EXEC_PROFILE_DEFAULT
        myEProfile = ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy(
            local_dc='datacenter1', # replace with your DC name
        )
        )
        cassandra_options = {
        'protocol_version': 5,    # for Cassandra 4, change if needed
        'execution_profiles': {EXEC_PROFILE_DEFAULT: myEProfile},
        }

    And similarly for Astra DB:

    .. code-block:: python

        from cassandra.policies import DCAwareRoundRobinPolicy
        from cassandra.cluster import ExecutionProfile
        from cassandra.cluster import EXEC_PROFILE_DEFAULT
        myEProfile = ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy(
            local_dc='europe-west1',  # for Astra DB, region name = dc name
        )
        )
        cassandra_options = {
        'protocol_version': 4,      # for Astra DB
        'execution_profiles': {EXEC_PROFILE_DEFAULT: myEProfile},
        }

.. _conf-s3-result-backend:

S3 后端设置
-------------------

S3 backend settings

.. tab:: 中文

    .. note::

        此 S3 后端驱动依赖 :pypi:`s3`。

        要安装，请使用 :command:`s3`：

        .. code-block:: console

            $ pip install celery[s3]

        请参见 :ref:`bundles` 了解有关组合多个扩展依赖项的信息。

    此后端需要配置以下参数：

.. tab:: 英文

    .. note::

        This s3 backend driver requires :pypi:`s3`.

        To install, use :command:`s3`:

        .. code-block:: console

            $ pip install celery[s3]

        See :ref:`bundles` for information on combining multiple extension
        requirements.

    This backend requires the following configuration directives to be set.

.. setting:: s3_access_key_id

``s3_access_key_id``
~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    S3 的访问密钥 ID。例如::

        s3_access_key_id = 'access_key_id'

.. tab:: 英文

    The s3 access key id. For example::

        s3_access_key_id = 'access_key_id'

.. setting:: s3_secret_access_key

``s3_secret_access_key``
~~~~~~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    S3 的访问密钥。例如::

        s3_secret_access_key = 'access_secret_access_key'

.. tab:: 英文

    The s3 secret access key. For example::

        s3_secret_access_key = 'access_secret_access_key'

.. setting:: s3_bucket

``s3_bucket``
~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    S3 的存储桶名称。例如::

        s3_bucket = 'bucket_name'

.. tab:: 英文

    The s3 bucket name. For example::

        s3_bucket = 'bucket_name'

.. setting:: s3_base_path

``s3_base_path``
~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    用于存储结果键的 S3 存储桶中的基础路径。例如::

        s3_base_path = '/prefix'

.. tab:: 英文

    A base path in the s3 bucket to use to store result keys. For example::

        s3_base_path = '/prefix'

.. setting:: s3_endpoint_url

``s3_endpoint_url``
~~~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    自定义的 S3 端点 URL。可用于连接自托管的 S3 兼容后端（如 Ceph、Scality 等）。例如::

        s3_endpoint_url = 'https://.s3.custom.url'

.. tab:: 英文

    A custom s3 endpoint url. Use it to connect to a custom self-hosted s3 compatible backend (Ceph, Scality...). For example::

        s3_endpoint_url = 'https://.s3.custom.url'

.. setting:: s3_region

``s3_region``
~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    S3 使用的 AWS 区域。例如::

        s3_region = 'us-east-1'

.. tab:: 英文

    The s3 aws region. For example::

        s3_region = 'us-east-1'

示例配置
~~~~~~~~~~~~~~~~~~~~~

Example configuration

    .. code-block:: python

        s3_access_key_id = 's3-access-key-id'
        s3_secret_access_key = 's3-secret-access-key'
        s3_bucket = 'mybucket'
        s3_base_path = '/celery_result_backend'
        s3_endpoint_url = 'https://endpoint_url'

.. _conf-azureblockblob-result-backend:

Azure Block Blob 后端设置
---------------------------------

Azure Block Blob backend settings

.. tab:: 中文

    要使用 `AzureBlockBlob`_ 作为结果后端，只需将 :setting:`result_backend` 配置为正确的 URL。

    所需的 URL 格式为 ``azureblockblob://``，后跟存储连接字符串。你可以在 Azure 门户中存储帐户资源的 ``Access Keys`` 面板中找到该连接字符串。

.. tab:: 英文

    To use `AzureBlockBlob`_ as the result backend you simply need to
    configure the :setting:`result_backend` setting with the correct URL.

    The required URL format is ``azureblockblob://`` followed by the storage
    connection string. You can find the storage connection string in the
    ``Access Keys`` pane of your storage account resource in the Azure Portal.

示例配置
~~~~~~~~~~~~~~~~~~~~~

Example configuration

    .. code-block:: python

        result_backend = 'azureblockblob://DefaultEndpointsProtocol=https;AccountName=somename;AccountKey=Lou...bzg==;EndpointSuffix=core.windows.net'

.. setting:: azureblockblob_container_name

``azureblockblob_container_name``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: celery.

.. tab:: 中文

    用于存储结果的存储容器名称。

.. tab:: 英文

    The name for the storage container in which to store the results.

.. setting:: azureblockblob_base_path

``azureblockblob_base_path``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.1

Default: None.

.. tab:: 中文

    存储容器中用于存放结果键的基础路径。例如::

        azureblockblob_base_path = 'prefix/'

.. tab:: 英文

    A base path in the storage container to use to store result keys. For example::

        azureblockblob_base_path = 'prefix/'

.. setting:: azureblockblob_retry_initial_backoff_sec

``azureblockblob_retry_initial_backoff_sec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 2.

.. tab:: 中文

    第一次重试的初始退避时间（以秒为单位）。
    后续重试将采用指数退避策略。

.. tab:: 英文

    The initial backoff interval, in seconds, for the first retry.
    Subsequent retries are attempted with an exponential strategy.

.. setting:: azureblockblob_retry_increment_base

``azureblockblob_retry_increment_base``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 2.

.. setting:: azureblockblob_retry_max_attempts

``azureblockblob_retry_max_attempts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 3.

.. tab:: 中文

    最大重试次数。

.. tab:: 英文

    The maximum number of retry attempts.

.. setting:: azureblockblob_connection_timeout

``azureblockblob_connection_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 20.

.. tab:: 中文

    建立 Azure Block Blob 连接的超时时间（秒）。

.. tab:: 英文

    Timeout in seconds for establishing the azure block blob connection.

.. setting:: azureblockblob_read_timeout

``azureblockblob_read_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 120.

.. tab:: 中文

    读取 Azure Block Blob 的超时时间（秒）。

.. tab:: 英文

    Timeout in seconds for reading of an azure block blob.

.. _conf-gcs-result-backend:

GCS 后端设置
--------------------

GCS backend settings

.. tab:: 中文

    .. note::

        此 GCS 后端驱动依赖 :pypi:`google-cloud-storage` 和 :pypi:`google-cloud-firestore`。

        要安装，请使用 :command:`gcs`：

        .. code-block:: console

            $ pip install celery[gcs]

        请参阅 :ref:`bundles` 获取关于组合多个扩展依赖项的信息。

    可以通过 :setting:`result_backend` 中提供的 URL 配置 GCS，例如::

        result_backend = 'gs://mybucket/some-prefix?gcs_project=myproject&ttl=600'
        result_backend = 'gs://mybucket/some-prefix?gcs_project=myproject?firestore_project=myproject2&ttl=600'

    此后端需要配置以下参数：

.. tab:: 英文

    .. note::

        This gcs backend driver requires :pypi:`google-cloud-storage` and :pypi:`google-cloud-firestore`.

        To install, use :command:`gcs`:

        .. code-block:: console

            $ pip install celery[gcs]

        See :ref:`bundles` for information on combining multiple extension
        requirements.

    GCS could be configured via the URL provided in :setting:`result_backend`, for example::

        result_backend = 'gs://mybucket/some-prefix?gcs_project=myproject&ttl=600'
        result_backend = 'gs://mybucket/some-prefix?gcs_project=myproject?firestore_project=myproject2&ttl=600'

    This backend requires the following configuration directives to be set:

.. setting:: gcs_bucket

``gcs_bucket``
~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    GCS 的存储桶名称。例如::

        gcs_bucket = 'bucket_name'

.. tab:: 英文

    The gcs bucket name. For example::

        gcs_bucket = 'bucket_name'

.. setting:: gcs_project

``gcs_project``
~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    GCS 的项目名称。例如::

        gcs_project = 'test-project'

.. tab:: 英文

    The gcs project name. For example::

        gcs_project = 'test-project'

.. setting:: gcs_base_path

``gcs_base_path``
~~~~~~~~~~~~~~~~~

Default: None.

.. tab:: 中文

    GCS 存储桶中用于存储所有结果键的基础路径。例如::

        gcs_base_path = '/prefix'

.. tab:: 英文

    A base path in the gcs bucket to use to store all result keys. For example::

        gcs_base_path = '/prefix'

``gcs_ttl``
~~~~~~~~~~~

Default: 0.

.. tab:: 中文

    结果 Blob 的生存时间（秒）。
    要求 GCS 存储桶启用 “删除” 对象生命周期管理操作。
    可用于在 Cloud Storage 中自动删除结果。

    例如，若要在 24 小时后自动删除结果::

        gcs_ttl = 86400

.. tab:: 英文

    The time to live in seconds for the results blobs.
    Requires a GCS bucket with "Delete" Object Lifecycle Management action enabled.
    Use it to automatically delete results from Cloud Storage Buckets.

    For example to auto remove results after 24 hours::

        gcs_ttl = 86400

``gcs_threadpool_maxsize``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 10.

.. tab:: 中文

    用于 GCS 操作的线程池大小。该值也决定连接池大小。
    允许控制并发操作的数量。例如::

        gcs_threadpool_maxsize = 20

.. tab:: 英文

    Threadpool size for GCS operations. Same value defines the connection pool size.
    Allows to control the number of concurrent operations. For example::

        gcs_threadpool_maxsize = 20

``firestore_project``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: gcs_project.

.. tab:: 中文

    用于 Chord 引用计数的 Firestore 项目名称。启用原生 Chord 引用计数。
    若未指定，默认为 :setting:`gcs_project`。
    例如::

        firestore_project = 'test-project2'

.. tab:: 英文

    The Firestore project for Chord reference counting. Allows native chord ref counts.
    If not specified defaults to :setting:`gcs_project`.
    For example::

        firestore_project = 'test-project2'

示例配置
~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. code-block:: python

    gcs_bucket = 'mybucket'
    gcs_project = 'myproject'
    gcs_base_path = '/celery_result_backend'
    gcs_ttl = 86400

.. _conf-elasticsearch-result-backend:

Elasticsearch 后端设置
------------------------------

Elasticsearch backend settings

.. tab:: 中文

    要使用 `Elasticsearch`_ 作为结果后端，只需将 :setting:`result_backend` 配置为正确的 URL。

.. tab:: 英文

    To use `Elasticsearch`_ as the result backend you simply need to
    configure the :setting:`result_backend` setting with the correct URL.

示例配置
~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. code-block:: python

    result_backend = 'elasticsearch://example.com:9200/index_name/doc_type'

.. setting:: elasticsearch_retry_on_timeout

``elasticsearch_retry_on_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`False`

.. tab:: 中文

    是否在超时后尝试切换到其他节点进行重试？

.. tab:: 英文

    Should timeout trigger a retry on different node?

.. setting:: elasticsearch_max_retries

``elasticsearch_max_retries``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 3.

.. tab:: 中文

    在抛出异常前允许的最大重试次数。

.. tab:: 英文

    Maximum number of retries before an exception is propagated.

.. setting:: elasticsearch_timeout

``elasticsearch_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 10.0 seconds.

.. tab:: 中文

    Elasticsearch 结果后端使用的全局超时时间。

.. tab:: 英文

    Global timeout,used by the elasticsearch result backend.

.. setting:: elasticsearch_save_meta_as_text

``elasticsearch_save_meta_as_text``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`True`

.. tab:: 中文

    元数据应以文本还是原生 JSON 格式保存。
    结果始终以文本形式序列化。

.. tab:: 英文

    Should meta saved as text or as native json.
    Result is always serialized as text.

.. _conf-dynamodb-result-backend:

AWS DynamoDB 后端设置
-----------------------------

AWS DynamoDB backend settings

.. tab:: 中文

    .. note::

        Dynamodb 后端需要依赖 :pypi:`boto3` 库。

        要安装此软件包，请使用 :command:`pip`：

        .. code-block:: console

            $ pip install celery[dynamodb]

        请参阅 :ref:`bundles` 获取关于组合多个扩展依赖项的信息。

    .. warning::

        Dynamodb 后端与定义了排序键（sort key）的表不兼容。

        如果你希望基于分区键以外的字段查询结果表，请使用全局二级索引（GSI）。

    此后端要求通过 :setting:`result_backend` 设置一个 DynamoDB URL::

        result_backend = 'dynamodb://aws_access_key_id:aws_secret_access_key@region:port/table?read=n&write=m'

    例如，指定 AWS 区域和表名::

        result_backend = 'dynamodb://@us-east-1/celery_results'

    或从环境变量中读取 AWS 配置参数，使用默认表名（``celery``）并设置读写吞吐量::

        result_backend = 'dynamodb://@/?read=5&write=5'

    或使用 `可下载版本 <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html>`_
    在本地部署的 `DynamoDB <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.Endpoint.html>`_::

        result_backend = 'dynamodb://@localhost:8000'

    或使用可下载版本或其他部署在任意主机上的兼容 API 服务::

        result_backend = 'dynamodb://@us-east-1'
        dynamodb_endpoint_url = 'http://192.168.0.40:8000'

    ``result_backend`` 中的 DynamoDB URL 字段定义如下：

    #. ``aws_access_key_id & aws_secret_access_key``
        用于访问 AWS API 资源的凭据。也可通过 :pypi:`boto3` 库从多种来源解析，
        详见 `此处 <http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials>`_。

    #. ``region``
        AWS 区域，例如 ``us-east-1``，或 `可下载版本 <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html>`_ 使用的 ``localhost``。
        可参考 :pypi:`boto3` 的 `文档 <http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration>`_ 获取可选值定义。

    #. ``port``
        如果使用的是本地版本，此为本地 DynamoDB 实例的监听端口。
        如果 ``region`` 未设置为 ``localhost``，此参数将 **不起作用**。

    #. ``table``
        使用的表名，默认值为 ``celery``。
        表名的允许字符与长度要求可参考
        `DynamoDB 命名规则 <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-naming-rules>`_。

    #. ``read & write``
        创建的 DynamoDB 表的读/写容量单位，默认均为 ``1``。
        详细说明可参考 `吞吐量配置文档 <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ProvisionedThroughput.html>`_。

    #. ``ttl_seconds``
        结果在过期前的存活时间（秒）。默认不设置过期，并且不修改 DynamoDB 表的 TTL 设置。
        如果设置为正数，结果将在该时间后过期；
        如果设置为负数，则表示不设置过期，并主动禁用表的 TTL 设置。
        注意：短时间内频繁修改 TTL 设置可能会导致限速错误。
        详见 `DynamoDB TTL 文档 <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html>`_。

.. tab:: 英文

    .. note::

        The Dynamodb backend requires the :pypi:`boto3` library.

        To install this package use :command:`pip`:

        .. code-block:: console

            $ pip install celery[dynamodb]

        See :ref:`bundles` for information on combining multiple extension
        requirements.

    .. warning::

        The Dynamodb backend is not compatible with tables that have a sort key defined.

        If you want to query the results table based on something other than the partition key,
        please define a global secondary index (GSI) instead.

    This backend requires the :setting:`result_backend`
    setting to be set to a DynamoDB URL::

        result_backend = 'dynamodb://aws_access_key_id:aws_secret_access_key@region:port/table?read=n&write=m'

    For example, specifying the AWS region and the table name::

        result_backend = 'dynamodb://@us-east-1/celery_results'

    or retrieving AWS configuration parameters from the environment, using the default table name (``celery``)
    and specifying read and write provisioned throughput::

        result_backend = 'dynamodb://@/?read=5&write=5'

    or using the `downloadable version <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html>`_
    of DynamoDB
    `locally <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.Endpoint.html>`_::

        result_backend = 'dynamodb://@localhost:8000'

    or using downloadable version or other service with conforming API deployed on any host::

        result_backend = 'dynamodb://@us-east-1'
        dynamodb_endpoint_url = 'http://192.168.0.40:8000'

    The fields of the DynamoDB URL in ``result_backend`` are defined as follows:

    #. ``aws_access_key_id & aws_secret_access_key``
        The credentials for accessing AWS API resources. These can also be resolved
        by the :pypi:`boto3` library from various sources, as
        described `here <http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials>`_.

    #. ``region``
        The AWS region, e.g. ``us-east-1`` or ``localhost`` for the `Downloadable Version <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html>`_.
        See the :pypi:`boto3` library `documentation <http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration>`_
        for definition options.

    #. ``port``
        The listening port of the local DynamoDB instance, if you are using the downloadable version.
        If you have not specified the ``region`` parameter as ``localhost``,
        setting this parameter has **no effect**.

    #. ``table``
        Table name to use. Default is ``celery``.
        See the `DynamoDB Naming Rules <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html#limits-naming-rules>`_
        for information on the allowed characters and length.

    #. ``read & write``
        The Read & Write Capacity Units for the created DynamoDB table. Default is ``1`` for both read and write.
        More details can be found in the `Provisioned Throughput documentation <http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ProvisionedThroughput.html>`_.

    #. ``ttl_seconds``
        Time-to-live (in seconds) for results before they expire. The default is to
        not expire results, while also leaving the DynamoDB table's Time to Live
        settings untouched. If ``ttl_seconds`` is set to a positive value, results
        will expire after the specified number of seconds. Setting ``ttl_seconds``
        to a negative value means to not expire results, and also to actively
        disable the DynamoDB table's Time to Live setting. Note that trying to
        change a table's Time to Live setting multiple times in quick succession
        will cause a throttling error. More details can be found in the
        `DynamoDB TTL documentation <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html>`_

.. _conf-ironcache-result-backend:

IronCache 后端设置
--------------------------

IronCache backend settings

.. tab:: 中文

    .. note::

        IronCache 后端需要 :pypi:`iron_celery` 库：

        要安装此软件包，请使用 :command:`pip`：

        .. code-block:: console

            $ pip install iron_celery

    IronCache 可通过 :setting:`result_backend` 中提供的 URL 配置，例如::

        result_backend = 'ironcache://project_id:token@'

    或修改缓存名称::

        ironcache:://project_id:token@/awesomecache

    更多信息参见： https://github.com/iron-io/iron_celery

.. tab:: 英文

    .. note::

        The IronCache backend requires the :pypi:`iron_celery` library:

        To install this package use :command:`pip`:

        .. code-block:: console

            $ pip install iron_celery

    IronCache is configured via the URL provided in :setting:`result_backend`, for example::

        result_backend = 'ironcache://project_id:token@'

    Or to change the cache name::

        ironcache:://project_id:token@/awesomecache

    For more information, see: https://github.com/iron-io/iron_celery

.. _conf-couchbase-result-backend:

Couchbase 后端设置
--------------------------

Couchbase backend settings

.. tab:: 中文

    .. note::

        Couchbase 后端依赖 :pypi:`couchbase` 库。

        安装该库可使用 :command:`pip` 命令：

        .. code-block:: console

            $ pip install celery[couchbase]

        有关如何组合多个扩展依赖项的说明，请参见 :ref:`bundles`。

    该后端可通过 :setting:`result_backend` 设置为 Couchbase URL 进行配置：

    .. code-block:: python

        result_backend = 'couchbase://username:password@host:port/bucket'

.. tab:: 英文

    .. note::

        The Couchbase backend requires the :pypi:`couchbase` library.

        To install this package use :command:`pip`:

        .. code-block:: console

            $ pip install celery[couchbase]

        See :ref:`bundles` for instructions how to combine multiple extension
        requirements.

    This backend can be configured via the :setting:`result_backend`
    set to a Couchbase URL:

    .. code-block:: python

        result_backend = 'couchbase://username:password@host:port/bucket'

.. setting:: couchbase_backend_settings

``couchbase_backend_settings``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    这是一个字典，支持以下键：

    * ``host``  
        Couchbase 服务器的主机名，默认为 ``localhost``。

    * ``port``  
        Couchbase 服务器监听的端口，默认为 ``8091``。

    * ``bucket``  
        Couchbase 服务器写入的默认 bucket，默认为 ``default``。

    * ``username``  
        用于认证 Couchbase 服务器的用户名（可选）。

    * ``password``  
        用于认证 Couchbase 服务器的密码（可选）。

.. tab:: 英文

    This is a dict supporting the following keys:

    * ``host``
        Host name of the Couchbase server. Defaults to ``localhost``.

    * ``port``
        The port the Couchbase server is listening to. Defaults to ``8091``.

    * ``bucket``
        The default bucket the Couchbase server is writing to.
        Defaults to ``default``.

    * ``username``
        User name to authenticate to the Couchbase server as (optional).

    * ``password``
        Password to authenticate to the Couchbase server (optional).

.. _conf-arangodb-result-backend:

ArangoDB 后端设置
--------------------------

ArangoDB backend settings

.. tab:: 中文

    .. note::

        ArangoDB 后端依赖 :pypi:`pyArango` 库。

        安装该库可使用 :command:`pip` 命令：

        .. code-block:: console

            $ pip install celery[arangodb]

        有关如何组合多个扩展依赖项的说明，请参见 :ref:`bundles`。

    该后端可通过 :setting:`result_backend` 设置为 ArangoDB URL 进行配置：

    .. code-block:: python

        result_backend = 'arangodb://username:password@host:port/database/collection'

.. tab:: 英文

    .. note::

        The ArangoDB backend requires the :pypi:`pyArango` library.

        To install this package use :command:`pip`:

        .. code-block:: console

            $ pip install celery[arangodb]

        See :ref:`bundles` for instructions how to combine multiple extension
        requirements.

    This backend can be configured via the :setting:`result_backend`
    set to a ArangoDB URL:

    .. code-block:: python

        result_backend = 'arangodb://username:password@host:port/database/collection'

.. setting:: arangodb_backend_settings

``arangodb_backend_settings``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    这是一个字典，支持以下键：

    * ``host``  
        ArangoDB 服务器的主机名，默认为 ``localhost``。

    * ``port``  
        ArangoDB 服务器监听的端口，默认为 ``8529``。

    * ``database``  
        ArangoDB 服务器写入的默认数据库，默认为 ``celery``。

    * ``collection``  
        ArangoDB 数据库中写入的默认集合，默认为 ``celery``。

    * ``username``  
        用于认证 ArangoDB 服务器的用户名（可选）。

    * ``password``  
        用于认证 ArangoDB 服务器的密码（可选）。

    * ``http_protocol``  
        ArangoDB 连接中使用的 HTTP 协议，默认为 ``http``。

    * ``verify``  
        建立 ArangoDB HTTPS 连接时是否执行证书校验，默认为 ``False``。

.. tab:: 英文

    This is a dict supporting the following keys:

    * ``host``

        Host name of the ArangoDB server. Defaults to ``localhost``.

    * ``port``

        The port the ArangoDB server is listening to. Defaults to ``8529``.

    * ``database``

        The default database in the ArangoDB server is writing to.
        Defaults to ``celery``.

    * ``collection``

        The default collection in the ArangoDB servers database is writing to.
        Defaults to ``celery``.

    * ``username``

        User name to authenticate to the ArangoDB server as (optional).

    * ``password``

        Password to authenticate to the ArangoDB server (optional).

    * ``http_protocol``

        HTTP Protocol in ArangoDB server connection.
        Defaults to ``http``.

    * ``verify``

        HTTPS Verification check while creating the ArangoDB connection.
        Defaults to ``False``.

.. _conf-cosmosdbsql-result-backend:

CosmosDB 后端设置（实验性）
----------------------------------------

CosmosDB backend settings (experimental)

.. tab:: 中文

    要使用 `CosmosDB`_ 作为结果后端，仅需将 :setting:`result_backend` 设置为正确的 URL 即可。

.. tab:: 英文

    To use `CosmosDB`_ as the result backend, you simply need to configure the
    :setting:`result_backend` setting with the correct URL.

示例配置
~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. code-block:: python

    result_backend = 'cosmosdbsql://:{InsertAccountPrimaryKeyHere}@{InsertAccountNameHere}.documents.azure.com'

.. setting:: cosmosdbsql_database_name

``cosmosdbsql_database_name``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: celerydb.

.. tab:: 中文

    存储结果的数据库名称。

.. tab:: 英文

    The name for the database in which to store the results.

.. setting:: cosmosdbsql_collection_name

``cosmosdbsql_collection_name``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: celerycol.

.. tab:: 中文

    存储结果的集合名称。

.. tab:: 英文

    The name of the collection in which to store the results.

.. setting:: cosmosdbsql_consistency_level

``cosmosdbsql_consistency_level``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Session.

.. tab:: 中文

    表示 Azure Cosmos DB 客户端操作支持的一致性级别。

    一致性级别按强度顺序为：Strong、BoundedStaleness、Session、ConsistentPrefix 和 Eventual。

.. tab:: 英文

    Represents the consistency levels supported for Azure Cosmos DB client operations.

    Consistency levels by order of strength are: Strong, BoundedStaleness, Session, ConsistentPrefix and Eventual.

.. setting:: cosmosdbsql_max_retry_attempts

``cosmosdbsql_max_retry_attempts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 9.

.. tab:: 中文

    执行请求的最大重试次数。

.. tab:: 英文

    Maximum number of retries to be performed for a request.

.. setting:: cosmosdbsql_max_retry_wait_time

``cosmosdbsql_max_retry_wait_time``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 30.

.. tab:: 中文

    在重试期间等待请求完成的最大等待时间（单位为秒）。

.. tab:: 英文

    Maximum wait time in seconds to wait for a request while the retries are happening.

.. _conf-couchdb-result-backend:

CouchDB 后端设置
------------------------

CouchDB backend settings

.. tab:: 中文

    .. note::

        CouchDB 后端依赖 :pypi:`pycouchdb` 库：

        安装该 CouchDB 库可使用 :command:`pip` 命令：

        .. code-block:: console

            $ pip install celery[couchdb]

        有关如何组合多个扩展依赖项的说明，请参见 :ref:`bundles`。

    该后端可通过 :setting:`result_backend` 设置为 CouchDB URL 进行配置::

        result_backend = 'couchdb://username:password@host:port/container'

    URL 由以下部分组成：

    * ``username``  
        用于认证 CouchDB 服务器的用户名（可选）。

    * ``password``  
        用于认证 CouchDB 服务器的密码（可选）。

    * ``host``  
        CouchDB 服务器的主机名，默认为 ``localhost``。

    * ``port``  
        CouchDB 服务器监听的端口，默认为 ``8091``。

    * ``container``  
        CouchDB 服务器写入的默认容器，默认为 ``default``。

.. tab:: 英文

    .. note::

        The CouchDB backend requires the :pypi:`pycouchdb` library:

        To install this Couchbase package use :command:`pip`:

        .. code-block:: console

            $ pip install celery[couchdb]

        See :ref:`bundles` for information on combining multiple extension
        requirements.

    This backend can be configured via the :setting:`result_backend`
    set to a CouchDB URL::

        result_backend = 'couchdb://username:password@host:port/container'

    The URL is formed out of the following parts:

    * ``username``
        User name to authenticate to the CouchDB server as (optional).

    * ``password``
        Password to authenticate to the CouchDB server (optional).

    * ``host``
        Host name of the CouchDB server. Defaults to ``localhost``.

    * ``port``
        The port the CouchDB server is listening to. Defaults to ``8091``.

    * ``container``
        The default container the CouchDB server is writing to.
        Defaults to ``default``.

.. _conf-filesystem-result-backend:

文件系统后端设置
----------------------------

File-system backend settings

.. tab:: 中文

    该后端也可以使用文件 URL 配置，例如::

        CELERY_RESULT_BACKEND = 'file:///var/celery/results'

    所配置的目录必须对使用该后端的所有服务器可共享并具有可写权限。

    如果你仅在单机上试用 Celery，可以直接使用该后端而无需额外配置。
    对于大型集群，你可以使用 NFS、 `GlusterFS`_、 CIFS、 `HDFS`_ （使用 FUSE）或其他任何文件系统。

.. tab:: 英文

    This backend can be configured using a file URL, for example::

        CELERY_RESULT_BACKEND = 'file:///var/celery/results'

    The configured directory needs to be shared and writable by all servers using
    the backend.

    If you're trying Celery on a single system you can simply use the backend
    without any further configuration. For larger clusters you could use NFS,
    `GlusterFS`_, CIFS, `HDFS`_ (using FUSE), or any other file-system.

.. _`GlusterFS`: http://www.gluster.org/
.. _`HDFS`: http://hadoop.apache.org/

.. _conf-consul-result-backend:

Consul 键值存储后端设置
---------------------------------

Consul K/V store backend settings

.. tab:: 中文

    .. note::

        Consul 后端需要安装 :pypi:`python-consul2` 库：

        使用 :command:`pip` 安装此软件包：

        .. code-block:: console

            $ pip install python-consul2

    Consul 后端可以通过 URL 进行配置，例如::

        CELERY_RESULT_BACKEND = 'consul://localhost:8500/'

    或::

        result_backend = 'consul://localhost:8500/'

    该后端将在 Consul 的 K/V 存储中以独立键的形式存储结果。
    该后端支持使用 Consul 中的 TTL 自动过期结果。
    URL 的完整语法如下：

    .. code-block:: text

        consul://host:port[?one_client=1]

    该 URL 由以下部分组成：

    * ``host``  
        Consul 服务器的主机名。

    * ``port``  
        Consul 服务器监听的端口。

    * ``one_client``  
        默认情况下，为了确保正确性，该后端在每次操作时都会使用独立的客户端连接。
        在负载极高的情况下，频繁创建新连接可能导致 Consul 服务器返回 HTTP 429 “连接过多” 错误。
        推荐的处理方式是参考此补丁为 ``python-consul2`` 启用重试功能：
        https://github.com/poppyred/python-consul2/pull/31。

        或者，如果设置了 ``one_client`` 参数，则所有操作将复用单个客户端连接。
        这样可以避免 HTTP 429 错误，但后端存储结果的可靠性可能会降低。

.. tab:: 英文

    .. note::

        The Consul backend requires the :pypi:`python-consul2` library:

        To install this package use :command:`pip`:

        .. code-block:: console

            $ pip install python-consul2

    The Consul backend can be configured using a URL, for example::

        CELERY_RESULT_BACKEND = 'consul://localhost:8500/'

    or::

        result_backend = 'consul://localhost:8500/'

    The backend will store results in the K/V store of Consul
    as individual keys. The backend supports auto expire of results using TTLs in
    Consul. The full syntax of the URL is:

    .. code-block:: text

        consul://host:port[?one_client=1]

    The URL is formed out of the following parts:

    * ``host``
        Host name of the Consul server.

    * ``port``
        The port the Consul server is listening to.

    * ``one_client``
        By default, for correctness, the backend uses a separate client connection
        per operation. In cases of extreme load, the rate of creation of new
        connections can cause HTTP 429 "too many connections" error responses from
        the Consul server when under load. The recommended way to handle this is to
        enable retries in ``python-consul2`` using the patch at
        https://github.com/poppyred/python-consul2/pull/31.

        Alternatively, if ``one_client`` is set, a single client connection will be
        used for all operations instead. This should eliminate the HTTP 429 errors,
        but the storage of results in the backend can become unreliable.

.. _conf-messaging:

消息路由
---------------

Message Routin

.. _conf-messaging-routing:

.. setting:: task_queues

``task_queues``
~~~~~~~~~~~~~~~

.. tab:: 中文

    默认值：:const:`None` （队列将从默认队列设置中获取）。

    大多数用户无需手动设置此选项，而应使用
    :ref:`自动路由机制 <routing-automatic>`。

    如果确实需要配置高级路由策略，该设置应为
    一个由 :class:`kombu.Queue` 对象组成的列表，Worker 将从中消费任务。

    需要注意的是，Worker 可通过 :option:`-Q <celery worker -Q>` 选项覆盖该设置，
    或使用 :option:`-X <celery worker -X>` 选项排除该列表中的部分队列（按名称）。

    详见 :ref:`routing-basics` 了解更多信息。

    默认使用名为 ``celery`` 的队列/交换机/绑定键，
    交换机类型为 ``direct``。

    另见 :setting:`task_routes`

.. tab:: 英文

    Default: :const:`None` (queue taken from default queue settings).

    Most users will not want to specify this setting and should rather use
    the :ref:`automatic routing facilities <routing-automatic>`.

    If you really want to configure advanced routing, this setting should
    be a list of :class:`kombu.Queue` objects the worker will consume from.

    Note that workers can be overridden this setting via the
    :option:`-Q <celery worker -Q>` option, or individual queues from this
    list (by name) can be excluded using the :option:`-X <celery worker -X>`
    option.

    Also see :ref:`routing-basics` for more information.

    The default is a queue/exchange/binding key of ``celery``, with
    exchange type ``direct``.

    See also :setting:`task_routes`

.. setting:: task_routes

``task_routes``
~~~~~~~~~~~~~~~

.. tab:: 中文

    默认值：:const:`None`。

    该设置应为一个路由器列表，或一个用于将任务路由到队列的路由器。
    在确定任务最终投递位置时，系统会按顺序调用这些路由器。

    路由器可按以下几种形式指定：

    *  函数，签名为 ``(name, args, kwargs, options, task=None, **kwargs)``
    *  字符串，提供指向路由函数的路径。
    *  字典，包含路由器说明：将转换为 :class:`celery.routes.MapRoute` 实例。
    *  ``(pattern, route)`` 元组组成的列表：将转换为 :class:`celery.routes.MapRoute` 实例。

    示例：

    .. code-block:: python

        task_routes = {
            'celery.ping': 'default',
            'mytasks.add': 'cpu-bound',
            'feed.tasks.*': 'feeds',                           # <-- 通配符模式
            re.compile(r'(image|video)\.tasks\..*'): 'media',  # <-- 正则表达式
            'video.encode': {
                'queue': 'video',
                'exchange': 'media',
                'routing_key': 'media.video.encode',
            },
        }

        task_routes = ('myapp.tasks.route_task', {'celery.ping': 'default'})

    其中 ``myapp.tasks.route_task`` 可以是：

    .. code-block:: python

        def route_task(self, name, args, kwargs, options, task=None, **kw):
            if task == 'celery.ping':
                return {'queue': 'default'}

    ``route_task`` 可返回字符串或字典。
    字符串表示 :setting:`task_queues` 中的队列名；
    字典表示自定义路由设置。

    在发送任务时，系统将依序查询各路由器。
    第一个返回非 ``None`` 的路由器即为选中路由，
    任务消息的选项将与该路由配置合并，任务设置优先。

    例如，调用 :func:`~celery.execute.apply_async` 传入如下参数：

    .. code-block:: python

    Task.apply_async(immediate=False, exchange='video',
                        routing_key='video.compress')

    而某路由器返回：

    .. code-block:: python

        {'immediate': True, 'exchange': 'urgent'}

    则最终消息选项为：

    .. code-block:: python

        immediate=False, exchange='video', routing_key='video.compress'

    （还包括 :class:`~celery.app.task.Task` 类中定义的默认消息选项）

    在合并 :setting:`task_routes` 与 :setting:`task_queues` 的设置时，
    前者具有更高优先级。

    例如，设置如下：

    .. code-block:: python

        task_queues = {
            'cpubound': {
                'exchange': 'cpubound',
                'routing_key': 'cpubound',
            },
        }

        task_routes = {
            'tasks.add': {
                'queue': 'cpubound',
                'routing_key': 'tasks.add',
                'serializer': 'json',
            },
        }

    则 ``tasks.add`` 的最终路由选项为：

    .. code-block:: javascript

        {'exchange': 'cpubound',
        'routing_key': 'tasks.add',
        'serializer': 'json'}

    参见 :ref:`routers` 获取更多示例。

.. tab:: 英文

    Default: :const:`None`.

    A list of routers, or a single router used to route tasks to queues.
    When deciding the final destination of a task the routers are consulted
    in order.

    A router can be specified as either:

    *  A function with the signature ``(name, args, kwargs, options, task=None, **kwargs)``
    *  A string providing the path to a router function.
    *  A dict containing router specification: Will be converted to a :class:`celery.routes.MapRoute` instance.
    * A list of ``(pattern, route)`` tuples: Will be converted to a :class:`celery.routes.MapRoute` instance.

    Examples:

    .. code-block:: python

        task_routes = {
            'celery.ping': 'default',
            'mytasks.add': 'cpu-bound',
            'feed.tasks.*': 'feeds',                           # <-- glob pattern
            re.compile(r'(image|video)\.tasks\..*'): 'media',  # <-- regex
            'video.encode': {
                'queue': 'video',
                'exchange': 'media',
                'routing_key': 'media.video.encode',
            },
        }

        task_routes = ('myapp.tasks.route_task', {'celery.ping': 'default'})

    Where ``myapp.tasks.route_task`` could be:

    .. code-block:: python

        def route_task(self, name, args, kwargs, options, task=None, **kw):
            if task == 'celery.ping':
                return {'queue': 'default'}

    ``route_task`` may return a string or a dict. A string then means
    it's a queue name in :setting:`task_queues`, a dict means it's a custom route.

    When sending tasks, the routers are consulted in order. The first
    router that doesn't return ``None`` is the route to use. The message options
    is then merged with the found route settings, where the task's settings
    have priority.

    Example if :func:`~celery.execute.apply_async` has these arguments:

    .. code-block:: python

    Task.apply_async(immediate=False, exchange='video',
                        routing_key='video.compress')

    and a router returns:

    .. code-block:: python

        {'immediate': True, 'exchange': 'urgent'}

    the final message options will be:

    .. code-block:: python

        immediate=False, exchange='video', routing_key='video.compress'

    (and any default message options defined in the
    :class:`~celery.app.task.Task` class)

    Values defined in :setting:`task_routes` have precedence over values defined in
    :setting:`task_queues` when merging the two.

    With the follow settings:

    .. code-block:: python

        task_queues = {
            'cpubound': {
                'exchange': 'cpubound',
                'routing_key': 'cpubound',
            },
        }

        task_routes = {
            'tasks.add': {
                'queue': 'cpubound',
                'routing_key': 'tasks.add',
                'serializer': 'json',
            },
        }

    The final routing options for ``tasks.add`` will become:

    .. code-block:: javascript

        {'exchange': 'cpubound',
        'routing_key': 'tasks.add',
        'serializer': 'json'}

    See :ref:`routers` for more examples.

.. setting:: task_queue_max_priority

``task_queue_max_priority``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:brokers: RabbitMQ

Default: :const:`None`.

See :ref:`routing-options-rabbitmq-priorities`.

.. setting:: task_default_priority

``task_default_priority``
~~~~~~~~~~~~~~~~~~~~~~~~~~~
:brokers: RabbitMQ, Redis

Default: :const:`None`.

See :ref:`routing-options-rabbitmq-priorities`.

.. setting:: task_inherit_parent_priority

``task_inherit_parent_priority``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:brokers: RabbitMQ

.. tab:: 中文

    默认值：:const:`False`。

    如果启用，子任务将继承父任务的优先级。

    .. code-block:: python

        # 链中最后一个任务也将具有优先级 5。
        chain = celery.chain(add.s(2) | add.s(2).set(priority=5) | add.s(3))

    在使用 `delay` 或 `apply_async` 从父任务调用子任务时，优先级继承同样适用。

    参见 :ref:`routing-options-rabbitmq-priorities`。

.. tab:: 英文

    Default: :const:`False`.

    If enabled, child tasks will inherit priority of the parent task.

    .. code-block:: python

        # The last task in chain will also have priority set to 5.
        chain = celery.chain(add.s(2) | add.s(2).set(priority=5) | add.s(3))

    Priority inheritance also works when calling child tasks from a parent task
    with `delay` or `apply_async`.

    See :ref:`routing-options-rabbitmq-priorities`.


.. setting:: worker_direct

``worker_direct``
~~~~~~~~~~~~~~~~~

Default: Disabled.

.. tab:: 中文

    此选项允许为每个 worker 创建一个专用队列，以便可以将任务路由到特定的 worker。

    每个 worker 的队列名称是基于 worker 的主机名并添加 ``.dq`` 后缀自动生成的，使用的是 ``C.dq2`` 交换机。

    例如，节点名称为 ``w1@example.com`` 的 worker 对应的队列名称为::

        w1@example.com.dq

    然后你可以通过指定主机名作为路由键，并使用 ``C.dq2`` 交换机将任务路由到该 worker::

        task_routes = {
            'tasks.add': {'exchange': 'C.dq2', 'routing_key': 'w1@example.com'}
        }

.. tab:: 英文

    This option enables so that every worker has a dedicated queue,
    so that tasks can be routed to specific workers.

    The queue name for each worker is automatically generated based on
    the worker hostname and a ``.dq`` suffix, using the ``C.dq2`` exchange.

    For example the queue name for the worker with node name ``w1@example.com``
    becomes::

        w1@example.com.dq

    Then you can route the task to the worker by specifying the hostname
    as the routing key and the ``C.dq2`` exchange::

        task_routes = {
            'tasks.add': {'exchange': 'C.dq2', 'routing_key': 'w1@example.com'}
        }

.. setting:: task_create_missing_queues

``task_create_missing_queues``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Enabled.

.. tab:: 中文

    如果启用（默认启用），任何未在 :setting:`task_queues` 中定义的队列将被自动创建。参见 :ref:`routing-automatic`。

.. tab:: 英文

    If enabled (default), any queues specified that aren't defined in
    :setting:`task_queues` will be automatically created. See
    :ref:`routing-automatic`.

.. setting:: task_default_queue

``task_default_queue``
~~~~~~~~~~~~~~~~~~~~~~

Default: ``"celery"``.

.. tab:: 中文

    `.apply_async` 在消息没有指定路由或没有自定义队列的情况下所使用的默认队列名称。

    该队列必须在 :setting:`task_queues` 中列出。
    如果未指定 :setting:`task_queues`，则会自动创建一个包含该队列名称的队列条目。

    .. seealso::

        :ref:`routing-changing-default-queue`

.. tab:: 英文

    The name of the default queue used by `.apply_async` if the message has
    no route or no custom queue has been specified.

    This queue must be listed in :setting:`task_queues`.
    If :setting:`task_queues` isn't specified then it's automatically
    created containing one queue entry, where this name is used as the name of
    that queue.

    .. seealso::

        :ref:`routing-changing-default-queue`

.. setting:: task_default_queue_type

``task_default_queue_type``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.5

.. tab:: 中文

    默认值： ``"classic"``。

    该设置用于更改 :setting:`task_default_queue` 所使用的默认队列类型。另一个可用选项是 ``"quorum"``，仅在 RabbitMQ 中支持，会使用队列参数 ``x-queue-type`` 将队列类型设置为 ``quorum``。

    如果启用了 :setting:`worker_detect_quorum_queues` 设置，worker 将自动检测队列类型并相应地禁用全局 QoS。

    .. warning::

        quorum 队列需要启用 confirm publish。
        使用 :setting:`broker_transport_options` 设置以启用 confirm publish：

        .. code-block:: python

            broker_transport_options = {"confirm_publish": True}

        更多信息请参见 `RabbitMQ 官方文档 <https://www.rabbitmq.com/docs/quorum-queues#use-cases>`_。

.. tab:: 英文

    Default: ``"classic"``.

    This setting is used to allow changing the default queue type for the
    :setting:`task_default_queue` queue. The other viable option is ``"quorum"`` which
    is only supported by RabbitMQ and sets the queue type to ``quorum`` using the ``x-queue-type``
    queue argument.

    If the :setting:`worker_detect_quorum_queues` setting is enabled, the worker will
    automatically detect the queue type and disable the global QoS accordingly.

    .. warning::

        Quorum queues require confirm publish to be enabled.
        Use :setting:`broker_transport_options` to enable confirm publish by setting:

        .. code-block:: python

            broker_transport_options = {"confirm_publish": True}

        For more information, see `RabbitMQ documentation <https://www.rabbitmq.com/docs/quorum-queues#use-cases>`_.

.. setting:: task_default_exchange

``task_default_exchange``
~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    默认值：使用 :setting:`task_default_queue` 的值。

    在没有为 :setting:`task_queues` 中的条目指定自定义交换机时所使用的默认交换机名称。

.. tab:: 英文

    Default: Uses the value set for :setting:`task_default_queue`.

    Name of the default exchange to use when no custom exchange is
    specified for a key in the :setting:`task_queues` setting.

.. setting:: task_default_exchange_type

``task_default_exchange_type``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    默认值： ``"direct"``。

    在没有为 :setting:`task_queues` 中的条目指定自定义交换机类型时所使用的默认交换机类型。

.. tab:: 英文

    Default: ``"direct"``.

    Default exchange type used when no custom exchange type is specified
    for a key in the :setting:`task_queues` setting.

.. setting:: task_default_routing_key

``task_default_routing_key``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    默认值：使用 :setting:`task_default_queue` 的值。

    在没有为 :setting:`task_queues` 中的条目指定自定义路由键时所使用的默认路由键。

.. tab:: 英文

    Default: Uses the value set for :setting:`task_default_queue`.

    The default routing key used when no custom routing key
    is specified for a key in the :setting:`task_queues` setting.

.. setting:: task_default_delivery_mode

``task_default_delivery_mode``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``"persistent"``.

.. tab:: 中文

    可以为 `transient` （消息不写入磁盘）或 `persistent` （写入磁盘）。

.. tab:: 英文

    Can be `transient` (messages not written to disk) or `persistent` (written to
    disk).

.. _conf-broker-settings:

Broker 设置
---------------

Broker Settings

.. setting:: broker_url

``broker_url``
~~~~~~~~~~~~~~

Default: ``"amqp://"``

.. tab:: 中文

    默认的 broker URL。它必须是以下格式的 URL::

        transport://userid:password@hostname:port/virtual_host

    仅 scheme 部分（``transport://``）是必须的，其余部分是可选的，若未提供，则使用所选传输方式的默认值。

    transport 部分表示所使用的 broker 实现，默认是 ``amqp`` （如果安装了 ``librabbitmq`` 则使用之，否则回退至 ``pyamqp``）。还支持其他选项，如：``redis://``、``sqs://`` 和 ``qpid://``。

    scheme 也可以是你自定义传输实现的完整路径::

        broker_url = 'proj.transports.MyTransport://localhost'

    还可以指定多个相同传输方式的 broker URL。
    这些 broker URL 可以作为用分号分隔的单个字符串传入::

        broker_url = 'transport://userid:password@hostname:port//;transport://userid:password@hostname:port//'

    也可以作为列表指定::

        broker_url = [
            'transport://userid:password@localhost:port//',
            'transport://userid:password@hostname:port//'
        ]

    这些 broker 将按 :setting:`broker_failover_strategy` 设置使用。

    更多信息参见 Kombu 文档中的 :ref:`kombu:connection-urls`。

.. tab:: 英文

    Default broker URL. This must be a URL in the form of::

        transport://userid:password@hostname:port/virtual_host

    Only the scheme part (``transport://``) is required, the rest
    is optional, and defaults to the specific transports default values.

    The transport part is the broker implementation to use, and the
    default is ``amqp``, (uses ``librabbitmq`` if installed or falls back to
    ``pyamqp``). There are also other choices available, including;
    ``redis://``, ``sqs://``, and ``qpid://``.

    The scheme can also be a fully qualified path to your own transport
    implementation::

        broker_url = 'proj.transports.MyTransport://localhost'

    More than one broker URL, of the same transport, can also be specified.
    The broker URLs can be passed in as a single string that's semicolon delimited::

        broker_url = 'transport://userid:password@hostname:port//;transport://userid:password@hostname:port//'

    Or as a list::

        broker_url = [
            'transport://userid:password@localhost:port//',
            'transport://userid:password@hostname:port//'
        ]

    The brokers will then be used in the :setting:`broker_failover_strategy`.

    See :ref:`kombu:connection-urls` in the Kombu documentation for more
    information.

.. setting:: broker_read_url

.. setting:: broker_write_url

``broker_read_url`` / ``broker_write_url``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Taken from :setting:`broker_url`.

.. tab:: 中文

    以下设置可用于替代 :setting:`broker_url`，分别指定用于消费和生产的连接参数。

    示例::

        broker_read_url = 'amqp://user:pass@broker.example.com:56721'
        broker_write_url = 'amqp://user:pass@broker.example.com:56722'

    这两个选项也可以指定为列表以实现故障转移备用，更多信息参见 :setting:`broker_url`。

.. tab:: 英文

    These settings can be configured, instead of :setting:`broker_url` to specify
    different connection parameters for broker connections used for consuming and
    producing.

    Example::

        broker_read_url = 'amqp://user:pass@broker.example.com:56721'
        broker_write_url = 'amqp://user:pass@broker.example.com:56722'

    Both options can also be specified as a list for failover alternates, see
    :setting:`broker_url` for more information.

.. setting:: broker_failover_strategy

``broker_failover_strategy``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``"round-robin"``.

.. tab:: 中文

    用于 broker Connection 对象的默认故障转移策略。如果提供的值是字符串，则应映射至 'kombu.connection.failover_strategies' 中的键；也可以是一个方法引用，该方法从提供的列表中生成单个项。

    示例::

        # 随机故障转移策略
        def random_failover_strategy(servers):
            it = list(servers)  # 不修改调用方的列表
            shuffle = random.shuffle
            for _ in repeat(None):
                shuffle(it)
                yield it[0]

        broker_failover_strategy = random_failover_strategy

.. tab:: 英文

    Default failover strategy for the broker Connection object. If supplied,
    may map to a key in 'kombu.connection.failover_strategies', or be a reference
    to any method that yields a single item from a supplied list.

    Example::

        # Random failover strategy
        def random_failover_strategy(servers):
            it = list(servers)  # don't modify callers list
            shuffle = random.shuffle
            for _ in repeat(None):
                shuffle(it)
                yield it[0]

        broker_failover_strategy = random_failover_strategy

.. setting:: broker_heartbeat

``broker_heartbeat``
~~~~~~~~~~~~~~~~~~~~
:transports supported: ``pyamqp``

.. tab:: 中文

    默认值：``120.0`` （由服务器协商）。

    .. note::

        此值仅由 Worker 使用，客户端当前不会使用心跳机制。

    仅通过 TCP/IP 并不总能及时检测连接丢失，因此 AMQP 定义了一种称为心跳（heartbeat）的机制，
    由客户端和 broker 双方使用，以检测连接是否已关闭。

    如果心跳值设置为 10 秒，那么心跳检测的间隔由 :setting:`broker_heartbeat_checkrate` 设置控制
    （默认值是心跳值的两倍速率，也就是说，对于 10 秒的心跳值，心跳会每 5 秒检测一次）。

.. tab:: 英文

    Default: ``120.0`` (negotiated by server).

    Note: This value is only used by the worker, clients do not use
    a heartbeat at the moment.

    It's not always possible to detect connection loss in a timely
    manner using TCP/IP alone, so AMQP defines something called heartbeats
    that's is used both by the client and the broker to detect if
    a connection was closed.

    If the heartbeat value is 10 seconds, then
    the heartbeat will be monitored at the interval specified
    by the :setting:`broker_heartbeat_checkrate` setting (by default
    this is set to double the rate of the heartbeat value,
    so for the 10 seconds, the heartbeat is checked every 5 seconds).

.. setting:: broker_heartbeat_checkrate

``broker_heartbeat_checkrate``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:transports supported: ``pyamqp``

.. tab:: 中文

    Default: 2.0.

    Worker 会周期性地监控 broker 是否丢失过多心跳。该检查的速率通过将 :setting:`broker_heartbeat`
    除以该设置值计算得出，所以如果心跳为 10.0 且检测速率为默认的 2.0，检查将每 5 秒执行一次
    （即发送心跳的两倍速率）。

.. tab:: 英文

    Default: 2.0.

    At intervals the worker will monitor that the broker hasn't missed
    too many heartbeats. The rate at which this is checked is calculated
    by dividing the :setting:`broker_heartbeat` value with this value,
    so if the heartbeat is 10.0 and the rate is the default 2.0, the check
    will be performed every 5 seconds (twice the heartbeat sending rate).

.. setting:: broker_use_ssl

``broker_use_ssl``
~~~~~~~~~~~~~~~~~~
:transports supported: ``pyamqp``, ``redis``

Default: Disabled.

.. tab:: 中文

    切换 broker 连接上的 SSL 使用与相关设置。

    该选项的有效值取决于所用的传输类型。

.. tab:: 英文

    Toggles SSL usage on broker connection and SSL settings.

    The valid values for this option vary by transport.

``pyamqp``
__________

.. tab:: 中文

    如果为 ``True``，连接将使用默认 SSL 设置启用 SSL。
    如果为字典，将根据给定策略配置 SSL 连接，格式为 Python 的 :func:`ssl.wrap_socket` 选项格式。

    请注意，SSL 套接字通常由 broker 提供服务于单独的端口。

    以下是一个提供客户端证书并使用自定义 CA 验证服务端证书的示例：

    .. code-block:: python

        import ssl

        broker_use_ssl = {
        'keyfile': '/var/ssl/private/worker-key.pem',
        'certfile': '/var/ssl/amqp-server-cert.pem',
        'ca_certs': '/var/ssl/myca.pem',
        'cert_reqs': ssl.CERT_REQUIRED
        }

    .. versionadded:: 5.1

        从 Celery 5.1 开始，py-amqp 将始终验证从服务器收到的证书，
        因此不再需要手动设置 ``cert_reqs`` 为 ``ssl.CERT_REQUIRED``。

        之前的默认值 ``ssl.CERT_NONE`` 是不安全的，应避免使用。
        如果你希望恢复之前不安全的默认行为，可将 ``cert_reqs`` 设置为 ``ssl.CERT_NONE``。

.. tab:: 英文

    If ``True`` the connection will use SSL with default SSL settings.
    If set to a dict, will configure SSL connection according to the specified
    policy. The format used is Python's :func:`ssl.wrap_socket` options.

    Note that SSL socket is generally served on a separate port by the broker.

    Example providing a client cert and validating the server cert against a custom
    certificate authority:

    .. code-block:: python

        import ssl

        broker_use_ssl = {
        'keyfile': '/var/ssl/private/worker-key.pem',
        'certfile': '/var/ssl/amqp-server-cert.pem',
        'ca_certs': '/var/ssl/myca.pem',
        'cert_reqs': ssl.CERT_REQUIRED
        }

    .. versionadded:: 5.1

        Starting from Celery 5.1, py-amqp will always validate certificates received from the server
        and it is no longer required to manually set ``cert_reqs`` to ``ssl.CERT_REQUIRED``.

        The previous default, ``ssl.CERT_NONE`` is insecure and we its usage should be discouraged.
        If you'd like to revert to the previous insecure default set ``cert_reqs`` to ``ssl.CERT_NONE``


``redis``
_________

.. tab:: 中文

    该设置必须是包含以下键的字典：

    * ``ssl_cert_reqs`` （必需）：为 ``SSLContext.verify_mode`` 中的一个值：
    
    * ``ssl.CERT_NONE``
    * ``ssl.CERT_OPTIONAL``
    * ``ssl.CERT_REQUIRED``

    * ``ssl_ca_certs`` （可选）：CA 证书路径
    * ``ssl_certfile`` （可选）：客户端证书路径
    * ``ssl_keyfile`` （可选）：客户端密钥路径

.. tab:: 英文


    The setting must be a dict with the following keys:

    *  ``ssl_cert_reqs`` (required): one of the ``SSLContext.verify_mode`` values:
        * ``ssl.CERT_NONE``
        * ``ssl.CERT_OPTIONAL``
        * ``ssl.CERT_REQUIRED``
    *  ``ssl_ca_certs`` (optional): path to the CA certificate
    *  ``ssl_certfile`` (optional): path to the client certificate
    *  ``ssl_keyfile`` (optional): path to the client key


.. setting:: broker_pool_limit

``broker_pool_limit``
~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.3

Default: 10.

.. tab:: 中文

    连接池中可同时打开的最大连接数。

    自 2.5 版本起，连接池默认启用，默认限制为 10 个连接。
    该数值可根据使用连接的线程 / green-thread 数量（如 eventlet / gevent）进行调整。
    例如，当使用 eventlet 并拥有 1000 个使用 broker 连接的 greenlet 时，可能会产生争用，
    此时应考虑提高连接池上限。

    若设置为 :const:`None` 或 0，则连接池将被禁用，且每次使用时都会建立并关闭连接。

.. tab:: 英文

    The maximum number of connections that can be open in the connection pool.

    The pool is enabled by default since version 2.5, with a default limit of ten
    connections. This number can be tweaked depending on the number of
    threads/green-threads (eventlet/gevent) using a connection. For example
    running eventlet with 1000 greenlets that use a connection to the broker,
    contention can arise and you should consider increasing the limit.

    If set to :const:`None` or 0 the connection pool will be disabled and
    connections will be established and closed for every use.

.. setting:: broker_connection_timeout

``broker_connection_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 4.0.

.. tab:: 中文

    建立与 AMQP 服务器连接时的默认超时时间（单位：秒）。使用 gevent 时此设置将被禁用。

    .. note::

        broker 连接超时仅适用于 Worker 尝试连接 broker 的场景。
        它不适用于生产者（producer）发送任务的情况。有关该场景中如何设置超时，
        请参见 :setting:`broker_transport_options`。

.. tab:: 英文

    The default timeout in seconds before we give up establishing a connection
    to the AMQP server. This setting is disabled when using
    gevent.

    .. note::

        The broker connection timeout only applies to a worker attempting to
        connect to the broker. It does not apply to producer sending a task, see
        :setting:`broker_transport_options` for how to provide a timeout for that
        situation.

.. setting:: broker_connection_retry

``broker_connection_retry``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Enabled.

.. tab:: 中文

    在初次建立连接后，如果连接丢失，将自动尝试重新连接到 AMQP broker。

    重试之间的间隔会逐次递增，直到超过 :setting:`broker_connection_max_retries` 设置的最大重试次数。

    .. warning::

        从 Celery 6.0 起，配置项 ``broker_connection_retry`` 将不再决定
        启动期间是否进行连接重试。
        如果你希望在启动时不进行连接重试，应将 ``broker_connection_retry_on_startup`` 设置为 ``False``。

.. tab:: 英文

    Automatically try to re-establish the connection to the AMQP broker if lost
    after the initial connection is made.

    The time between retries is increased for each retry, and is
    not exhausted before :setting:`broker_connection_max_retries` is
    exceeded.

    .. warning::

        The broker_connection_retry configuration setting will no longer determine
        whether broker connection retries are made during startup in Celery 6.0 and above.
        If you wish to refrain from retrying connections on startup,
        you should set broker_connection_retry_on_startup to False instead.

.. setting:: broker_connection_retry_on_startup

``broker_connection_retry_on_startup``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Enabled.

.. tab:: 中文

    在 Celery 启动时，如果 broker 不可用，将自动尝试连接 AMQP broker。

    重试之间的间隔会逐次递增，直到超过 :setting:`broker_connection_max_retries` 设置的最大重试次数。

.. tab:: 英文

    Automatically try to establish the connection to the AMQP broker on Celery startup if it is unavailable.

    The time between retries is increased for each retry, and is
    not exhausted before :setting:`broker_connection_max_retries` is
    exceeded.

.. setting:: broker_connection_max_retries

``broker_connection_max_retries``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 100.

.. tab:: 中文

    在放弃重新连接 AMQP broker 之前的最大重试次数。

    如果设置为 :const:`None`，则将永久重试，直到连接成功。

.. tab:: 英文

    Maximum number of retries before we give up re-establishing a connection
    to the AMQP broker.

    If this is set to :const:`None`, we'll retry forever.

``broker_channel_error_retry``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.3

Default: Disabled.

.. tab:: 中文

    在收到无效响应时，自动尝试重新连接 AMQP broker。

    该选项的重试次数和间隔与 ``broker_connection_retry`` 相同。
    此外，当 ``broker_connection_retry`` 为 ``False`` 时，此选项也不会生效。

.. tab:: 英文

    Automatically try to re-establish the connection to the AMQP broker
    if any invalid response has been returned.

    The retry count and interval is the same as that of `broker_connection_retry`.
    Also, this option doesn't work when `broker_connection_retry` is `False`.

.. setting:: broker_login_method

``broker_login_method``
~~~~~~~~~~~~~~~~~~~~~~~

Default: ``"AMQPLAIN"``.

.. tab:: 中文

    设置自定义 AMQP 登录方式。

.. tab:: 英文

    Set custom amqp login method.

.. setting:: broker_native_delayed_delivery_queue_type

``broker_native_delayed_delivery_queue_type``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.5

:transports supported: ``pyamqp``

Default: ``"quorum"``.

.. tab:: 中文

    此设置用于更改原生延迟投递队列的默认队列类型。
    另一个可用的选项为 ``"classic"``，仅 RabbitMQ 支持，
    它会通过 ``x-queue-type`` 队列参数将队列类型设置为 ``classic``。

.. tab:: 英文

    This setting is used to allow changing the default queue type for the
    native delayed delivery queues. The other viable option is ``"classic"`` which
    is only supported by RabbitMQ and sets the queue type to ``classic`` using the ``x-queue-type``
    queue argument.

.. setting:: broker_transport_options

``broker_transport_options``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.2

Default: ``{}`` (empty mapping).

.. tab:: 中文

    传递给底层传输机制的额外选项字典。

    请参考所用传输方式的用户手册，以了解支持的选项（如有）。

    以下示例为设置可见性超时（Redis 和 SQS 传输支持）：

    .. code-block:: python

        broker_transport_options = {'visibility_timeout': 18000}  # 5 小时

    以下示例为设置生产者连接的最大重试次数
    （这样在首次任务执行时，如果 broker 不可用，生产者不会无限重试）：

    .. code-block:: python

        broker_transport_options = {'max_retries': 5}

.. tab:: 英文

    A dict of additional options passed to the underlying transport.

    See your transport user manual for supported options (if any).

    Example setting the visibility timeout (supported by Redis and SQS
    transports):

    .. code-block:: python

        broker_transport_options = {'visibility_timeout': 18000}  # 5 hours

    Example setting the producer connection maximum number of retries (so producers
    won't retry forever if the broker isn't available at the first task execution):

    .. code-block:: python

        broker_transport_options = {'max_retries': 5}

.. _conf-worker:

Worker
------

.. setting:: imports

``imports``
~~~~~~~~~~~

Default: ``[]`` (empty list).

.. tab:: 中文

    Worker 启动时要导入的一组模块序列。

    该设置用于指定要导入的任务模块，同时也可用于导入信号处理器、扩展远程控制命令等。

    模块将按照定义顺序依次导入。

.. tab:: 英文

    A sequence of modules to import when the worker starts.

    This is used to specify the task modules to import, but also
    to import signal handlers and additional remote control commands, etc.

    The modules will be imported in the original order.

.. setting:: include

``include``
~~~~~~~~~~~

Default: ``[]`` (empty list).

.. tab:: 中文

    该设置语义与 :setting:`imports` 完全相同，但可用于区分类别不同的导入项。

    此设置中的模块会在 :setting:`imports` 中定义的模块之后导入。

.. tab:: 英文

    Exact same semantics as :setting:`imports`, but can be used as a means
    to have different import categories.

    The modules in this setting are imported after the modules in
    :setting:`imports`.

.. setting:: worker_deduplicate_successful_tasks

``worker_deduplicate_successful_tasks``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.1

Default: False

.. tab:: 中文

    在每次任务执行前，指示 Worker 检查该任务是否为重复消息。

    去重仅适用于以下任务：具有相同的标识符、启用了延迟确认（late acknowledgment）、由消息代理重新投递，并且其状态在结果后端为 ``SUCCESS``。

    为避免在结果后端产生过多查询，Worker 会在查询结果后端之前先检查本地缓存，以判断任务是否已在本地成功执行过。

    可通过设置 :setting:`worker_state_db` 使此缓存持久化。

    如果结果后端不是 `持久化的 <https://github.com/celery/celery/blob/main/celery/backends/base.py#L102>`_
    （如 RPC 后端），此设置将被忽略。

.. tab:: 英文

    Before each task execution, instruct the worker to check if this task is
    a duplicate message.

    Deduplication occurs only with tasks that have the same identifier,
    enabled late acknowledgment, were redelivered by the message broker
    and their state is ``SUCCESS`` in the result backend.

    To avoid overflowing the result backend with queries, a local cache of
    successfully executed tasks is checked before querying the result backend
    in case the task was already successfully executed by the same worker that
    received the task.

    This cache can be made persistent by setting the :setting:`worker_state_db`
    setting.

    If the result backend is not `persistent <https://github.com/celery/celery/blob/main/celery/backends/base.py#L102>`_
    (the RPC backend, for example), this setting is ignored.

.. _conf-concurrency:

.. setting:: worker_concurrency

``worker_concurrency``
~~~~~~~~~~~~~~~~~~~~~~

Default: Number of CPU cores.

.. tab:: 中文

    同时执行任务的并发 Worker 进程/线程/协程数量。

    如果任务主要是 I/O 密集型，可设置更多并发；
    但如果是 CPU 密集型，建议将该值设为与主机 CPU 核心数接近。
    如果未设置，则使用主机的 CPU 核心数。

.. tab:: 英文

    The number of concurrent worker processes/threads/green threads executing
    tasks.

    If you're doing mostly I/O you can have more processes,
    but if mostly CPU-bound, try to keep it close to the
    number of CPUs on your machine. If not set, the number of CPUs/cores
    on the host will be used.

.. setting:: worker_prefetch_multiplier

``worker_prefetch_multiplier``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 4.

.. tab:: 中文

    每个进程可预取的消息数量，乘以并发进程数量。默认值为 4（即每个进程预取 4 条消息）。
    此默认设置通常是合适的，但若任务运行时间很长，并且你在 Worker 启动后才开始处理，
    注意第一个启动的 Worker 将一次性接收 4 倍数量的消息，可能导致任务分配不均。

    若要禁用预取行为，将 :setting:`worker_prefetch_multiplier` 设置为 1。
    如果设置为 0，则允许 Worker 不受限制地持续消费消息。

    有关预取机制的详细信息，请参阅 :ref:`optimizing-prefetch-limit`

    .. note::

        带 ETA/countdown 的任务不受预取限制影响。

.. tab:: 英文

    How many messages to prefetch at a time multiplied by the number of
    concurrent processes. The default is 4 (four messages for each
    process). The default setting is usually a good choice, however -- if you
    have very long running tasks waiting in the queue and you have to start the
    workers, note that the first worker to start will receive four times the
    number of messages initially. Thus the tasks may not be fairly distributed
    to the workers.

    To disable prefetching, set :setting:`worker_prefetch_multiplier` to 1.
    Changing that setting to 0 will allow the worker to keep consuming
    as many messages as it wants.

    For more on prefetching, read :ref:`optimizing-prefetch-limit`

    .. note::

        Tasks with ETA/countdown aren't affected by prefetch limits.

.. setting:: worker_enable_prefetch_count_reduction

``worker_enable_prefetch_count_reduction``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: Enabled.

.. tab:: 中文

    设置项 ``worker_enable_prefetch_count_reduction`` 控制在与消息代理断开连接后，
    Worker 是否会将预取计数恢复至最大允许值。默认该设置是启用的。

    当连接丢失时，Celery 会自动尝试重新连接 broker，前提是
    :setting:`broker_connection_retry_on_startup` 或 :setting:`broker_connection_retry` 没有被设为 False。
    在连接丢失期间，消息代理不会追踪已被获取的任务数量。为合理控制任务负载并防止过载，
    Celery 会根据当前正在运行的任务数来减少预取计数。

    预取计数是指 Worker 从 broker 一次性获取的消息数量。
    在重连期间降低预取计数有助于避免消息被过量获取。

    当 ``worker_enable_prefetch_count_reduction`` 保持默认启用状态时，每当一个在连接丢失前已启动的任务完成时，
    预取计数将逐步恢复到最大值。此机制有助于在 Worker 之间保持任务的合理分布，并有效管理负载。

    若要禁用此机制，即禁止在重连后减少和恢复预取计数，
    可将 ``worker_enable_prefetch_count_reduction`` 设置为 False。
    在某些场景下，例如需要使用固定预取计数来控制任务处理速率或管理 Worker 负载，
    特别是在网络连接波动的环境中，禁用此设置可能更合适。

    ``worker_enable_prefetch_count_reduction`` 提供了一种方式，
    用于控制在连接丢失后恢复预取计数的行为，从而帮助在 Worker 之间维持任务平衡和负载管理。

.. tab:: 英文

    The ``worker_enable_prefetch_count_reduction`` setting governs the restoration behavior of the
    prefetch count to its maximum allowable value following a connection loss to the message
    broker. By default, this setting is enabled.

    Upon a connection loss, Celery will attempt to reconnect to the broker automatically,
    provided the :setting:`broker_connection_retry_on_startup` or :setting:`broker_connection_retry`
    is not set to False. During the period of lost connection, the message broker does not keep track
    of the number of tasks already fetched. Therefore, to manage the task load effectively and prevent
    overloading, Celery reduces the prefetch count based on the number of tasks that are
    currently running.

    The prefetch count is the number of messages that a worker will fetch from the broker at
    a time. The reduced prefetch count helps ensure that tasks are not fetched excessively
    during periods of reconnection.

    With ``worker_enable_prefetch_count_reduction`` set to its default value (Enabled), the prefetch
    count will be gradually restored to its maximum allowed value each time a task that was
    running before the connection was lost is completed. This behavior helps maintain a
    balanced distribution of tasks among the workers while managing the load effectively.

    To disable the reduction and restoration of the prefetch count to its maximum allowed value on
    reconnection, set ``worker_enable_prefetch_count_reduction`` to False. Disabling this setting might
    be useful in scenarios where a fixed prefetch count is desired to control the rate of task
    processing or manage the worker load, especially in environments with fluctuating connectivity.

    The ``worker_enable_prefetch_count_reduction`` setting provides a way to control the
    restoration behavior of the prefetch count following a connection loss, aiding in
    maintaining a balanced task distribution and effective load management across the workers.

.. setting:: worker_lost_wait

``worker_lost_wait``
~~~~~~~~~~~~~~~~~~~~

Default: 10.0 seconds.

.. tab:: 中文

    在某些情况下，Worker 可能被异常终止，未能正常清理资源，
    并且可能在终止前已发布了任务结果。
    此设置值指定在引发 :exc:`@WorkerLostError` 异常前，等待缺失结果的最大时长。

.. tab:: 英文

    In some cases a worker may be killed without proper cleanup,
    and the worker may have published a result before terminating.
    This value specifies how long we wait for any missing results before
    raising a :exc:`@WorkerLostError` exception.

.. setting:: worker_max_tasks_per_child

``worker_max_tasks_per_child``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    每个进程池中的 Worker 子进程在被替换前最多可执行的任务数。默认没有限制。

.. tab:: 英文

    Maximum number of tasks a pool worker process can execute before
    it's replaced with a new one. Default is no limit.

.. setting:: worker_max_memory_per_child

``worker_max_memory_per_child``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: No limit.
Type: int (kilobytes)

.. tab:: 中文

    Worker 进程允许使用的最大常驻内存量（以 KB 为单位，1 KB = 1024 字节），
    超出该限制后 Worker 将被替换为新的进程。
    若单个任务导致该限制被超出，该任务会先完成，然后 Worker 被替换。

    示例：

    .. code-block:: python

        worker_max_memory_per_child = 12288  # 12 * 1024 = 12 MB

.. tab:: 英文

    Maximum amount of resident memory, in kilobytes (1024 bytes), that may be
    consumed by a worker before it will be replaced by a new worker. If a single
    task causes a worker to exceed this limit, the task will be completed, and the
    worker will be replaced afterwards.

    Example:

    .. code-block:: python

        worker_max_memory_per_child = 12288  # 12 * 1024 = 12 MB

.. setting:: worker_disable_rate_limits

``worker_disable_rate_limits``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled (rate limits enabled).

.. tab:: 中文

    禁用所有速率限制，即使任务显式设置了速率限制也无效。

.. tab:: 英文

    Disable all rate limits, even if tasks has explicit rate limits set.

.. setting:: worker_state_db

``worker_state_db``
~~~~~~~~~~~~~~~~~~~

Default: :const:`None`.

.. tab:: 中文

    用于存储 Worker 持久状态（例如被撤销的任务）的文件名。
    可以是相对路径或绝对路径，但请注意根据 Python 版本的不同，
    文件名可能会自动附加 `.db` 后缀。

    也可以通过 :option:`celery worker --statedb` 命令行参数进行设置。

.. tab:: 英文

    Name of the file used to stores persistent worker state (like revoked tasks).
    Can be a relative or absolute path, but be aware that the suffix `.db`
    may be appended to the file name (depending on Python version).

    Can also be set via the :option:`celery worker --statedb` argument.

.. setting:: worker_timer_precision

``worker_timer_precision``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 1.0 seconds.

.. tab:: 中文

    设置 ETA 调度器在重新检查调度计划之间最长可休眠的时间（以秒为单位）。

    若设置为 1 秒，则调度器的精度为 1 秒；
    若需近似毫秒级精度，可将其设置为 0.1。

.. tab:: 英文

    Set the maximum time in seconds that the ETA scheduler can sleep between
    rechecking the schedule.

    Setting this value to 1 second means the schedulers precision will
    be 1 second. If you need near millisecond precision you can set this to 0.1.

.. setting:: worker_enable_remote_control

``worker_enable_remote_control``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Enabled by default.

.. tab:: 中文

    指定是否启用对 Worker 的远程控制功能。

.. tab:: 英文

    Specify if remote control of the workers is enabled.

.. setting:: worker_proc_alive_timeout

``worker_proc_alive_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 4.0.

.. tab:: 中文

    等待新 Worker 进程启动的超时时间（单位为秒，支持整数或浮点数）。

.. tab:: 英文

    The timeout in seconds (int/float) when waiting for a new worker process to start up.

.. setting:: worker_cancel_long_running_tasks_on_connection_loss

``worker_cancel_long_running_tasks_on_connection_loss``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.1

Default: Disabled by default.

.. tab:: 中文

    在连接丢失时，终止所有启用了延迟确认的长时间运行任务。

    由于连接通道丢失，尚未确认的任务将无法完成确认，
    并将重新进入队列。因此启用了延迟确认的任务必须是幂等的，
    因为它们可能会被执行多次。
    在这种情况下，每次连接丢失都会导致任务被重复执行（有时甚至由多个 Worker 并行执行）。

    启用此选项后，尚未完成的任务将被取消，其执行会被终止。
    在连接丢失前已完成的任务，
    只要未启用 :setting:`task_ignore_result`，其结果仍会被写入结果后端。

    .. warning::

        此特性是将来的破坏性变更。

        若未启用，Celery 将发出警告信息。

        在 Celery 6.0 中，:setting:`worker_cancel_long_running_tasks_on_connection_loss`
        将默认设为 ``True``，因为当前行为引发的问题多于解决的问题。

.. tab:: 英文

    Kill all long-running tasks with late acknowledgment enabled on connection loss.

    Tasks which have not been acknowledged before the connection loss cannot do so
    anymore since their channel is gone and the task is redelivered back to the queue.
    This is why tasks with late acknowledged enabled must be idempotent as they may be executed more than once.
    In this case, the task is being executed twice per connection loss (and sometimes in parallel in other workers).

    When turning this option on, those tasks which have not been completed are
    cancelled and their execution is terminated.
    Tasks which have completed in any way before the connection loss
    are recorded as such in the result backend as long as :setting:`task_ignore_result` is not enabled.

    .. warning::

        This feature was introduced as a future breaking change.
        If it is turned off, Celery will emit a warning message.

        In Celery 6.0, the :setting:`worker_cancel_long_running_tasks_on_connection_loss`
        will be set to ``True`` by default as the current behavior leads to more
        problems than it solves.

.. setting:: worker_detect_quorum_queues

``worker_detect_quorum_queues``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.5

Default: Enabled.

.. tab:: 中文

    自动检测 :setting:`task_queues` 中的队列（包括 :setting:`task_default_queue`）是否为 Quorum 队列，
    如果存在任意 Quorum 队列，将禁用全局 QoS。

.. tab:: 英文

    Automatically detect if any of the queues in :setting:`task_queues` are quorum queues
    (including the :setting:`task_default_queue`) and disable the global QoS if any quorum queue is detected.

.. setting:: worker_soft_shutdown_timeout

``worker_soft_shutdown_timeout``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.5

Default: 0.0.

.. tab:: 中文

    标准的 :ref:`温关 <worker-warm-shutdown>` 会等待所有任务执行完毕后再关闭，
    除非触发冷关。:ref:`软关 <worker-soft-shutdown>` 会在启动冷关前加入等待时间。
    此设置用于指定 Worker 在冷关启动前的最大等待时长。

    即使未先执行温关，Worker 触发 :ref:`冷关 <worker-cold-shutdown>` 时也适用此设置。

    若该值设为 0.0，则软关将几乎等同于禁用。
    无论该值为何，若当前没有运行任务（除非启用 :setting:`worker_enable_soft_shutdown_on_idle`），
    软关将被跳过。

    建议尝试不同值来找到最适合你任务的优雅退出时间，推荐值包括 10、30、60 秒。
    过大的值可能导致 Worker 关闭延迟过长，甚至会被主机系统发送 :sig:`KILL` 信号强制终止。

.. tab:: 英文

    The standard :ref:`warm shutdown <worker-warm-shutdown>` will wait for all tasks to finish before shutting down
    unless the cold shutdown is triggered. The :ref:`soft shutdown <worker-soft-shutdown>` will add a waiting time
    before the cold shutdown is initiated. This setting specifies how long the worker will wait before the cold shutdown
    is initiated and the worker is terminated.

    This will apply also when the worker initiate :ref:`cold shutdown <worker-cold-shutdown>` without doing a warm shutdown first.

    If the value is set to 0.0, the soft shutdown will be practically disabled. Regardless of the value, the soft shutdown
    will be disabled if there are no tasks running (unless :setting:`worker_enable_soft_shutdown_on_idle` is enabled).

    Experiment with this value to find the optimal time for your tasks to finish gracefully before the worker is terminated.
    Recommended values can be 10, 30, 60 seconds. Too high value can lead to a long waiting time before the worker is terminated
    and trigger a :sig:`KILL` signal to forcefully terminate the worker by the host system.

.. setting:: worker_enable_soft_shutdown_on_idle

``worker_enable_soft_shutdown_on_idle``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.5

Default: False.

.. tab:: 中文

    若 :setting:`worker_soft_shutdown_timeout` 大于 0.0，但当前没有任务运行，
    Worker 仍会跳过 :ref:`软关 <worker-soft-shutdown>`。启用本设置后，
    即使无任务运行也会触发软关行为。

    .. tip::

        当 Worker 收到 ETA 任务，但尚未到达 ETA 时间，同时触发关机时，
        如果没有其他任务正在运行，Worker 会 **跳过** 软关，立即进入冷关流程。
        这可能导致 ETA 任务在 Worker 关闭过程中无法重新入队。
        为避免该问题，启用此设置可确保 Worker 等待一定时间，
        为 ETA 任务的重新入队和优雅关闭提供充足时间。

.. tab:: 英文

    If the :setting:`worker_soft_shutdown_timeout` is set to a value greater than 0.0, the worker will skip
    the :ref:`soft shutdown <worker-soft-shutdown>` anyways if there are no tasks running. This setting will
    enable the soft shutdown even if there are no tasks running.

    .. tip::

        When the worker received ETA tasks, but the ETA has not been reached yet, and a shutdown is initiated,
        the worker will **skip** the soft shutdown and initiate the cold shutdown immediately if there are no
        tasks running. This may lead to failure in re-queueing the ETA tasks during worker teardown. To mitigate
        this, enable this configuration to ensure the worker waits regadless, which gives enough time for a
        graceful shutdown and successful re-queueing of the ETA tasks.

.. _conf-events:

Events
------

.. setting:: worker_send_task_events

``worker_send_task_events``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled by default.

.. tab:: 中文

    发送任务相关事件，以便使用如 `flower` 等工具进行监控。
    该设置控制 Worker 的默认 :option:`-E <celery worker -E>` 参数。

.. tab:: 英文

    Send task-related events so that tasks can be monitored using tools like
    `flower`. Sets the default value for the workers
    :option:`-E <celery worker -E>` argument.

.. setting:: task_send_sent_event

``task_send_sent_event``
~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.2

Default: Disabled by default.

.. tab:: 中文

    若启用，则每个任务都会发送 :event:`task-sent` 事件，
    以便在任务被 Worker 消费前就能进行追踪。

.. tab:: 英文

    If enabled, a :event:`task-sent` event will be sent for every task so tasks can be
    tracked before they're consumed by a worker.

.. setting:: event_queue_ttl

``event_queue_ttl``
~~~~~~~~~~~~~~~~~~~
:transports supported: ``amqp``

Default: 5.0 seconds.

.. tab:: 中文

    消息在发送到监控客户端的事件队列后，其过期时间（以秒为单位，支持 int 或 float）。
    该设置将被用作消息的 ``x-message-ttl`` 属性。

    例如，若该值设为 10，则投递到该队列的消息将在 10 秒后被删除。

.. tab:: 英文

    Message expiry time in seconds (int/float) for when messages sent to a monitor clients
    event queue is deleted (``x-message-ttl``)

    For example, if this value is set to 10 then a message delivered to this queue
    will be deleted after 10 seconds.

.. setting:: event_queue_expires

``event_queue_expires``
~~~~~~~~~~~~~~~~~~~~~~~
:transports supported: ``amqp``

Default: 60.0 seconds.

.. tab:: 中文

    监控客户端的事件队列在未使用后被自动删除的过期时间（以秒为单位，支持 int 或 float）。
    该设置对应于 ``x-expires`` 属性。

.. tab:: 英文

    Expiry time in seconds (int/float) for when after a monitor clients
    event queue will be deleted (``x-expires``).

.. setting:: event_queue_prefix

``event_queue_prefix``
~~~~~~~~~~~~~~~~~~~~~~

Default: ``"celeryev"``.

.. tab:: 中文

    事件接收器队列名称使用的前缀。

.. tab:: 英文

    The prefix to use for event receiver queue names.

.. setting:: event_exchange

``event_exchange``
~~~~~~~~~~~~~~~~~~~~~~

Default: ``"celeryev"``.

.. tab:: 中文

    事件交换机（exchange）的名称。

    .. warning::

        此选项仍处于实验阶段，请谨慎使用。

.. tab:: 英文

    Name of the event exchange.

    .. warning::

        This option is in experimental stage, please use it with caution.

.. setting:: event_serializer

``event_serializer``
~~~~~~~~~~~~~~~~~~~~

Default: ``"json"``.

.. tab:: 中文

    发送事件消息时使用的消息序列化格式。

    .. seealso::

        :ref:`calling-serializers`

.. tab:: 英文

    Message serialization format used when sending event messages.

    .. seealso::

        :ref:`calling-serializers`.


.. setting:: events_logfile

``events_logfile``
~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    可选项，指定 :program:`celery events` 的日志输出文件路径（默认为输出到 `stdout`）。

.. tab:: 英文

    An optional file path for :program:`celery events` to log into (defaults to `stdout`).

.. setting:: events_pidfile

``events_pidfile``
~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    可选项，指定 :program:`celery events` 的 PID 文件创建/存储路径（默认不创建 PID 文件）。

.. tab:: 英文

    An optional file path for :program:`celery events` to create/store its PID file (default to no PID file created).

.. setting:: events_uid

``events_uid``
~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    可选项，:program:`celery events` 在降权运行时使用的用户 ID（默认不更改 UID）。

.. tab:: 英文

    An optional user ID to use when events :program:`celery events` drops its privileges (defaults to no UID change).

.. setting:: events_gid

``events_gid``
~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    可选项，:program:`celery events` 以守护进程运行时使用的用户组 ID（默认不更改 GID）。

.. tab:: 英文

    An optional group ID to use when :program:`celery events` daemon drops its privileges (defaults to no GID change).

.. setting:: events_umask

``events_umask``
~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    可选项，:program:`celery events` 在守护进程化创建文件（如日志、PID）时使用的 `umask`。

.. tab:: 英文

    An optional `umask` to use when :program:`celery events` creates files (log, pid...) when daemonizing.

.. setting:: events_executable

``events_executable``
~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    可选项，:program:`celery events` 守护进程化时使用的 `python` 可执行文件路径
    （默认为 :data:`sys.executable`）。

.. tab:: 英文

    An optional `python` executable path for :program:`celery events` to use when deaemonizing (defaults to :data:`sys.executable`).


.. _conf-control:

远程控制命令
-----------------------

Remote Control Commands

.. tab:: 中文

    .. note::

        如需禁用远程控制命令，请参阅 :setting:`worker_enable_remote_control` 设置项。

.. tab:: 英文

    .. note::

        To disable remote control commands see
        the :setting:`worker_enable_remote_control` setting.

.. setting:: control_queue_ttl

``control_queue_ttl``
~~~~~~~~~~~~~~~~~~~~~

Default: 300.0

.. tab:: 中文

    远程控制命令队列中的消息在发送后将过期的时间（以秒为单位）。

    若使用默认值 300 秒，表示如果在 300 秒内没有任何 Worker 消费该远程控制命令，
    该命令将被丢弃。

    该设置同样适用于远程控制的响应队列。

.. tab:: 英文

    Time in seconds, before a message in a remote control command queue
    will expire.

    If using the default of 300 seconds, this means that if a remote control
    command is sent and no worker picks it up within 300 seconds, the command
    is discarded.

    This setting also applies to remote control reply queues.

.. setting:: control_queue_expires

``control_queue_expires``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 10.0

.. tab:: 中文

    未使用的远程控制命令队列在多久后从消息代理中删除（单位：秒）。

    该设置同样适用于远程控制的响应队列。

.. tab:: 英文

    Time in seconds, before an unused remote control command queue is deleted
    from the broker.

    This setting also applies to remote control reply queues.

.. setting:: control_exchange

``control_exchange``
~~~~~~~~~~~~~~~~~~~~~~

Default: ``"celery"``.

.. tab:: 中文

    控制命令交换机的名称。

    .. warning::

        此选项仍处于实验阶段，请谨慎使用。

.. tab:: 英文

    Name of the control command exchange.

    .. warning::

        This option is in experimental stage, please use it with caution.

.. _conf-logging:

日志
-------

Logging

.. setting:: worker_hijack_root_logger

``worker_hijack_root_logger``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.2

Default: Enabled by default (hijack root logger).

.. tab:: 中文

    默认情况下，Celery 会移除根日志记录器（root logger）上已存在的所有处理器。
    若你希望自定义日志处理器，可以通过将
    `worker_hijack_root_logger = False` 来禁用此行为。

    .. note::

        也可以通过监听 :signal:`celery.signals.setup_logging` 信号来自定义日志系统。

.. tab:: 英文

    By default any previously configured handlers on the root logger will be
    removed. If you want to customize your own logging handlers, then you
    can disable this behavior by setting
    `worker_hijack_root_logger = False`.

    .. note::

        Logging can also be customized by connecting to the
        :signal:`celery.signals.setup_logging` signal.

.. setting:: worker_log_color

``worker_log_color``
~~~~~~~~~~~~~~~~~~~~

.. tab:: 中文

    默认值：若应用日志输出到终端，则启用。

    是否在 Celery 应用的日志输出中启用颜色显示。

.. tab:: 英文

    Default: Enabled if app is logging to a terminal.

    Enables/disables colors in logging output by the Celery apps.

.. setting:: worker_log_format

``worker_log_format``
~~~~~~~~~~~~~~~~~~~~~

Default:

.. code-block:: text

    "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"

.. tab:: 中文

    日志消息使用的格式。

    有关日志格式的详细信息，请参阅 Python 的 :mod:`logging` 模块。

.. tab:: 英文

    The format to use for log messages.

    See the Python :mod:`logging` module for more information about log
    formats.

.. setting:: worker_task_log_format

``worker_task_log_format``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default:

.. code-block:: text

    "[%(asctime)s: %(levelname)s/%(processName)s]
        %(task_name)s[%(task_id)s]: %(message)s"

.. tab:: 中文

    任务中记录日志时使用的日志消息格式。

    有关日志格式的详细信息，请参阅 Python 的 :mod:`logging` 模块。

.. tab:: 英文

    The format to use for log messages logged in tasks.

    See the Python :mod:`logging` module for more information about log
    formats.

.. setting:: worker_redirect_stdouts

``worker_redirect_stdouts``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: Enabled by default.

.. tab:: 中文

    若启用此选项，则 `stdout` 与 `stderr` 的输出将被重定向至当前日志记录器。

    适用于 :program:`celery worker` 与 :program:`celery beat`。

.. tab:: 英文

    If enabled `stdout` and `stderr` will be redirected
    to the current logger.

    Used by :program:`celery worker` and :program:`celery beat`.

.. setting:: worker_redirect_stdouts_level

``worker_redirect_stdouts_level``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`WARNING`.

.. tab:: 中文

    用于记录 `stdout` 与 `stderr` 输出的日志等级。
    可选值包括：:const:`DEBUG`、 :const:`INFO`、 :const:`WARNING`、 :const:`ERROR`、 :const:`CRITICAL`。

.. tab:: 英文

    The log level output to `stdout` and `stderr` is logged as.
    Can be one of :const:`DEBUG`, :const:`INFO`, :const:`WARNING`,
    :const:`ERROR`, or :const:`CRITICAL`.

.. _conf-security:

安全
--------

Security

.. setting:: security_key

``security_key``
~~~~~~~~~~~~~~~~

Default: :const:`None`.

.. versionadded:: 2.5

.. tab:: 中文

    当启用 :ref:`message-signing` 时，此配置指定用于对消息签名的私钥文件路径（相对或绝对路径）。

.. tab:: 英文

    The relative or absolute path to a file containing the private key
    used to sign messages when :ref:`message-signing` is used.

.. setting:: security_key_password

``security_key_password``
~~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`None`.

.. versionadded:: 5.3.0

.. tab:: 中文

    当启用 :ref:`message-signing` 时，此配置用于解密私钥的密码。

.. tab:: 英文

    The password used to decrypt the private key when :ref:`message-signing`
    is used.

.. setting:: security_certificate

``security_certificate``
~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`None`.

.. versionadded:: 2.5

.. tab:: 中文

    当启用 :ref:`message-signing` 时，此配置指定用于签名消息的 X.509 证书文件路径（相对或绝对路径）。

.. tab:: 英文

    The relative or absolute path to an X.509 certificate file
    used to sign messages when :ref:`message-signing` is used.

.. setting:: security_cert_store

``security_cert_store``
~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`None`.

.. versionadded:: 2.5

.. tab:: 中文

    用于 :ref:`message-signing` 的 X.509 证书所在目录。可以使用通配符（glob）路径，
    例如 :file:`/etc/certs/*.pem`。

.. tab:: 英文

    The directory containing X.509 certificates used for
    :ref:`message-signing`. Can be a glob with wild-cards,
    (for example :file:`/etc/certs/*.pem`).

.. setting:: security_digest

``security_digest``
~~~~~~~~~~~~~~~~~~~~~~~~

Default: :const:`sha256`.

.. versionadded:: 4.3

.. tab:: 中文

    当启用 :ref:`message-signing` 时，使用的消息签名摘要算法。
    参见：https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#module-cryptography.hazmat.primitives.hashes

.. tab:: 英文

    A cryptography digest used to sign messages
    when :ref:`message-signing` is used.
    https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/#module-cryptography.hazmat.primitives.hashes

.. _conf-custom-components:

自定义组件类(高级)
-----------------------------------

Custom Component Classes (advanced)

.. setting:: worker_pool

``worker_pool``
~~~~~~~~~~~~~~~

Default: ``"prefork"`` (``celery.concurrency.prefork:TaskPool``).

.. tab:: 中文

    Worker 使用的进程池类名称。

    .. admonition:: Eventlet/Gevent

        请勿使用此选项选择 eventlet 或 gevent 池。
        应使用 :option:`-P <celery worker -P>` 参数传给 :program:`celery worker`，
        以确保 monkey patch 能够及时应用，避免因应用顺序错误导致程序异常。

.. tab:: 英文

    Name of the pool class used by the worker.

    .. admonition:: Eventlet/Gevent

        Never use this option to select the eventlet or gevent pool.
        You must use the :option:`-P <celery worker -P>` option to
        :program:`celery worker` instead, to ensure the monkey patches
        aren't applied too late, causing things to break in strange ways.

.. setting:: worker_pool_restarts

``worker_pool_restarts``
~~~~~~~~~~~~~~~~~~~~~~~~

Default: Disabled by default.

.. tab:: 中文

    启用后，可以通过 :control:`pool_restart` 远程控制命令重启 worker 的进程池。

.. tab:: 英文

    If enabled the worker pool can be restarted using the
    :control:`pool_restart` remote control command.

.. setting:: worker_autoscaler

``worker_autoscaler``
~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 2.2

Default: ``"celery.worker.autoscale:Autoscaler"``.

.. tab:: 中文

    用于自动扩缩容的类名称。

.. tab:: 英文

    Name of the autoscaler class to use.

.. setting:: worker_consumer

``worker_consumer``
~~~~~~~~~~~~~~~~~~~

Default: ``"celery.worker.consumer:Consumer"``.

.. tab:: 中文

    Worker 使用的消费者（consumer）类名称。

.. tab:: 英文

    Name of the consumer class used by the worker.

.. setting:: worker_timer

``worker_timer``
~~~~~~~~~~~~~~~~

Default: ``"kombu.asynchronous.hub.timer:Timer"``.

.. tab:: 中文

    Worker 使用的 ETA 调度器类名称。
    默认由进程池实现指定。

.. tab:: 英文

    Name of the ETA scheduler class used by the worker.
    Default is or set by the pool implementation.

.. setting:: worker_logfile

``worker_logfile``
~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery worker` 的可选日志输出文件路径（默认为输出到 `stdout`）。

.. tab:: 英文

    An optional file path for :program:`celery worker` to log into (defaults to `stdout`).

.. setting:: worker_pidfile

``worker_pidfile``
~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery worker` 的可选 PID 文件创建/存储路径（默认不创建 PID 文件）。

.. tab:: 英文

    An optional file path for :program:`celery worker` to create/store its PID file (defaults to no PID file created).

.. setting:: worker_uid

``worker_uid``
~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    当 :program:`celery worker` 守护进程化运行时，降权使用的用户 ID（默认不更改 UID）。

.. tab:: 英文

    An optional user ID to use when :program:`celery worker` daemon drops its privileges (defaults to no UID change).

.. setting:: worker_gid

``worker_gid``
~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    当 :program:`celery worker` 守护进程化运行时，降权使用的用户组 ID（默认不更改 GID）。

.. tab:: 英文

    An optional group ID to use when :program:`celery worker` daemon drops its privileges (defaults to no GID change).

.. setting:: worker_umask

``worker_umask``
~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery worker` 守护进程化运行时创建文件（日志、PID 文件等）使用的 `umask` （可选）。

.. tab:: 英文

    An optional `umask` to use when :program:`celery worker` creates files (log, pid...) when daemonizing.

.. setting:: worker_executable

``worker_executable``
~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery worker` 守护进程化运行时使用的 `python` 可执行文件路径（可选，默认为 :data:`sys.executable`）。

.. tab:: 英文

    An optional `python` executable path for :program:`celery worker` to use when deaemonizing (defaults to :data:`sys.executable`).

.. _conf-celerybeat:

调度设置 (:program:`celery beat`)
--------------------------------------

Beat Settings (:program:`celery beat`)

.. setting:: beat_schedule

``beat_schedule``
~~~~~~~~~~~~~~~~~

Default: ``{}`` (empty mapping).

.. tab:: 中文

    由 :mod:`~celery.bin.beat` 使用的周期性任务调度配置。
    参见 :ref:`beat-entries`。

.. tab:: 英文

    The periodic task schedule used by :mod:`~celery.bin.beat`.
    See :ref:`beat-entries`.

.. setting:: beat_scheduler

``beat_scheduler``
~~~~~~~~~~~~~~~~~~

Default: ``"celery.beat:PersistentScheduler"``.

.. tab:: 中文

    默认使用的调度器类。
    例如，在配合 :pypi:`django-celery-beat` 扩展使用时，可设置为
    ``"django_celery_beat.schedulers:DatabaseScheduler"``。

    也可以通过 :option:`celery beat -S` 参数进行设置。

.. tab:: 英文

    The default scheduler class. May be set to
    ``"django_celery_beat.schedulers:DatabaseScheduler"`` for instance,
    if used alongside :pypi:`django-celery-beat` extension.

    Can also be set via the :option:`celery beat -S` argument.

.. setting:: beat_schedule_filename

``beat_schedule_filename``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: ``"celerybeat-schedule"``.

.. tab:: 中文

    当使用 `PersistentScheduler` 时，存储周期性任务最后运行时间的文件名。
    可为相对路径或绝对路径，但注意在某些 Python 版本中可能自动添加 `.db` 后缀。

    也可通过 :option:`celery beat --schedule` 参数进行设置。

.. tab:: 英文

    Name of the file used by `PersistentScheduler` to store the last run times
    of periodic tasks. Can be a relative or absolute path, but be aware that the
    suffix `.db` may be appended to the file name (depending on Python version).

    Can also be set via the :option:`celery beat --schedule` argument.

.. setting:: beat_sync_every

``beat_sync_every``
~~~~~~~~~~~~~~~~~~~

Default: 0.

.. tab:: 中文

    在执行下一次数据库同步前，最多允许调度的周期性任务数量。

    默认值为 0，表示根据时间间隔进行同步——默认间隔为 3 分钟，由 scheduler.sync_every 决定。
    若设置为 1，则每发送一个任务消息就执行一次同步。

.. tab:: 英文

    The number of periodic tasks that can be called before another database sync
    is issued.
    A value of 0 (default) means sync based on timing - default of 3 minutes as determined by
    scheduler.sync_every. If set to 1, beat will call sync after every task
    message sent.

.. setting:: beat_max_loop_interval

``beat_max_loop_interval``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Default: 0.

.. tab:: 中文

    :mod:`~celery.bin.beat` 在两次检查调度之间最多可休眠的秒数。

    此值的默认取决于具体调度器。
    对于默认的 Celery beat 调度器，默认值为 300 秒（5 分钟）；
    而对基于 :pypi:`django-celery-beat` 的数据库调度器而言，默认值为 5 秒，
    因为调度计划可能由外部更改，因此需要及时感知并应用变更。

    此外，当在 Jython 环境中以线程方式嵌入运行 Celery beat（使用 :option:`-B <celery worker -B>`）时，
    最大间隔会被重写为 1 秒，以保证能够及时关闭线程。

.. tab:: 英文

    The maximum number of seconds :mod:`~celery.bin.beat` can sleep
    between checking the schedule.

    The default for this value is scheduler specific.
    For the default Celery beat scheduler the value is 300 (5 minutes),
    but for the :pypi:`django-celery-beat` database scheduler it's 5 seconds
    because the schedule may be changed externally, and so it must take
    changes to the schedule into account.

    Also when running Celery beat embedded (:option:`-B <celery worker -B>`)
    on Jython as a thread the max interval is overridden and set to 1 so
    that it's possible to shut down in a timely manner.

.. setting:: beat_cron_starting_deadline

``beat_cron_starting_deadline``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.3

Default: None.

.. tab:: 中文

    在使用 cron 调度时，:mod:`~celery.bin.beat` 在判断调度是否到期时可向前回溯的秒数。
    当设置为 `None` 时，所有超时的 cron 任务都会被立即执行。

.. tab:: 英文

    When using cron, the number of seconds :mod:`~celery.bin.beat` can look back
    when deciding whether a cron schedule is due. When set to `None`, cronjobs that
    are past due will always run immediately.

.. setting:: beat_logfile

``beat_logfile``
~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery beat` 的可选日志输出文件路径（默认为输出到 `stdout`）。

.. tab:: 英文

    An optional file path for :program:`celery beat` to log into (defaults to `stdout`).

.. setting:: beat_pidfile

``beat_pidfile``
~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery beat` 的可选 PID 文件创建/存储路径（默认不创建 PID 文件）。

.. tab:: 英文

    An optional file path for :program:`celery beat` to create/store it PID file (defaults to no PID file created).

.. setting:: beat_uid

``beat_uid``
~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    当 :program:`celery beat` 守护进程化运行时，降权使用的用户 ID（默认不更改 UID）。

.. tab:: 英文

    An optional user ID to use when beat :program:`celery beat` drops its privileges (defaults to no UID change).

.. setting:: beat_gid

``beat_gid``
~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    当 :program:`celery beat` 守护进程化运行时，降权使用的用户组 ID（默认不更改 GID）。

.. tab:: 英文

    An optional group ID to use when :program:`celery beat` daemon drops its privileges (defaults to no GID change).

.. setting:: beat_umask

``beat_umask``
~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery beat` 守护进程化运行时创建文件（日志、PID 文件等）使用的 `umask` （可选）。

.. tab:: 英文

    An optional `umask` to use when :program:`celery beat` creates files (log, pid...) when daemonizing.

.. setting:: beat_executable

``beat_executable``
~~~~~~~~~~~~~~~~~~~

.. versionadded:: 5.4

Default: :const:`None`

.. tab:: 中文

    :program:`celery beat` 守护进程化运行时使用的 `python` 可执行文件路径（可选，默认为 :data:`sys.executable`）。

.. tab:: 英文

    An optional `python` executable path for :program:`celery beat` to use when deaemonizing (defaults to :data:`sys.executable`).
