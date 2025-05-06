.. _guide-security:

==========
安全
==========

Security


简介
============

Introduction

.. tab:: 中文

    虽然 Celery 在设计时考虑了安全性，但它仍应被视为一个不安全的组件。

    根据您的 `Security Policy`_，您可以采取多种步骤来增强 Celery 安装的安全性。

.. tab:: 英文

    While Celery is written with security in mind, it should be treated as an
    unsafe component.

    Depending on your `Security Policy`_, there are
    various steps you can take to make your Celery installation more secure.


.. _`Security Policy`: https://en.wikipedia.org/wiki/Security_policy


关注领域
================

Areas of Concern

Broker
------

.. tab:: 中文

    首先，必须确保 broker 免受未经授权的访问，特别是当其对外部公开可访问时。
    默认情况下，worker 会信任它从 broker 获得的数据没有被篡改。有关如何使 broker 连接更可信的信息，请参阅 `Message Signing`_。

    防御的第一道防线应是将防火墙放置在 broker 前面，只允许白名单中的机器访问它。

    请记住，防火墙配置错误和临时禁用防火墙在现实中非常常见。强有力的安全策略应包括对防火墙设备的监控，以检测防火墙是否被禁用，无论是意外禁用还是故意禁用。

    换句话说，不应该盲目信任防火墙。

    如果您的 broker 支持细粒度的访问控制，例如 RabbitMQ，您应当考虑启用该功能。例如，请参阅 http://www.rabbitmq.com/access-control.html。

    如果您的 broker 后端支持，您可以通过使用 :setting:`broker_use_ssl` 启用端到端的 SSL 加密和身份验证。

.. tab:: 英文

    It's imperative that the broker is guarded from unwanted access, especially
    if accessible to the public.
    By default, workers trust that the data they get from the broker hasn't
    been tampered with. See `Message Signing`_ for information on how to make
    the broker connection more trustworthy.

    The first line of defense should be to put a firewall in front of the broker,
    allowing only white-listed machines to access it.

    Keep in mind that both firewall misconfiguration, and temporarily disabling
    the firewall, is common in the real world. Solid security policy includes
    monitoring of firewall equipment to detect if they've been disabled, be it
    accidentally or on purpose.

    In other words, one shouldn't blindly trust the firewall either.

    If your broker supports fine-grained access control, like RabbitMQ,
    this is something you should look at enabling. See for example
    http://www.rabbitmq.com/access-control.html.

    If supported by your broker backend, you can enable end-to-end SSL encryption
    and authentication using :setting:`broker_use_ssl`.

客户端
------

Client

.. tab:: 中文

    在 Celery 中，“client” 指代任何向 broker 发送消息的组件，例如应用任务的 Web 服务器。

    如果 broker 已正确安全配置，但客户端仍能发送任意消息，那么安全性仍然得不到保障。

.. tab:: 英文

    In Celery, "client" refers to anything that sends messages to the
    broker, for example web-servers that apply tasks.

    Having the broker properly secured doesn't matter if arbitrary messages
    can be sent through a client.

*[Need more text here]*

工作器
------

Worker

.. tab:: 中文

    在 worker 中运行的任务的默认权限与 worker 本身的权限相同。这适用于资源，如内存、文件系统和设备。

    这一规则的例外情况是使用基于多进程的任务池时，这也是当前的默认设置。在这种情况下，任务将能够访问通过 :func:`fork` 调用复制的任何内存，并访问由父任务写入同一 worker 子进程中的内存内容。

    通过在子进程中启动每个任务（使用 :func:`fork` + :func:`execve`）可以限制对内存内容的访问。

    通过使用 `chroot`_、 `jail`_、 `sandboxing`_、虚拟机或其他由平台或附加软件启用的机制，可以限制对文件系统和设备的访问。

    还需要注意，worker 中执行的任何任务将具有与其运行所在机器相同的网络访问权限。如果 worker 位于内部网络中，建议为出站流量添加防火墙规则。

.. tab:: 英文

    The default permissions of tasks running inside a worker are the same ones as
    the privileges of the worker itself. This applies to resources, such as;
    memory, file-systems, and devices.

    An exception to this rule is when using the multiprocessing based task pool,
    which is currently the default. In this case, the task will have access to
    any memory copied as a result of the :func:`fork` call,
    and access to memory contents written by parent tasks in the same worker
    child process.

    Limiting access to memory contents can be done by launching every task
    in a subprocess (:func:`fork` + :func:`execve`).

    Limiting file-system and device access can be accomplished by using
    `chroot`_, `jail`_, `sandboxing`_, virtual machines, or other
    mechanisms as enabled by the platform or additional software.

    Note also that any task executed in the worker will have the
    same network access as the machine on which it's running. If the worker
    is located on an internal network it's recommended to add firewall rules for
    outbound traffic.

.. _`chroot`: https://en.wikipedia.org/wiki/Chroot
.. _`jail`: https://en.wikipedia.org/wiki/FreeBSD_jail
.. _`sandboxing`:
    https://en.wikipedia.org/wiki/Sandbox_(computer_security)

.. _security-serializers:

序列化器
===========

Serializers

.. tab:: 中文

    默认的序列化器是 JSON，从 4.0 版本开始，但由于它仅支持有限的类型集，您可能需要考虑改用 pickle 进行序列化。

    `pickle` 序列化器非常方便，因为它几乎可以序列化任何 Python 对象，甚至可以通过一些工作序列化函数，但由于同样的原因， `pickle` 本质上是不安全的 [*]_,
    因此应避免在客户端不受信任或未经身份验证的情况下使用。

    您可以通过在 :setting:`accept_content` 设置中指定允许的内容类型白名单来禁用不受信任的内容：

    .. versionadded:: 3.0.18

    .. note::

        此设置在 3.0.18 版本中首次支持。如果您使用的是较早版本，它将被忽略，因此请确保您使用的是支持该功能的版本。

    .. code-block:: python

        accept_content = ['json']


    此设置接受一个序列化器名称和内容类型的列表，因此您还可以为 json 指定内容类型：

    .. code-block:: python

        accept_content = ['application/json']

    Celery 还提供了一种特殊的 `auth` 序列化器，用于验证 Celery 客户端与 worker 之间的通信，确保消息来自受信任的来源。
    使用 :ref:`公钥密码学 <Public-key cryptography>`， `auth` 序列化器可以验证发送者的真实性。要启用此功能，请阅读 :ref:`message-signing` 了解更多信息。

.. tab:: 英文

    The default serializer is JSON since version 4.0, but since it has
    only support for a restricted set of types you may want to consider
    using pickle for serialization instead.

    The `pickle` serializer is convenient as it can serialize
    almost any Python object, even functions with some work,
    but for the same reasons `pickle` is inherently insecure [*]_,
    and should be avoided whenever clients are untrusted or
    unauthenticated.

    You can disable untrusted content by specifying
    a white-list of accepted content-types in the :setting:`accept_content`
    setting:

    .. versionadded:: 3.0.18

    .. note::

        This setting was first supported in version 3.0.18. If you're
        running an earlier version it will simply be ignored, so make
        sure you're running a version that supports it.

    .. code-block:: python

        accept_content = ['json']


    This accepts a list of serializer names and content-types, so you could
    also specify the content type for json:

    .. code-block:: python

        accept_content = ['application/json']

    Celery also comes with a special `auth` serializer that validates
    communication between Celery clients and workers, making sure
    that messages originates from trusted sources.
    Using `Public-key cryptography` the `auth` serializer can verify the
    authenticity of senders, to enable this read :ref:`message-signing`
    for more information.

.. _`Public-key cryptography`:
    https://en.wikipedia.org/wiki/Public-key_cryptography

.. _message-signing:

.. _Message Signing:

消息签名
===============

Message Signing

.. tab:: 中文

    Celery 可以使用 :pypi:`cryptography` 库来使用 :ref:`公钥密码学 <Public-key cryptography>` 签署消息，其中
    客户端发送的消息使用私钥进行签名，之后 worker 使用公钥证书验证消息。

    最佳情况下，证书应由官方 :ref:`证书颁发机构 <Certificate Authority>` 签署，但它们也可以是自签名证书。

    要启用此功能，您应将 :setting:`task_serializer` 设置为使用 `auth` 序列化器。为了强制 worker 仅接受签名消息，您应将 `accept_content` 设置为 `['auth']`。
    要为事件协议添加额外的签名，请将 `event_serializer` 设置为 `auth`。
    还需要配置用于定位私钥和证书的文件系统路径：分别为 :setting:`security_key`、:setting:`security_certificate` 和 :setting:`security_cert_store` 设置。
    您可以使用 :setting:`security_digest` 调整签名算法。
    如果使用加密的私钥，则可以使用 :setting:`security_key_password` 配置密码。

    配置好这些后，还需要调用 :func:`celery.setup_security` 函数。请注意，这也会禁用所有不安全的序列化器，因此 worker 不会接受带有不受信任内容类型的消息。

    以下是使用 `auth` 序列化器的示例配置，私钥和证书文件位于 `/etc/ssl`：

    .. code-block:: python

        app = Celery()
        app.conf.update(
            security_key='/etc/ssl/private/worker.key'
            security_certificate='/etc/ssl/certs/worker.pem'
            security_cert_store='/etc/ssl/certs/*.pem',
            security_digest='sha256',
            task_serializer='auth',
            event_serializer='auth',
            accept_content=['auth']
        )
        app.setup_security()

    .. note::

        虽然不禁止使用相对路径，但建议使用绝对路径来存放这些文件。

        还需要注意，`auth` 序列化器不会加密消息的内容，因此如果需要加密，必须单独启用该功能。

.. tab:: 英文

    Celery can use the :pypi:`cryptography` library to sign message using
    `Public-key cryptography`, where
    messages sent by clients are signed using a private key
    and then later verified by the worker using a public certificate.

    Optimally certificates should be signed by an official
    `Certificate Authority`_, but they can also be self-signed.

    To enable this you should configure the :setting:`task_serializer`
    setting to use the `auth` serializer. Enforcing the workers to only accept
    signed messages, you should set `accept_content` to `['auth']`.
    For additional signing of the event protocol, set `event_serializer` to `auth`.
    Also required is configuring the
    paths used to locate private keys and certificates on the file-system:
    the :setting:`security_key`,
    :setting:`security_certificate`, and :setting:`security_cert_store`
    settings respectively.
    You can tweak the signing algorithm with :setting:`security_digest`.
    If using an encrypted private key, the password can be configured with
    :setting:`security_key_password`.

    With these configured it's also necessary to call the
    :func:`celery.setup_security` function. Note that this will also
    disable all insecure serializers so that the worker won't accept
    messages with untrusted content types.

    This is an example configuration using the `auth` serializer,
    with the private key and certificate files located in `/etc/ssl`.

    .. code-block:: python

        app = Celery()
        app.conf.update(
            security_key='/etc/ssl/private/worker.key'
            security_certificate='/etc/ssl/certs/worker.pem'
            security_cert_store='/etc/ssl/certs/*.pem',
            security_digest='sha256',
            task_serializer='auth',
            event_serializer='auth',
            accept_content=['auth']
        )
        app.setup_security()

    .. note::

        While relative paths aren't disallowed, using absolute paths
        is recommended for these files.

        Also note that the `auth` serializer won't encrypt the contents of
        a message, so if needed this will have to be enabled separately.

.. _`X.509`: https://en.wikipedia.org/wiki/X.509
.. _`Certificate Authority`:
    https://en.wikipedia.org/wiki/Certificate_authority

入侵检测
===================

Intrusion Detection

.. tab:: 中文

    在防御系统免受入侵时，最重要的部分是能够检测系统是否已被攻破。

.. tab:: 英文

    The most important part when defending your systems against intruders is being able to detect if the system has been compromised.

日志
----

Logs

.. tab:: 中文

    日志通常是寻找安全漏洞证据的首选地方，但如果日志被篡改，它们将毫无用处。

    一个好的解决方案是设置集中式日志记录并使用专用的日志服务器。对此的访问应该受到限制。
    除了将所有日志集中在一个地方，如果配置得当，它还可以使入侵者更难篡改日志。

    这应该很容易通过 syslog 设置（另请参见 `syslog-ng`_ 和 `rsyslog`_ ）。Celery 使用 :mod:`logging` 库，并且已经支持使用 syslog。

    对于过度谨慎的人来说，一个小贴士是通过 UDP 发送日志，并切断日志服务器网络电缆的传输部分 :-)

.. tab:: 英文

    Logs are usually the first place to look for evidence
    of security breaches, but they're useless if they can be tampered with.

    A good solution is to set up centralized logging with a dedicated logging
    server. Access to it should be restricted.
    In addition to having all of the logs in a single place, if configured
    correctly, it can make it harder for intruders to tamper with your logs.

    This should be fairly easy to setup using syslog (see also `syslog-ng`_ and
    `rsyslog`_). Celery uses the :mod:`logging` library, and already has
    support for using syslog.

    A tip for the paranoid is to send logs using UDP and cut the
    transmit part of the logging server's network cable :-)

.. _`syslog-ng`: https://en.wikipedia.org/wiki/Syslog-ng
.. _`rsyslog`: http://www.rsyslog.com/

Tripwire
--------

Tripwire

.. tab:: 中文

    `Tripwire`_ 是一个（现在是商业化的）数据完整性工具，具有多个
    开源实现，用于保持文件系统中文件的加密哈希，以便管理员
    在文件发生变化时可以收到警报。通过这种方式，当损害已经发生且系统
    已被攻破时，您可以准确地知道入侵者更改了哪些文件（例如密码文件、日志、后门、根套件等）。
    通常这是检测入侵的唯一方法。

    一些开源实现包括：

    * `OSSEC`_
    * `Samhain`_
    * `Open Source Tripwire`_
    * `AIDE`_

    此外， `ZFS`_ 文件系统自带有可以使用的内置完整性检查。

.. tab:: 英文

    `Tripwire`_ is a (now commercial) data integrity tool, with several
    open source implementations, used to keep
    cryptographic hashes of files in the file-system, so that administrators
    can be alerted when they change. This way when the damage is done and your
    system has been compromised you can tell exactly what files intruders
    have changed  (password files, logs, back-doors, root-kits, and so on).
    Often this is the only way you'll be able to detect an intrusion.

    Some open source implementations include:

    * `OSSEC`_
    * `Samhain`_
    * `Open Source Tripwire`_
    * `AIDE`_

    Also, the `ZFS`_ file-system comes with built-in integrity checks
    that can be used.

.. _`Tripwire`: http://tripwire.com/
.. _`OSSEC`: http://www.ossec.net/
.. _`Samhain`: http://la-samhna.de/samhain/index.html
.. _`AIDE`: http://aide.sourceforge.net/
.. _`Open Source Tripwire`: https://github.com/Tripwire/tripwire-open-source
.. _`ZFS`: https://en.wikipedia.org/wiki/ZFS

.. rubric:: 脚注/Footnotes

.. [*] https://blog.nelhage.com/2011/03/exploiting-pickle/
