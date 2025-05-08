.. _broker-rabbitmq:

================
使用 RabbitMQ
================

Using RabbitMQ

安装与配置
============================

Installation & Configuration

.. tab:: 中文

    RabbitMQ 是默认的 broker，因此除了你希望使用的 broker 实例的 URL 地址外，不需要额外依赖或初始配置：

    .. code-block:: python

        broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'

    有关 broker URL 的说明以及 Celery 支持的各种 broker 配置选项的完整列表，请参阅 :ref:`conf-broker-settings`，下文也有关于设置用户名、密码和虚拟主机的说明。

.. tab:: 英文

    RabbitMQ is the default broker so it doesn't require any additional
    dependencies or initial configuration, other than the URL location of
    the broker instance you want to use:

    .. code-block:: python

        broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'

    For a description of broker URLs and a full list of the
    various broker configuration options available to Celery,
    see :ref:`conf-broker-settings`, and see below for setting up the
    username, password and vhost.

.. _installing-rabbitmq:

安装 RabbitMQ 服务
==============================

Installing the RabbitMQ Server

.. tab:: 中文

    请参阅 RabbitMQ 官方网站的 `Downloading and Installing RabbitMQ`_ 页面。macOS 用户请参阅 :ref:`Installing RabbitMQ on macOS <rabbitmq-macOS-installation>`。

    .. note::

        如果你在安装并使用 :command:`rabbitmqctl` 后遇到 `nodedown` 错误，可参考以下博文帮助你定位问题来源：

            http://www.somic.org/2009/02/19/on-rabbitmqctl-and-badrpcnodedown/

.. tab:: 英文

    See `Downloading and Installing RabbitMQ`_ over at RabbitMQ's website. For macOS
    see `Installing RabbitMQ on macOS`_.

    .. note::

        If you're getting `nodedown` errors after installing and using
        :command:`rabbitmqctl` then this blog post can help you identify
        the source of the problem:

            http://www.somic.org/2009/02/19/on-rabbitmqctl-and-badrpcnodedown/

.. _`Downloading and Installing RabbitMQ`: https://www.rabbitmq.com/download.html

.. _rabbitmq-configuration:

.. _Setting up RabbitMQ:

配置 RabbitMQ
-------------------

Setting up RabbitMQ

.. tab:: 中文

    要让 Celery 正常运行，我们需要创建一个 RabbitMQ 用户、一个虚拟主机，并允许该用户访问该虚拟主机：

    .. code-block:: console

        $ sudo rabbitmqctl add_user myuser mypassword

    .. code-block:: console

        $ sudo rabbitmqctl add_vhost myvhost

    .. code-block:: console

        $ sudo rabbitmqctl set_user_tags myuser mytag

    .. code-block:: console

        $ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

    请将 ``myuser``、 ``mypassword`` 和 ``myvhost`` 替换为你实际要使用的值。

    更多关于 `访问控制 <https://www.rabbitmq.com/access-control.html>`_ 的信息，请参阅 RabbitMQ 的 `Admin Guide`_。

.. tab:: 英文

    To use Celery we need to create a RabbitMQ user, a virtual host and
    allow that user access to that virtual host:

    .. code-block:: console

        $ sudo rabbitmqctl add_user myuser mypassword

    .. code-block:: console

        $ sudo rabbitmqctl add_vhost myvhost

    .. code-block:: console

        $ sudo rabbitmqctl set_user_tags myuser mytag

    .. code-block:: console

        $ sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

    Substitute in appropriate values for ``myuser``, ``mypassword`` and ``myvhost`` above.

    See the RabbitMQ `Admin Guide`_ for more information about `access control`_.

.. _`Admin Guide`: https://www.rabbitmq.com/admin-guide.html

.. _`access control`: https://www.rabbitmq.com/access-control.html

.. _rabbitmq-macOS-installation:

在 macOS 上安装 RabbitMQ
----------------------------

Installing RabbitMQ on macOS

.. tab:: 中文

    在 macOS 上安装 RabbitMQ 最简单的方法是使用 `Homebrew`_，这是一款适用于 macOS 的新一代软件包管理器。

    首先，根据 `Homebrew documentation`_ 提供的一行命令安装 Homebrew：

    .. code-block:: console

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    然后使用 :command:`brew` 安装 RabbitMQ：

    .. code-block:: console

        $ brew install rabbitmq

    .. _rabbitmq-macOS-system-hostname:

    使用 :command:`brew` 安装 RabbitMQ 后，您需要将以下内容添加到您的路径中才能启动和停止代理：将其添加到您的 shell 的启动文件中（例如， :file:`.bash_profile` 或 :file:`.profile` ）。

    .. code-block:: bash

        PATH=$PATH:/usr/local/sbin

.. tab:: 英文

    The easiest way to install RabbitMQ on macOS is using `Homebrew`_ the new and
    shiny package management system for macOS.

    First, install Homebrew using the one-line command provided by the `Homebrew
    documentation`_:

    .. code-block:: console

        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    Finally, we can install RabbitMQ using :command:`brew`:

    .. code-block:: console

        $ brew install rabbitmq

    After you've installed RabbitMQ with :command:`brew` you need to add the following to
    your path to be able to start and stop the broker: add it to the start-up file for your
    shell (e.g., :file:`.bash_profile` or :file:`.profile`).

    .. code-block:: bash

        PATH=$PATH:/usr/local/sbin

.. _`Homebrew`: https://github.com/mxcl/homebrew/
.. _`Homebrew documentation`: https://github.com/Homebrew/homebrew/wiki/Installation

配置系统主机名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Configuring the system host name

.. tab:: 中文

    如果你的 DHCP 服务器分配了一个随机主机名，你需要永久设置主机名。这是因为 RabbitMQ 使用主机名与节点通信。

    可以使用 :command:`scutil` 命令永久设置主机名：

    .. code-block:: console

        $ sudo scutil --set HostName myhost.local

    然后将该主机名添加到 :file:`/etc/hosts` 文件中，以便能够解析为 IP 地址::

        127.0.0.1       localhost myhost myhost.local

    此时如果启动 :command:`rabbitmq-server`，Rabbit 节点应该为 `rabbit@myhost`，可以通过 :command:`rabbitmqctl` 验证：

    .. code-block:: console

        $ sudo rabbitmqctl status
        Status of node rabbit@myhost ...
        [{running_applications,[{rabbit,"RabbitMQ","1.7.1"},
                            {mnesia,"MNESIA  CXC 138 12","4.4.12"},
                            {os_mon,"CPO  CXC 138 46","2.2.4"},
                            {sasl,"SASL  CXC 138 11","2.1.8"},
                            {stdlib,"ERTS  CXC 138 10","1.16.4"},
                            {kernel,"ERTS  CXC 138 10","2.13.4"}]},
        {nodes,[rabbit@myhost]},
        {running_nodes,[rabbit@myhost]}]
        ...done.

    特别需要注意的是，如果 DHCP 分配的主机名以 IP 地址开头（例如 `23.10.112.31.comcast.net`），RabbitMQ 将尝试使用 `rabbit@23`，这是不合法的主机名。


.. tab:: 英文

    If you're using a DHCP server that's giving you a random host name, you need
    to permanently configure the host name. This is because RabbitMQ uses the host name
    to communicate with nodes.

    Use the :command:`scutil` command to permanently set your host name:

    .. code-block:: console

        $ sudo scutil --set HostName myhost.local

    Then add that host name to :file:`/etc/hosts` so it's possible to resolve it
    back into an IP address::

        127.0.0.1       localhost myhost myhost.local

    If you start the :command:`rabbitmq-server`, your rabbit node should now
    be `rabbit@myhost`, as verified by :command:`rabbitmqctl`:

    .. code-block:: console

        $ sudo rabbitmqctl status
        Status of node rabbit@myhost ...
        [{running_applications,[{rabbit,"RabbitMQ","1.7.1"},
                            {mnesia,"MNESIA  CXC 138 12","4.4.12"},
                            {os_mon,"CPO  CXC 138 46","2.2.4"},
                            {sasl,"SASL  CXC 138 11","2.1.8"},
                            {stdlib,"ERTS  CXC 138 10","1.16.4"},
                            {kernel,"ERTS  CXC 138 10","2.13.4"}]},
        {nodes,[rabbit@myhost]},
        {running_nodes,[rabbit@myhost]}]
        ...done.

    This is especially important if your DHCP server gives you a host name
    starting with an IP address, (e.g., `23.10.112.31.comcast.net`).  In this
    case RabbitMQ will try to use `rabbit@23`: an illegal host name.

.. _rabbitmq-macOS-start-stop:

启动/停止 RabbitMQ 服务
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting/Stopping the RabbitMQ server

.. tab:: 中文

    启动服务器：

    .. code-block:: console

        $ sudo rabbitmq-server

    也可以通过添加 ``-detached`` 选项在后台运行（注意：是一个短横线）：

    .. code-block:: console

        $ sudo rabbitmq-server -detached

    不要使用 :command:`kill` (:manpage:`kill(1)`) 命令来停止 RabbitMQ 服务器，而应该使用 :command:`rabbitmqctl`：

    .. code-block:: console

        $ sudo rabbitmqctl stop

    当服务器运行后，你可以继续阅读 :ref:`设置 RabbitMQ <Setting up RabbitMQ>` 一节。

.. tab:: 英文

    To start the server:

    .. code-block:: console

        $ sudo rabbitmq-server

    you can also run it in the background by adding the ``-detached`` option
    (note: only one dash):

    .. code-block:: console

        $ sudo rabbitmq-server -detached

    Never use :command:`kill` (:manpage:`kill(1)`) to stop the RabbitMQ server,
    but rather use the :command:`rabbitmqctl` command:

    .. code-block:: console

        $ sudo rabbitmqctl stop

    When the server is running, you can continue reading `Setting up RabbitMQ`_.

.. _using-quorum-queues:

使用 Quorum 队列
===================

Using Quorum Queues

.. versionadded:: 5.5

.. tab:: 中文

    .. warning::

        Quorum 队列需要关闭全局 QoS，这意味着某些功能可能无法按预期工作。
        详情请参阅下方的 `限制说明`_。

    Celery 支持通过将 ``x-queue-type`` 头设置为 ``quorum`` 来使用 `Quorum Queues`_：

    .. code-block:: python

        from kombu import Queue

        task_queues = [Queue('my-queue', queue_arguments={'x-queue-type': 'quorum'})]
        broker_transport_options = {"confirm_publish": True}

    如果你想更改默认队列的类型，可将 :setting:`task_default_queue_type` 设置为 ``quorum``。

    Celery 会使用 :setting:`worker_detect_quorum_queues` 设置自动检测是否使用了 quorum 队列。
    建议保持该默认行为开启。

    如果你希望从经典镜像队列迁移到 quorum 队列，请参考 RabbitMQ 的 `官方迁移文档 <https://www.rabbitmq.com/blog/2023/03/02/quorum-queues-migration>`_。


.. tab:: 英文

    .. warning::

        Quorum Queues require disabling global QoS which means some features won't work as expected.
        See `limitations`_ for details.

    Celery supports `Quorum Queues`_ by setting the ``x-queue-type`` header to ``quorum`` like so:

    .. code-block:: python

        from kombu import Queue

        task_queues = [Queue('my-queue', queue_arguments={'x-queue-type': 'quorum'})]
        broker_transport_options = {"confirm_publish": True}

    If you'd like to change the type of the default queue, set the :setting:`task_default_queue_type` setting to ``quorum``.

    Celery automatically detects if quorum queues are used using the :setting:`worker_detect_quorum_queues` setting.
    We recommend to keep the default behavior turned on.

    To migrate from classic mirrored queues to quorum queues, please refer to RabbitMQ's `documentation <https://www.rabbitmq.com/blog/2023/03/02/quorum-queues-migration>`_ on the subject.

.. _`Quorum Queues`: https://www.rabbitmq.com/docs/quorum-queues

.. _limitations:

限制说明
-----------

Limitations

.. tab:: 中文

    关闭全局 QoS 意味着每个 channel 的 QoS 变为静态。这会导致某些 Celery 功能无法在启用 Quorum 队列时使用。

    自动扩缩容机制依赖于在新进程启动或结束时调整预取数量，因此在检测到 Quorum 队列时将无法使用。

    同样地，即使将 :setting:`worker_enable_prefetch_count_reduction` 设置为 ``True``，也不会生效。

    此外，当启用了 ETA / Countdown（ :ref:`ETA/Countdown <calling-eta>` ）时，由于无法提升预取数量获取下一个任务，worker 会在任务的 ETA 到达前被阻塞。

    为了解决上述问题，Celery 会在检测到 quorum 队列时自动启用 :ref:`原生延迟投递 <native-delayed-delivery>`，用于调度 ETA/Countdown 类型的任务。


.. tab:: 英文

    Disabling global QoS means that the the per-channel QoS is now static.
    This means that some Celery features won't work when using Quorum Queues.

    Autoscaling relies on increasing and decreasing the prefetch count whenever a new process is instantiated
    or terminated so it won't work when Quorum Queues are detected.

    Similarly, the :setting:`worker_enable_prefetch_count_reduction` setting will be a no-op even when set to ``True``
    when Quorum Queues are detected.

    In addition, :ref:`ETA/Countdown <calling-eta>` will block the worker when received until the ETA arrives since
    we can no longer increase the prefetch count and fetch another task from the queue.

    In order to properly schedule ETA/Countdown tasks we automatically detect if quorum queues are used
    and in case they are, Celery automatically enables :ref:`Native Delayed Delivery <native-delayed-delivery>`.

.. _native-delayed-delivery:

原生延迟投递
-----------------------

Native Delayed Delivery

.. tab:: 中文

    由于 ETA/Countdown 类型的任务会阻塞 worker 直到计划时间到达，我们需要使用 RabbitMQ 的原生能力来调度任务执行时间。

    该设计借鉴自 NServiceBus。如果你对实现细节感兴趣，可以参考他们的 `官方文档 <https://docs.particular.net/transports/rabbitmq/delayed-delivery>`_。

    当检测到 Quorum 队列时，Celery 会自动启用原生延迟投递。

    默认情况下，原生延迟投递使用的是 Quorum 队列。如果你希望改用经典队列，可以将 :setting:`broker_native_delayed_delivery_queue_type` 设置为 classic。


.. tab:: 英文

    Since tasks with ETA/Countdown will block the worker until they are scheduled for execution,
    we need to use RabbitMQ's native capabilities to schedule the execution of tasks.

    The design is borrowed from NServiceBus. If you are interested in the implementation details, refer to their `documentation`_.

    Native Delayed Delivery is automatically enabled when quorum queues are detected.

    By default the Native Delayed Delivery queues are quorum queues.
    If you'd like to change them to classic queues you can set the :setting:`broker_native_delayed_delivery_queue_type`
    to classic.

.. _documentation: https://docs.particular.net/transports/rabbitmq/delayed-delivery
