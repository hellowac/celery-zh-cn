.. _glossary:

术语
========

Glossary

.. glossary::
    :sorted:

    acknowledged

        .. tab:: 中文

            Worker 通过确认（acknowledge）消息来表示某条消息已被处理。如果未确认某条消息，则该消息将会被重新投递。事务在何时被视为失败取决于所使用的传输机制。在 AMQP 中，当连接或信道关闭（或丢失）时事务被视为失败；而在 Redis/SQS 中，事务在配置的时间（ ``visibility_timeout`` ）之后超时。

        .. tab:: 英文
        
            Workers acknowledge messages to signify that a message has been handled. Failing to acknowledge a message will cause the message to be redelivered. Exactly when a transaction is considered a failure varies by transport. In AMQP the transaction fails when the connection/channel is closed (or lost), but in Redis/SQS the transaction times out after a configurable amount of time (the ``visibility_timeout``).

    ack

        .. tab:: 中文

            为 :term:`acknowledged` 的简写。

        .. tab:: 英文

            Short for :term:`acknowledged`.

    early acknowledgment

        .. tab:: 中文

            任务在执行之前即时被 :term:`acknowledged`，意味着如果机器在执行过程中断电，或者 worker 实例被突然终止，该任务不会被重新投递给其他 worker。

            通过 :setting:`task_acks_late` 配置。

        .. tab:: 英文

            Task is :term:`acknowledged` just-in-time before being executed, meaning the task won't be redelivered to another worker if the machine loses power, or the worker instance is abruptly killed, mid-execution.

            Configured using :setting:`task_acks_late`.

    late acknowledgment

        .. tab:: 中文

            任务在执行之后被 :term:`acknowledged` （无论成功与否，包括抛出错误的情况），这意味着如果机器在任务执行过程中断电，或者 worker 被杀死，该任务将被重新投递给其他 worker。

            通过 :setting:`task_acks_late` 配置。

        .. tab:: 英文

            Task is :term:`acknowledged` after execution (both if successful, or if the task is raising an error), which means the task will be redelivered to another worker in the event of the machine losing power, or the worker instance being killed mid-execution.

            Configured using :setting:`task_acks_late`.

    early ack

        .. tab:: 中文

            为 :term:`early acknowledgment` 的简写。

        .. tab:: 英文

            Short for :term:`early acknowledgment`

    late ack

        .. tab:: 中文

            为 :term:`early acknowledgment` 的简写。

        .. tab:: 英文

            Short for :term:`late acknowledgment`

    ETA

        .. tab:: 中文

            “预计到达时间（Estimated Time of Arrival）”，在 Celery 和 Google Task Queue 等系统中，用于表示延迟消息，即该消息在指定的 ETA 时间之前不应被处理。参见 :ref:`calling-eta`。


        .. tab:: 英文

            "Estimated Time of Arrival", in Celery and Google Task Queue, etc., used as the term for a delayed message that should not be processed until the specified ETA time.  See :ref:`calling-eta`.

    request

        .. tab:: 中文

            任务消息在 worker 内部被转换为 *请求（requests）*。请求信息也可以通过任务的 :term:`context` （即 ``task.request`` 属性）获取。

        .. tab:: 英文

            Task messages are converted to *requests* within the worker. The request information is also available as the task's :term:`context` (the ``task.request`` attribute).

    calling

        .. tab:: 中文

            发送任务消息，使得该任务函数由某个 worker :term:`执行 <executing>`。

        .. tab:: 英文

            Sends a task message so that the task function is :term:`executed <executing>` by a worker.

    kombu

        .. tab:: 中文

            Celery 使用的 Python 消息库，用于发送和接收消息。

        .. tab:: 英文

            Python messaging library used by Celery to send and receive messages.

    billiard

        .. tab:: 中文

            是 Python `multiprocessing` 库的分支，包含了 Celery 所需的增强功能。

        .. tab:: 英文

            Fork of the Python multiprocessing library containing improvements required by Celery.

    executing

        .. tab:: 中文

            Worker 会 *执行* 任务 :term:`请求 <request>`。

        .. tab:: 英文

            Workers *execute* task :term:`requests <request>`.

    apply

        .. tab:: 中文

            最初是 :term:`调用 <calling>` 的同义词，但用于表示该函数由当前进程执行。

        .. tab:: 英文

            Originally a synonym to :term:`call <calling>` but used to signify that a function is executed by the current process.

    context

        .. tab:: 中文

            任务的上下文包含诸如任务 ID、参数、被投递到的队列等信息。它可以通过任务的 ``request`` 属性访问。参见 :ref:`task-request-info`。

        .. tab:: 英文

            The context of a task contains information like the id of the task, it's arguments and what queue it was delivered to. It can be accessed as the tasks ``request`` attribute. See :ref:`task-request-info`

    idempotent

        .. tab:: 中文

            幂等性是一个数学属性，描述一个函数可以被多次调用而不会改变结果。在实际应用中，这意味着函数可以重复调用而不会产生意外的副作用，但这并不意味着其完全无副作用（可与 :term:`nullipotent` 对比）。

            延伸阅读：https://en.wikipedia.org/wiki/Idempotent

        .. tab:: 英文

            Idempotence is a mathematical property that describes a function that can be called multiple times without changing the result. Practically it means that a function can be repeated many times without unintended effects, but not necessarily side-effect free in the pure sense (compare to :term:`nullipotent`).

            Further reading: https://en.wikipedia.org/wiki/Idempotent

    nullipotent

        .. tab:: 中文

            描述一个函数在被调用零次或多次时，仍具有相同效果并产生相同结果（完全无副作用）。是 :term:`idempotent` 的更强版本。

        .. tab:: 英文

            describes a function that'll have the same effect, and give the same result, even if called zero or multiple times (side-effect free). A stronger version of :term:`idempotent`.

    reentrant

        .. tab:: 中文

            描述一个函数在执行过程中（例如被硬件中断或信号中断）可以被安全地中断，并可稍后重新调用。可重入性不同于 :term:`幂等性 <idempotent>`，因为其返回值在相同输入下不必一致，并且可重入函数可以有副作用，只要它们可以被安全中断；幂等函数总是可重入的，但反之则不然。

        .. tab:: 英文

            describes a function that can be interrupted in the middle of execution (e.g., by hardware interrupt or signal), and then safely called again later. Reentrancy isn't the same as :term:`idempotence <idempotent>` as the return value doesn't have to be the same given the same inputs, and a reentrant function may have side effects as long as it can be interrupted;  An idempotent function is always reentrant, but the reverse may not be true.

    cipater

        .. tab:: 中文

            Celery 3.1 版本以 Autechre 的歌曲命名（http://www.youtube.com/watch?v=OHsaqUr_33Y）

        .. tab:: 英文

            Celery release 3.1 named after song by Autechre (http://www.youtube.com/watch?v=OHsaqUr_33Y)

    prefetch multiplier

        .. tab:: 中文

            :term:`预取计数（prefetch count）` 通过 :setting:`worker_prefetch_multiplier` 设置配置，该值会乘以池中的槽位数量（线程/进程/绿色线程）。

        .. tab:: 英文

            The :term:`prefetch count` is configured by using the :setting:`worker_prefetch_multiplier` setting, which is multiplied by the number of pool slots (threads/processes/greenthreads).

    `prefetch count`

        .. tab:: 中文

            消费者可持有的最大未确认消息数，若超过该数量，传输层将不再向该消费者投递更多消息。参见 :ref:`optimizing-prefetch-limit`。

        .. tab:: 英文

            Maximum number of unacknowledged messages a consumer can hold and if exceeded the transport shouldn't deliver any more messages to that consumer. See :ref:`optimizing-prefetch-limit`.

    pidbox

        .. tab:: 中文

            进程邮箱，用于实现远程控制命令。

        .. tab:: 英文

            A process mailbox, used to implement remote control commands.
