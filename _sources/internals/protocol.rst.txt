.. _message-protocol:

===================
消息协议
===================

Message Protocol


.. _message-protocol-task:
.. _internals-task-message-protocol:

Task 消息
=============

Task messages

.. _message-protocol-task-v2:

版本 2
---------

Version 2

定义
~~~~~~~~~~

Definition

.. code-block:: python

    properties = {
        'correlation_id': uuid task_id,
        'content_type': string mimetype,
        'content_encoding': string encoding,

        # optional
        'reply_to': string queue_or_url,
    }
    headers = {
        'lang': string 'py'
        'task': string task,
        'id': uuid task_id,
        'root_id': uuid root_id,
        'parent_id': uuid parent_id,
        'group': uuid group_id,

        # optional
        'meth': string method_name,
        'shadow': string alias_name,
        'eta': iso8601 ETA,
        'expires': iso8601 expires,
        'retries': int retries,
        'timelimit': (soft, hard),
        'argsrepr': str repr(args),
        'kwargsrepr': str repr(kwargs),
        'origin': str nodename,
        'replaced_task_nesting': int
    }

    body = (
        object[] args,
        Mapping kwargs,
        Mapping embed {
            'callbacks': Signature[] callbacks,
            'errbacks': Signature[] errbacks,
            'chain': Signature[] chain,
            'chord': Signature chord_callback,
        }
    )

示例
~~~~~~~

Example

.. tab:: 中文

    此示例使用协议版本 2 发送任务消息：

.. tab:: 英文

    This example sends a task message using version 2 of the protocol:

.. code-block:: python

    # chain: add(add(add(2, 2), 4), 8) == 2 + 2 + 4 + 8

    import json
    import os
    import socket

    task_id = uuid()
    args = (2, 2)
    kwargs = {}
    basic_publish(
        message=json.dumps((args, kwargs, None)),
        application_headers={
            'lang': 'py',
            'task': 'proj.tasks.add',
            'argsrepr': repr(args),
            'kwargsrepr': repr(kwargs),
            'origin': '@'.join([os.getpid(), socket.gethostname()])
        }
        properties={
            'correlation_id': task_id,
            'content_type': 'application/json',
            'content_encoding': 'utf-8',
        }
    )

与版本 1 的变更
~~~~~~~~~~~~~~~~~~~~~~

Changes from version 1

.. tab:: 中文

    - 通过 ``task`` 消息头检测协议版本。

    - 通过 ``lang`` 消息头支持多语言。  
      Worker 可以将消息重定向给支持该语言的其他 worker。

    - 元数据迁移至消息头（headers）。  
      这意味着 worker 或中间件可以在不解码消息主体（payload）的情况下  
      基于消息头内容做出决策，例如 payload 使用了 Python 特有的 pickle 序列化方式。

    - 始终使用 UTC 时间  
      不再使用 ``utc`` 标志，因此任何缺失时区信息的时间值将被视为 UTC 时间。

    - 消息体（body）仅用于语言相关的数据。  
      - Python 将 args/kwargs 和嵌入的签名存储于消息体中。  
      - 如果消息使用原始编码（raw encoding），则原始数据会作为单一参数传递给函数。  
      - Java/C 等语言可以使用 Thrift/protobuf 文档作为消息体内容。

    - ``origin`` 表示发送任务的节点名称。

    - 基于 ``task`` 与 ``meth`` 消息头分发给对应 actor。  
      ``meth`` 在 Python 中未使用，但将来可能用于指定类+方法对。

    - Chain（链式调用）获得了专用字段。  
      之前将 chain 递归地嵌套在 ``callbacks`` 参数中，  
      会在递归层级过深时导致问题。

      新消息协议通过指定一个签名列表来解决此问题，  
      每个任务在发送下一个消息时从列表中弹出一个签名：

      .. code-block:: python

          execute_task(message)
          chain = embed['chain']
          if chain:
              sig = maybe_signature(chain.pop())
              sig.apply_async(chain=chain)

    - ``correlation_id`` 替代了原先的 ``task_id`` 字段。

    - ``root_id`` 和 ``parent_id`` 字段用于追踪完整的工作流链路。

    - ``shadow`` 允许为日志指定不同的任务名称，  
      监控工具可用于表示某些以函数作为参数调用的任务概念：

      .. code-block:: python

          from celery.utils.imports import qualname

          class PickleTask(Task):

              def unpack_args(self, fun, args=()):
                  return fun, args

              def apply_async(self, args, kwargs, **options):
                  fun, real_args = self.unpack_args(*args)
                  return super().apply_async(
                      (fun, real_args, kwargs), shadow=qualname(fun), **options
                  )

          @app.task(base=PickleTask)
          def call(fun, args, kwargs):
              return fun(*args, **kwargs)


.. tab:: 英文

    - Protocol version detected by the presence of a ``task`` message header.

    - Support for multiple languages via the ``lang`` header.
        Worker may redirect the message to a worker that supports
        the language.

    - Meta-data moved to headers.
        This means that workers/intermediates can inspect the message
        and make decisions based on the headers without decoding
        the payload (that may be language specific, for example serialized by the
        Python specific pickle serializer).

    - Always UTC
        There's no ``utc`` flag anymore, so any time information missing timezone
        will be expected to be in UTC time.

    - Body is only for language specific data.
        - Python stores args/kwargs and embedded signatures in body.

        - If a message uses raw encoding then the raw data
        will be passed as a single argument to the function.

        - Java/C, etc. can use a Thrift/protobuf document as the body

    - ``origin`` is the name of the node sending the task.

    - Dispatches to actor based on ``task``, ``meth`` headers
        ``meth`` is unused by Python, but may be used in the future
        to specify class+method pairs.

    - Chain gains a dedicated field.
        Reducing the chain into a recursive ``callbacks`` argument
        causes problems when the recursion limit is exceeded.

        This is fixed in the new message protocol by specifying
        a list of signatures, each task will then pop a task off the list
        when sending the next message:

        .. code-block:: python

            execute_task(message)
            chain = embed['chain']
            if chain:
                sig = maybe_signature(chain.pop())
                sig.apply_async(chain=chain)

    - ``correlation_id`` replaces ``task_id`` field.

    - ``root_id`` and ``parent_id`` fields helps keep track of work-flows.

    - ``shadow`` lets you specify a different name for logs, monitors can be used for concepts like tasks that calls a function specified as argument:
        .. code-block:: python

            from celery.utils.imports import qualname

            class PickleTask(Task):

                def unpack_args(self, fun, args=()):
                    return fun, args

                def apply_async(self, args, kwargs, **options):
                    fun, real_args = self.unpack_args(*args)
                    return super().apply_async(
                        (fun, real_args, kwargs), shadow=qualname(fun), **options
                    )

            @app.task(base=PickleTask)
            def call(fun, args, kwargs):
                return fun(*args, **kwargs)


.. _message-protocol-task-v1:
.. _task-message-protocol-v1:

版本 1
---------

Version 1

.. tab:: 中文

    在协议的第 1 版中，所有字段都存储在消息体中：  
    这意味着 worker 和中间消费者必须反序列化 payload 才能读取字段内容。

.. tab:: 英文

    In version 1 of the protocol all fields are stored in the message body:
    meaning workers and intermediate consumers must deserialize the payload
    to read the fields.

消息正文
~~~~~~~~~~~~

Message body

.. tab:: 中文

    * ``task``  
        :`string`:

        任务名称。**必需**

    * ``id``  
        :`string`:

        任务的唯一标识（UUID）。**必需**

    * ``args``  
        :`list`:

        参数列表。如果未提供则为一个空列表。

    * ``kwargs``  
        :`dictionary`:

        关键字参数字典。如果未提供则为一个空字典。

    * ``retries``  
        :`int`:

        当前任务已重试的次数。如果未指定则默认为 `0`。

    * ``eta``  
        :`string` (ISO 8601):

        预计到达时间，采用 ISO 8601 格式的日期和时间。  
        如果未提供，该消息不会被调度，而是尽快执行。

    * ``expires``  
        :`string` (ISO 8601):

        .. versionadded:: 2.0.2

        过期时间，采用 ISO 8601 格式的日期和时间。  
        如果未提供，该消息将永不过期。  
        当消息被接收时若已超出过期时间，则该消息将被视为已过期。

    * ``taskset``  
        :`string`:

        此任务所属的任务组（如果有）。

    * ``chord``  
        :`Signature`:

        .. versionadded:: 2.3

        表示该任务是 chord 的 header 部分之一。  
        该字段的值是 chord 的 body，  
        它将在所有 header 中的任务完成后被执行。

    * ``utc``  
        :`bool`:

        .. versionadded:: 2.5

        若为 true，则时间使用 UTC 时区；否则应使用当前本地时区。

    * ``callbacks``  
        :`<list>Signature`:

        .. versionadded:: 3.0

        当任务成功完成时将调用的签名列表。

    * ``errbacks``  
        :`<list>Signature`:

        .. versionadded:: 3.0

        当任务执行出错时将调用的签名列表。

    * ``timelimit``  
        :`<tuple>(float, float)`:

        .. versionadded:: 3.1

        任务执行时间限制配置。此字段是一个包含软/硬超时的元组  
        （可为 `int`/`float`，或使用 :const:`None` 表示不限制）。

        以下示例表示软时间限制为 3 秒，硬时间限制为 10 秒::

            {'timelimit': (3.0, 10.0)}

.. tab:: 英文

    * ``task``
        :`string`:

        Name of the task. **required**

    * ``id``
        :`string`:

        Unique id of the task (UUID). **required**

    * ``args``
        :`list`:

        List of arguments. Will be an empty list if not provided.

    * ``kwargs``
        :`dictionary`:

        Dictionary of keyword arguments. Will be an empty dictionary if not
        provided.

    * ``retries``
        :`int`:

        Current number of times this task has been retried.
        Defaults to `0` if not specified.

    * ``eta``
        :`string` (ISO 8601):

        Estimated time of arrival. This is the date and time in ISO 8601
        format. If not provided the message isn't scheduled, but will be
        executed asap.

    * ``expires``
        :`string` (ISO 8601):

        .. versionadded:: 2.0.2

        Expiration date. This is the date and time in ISO 8601 format.
        If not provided the message will never expire. The message
        will be expired when the message is received and the expiration date
        has been exceeded.

    * ``taskset``
        :`string`:

        The group this task is part of (if any).

    * ``chord``
        :`Signature`:

        .. versionadded:: 2.3

        Signifies that this task is one of the header parts of a chord. The value
        of this key is the body of the cord that should be executed when all of
        the tasks in the header has returned.

    * ``utc``
        :`bool`:

        .. versionadded:: 2.5

        If true time uses the UTC timezone, if not the current local timezone
        should be used.

    * ``callbacks``
        :`<list>Signature`:

        .. versionadded:: 3.0

        A list of signatures to call if the task exited successfully.

    * ``errbacks``
        :`<list>Signature`:

        .. versionadded:: 3.0

        A list of signatures to call if an error occurs while executing the task.

    * ``timelimit``
        :`<tuple>(float, float)`:

        .. versionadded:: 3.1

        Task execution time limit settings. This is a tuple of hard and soft time
        limit value (`int`/`float` or :const:`None` for no limit).

        Example value specifying a soft time limit of 3 seconds, and a hard time
        limit of 10 seconds::

            {'timelimit': (3.0, 10.0)}


示例消息
~~~~~~~~~~~~~~~

Example message

.. tab:: 中文

    以下是以 JSON 格式调用 `celery.task.ping` 任务的示例：

    .. code-block:: javascript

        {"id": "4cc7438e-afd4-4f8f-a2f3-f46567e7ca77",
         "task": "celery.task.PingTask",
         "args": [],
         "kwargs": {},
         "retries": 0,
         "eta": "2009-11-17T12:30:56.527191"}


.. tab:: 英文

    This is an example invocation of a `celery.task.ping` task in json
    format:

    .. code-block:: javascript

        {"id": "4cc7438e-afd4-4f8f-a2f3-f46567e7ca77",
         "task": "celery.task.PingTask",
         "args": [],
         "kwargs": {},
         "retries": 0,
         "eta": "2009-11-17T12:30:56.527191"}

任务序列化
------------------

Task Serialization

.. tab:: 中文

    使用 `content_type` 消息头支持多种类型的序列化格式。

    默认支持的 MIME 类型如下表所示：

    =============== =================================
            Scheme                 MIME 类型
    =============== =================================
    json            application/json
    yaml            application/x-yaml
    pickle          application/x-python-serialize
    msgpack         application/x-msgpack
    =============== =================================

.. tab:: 英文

    Several types of serialization formats are supported using the
    `content_type` message header.

    The MIME-types supported by default are shown in the following table.

    =============== =================================
            Scheme                 MIME Type
    =============== =================================
    json            application/json
    yaml            application/x-yaml
    pickle          application/x-python-serialize
    msgpack         application/x-msgpack
    =============== =================================

.. _message-protocol-event:

Event 消息
==============

Event Messages

.. tab:: 中文

    事件消息始终使用 JSON 进行序列化，并可包含任意的消息体字段。

    自 4.0 版本起，消息体可以是单个映射（单个事件），也可以是映射列表（多个事件）。

    此外，事件消息中还必须包含一些标准字段：

.. tab:: 英文

    Event messages are always JSON serialized and can contain arbitrary message
    body fields.

    Since version 4.0. the body can consist of either a single mapping (one event),
    or a list of mappings (multiple events).

    There are also standard fields that must always be present in an event
    message:

标准正文字段
--------------------

Standard body fields

.. tab:: 中文

    - *string* ``type``  
        事件类型。该字段是一个字符串，包含 *类别* 与 *动作*，  
        两者之间以连字符分隔（例如：``task-succeeded``）。

    - *string* ``hostname``  
        发生事件的完整主机名。

    - *unsigned long long* ``clock``  
        此事件的逻辑时钟值（Lamport 时间戳）。

    - *float* ``timestamp``  
        事件发生时对应的 UNIX 时间戳。

    - *signed short* ``utcoffset``  
        描述事件源主机的时区。该字段表示相对于 UTC 的时差小时数  
        （例如：-2 或 +1）。

    - *unsigned long long* ``pid``  
        事件来源进程的进程 ID。

.. tab:: 英文

    - *string* ``type``
        The type of event. This is a string containing the *category* and
        *action* separated by a dash delimiter (e.g., ``task-succeeded``).

    - *string* ``hostname``
        The fully qualified hostname of where the event occurred at.

    - *unsigned long long* ``clock``
        The logical clock value for this event (Lamport time-stamp).

    - *float* ``timestamp``
        The UNIX time-stamp corresponding to the time of when the event occurred.

    - *signed short* ``utcoffset``
        This field describes the timezone of the originating host, and is
        specified as the number of hours ahead of/behind UTC (e.g., -2 or
        +1).

    - *unsigned long long* ``pid``
        The process id of the process the event originated in.

标准事件类型
--------------------

Standard event types

.. tab:: 中文

    有关标准事件类型及其字段的完整列表，请参阅 :ref:`event-reference`。

.. tab:: 英文

    For a list of standard event types and their fields see the :ref:`event-reference`.

示例消息
---------------

Example message

.. tab:: 中文

    以下是 ``task-succeeded`` 事件的消息字段示例：

    .. code-block:: python

        properties = {
            'routing_key': 'task.succeeded',
            'exchange': 'celeryev',
            'content_type': 'application/json',
            'content_encoding': 'utf-8',
            'delivery_mode': 1,
        }
        headers = {
            'hostname': 'worker1@george.vandelay.com',
        }
        body = {
            'type': 'task-succeeded',
            'hostname': 'worker1@george.vandelay.com',
            'pid': 6335,
            'clock': 393912923921,
            'timestamp': 1401717709.101747,
            'utcoffset': -1,
            'uuid': '9011d855-fdd1-4f8f-adb3-a413b499eafb',
            'retval': '4',
            'runtime': 0.0003212,
        }

.. tab:: 英文

    This is the message fields for a ``task-succeeded`` event:

    .. code-block:: python

        properties = {
            'routing_key': 'task.succeeded',
            'exchange': 'celeryev',
            'content_type': 'application/json',
            'content_encoding': 'utf-8',
            'delivery_mode': 1,
        }
        headers = {
            'hostname': 'worker1@george.vandelay.com',
        }
        body = {
            'type': 'task-succeeded',
            'hostname': 'worker1@george.vandelay.com',
            'pid': 6335,
            'clock': 393912923921,
            'timestamp': 1401717709.101747,
            'utcoffset': -1,
            'uuid': '9011d855-fdd1-4f8f-adb3-a413b499eafb',
            'retval': '4',
            'runtime': 0.0003212,
        )
