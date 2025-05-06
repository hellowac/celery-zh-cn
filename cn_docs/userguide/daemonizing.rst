.. _daemonizing:

======================================================================
守护进程
======================================================================

Daemonization

.. tab:: 中文

    如今，大多数 Linux 发行版使用 systemd 来管理系统和用户服务的生命周期。

    你可以通过输入以下命令检查你的 Linux 发行版是否使用 systemd：

    .. code-block:: console

        $ systemctl --version
        systemd 249 (v249.9-1.fc35)
        +PAM +AUDIT +SELINUX -APPARMOR +IMA +SMACK +SECCOMP +GCRYPT +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 +PWQUALITY +P11KIT +QRENCODE +BZIP2 +LZ4 +XZ +ZLIB +ZSTD +XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified

    如果你的输出类似于上面所示，请参考
    :ref:`我们的 systemd 文档 <daemon-systemd-generic>` 以获取更多指导。

    然而，init.d 脚本在这些 Linux 发行版中仍然应该能正常工作，因为 systemd 提供了 systemd-sysv 兼容层
    ，该层会自动根据我们提供的 init.d 脚本生成服务。

    如果你为多个 Linux 发行版打包 Celery，
    并且有些不支持 systemd，或者打算支持其他 Unix 系统，
    你可能需要参考 :ref:`我们的 init.d 文档 <daemon-generic>`。

.. tab:: 英文

    Most Linux distributions these days use systemd for managing the lifecycle of system
    and user services.

    You can check if your Linux distribution uses systemd by typing:

    .. code-block:: console

        $ systemctl --version
        systemd 249 (v249.9-1.fc35)
        +PAM +AUDIT +SELINUX -APPARMOR +IMA +SMACK +SECCOMP +GCRYPT +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN +IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 +PWQUALITY +P11KIT +QRENCODE +BZIP2 +LZ4 +XZ +ZLIB +ZSTD +XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified

    If you have output similar to the above, please refer to
    :ref:`our systemd documentation <daemon-systemd-generic>` for guidance.

    However, the init.d script should still work in those Linux distributions
    as well since systemd provides the systemd-sysv compatibility layer
    which generates services automatically from the init.d scripts we provide.

    If you package Celery for multiple Linux distributions
    and some do not support systemd or to other Unix systems as well,
    you may want to refer to :ref:`our init.d documentation <daemon-generic>`.

.. _daemon-generic:

通用初始化脚本
======================================================================

Generic init-scripts

.. tab:: 中文

    请查看 Celery 发行版中的 `extra/generic-init.d/`_ 目录。

    此目录包含用于
    :program:`celery worker` 程序的通用 bash 初始化脚本，
    这些脚本应该能够在 Linux、FreeBSD、OpenBSD 和其他类 Unix 平台上运行。

.. tab:: 英文

    See the `extra/generic-init.d/`_ directory Celery distribution.

    This directory contains generic bash init-scripts for the
    :program:`celery worker` program,
    these should run on Linux, FreeBSD, OpenBSD, and other Unix-like platforms.

.. _`extra/generic-init.d/`: https://github.com/celery/celery/tree/main/extra/generic-init.d/

.. _generic-initd-celeryd:

初始化脚本： ``celeryd``
----------------------------------------------------------------------

Init-script: ``celeryd``

.. tab:: 中文

    :用法: `/etc/init.d/celeryd {start|stop|restart|status}`
    :配置文件: :file:`/etc/default/celeryd`

    为了正确配置此脚本以运行 worker，你可能至少需要告诉它
    启动时应该切换到哪个目录（以便找到包含你应用程序或配置模块的模块）。

    守护进程脚本由 :file:`/etc/default/celeryd` 文件配置。
    这是一个 shell (:command:`sh`) 脚本，你可以在其中添加类似下面的配置选项环境变量。
    要添加真正影响 worker 的环境变量，你还必须导出它们（例如：:command:`export DISPLAY=":0"`）。

    .. Admonition:: 需要超级用户权限

        初始化脚本只能由 root 用户使用，
        并且 shell 配置文件必须归 root 所有。

        非特权用户不需要使用初始化脚本，
        他们可以使用 :program:`celery multi` 工具（或
        :program:`celery worker --detach`）：

        .. code-block:: console

            $ celery -A proj multi start worker1 \
                --pidfile="$HOME/run/celery/%n.pid" \
                --logfile="$HOME/log/celery/%n%I.log"

            $ celery -A proj multi restart worker1 \
                --logfile="$HOME/log/celery/%n%I.log" \
                --pidfile="$HOME/run/celery/%n.pid

            $ celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"


.. tab:: 英文

    :Usage: `/etc/init.d/celeryd {start|stop|restart|status}`
    :Configuration file: :file:`/etc/default/celeryd`

    To configure this script to run the worker properly you probably need to at least
    tell it where to change
    directory to when it starts (to find the module containing your app, or your
    configuration module).

    The daemonization script is configured by the file :file:`/etc/default/celeryd`.
    This is a shell (:command:`sh`) script where you can add environment variables like
    the configuration options below.  To add real environment variables affecting
    the worker you must also export them (e.g., :command:`export DISPLAY=":0"`)

    .. Admonition:: Superuser privileges required

        The init-scripts can only be used by root,
        and the shell configuration file must also be owned by root.

        Unprivileged users don't need to use the init-script,
        instead they can use the :program:`celery multi` utility (or
        :program:`celery worker --detach`):

        .. code-block:: console

            $ celery -A proj multi start worker1 \
                --pidfile="$HOME/run/celery/%n.pid" \
                --logfile="$HOME/log/celery/%n%I.log"

            $ celery -A proj multi restart worker1 \
                --logfile="$HOME/log/celery/%n%I.log" \
                --pidfile="$HOME/run/celery/%n.pid

            $ celery multi stopwait worker1 --pidfile="$HOME/run/celery/%n.pid"

.. _generic-initd-celeryd-example:

示例配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. tab:: 中文

    这是一个 Python 项目的示例配置。

    :file:`/etc/default/celeryd`:

    .. code-block:: bash

        # 要启动的节点名称
        #   大多数用户只会启动一个节点：
        CELERYD_NODES="worker1"
        #   但你也可以启动多个节点，并在 CELERYD_OPTS 中为每个节点配置设置
        #CELERYD_NODES="worker1 worker2 worker3"
        #   或者，你也可以指定要启动的节点数量：
        #CELERYD_NODES=10

        # 指向 'celery' 命令的绝对路径或相对路径：
        CELERY_BIN="/usr/local/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"

        # 要使用的应用实例
        # 如果你没有使用 app，可以注释掉此行
        CELERY_APP="proj"
        # 或使用完整限定名：
        #CELERY_APP="proj.tasks:app"

        # 启动时要切换的目录
        CELERYD_CHDIR="/opt/Myproject/"

        # 传递给 worker 的额外命令行参数
        CELERYD_OPTS="--time-limit=300 --concurrency=8"
        # 通过追加节点名来为特定节点配置设置：
        #CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

        # 将日志级别设置为 DEBUG
        #CELERYD_LOG_LEVEL="DEBUG"

        # %n 会被节点名称的首部替换
        CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
        CELERYD_PID_FILE="/var/run/celery/%n.pid"

        # worker 应以非特权用户身份运行
        #   你需要手动创建此用户（或选择一个已存在的用户/用户组组合，例如 nobody）
        CELERYD_USER="celery"
        CELERYD_GROUP="celery"

        # 启用后，如果 pid 和日志目录不存在，将自动创建，
        # 且将归属于配置的用户 ID/组
        CELERY_CREATE_DIRS=1

.. tab:: 英文

    This is an example configuration for a Python project.

    :file:`/etc/default/celeryd`:

    .. code-block:: bash

        # Names of nodes to start
        #   most people will only start one node:
        CELERYD_NODES="worker1"
        #   but you can also start multiple and configure settings
        #   for each in CELERYD_OPTS
        #CELERYD_NODES="worker1 worker2 worker3"
        #   alternatively, you can specify the number of nodes to start:
        #CELERYD_NODES=10

        # Absolute or relative path to the 'celery' command:
        CELERY_BIN="/usr/local/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"

        # App instance to use
        # comment out this line if you don't use an app
        CELERY_APP="proj"
        # or fully qualified:
        #CELERY_APP="proj.tasks:app"

        # Where to chdir at start.
        CELERYD_CHDIR="/opt/Myproject/"

        # Extra command-line arguments to the worker
        CELERYD_OPTS="--time-limit=300 --concurrency=8"
        # Configure node-specific settings by appending node name to arguments:
        #CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

        # Set logging level to DEBUG
        #CELERYD_LOG_LEVEL="DEBUG"

        # %n will be replaced with the first part of the nodename.
        CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
        CELERYD_PID_FILE="/var/run/celery/%n.pid"

        # Workers should run as an unprivileged user.
        #   You need to create this user manually (or you can choose
        #   a user/group combination that already exists (e.g., nobody).
        CELERYD_USER="celery"
        CELERYD_GROUP="celery"

        # If enabled pid and log directories will be created if missing,
        # and owned by the userid/group configured.
        CELERY_CREATE_DIRS=1

使用登录 shell
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using a login shell

.. tab:: 中文

    你可以通过使用登录 shell 来继承 ``CELERYD_USER`` 的环境：

    .. code-block:: bash

        CELERYD_SU_ARGS="-l"

    请注意，不建议使用此选项，除非在确有必要的情况下才使用。

.. tab:: 英文

    You can inherit the environment of the ``CELERYD_USER`` by using a login
    shell:

    .. code-block:: bash

        CELERYD_SU_ARGS="-l"

    Note that this isn't recommended, and that you should only use this option
    when absolutely necessary.

.. _generic-initd-celeryd-django-example:

示例 Django 配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example Django configuration

.. tab:: 中文

    Django 用户现在可以使用与上述完全相同的模板，
    但请确保定义你 Celery 应用实例的模块
    也设置了 :envvar:`DJANGO_SETTINGS_MODULE` 的默认值，
    参考 :ref:`django-first-steps` 中的 Django 项目示例。


.. tab:: 英文

    Django users now uses the exact same template as above,
    but make sure that the module that defines your Celery app instance
    also sets a default value for :envvar:`DJANGO_SETTINGS_MODULE`
    as shown in the example Django project in :ref:`django-first-steps`.

.. _generic-initd-celeryd-options:

可用选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Available options

.. tab:: 中文

    * ``CELERY_APP``
    
      要使用的应用实例（对应 :option:`--app <celery --app>` 参数的值）。
    
    * ``CELERY_BIN``
    
      :program:`celery` 程序的绝对路径或相对路径。
      示例：
    
      * :file:`celery`
      * :file:`/usr/local/bin/celery`
      * :file:`/virtualenvs/proj/bin/celery`
      * :file:`/virtualenvs/proj/bin/python -m celery`
    
    * ``CELERYD_NODES``
    
      要启动的节点名称列表（以空格分隔）。
    
    * ``CELERYD_OPTS``
    
      传递给 worker 的额外命令行参数，参见 `celery worker --help` 获取参数列表。
      此项也支持 `multi` 使用的扩展语法，可为各个节点分别配置参数。
      示例参见 `celery multi --help` 中的多节点配置说明。
    
    * ``CELERYD_CHDIR``
    
      启动时切换的目录路径。默认不会切换，保持当前目录。
    
    * ``CELERYD_PID_FILE``
    
      PID 文件的完整路径。默认为 /var/run/celery/%n.pid
    
    * ``CELERYD_LOG_FILE``
    
      worker 日志文件的完整路径。默认为 /var/log/celery/%n%I.log  
      **注意**：在使用 prefork 池时，使用 `%I` 是非常重要的，
      因为多个进程共享同一日志文件会引发竞争条件。
    
    * ``CELERYD_LOG_LEVEL``
    
      worker 的日志级别。默认为 INFO。
    
    * ``CELERYD_USER``
    
      运行 worker 的用户。默认为当前用户。
    
    * ``CELERYD_GROUP``
    
      运行 worker 的用户组。默认为当前用户。
    
    * ``CELERY_CREATE_DIRS``
    
      是否总是创建所需目录（如日志目录和 PID 文件目录）。
      默认仅在未设置自定义日志文件或 PID 文件路径时创建。
    
    * ``CELERY_CREATE_RUNDIR``
    
      是否总是创建 PID 文件目录。默认仅在未设置自定义 PID 文件路径时启用。
    
    * ``CELERY_CREATE_LOGDIR``
    
      是否总是创建日志文件目录。默认仅在未设置自定义日志路径时启用。

.. tab:: 英文
    
    * ``CELERY_APP``
    
      App instance to use (value for :option:`--app <celery --app>` argument).
    
    * ``CELERY_BIN``
    
      Absolute or relative path to the :program:`celery` program.
      Examples:
      
      * :file:`celery`
      * :file:`/usr/local/bin/celery`
      * :file:`/virtualenvs/proj/bin/celery`
      * :file:`/virtualenvs/proj/bin/python -m celery`
    
    * ``CELERYD_NODES``
    
      List of node names to start (separated by space).
    
    * ``CELERYD_OPTS``
    
      Additional command-line arguments for the worker, see
      `celery worker --help` for a list. This also supports the extended
      syntax used by `multi` to configure settings for individual nodes.
      See `celery multi --help` for some multi-node configuration examples.
    
    * ``CELERYD_CHDIR``
    
      Path to change directory to at start. Default is to stay in the current
      directory.
    
    * ``CELERYD_PID_FILE``
    
      Full path to the PID file. Default is /var/run/celery/%n.pid
    
    * ``CELERYD_LOG_FILE``
    
      Full path to the worker log file. Default is /var/log/celery/%n%I.log
      **Note**: Using `%I` is important when using the prefork pool as having
      multiple processes share the same log file will lead to race conditions.
    
    * ``CELERYD_LOG_LEVEL``
    
      Worker log level. Default is INFO.
    
    * ``CELERYD_USER``
    
      User to run the worker as. Default is current user.
    
    * ``CELERYD_GROUP``
    
      Group to run worker as. Default is current user.
    
    * ``CELERY_CREATE_DIRS``
    
      Always create directories (log directory and pid file directory).
      Default is to only create directories when no custom logfile/pidfile set.
    
    * ``CELERY_CREATE_RUNDIR``
    
      Always create pidfile directory. By default only enabled when no custom
      pidfile location set.
    
    * ``CELERY_CREATE_LOGDIR``
    
      Always create logfile directory. By default only enable when no custom
      logfile location set.

.. _generic-initd-celerybeat:

初始化脚本：``celerybeat``
----------------------------------------------------------------------

Init-script: ``celerybeat``

.. tab:: 中文

    :用法: `/etc/init.d/celerybeat {start|stop|restart}`
    :配置文件: :file:`/etc/default/celerybeat` 或 :file:`/etc/default/celeryd`.

.. tab:: 英文

    :Usage: `/etc/init.d/celerybeat {start|stop|restart}`
    :Configuration file: :file:`/etc/default/celerybeat` or
                        :file:`/etc/default/celeryd`.

.. _generic-initd-celerybeat-example:

示例配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. tab:: 中文

    以下是一个 Python 项目的示例配置：

    `/etc/default/celerybeat`:

    .. code-block:: bash

        # 指向 'celery' 命令的绝对路径或相对路径：
        CELERY_BIN="/usr/local/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"

        # 要使用的应用实例
        # 如果你没有使用 app，可以注释掉此行
        CELERY_APP="proj"
        # 或使用完整限定名：
        #CELERY_APP="proj.tasks:app"

        # 启动时要切换的目录
        CELERYBEAT_CHDIR="/opt/Myproject/"

        # 传递给 celerybeat 的额外参数
        CELERYBEAT_OPTS="--schedule=/var/run/celery/celerybeat-schedule"


.. tab:: 英文

    This is an example configuration for a Python project:

    `/etc/default/celerybeat`:

    .. code-block:: bash

        # Absolute or relative path to the 'celery' command:
        CELERY_BIN="/usr/local/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"

        # App instance to use
        # comment out this line if you don't use an app
        CELERY_APP="proj"
        # or fully qualified:
        #CELERY_APP="proj.tasks:app"

        # Where to chdir at start.
        CELERYBEAT_CHDIR="/opt/Myproject/"

        # Extra arguments to celerybeat
        CELERYBEAT_OPTS="--schedule=/var/run/celery/celerybeat-schedule"

.. _generic-initd-celerybeat-django-example:

示例 Django 配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example Django configuration

.. tab:: 中文

    你应该使用与上文相同的模板，但需确保设置并导出 ``DJANGO_SETTINGS_MODULE`` 变量，
    同时设置 ``CELERYD_CHDIR`` 指向项目目录：

    .. code-block:: bash

        export DJANGO_SETTINGS_MODULE="settings"

        CELERYD_CHDIR="/opt/MyProject"

.. tab:: 英文

    You should use the same template as above, but make sure the
    ``DJANGO_SETTINGS_MODULE`` variable is set (and exported), and that
    ``CELERYD_CHDIR`` is set to the projects directory:

    .. code-block:: bash

        export DJANGO_SETTINGS_MODULE="settings"

        CELERYD_CHDIR="/opt/MyProject"

.. _generic-initd-celerybeat-options:

可用选项
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Available options

.. tab:: 中文

    * ``CELERY_APP``
    
      要使用的应用实例（对应 :option:`--app <celery --app>` 参数的值）。
    
    * ``CELERYBEAT_OPTS``
    
      传递给 :program:`celery beat` 的额外参数，
      可使用 :command:`celery beat --help` 查看可用选项。
    
    * ``CELERYBEAT_PID_FILE``
    
      PID 文件的完整路径。默认为 :file:`/var/run/celeryd.pid`。
    
    * ``CELERYBEAT_LOG_FILE``
    
      日志文件的完整路径。默认为 :file:`/var/log/celeryd.log`。
    
    * ``CELERYBEAT_LOG_LEVEL``
    
      要使用的日志级别。默认为 ``INFO``。
    
    * ``CELERYBEAT_USER``
    
      运行 beat 的用户。默认为当前用户。
    
    * ``CELERYBEAT_GROUP``
    
      运行 beat 的用户组。默认为当前用户。
    
    * ``CELERY_CREATE_DIRS``
    
      是否总是创建所需目录（如日志目录和 PID 文件目录）。
      默认仅在未设置自定义日志文件或 PID 文件路径时创建。
    
    * ``CELERY_CREATE_RUNDIR``
    
      是否总是创建 PID 文件目录。默认仅在未设置自定义 PID 文件路径时启用。
    
    * ``CELERY_CREATE_LOGDIR``
    
      是否总是创建日志文件目录。默认仅在未设置自定义日志路径时启用。

.. tab:: 英文

    * ``CELERY_APP``
    
      App instance to use (value for :option:`--app <celery --app>` argument).
    
    * ``CELERYBEAT_OPTS``
    
      Additional arguments to :program:`celery beat`, see
      :command:`celery beat --help` for a list of available options.
    
    * ``CELERYBEAT_PID_FILE``
    
      Full path to the PID file. Default is :file:`/var/run/celeryd.pid`.
    
    * ``CELERYBEAT_LOG_FILE``
    
      Full path to the log file. Default is :file:`/var/log/celeryd.log`.
    
    * ``CELERYBEAT_LOG_LEVEL``
    
      Log level to use. Default is ``INFO``.
    
    * ``CELERYBEAT_USER``
    
      User to run beat as. Default is the current user.
    
    * ``CELERYBEAT_GROUP``
    
      Group to run beat as. Default is the current user.
    
    * ``CELERY_CREATE_DIRS``
    
      Always create directories (log directory and pid file directory).
      Default is to only create directories when no custom logfile/pidfile set.
    
    * ``CELERY_CREATE_RUNDIR``
    
      Always create pidfile directory. By default only enabled when no custom
      pidfile location set.
    
    * ``CELERY_CREATE_LOGDIR``
    
      Always create logfile directory. By default only enable when no custom
      logfile location set.

.. _generic-initd-troubleshooting:

故障排除
----------------------------------------------------------------------

Troubleshooting

.. tab:: 中文

    如果你无法让 init 脚本正常工作，可以尝试以 *verbose 模式* 启动它们：

    .. code-block:: console

        # sh -x /etc/init.d/celeryd start

    这将帮助你定位服务无法启动的原因。

    如果 worker 显示 *"OK"* 后几乎立刻退出，且日志文件中没有任何信息，
    很可能是有错误发生，但由于守护进程的标准输出已经关闭，
    这些信息将不会被记录。此时，你可以通过设置
    :envvar:`C_FAKEFORK` 环境变量来跳过守护化步骤：

    .. code-block:: console

        # C_FAKEFORK=1 sh -x /etc/init.d/celeryd start

    现在你就能看到具体的错误信息了。

    常见的错误原因包括对某个文件无读取或写入权限，
    也可能是配置模块、用户模块、第三方库，甚至 Celery 自身中存在语法错误
    （如果你发现了 Celery 的 bug，请 :ref:`报告它 <reporting-bugs>`）。

.. tab:: 英文

    If you can't get the init-scripts to work, you should try running
    them in *verbose mode*:

    .. code-block:: console

        # sh -x /etc/init.d/celeryd start

    This can reveal hints as to why the service won't start.

    If the worker starts with *"OK"* but exits almost immediately afterwards
    and there's no evidence in the log file, then there's probably an error
    but as the daemons standard outputs are already closed you'll
    not be able to see them anywhere. For this situation you can use
    the :envvar:`C_FAKEFORK` environment variable to skip the
    daemonization step:

    .. code-block:: console

        # C_FAKEFORK=1 sh -x /etc/init.d/celeryd start


    and now you should be able to see the errors.

    Commonly such errors are caused by insufficient permissions
    to read from, or write to a file, and also by syntax errors
    in configuration modules, user modules, third-party libraries,
    or even from Celery itself (if you've found a bug you
    should :ref:`report it <reporting-bugs>`).


.. _daemon-systemd-generic:

使用 ``systemd``
======================================================================

Usage ``systemd``

* `extra/systemd/`_

.. _`extra/systemd/`:
    https://github.com/celery/celery/tree/main/extra/systemd/

.. _generic-systemd-celery:

:Usage: `systemctl {start|stop|restart|status} celery.service`
:Configuration file: /etc/conf.d/celery

服务文件：celery.service
----------------------------------------------------------------------

Service file: celery.service

.. tab:: 中文

    以下是一个 systemd 配置文件示例：

    :file:`/etc/systemd/system/celery.service`:

    .. code-block:: bash

        [Unit]
        Description=Celery Service
        After=network.target

        [Service]
        Type=forking
        User=celery
        Group=celery
        EnvironmentFile=/etc/conf.d/celery
        WorkingDirectory=/opt/celery
        ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
            --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
            --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
        ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
            --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
            --loglevel="${CELERYD_LOG_LEVEL}"'
        ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
            --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
            --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
        Restart=always

        [Install]
        WantedBy=multi-user.target

    将该文件放入 :file:`/etc/systemd/system` 后，你应当运行
    :command:`systemctl daemon-reload` 来使 Systemd 识别该文件。
    每次修改该文件后也需要运行此命令。
    如果你希望在系统启动或重启时自动启动 celery 服务，
    可以运行 :command:`systemctl enable celery.service`。

    你也可以为 celery 服务指定额外的依赖项：
    例如，如果你使用 RabbitMQ 作为 broker，可以在 ``[Unit]`` 的
    ``After=`` 和 ``Requires=`` 中同时指定 ``rabbitmq-server.service``。
    详细选项可参考 `systemd section <https://www.freedesktop.org/software/systemd/man/systemd.unit.html#%5BUnit%5D%20Section%20Options>`_。

    要配置运行用户、用户组、以及目录切换行为，
    可编辑 :file:`/etc/systemd/system/celery.service` 中的
    ``User``、``Group`` 和 ``WorkingDirectory``。

    你也可以使用 systemd-tmpfiles 创建工作目录（如日志目录和 PID 文件目录）：

    :file:`/etc/tmpfiles.d/celery.conf`

    .. code-block:: bash

    d /run/celery 0755 celery celery -
    d /var/log/celery 0755 celery celery -

.. tab:: 英文

    This is an example systemd file:

    :file:`/etc/systemd/system/celery.service`:

    .. code-block:: bash

        [Unit]
        Description=Celery Service
        After=network.target

        [Service]
        Type=forking
        User=celery
        Group=celery
        EnvironmentFile=/etc/conf.d/celery
        WorkingDirectory=/opt/celery
        ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
            --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
            --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
        ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
            --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
            --loglevel="${CELERYD_LOG_LEVEL}"'
        ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
            --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
            --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
        Restart=always

        [Install]
        WantedBy=multi-user.target

    Once you've put that file in :file:`/etc/systemd/system`, you should run
    :command:`systemctl daemon-reload` in order that Systemd acknowledges that file.
    You should also run that command each time you modify it.
    Use :command:`systemctl enable celery.service` if you want the celery service to
    automatically start when (re)booting the system.

    Optionally you can specify extra dependencies for the celery service: e.g. if you use
    RabbitMQ as a broker, you could specify ``rabbitmq-server.service`` in both ``After=`` and ``Requires=``
    in the ``[Unit]`` `systemd section <https://www.freedesktop.org/software/systemd/man/systemd.unit.html#%5BUnit%5D%20Section%20Options>`_.

    To configure user, group, :command:`chdir` change settings:
    ``User``, ``Group``, and ``WorkingDirectory`` defined in
    :file:`/etc/systemd/system/celery.service`.

    You can also use systemd-tmpfiles in order to create working directories (for logs and pid).

    :file: `/etc/tmpfiles.d/celery.conf`

    .. code-block:: bash

        d /run/celery 0755 celery celery -
        d /var/log/celery 0755 celery celery -


.. _generic-systemd-celery-example:

示例配置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example configuration

.. tab:: 中文

    以下是一个针对 Python 项目的配置文件示例：

    :file:`/etc/conf.d/celery`:

    .. code-block:: bash

        # 要启动的节点名称
        # 这里仅启动一个节点
        CELERYD_NODES="w1"
        # 或者启动三个节点：
        #CELERYD_NODES="w1 w2 w3"

        # 'celery' 命令的绝对路径或相对路径：
        CELERY_BIN="/usr/local/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"

        # 要使用的应用实例
        # 如果未使用应用可注释此行
        CELERY_APP="proj"
        # 或使用完整限定名：
        #CELERY_APP="proj.tasks:app"

        # 调用 manage.py 的方式
        CELERYD_MULTI="multi"

        # 传递给 worker 的额外命令行参数
        CELERYD_OPTS="--time-limit=300 --concurrency=8"

        # - %n 会被替换为节点名称的第一部分
        # - %I 会被替换为当前子进程索引
        #   当使用 prefork 池时，该参数有助于避免竞争条件
        CELERYD_PID_FILE="/var/run/celery/%n.pid"
        CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
        CELERYD_LOG_LEVEL="INFO"

        # 如需使用 Celery Beat，可添加以下选项
        CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
        CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"

.. tab:: 英文

    This is an example configuration for a Python project:

    :file:`/etc/conf.d/celery`:

    .. code-block:: bash

        # Name of nodes to start
        # here we have a single node
        CELERYD_NODES="w1"
        # or we could have three nodes:
        #CELERYD_NODES="w1 w2 w3"

        # Absolute or relative path to the 'celery' command:
        CELERY_BIN="/usr/local/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"

        # App instance to use
        # comment out this line if you don't use an app
        CELERY_APP="proj"
        # or fully qualified:
        #CELERY_APP="proj.tasks:app"

        # How to call manage.py
        CELERYD_MULTI="multi"

        # Extra command-line arguments to the worker
        CELERYD_OPTS="--time-limit=300 --concurrency=8"

        # - %n will be replaced with the first part of the nodename.
        # - %I will be replaced with the current child process index
        #   and is important when using the prefork pool to avoid race conditions.
        CELERYD_PID_FILE="/var/run/celery/%n.pid"
        CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
        CELERYD_LOG_LEVEL="INFO"

        # you may wish to add these options for Celery Beat
        CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
        CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"

服务文件：celerybeat.service
----------------------------------------------------------------------

Service file: celerybeat.service

.. tab:: 中文

    以下是一个 Celery Beat 的 systemd 服务配置示例：

    :file:`/etc/systemd/system/celerybeat.service`:

    .. code-block:: bash

        [Unit]
        Description=Celery Beat Service
        After=network.target

        [Service]
        Type=simple
        User=celery
        Group=celery
        EnvironmentFile=/etc/conf.d/celery
        WorkingDirectory=/opt/celery
        ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
            --pidfile=${CELERYBEAT_PID_FILE} \
            --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
        Restart=always

        [Install]
        WantedBy=multi-user.target

    将该文件放入 :file:`/etc/systemd/system` 后，你应当运行
    :command:`systemctl daemon-reload` 来使 Systemd 识别该文件。
    每次修改该文件后也需要运行此命令。
    如果你希望在系统启动或重启时自动启动 celery beat 服务，
    可以运行 :command:`systemctl enable celerybeat.service`。

.. tab:: 英文

    This is an example systemd file for Celery Beat:
    
    :file:`/etc/systemd/system/celerybeat.service`:
    
    .. code-block:: bash
    
        [Unit]
        Description=Celery Beat Service
        After=network.target
    
        [Service]
        Type=simple
        User=celery
        Group=celery
        EnvironmentFile=/etc/conf.d/celery
        WorkingDirectory=/opt/celery
        ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat  \
            --pidfile=${CELERYBEAT_PID_FILE} \
            --logfile=${CELERYBEAT_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
        Restart=always
    
        [Install]
        WantedBy=multi-user.target
    
    Once you've put that file in :file:`/etc/systemd/system`, you should run
    :command:`systemctl daemon-reload` in order that Systemd acknowledges that file.
    You should also run that command each time you modify it.
    Use :command:`systemctl enable celerybeat.service` if you want the celery beat
    service to automatically start when (re)booting the system.

使用超级用户权限 (root) 运行工作器
======================================================================

Running the worker with superuser privileges (root)

.. tab:: 中文

    以超级用户权限运行 worker 是非常危险的做法。
    应始终寻找替代方案，避免以 root 用户身份运行。因为 Celery 可能会执行消息中使用 pickle 序列化的任意代码 —— 这在以 root 身份运行时尤其危险。

    默认情况下，Celery 不允许以 root 身份运行 worker。相关的错误信息可能不会出现在日志中，但如果使用了 :envvar:`C_FAKEFORK`，则可能会显示出来。

    若确实需要以 root 身份运行 Celery worker，可通过设置 :envvar:`C_FORCE_ROOT` 强制允许。

    如果以 root 身份运行但未设置 :envvar:`C_FORCE_ROOT`，worker 表面上会以 *"OK"* 状态启动，但随后会立即退出，且没有明显错误提示。这种问题通常出现在项目在新的开发或生产环境中（无意间）以 root 用户身份运行时。


.. tab:: 英文

    Running the worker with superuser privileges is a very dangerous practice.
    There should always be a workaround to avoid running as root. Celery may
    run arbitrary code in messages serialized with pickle - this is dangerous,
    especially when run as root.

    By default Celery won't run workers as root. The associated error
    message may not be visible in the logs but may be seen if :envvar:`C_FAKEFORK`
    is used.

    To force Celery to run workers as root use :envvar:`C_FORCE_ROOT`.

    When running as root without :envvar:`C_FORCE_ROOT` the worker will
    appear to start with *"OK"* but exit immediately after with no apparent
    errors. This problem may appear when running the project in a new development
    or production environment (inadvertently) as root.

.. _daemon-supervisord:

supervisor
======================================================================

:pypi:`supervisor`


* `extra/supervisord/`_

.. _`extra/supervisord/`:
    https://github.com/celery/celery/tree/main/extra/supervisord/

.. _daemon-launchd:

``launchd`` (macOS)
======================================================================

* `extra/macOS`_

.. _`extra/macOS`:
    https://github.com/celery/celery/tree/main/extra/macOS/
