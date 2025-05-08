.. _guide-beat:

================
周期性任务/Tasks
================

Periodic Tasks


简介
============

Introduction

.. tab:: 中文

    :program:`celery beat` 是一个调度器；它会在固定的时间间隔触发任务，
    随后由集群中可用的 worker 节点来执行这些任务。

    默认情况下，任务条目来源于 :setting:`beat_schedule` 配置项，
    但也可以使用自定义存储后端，比如将任务条目存储在 SQL 数据库中。

    你需要确保在任意时刻只运行一个调度器实例，否则会导致重复任务执行。
    采用集中式方式意味着调度无需同步，该服务在无需使用锁的情况下也可运行。

.. tab:: 英文

    :program:`celery beat` is a scheduler; It kicks off tasks at regular intervals,
    that are then executed by available worker nodes in the cluster.

    By default the entries are taken from the :setting:`beat_schedule` setting,
    but custom stores can also be used, like storing the entries in a SQL database.

    You have to ensure only a single scheduler is running for a schedule
    at a time, otherwise you'd end up with duplicate tasks. Using
    a centralized approach means the schedule doesn't have to be synchronized,
    and the service can operate without using locks.

.. _beat-timezones:

时区
==========

Time Zones

.. tab:: 中文

    定时任务调度默认使用 UTC 时区，
    但你可以通过 :setting:`timezone` 配置项来修改所使用的时区。

    一个示例时区为 `Europe/London`：

    .. code-block:: python

        timezone = 'Europe/London'

    该配置项必须添加到你的应用中，可以通过直接配置
    （``app.conf.timezone = 'Europe/London'``），
    或在使用 ``app.config_from_object`` 配置模块时添加。
    参见 :ref:`celerytut-configuration` 获取更多配置信息。

    默认调度器（使用 :file:`celerybeat-schedule` 文件存储调度信息）
    会自动检测时区变化并重置调度，
    但其他调度器可能无法做到这一点（例如 Django 的数据库调度器，见下文），
    此时你需要手动重置调度计划。

    .. admonition:: Django 用户

        Celery 推荐使用并兼容 Django 1.4 引入的 ``USE_TZ`` 设置。

        对于 Django 用户，将使用 ``TIME_ZONE`` 配置的时区，
        你也可以单独为 Celery 指定一个自定义时区，
        使用 :setting:`timezone` 配置项即可。

        当时区相关配置发生变化时，数据库调度器不会自动重置，
        因此你必须手动执行以下操作：

        .. code-block:: console

            $ python manage.py shell
            >>> from djcelery.models import PeriodicTask
            >>> PeriodicTask.objects.update(last_run_at=None)

        Django-Celery 仅支持 Celery 4.0 及以下版本，若使用 Celery 4.0 及以上版本，请按如下方式操作：

        .. code-block:: console

            $ python manage.py shell
            >>> from django_celery_beat.models import PeriodicTask
            >>> PeriodicTask.objects.update(last_run_at=None)

.. tab:: 英文

    The periodic task schedules uses the UTC time zone by default,
    but you can change the time zone used using the :setting:`timezone`
    setting.

    An example time zone could be `Europe/London`:

    .. code-block:: python

        timezone = 'Europe/London'

    This setting must be added to your app, either by configuring it directly
    using (``app.conf.timezone = 'Europe/London'``), or by adding
    it to your configuration module if you have set one up using
    ``app.config_from_object``. See :ref:`celerytut-configuration` for
    more information about configuration options.

    The default scheduler (storing the schedule in the :file:`celerybeat-schedule`
    file) will automatically detect that the time zone has changed, and so will
    reset the schedule itself, but other schedulers may not be so smart (e.g., the
    Django database scheduler, see below) and in that case you'll have to reset the
    schedule manually.

    .. admonition:: Django Users

        Celery recommends and is compatible with the ``USE_TZ`` setting introduced
        in Django 1.4.

        For Django users the time zone specified in the ``TIME_ZONE`` setting
        will be used, or you can specify a custom time zone for Celery alone
        by using the :setting:`timezone` setting.

        The database scheduler won't reset when timezone related settings
        change, so you must do this manually:

        .. code-block:: console

            $ python manage.py shell
            >>> from djcelery.models import PeriodicTask
            >>> PeriodicTask.objects.update(last_run_at=None)

        Django-Celery only supports Celery 4.0 and below, for Celery 4.0 and above, do as follow:

        .. code-block:: console

            $ python manage.py shell
            >>> from django_celery_beat.models import PeriodicTask
            >>> PeriodicTask.objects.update(last_run_at=None)

.. _beat-entries:

条目
=======

Entries

.. tab:: 中文

    要实现周期性任务调用，你需要在 beat 的调度列表中添加一个条目：

    .. code-block:: python

        from celery import Celery
        from celery.schedules import crontab

        app = Celery()

        @app.on_after_configure.connect
        def setup_periodic_tasks(sender: Celery, **kwargs):
            # 每 10 秒调用一次 test('hello')
            sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

            # 每 30 秒调用一次 test('hello')
            # 使用相同的签名并显式指定名称，以避免覆盖前一个任务
            sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

            # 每 30 秒调用一次 test('world')
            sender.add_periodic_task(30.0, test.s('world'), expires=10)

            # 每周一早上 7:30 执行一次
            sender.add_periodic_task(
                crontab(hour=7, minute=30, day_of_week=1),
                test.s('Happy Mondays!'),
            )

        @app.task
        def test(arg):
            print(arg)

        @app.task
        def add(x, y):
            z = x + y
            print(z)

    在 :data:`~@on_after_configure` 处理器中设置这些任务，
    意味着我们不会在模块级别对 app 进行求值（即使用 ``test.s()`` 不会在模块加载时执行）。
    注意 :data:`~@on_after_configure` 信号是在 app 设置完成后发送的，
    因此如果你的任务定义在声明 app 的模块之外（例如在通过
    :meth:`celery.Celery.autodiscover_tasks` 发现的 `tasks.py` 文件中），
    则应使用更晚触发的信号，例如 :data:`~@on_after_finalize`。

    :meth:`~@add_periodic_task` 方法会在后台将任务条目添加到
    :setting:`beat_schedule` 配置项中，
    你也可以手动使用该配置项来设置周期性任务：

    示例：每 30 秒运行一次 `tasks.add` 任务。

    .. code-block:: python

        app.conf.beat_schedule = {
            'add-every-30-seconds': {
                'task': 'tasks.add',
                'schedule': 30.0,
                'args': (16, 16)
            },
        }
        app.conf.timezone = 'UTC'


    .. note::

        如果你不确定这些配置应放在哪，请参阅 :ref:`celerytut-configuration`。
        你可以直接在 app 上设置这些选项，
        也可以使用独立的配置模块。

        如果你希望为 `args` 使用一个单元素的元组，请注意：
        元组的构造依赖逗号而非括号。

    如果使用 :class:`~datetime.timedelta` 作为调度方式，
    那么任务会每隔 30 秒被发送一次（第一次发送发生在 `celery beat` 启动后的 30 秒，
    之后每次都在上一次运行后的 30 秒）。

    也可以使用类 Crontab 的调度方式，详见 :ref:`Crontab 调度 <Crontab schedules>` 一节。

    如同 :command:`cron` 一样，如果第一个任务尚未完成，后一个任务就会触发，则会出现任务重叠问题。
    如果你担心这种情况发生，应使用锁机制确保同一时间只运行一个实例（参考 :ref:`cookbook-task-serial` ）。

.. tab:: 英文

    To call a task periodically you have to add an entry to the
    beat schedule list.

    .. code-block:: python

        from celery import Celery
        from celery.schedules import crontab

        app = Celery()

        @app.on_after_configure.connect
        def setup_periodic_tasks(sender: Celery, **kwargs):
            # Calls test('hello') every 10 seconds.
            sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

            # Calls test('hello') every 30 seconds.
            # It uses the same signature of previous task, an explicit name is
            # defined to avoid this task replacing the previous one defined.
            sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

            # Calls test('world') every 30 seconds
            sender.add_periodic_task(30.0, test.s('world'), expires=10)

            # Executes every Monday morning at 7:30 a.m.
            sender.add_periodic_task(
                crontab(hour=7, minute=30, day_of_week=1),
                test.s('Happy Mondays!'),
            )

        @app.task
        def test(arg):
            print(arg)

        @app.task
        def add(x, y):
            z = x + y
            print(z)



    Setting these up from within the :data:`~@on_after_configure` handler means
    that we'll not evaluate the app at module level when using ``test.s()``. Note that
    :data:`~@on_after_configure` is sent after the app is set up, so tasks outside the
    module where the app is declared (e.g. in a `tasks.py` file located by
    :meth:`celery.Celery.autodiscover_tasks`) must use a later signal, such as
    :data:`~@on_after_finalize`.

    The :meth:`~@add_periodic_task` function will add the entry to the
    :setting:`beat_schedule` setting behind the scenes, and the same setting
    can also be used to set up periodic tasks manually:

    Example: Run the `tasks.add` task every 30 seconds.

    .. code-block:: python

        app.conf.beat_schedule = {
            'add-every-30-seconds': {
                'task': 'tasks.add',
                'schedule': 30.0,
                'args': (16, 16)
            },
        }
        app.conf.timezone = 'UTC'


    .. note::

        If you're wondering where these settings should go then
        please see :ref:`celerytut-configuration`. You can either
        set these options on your app directly or you can keep
        a separate module for configuration.

        If you want to use a single item tuple for `args`, don't forget
        that the constructor is a comma, and not a pair of parentheses.

    Using a :class:`~datetime.timedelta` for the schedule means the task will
    be sent in 30 second intervals (the first task will be sent 30 seconds
    after `celery beat` starts, and then every 30 seconds
    after the last run).

    A Crontab like schedule also exists, see the section on `Crontab schedules`_.

    Like with :command:`cron`, the tasks may overlap if the first task doesn't complete
    before the next. If that's a concern you should use a locking
    strategy to ensure only one instance can run at a time (see for example
    :ref:`cookbook-task-serial`).

.. _beat-entry-fields:

可用字段
----------------

Available Fields

.. tab:: 中文

    * `task`
    
      要执行的任务名称。
    
      有关任务名称的说明，请参阅用户指南中的 :ref:`task-names` 部分。
      请注意，这不是任务的导入路径，尽管默认的命名模式看起来类似于导入路径。
    
    * `schedule`
    
      执行频率。
    
      可以是一个整数（表示秒数）、一个 :class:`~datetime.timedelta` 对象，
      或一个 :class:`~celery.schedules.crontab` 对象。
      你也可以通过扩展 :class:`~celery.schedules.schedule` 接口定义自定义的调度类型。
    
    * `args`
    
      位置参数（:class:`list` 或 :class:`tuple` 类型）。
    
    * `kwargs`
    
      关键字参数（:class:`dict` 类型）。
    
    * `options`
    
      执行选项（:class:`dict` 类型）。
    
      可以是任何被 :meth:`~celery.app.task.Task.apply_async` 支持的参数——
      比如 `exchange`、`routing_key`、`expires` 等。
    
    * `relative`
    
      如果 `relative` 为 true，则 :class:`~datetime.timedelta` 类型的调度将以“按时钟”的方式执行。
      这意味着调度周期将会被四舍五入为最接近的秒、分钟、小时或天，
      具体取决于 :class:`~datetime.timedelta` 所表示的周期。
      
      默认情况下，`relative` 为 false，调度不会被四舍五入，
      而是相对于 :program:`celery beat` 启动时的时间点来计算。

.. tab:: 英文

    * `task`
    
      The name of the task to execute.
      
      Task names are described in the :ref:`task-names` section of the User Guide.
      Note that this is not the import path of the task, even though the default
      naming pattern is built like it is.
    
    * `schedule`
    
      The frequency of execution.
      
      This can be the number of seconds as an integer, a
      :class:`~datetime.timedelta`, or a :class:`~celery.schedules.crontab`.
      You can also define your own custom schedule types, by extending the
      interface of :class:`~celery.schedules.schedule`.
    
    * `args`
    
      Positional arguments (:class:`list` or :class:`tuple`).
    
    * `kwargs`
    
      Keyword arguments (:class:`dict`).
    
    * `options`
    
      Execution options (:class:`dict`).
    
      This can be any argument supported by
      :meth:`~celery.app.task.Task.apply_async` --
      `exchange`, `routing_key`, `expires`, and so on.
    
    * `relative`
    
      If `relative` is true :class:`~datetime.timedelta` schedules are scheduled
      "by the clock." This means the frequency is rounded to the nearest
      second, minute, hour or day depending on the period of the
      :class:`~datetime.timedelta`.
    
      By default `relative` is false, the frequency isn't rounded and will be
      relative to the time when :program:`celery beat` was started.

.. _beat-crontab:

.. _Crontab schedules:

Crontab 调度
=================

Crontab schedules

.. tab:: 中文

    如果你希望对任务的执行时间有更精细的控制，例如特定的时间或星期几，
    你可以使用 :class:`~celery.schedules.crontab` 类型的调度：

    .. code-block:: python

        from celery.schedules import crontab

        app.conf.beat_schedule = {
            # 每周一早上 7:30 执行一次。
            'add-every-monday-morning': {
                'task': 'tasks.add',
                'schedule': crontab(hour=7, minute=30, day_of_week=1),
                'args': (16, 16),
            },
        }

    这些 Crontab 表达式的语法非常灵活。

    一些示例：

    .. list-table::

       * - **示例**
         - **含义**
       * - ``crontab()``
         - 每分钟执行一次.
       * - ``crontab(minute=0, hour=0)``
         - 每天午夜 12 点执行.
       * - ``crontab(minute=0, hour='*/3')``
         - 每三小时执行一次: 午夜, 3am, 6am, 9am, 中午, 3pm, 6pm, 9pm.
       * - ``crontab(minute=0,hour='0,3,6,9,12,15,18,21')``
         - 同上.
       * - ``crontab(minute='*/15')``
         - 每 15 分钟执行一次。
       * - ``crontab(day_of_week='sunday')``
         - 每周日每分钟执行一次（注意频率！）。
       * - ``crontab(minute='*', hour='*', day_of_week='sun')``
         - 同上。
       * - ``crontab(minute='*/10', hour='3,17,22', day_of_week='thu,fri')``
         - 每十分钟执行一次，但仅在以下时段： 凌晨 3-4 点、下午 5-6 点和晚上 10-11 点，并且仅限于周四和周五。
       * - ``crontab(minute=0, hour='*/2,*/3')``
         - 每个偶数小时执行一次，以及每个能被 3 整除的小时执行一次。也就是说，除以下时刻外均执行：1am、5am、7am、11am、1pm、5pm、7pm、11pm。
       * - ``crontab(minute=0, hour='*/5')``
         - 每个能被 5 整除的小时执行一次。即会在下午 3 点（即 24 小时制的 15 点）触发，而不是下午 5 点。
       * - ``crontab(minute=0, hour='*/3,8-17')``
         - 每个能被 3 整除的小时，以及每天的办公时段（早上 8 点至下午 5 点）都执行一次。
       * - ``crontab(0, 0, day_of_month='2')``
         - 每月的第 2 天执行一次。
       * - ``crontab(0, 0, day_of_month='2-30/2')``
         - 每个月的所有偶数日执行一次。
       * - ``crontab(0, 0, day_of_month='1-7,15-21')``
         - 每月的第 1 周和第 3 周执行一次。
       * - ``crontab(0, 0, day_of_month='11', month_of_year='5')``
         - 每年 5 月 11 日执行一次。
       * - ``crontab(0, 0, month_of_year='*/3')``
         - 每个季度的第一个月每天执行一次。

    更多信息请参见 :class:`celery.schedules.crontab` 的文档。


.. tab:: 英文

    If you want more control over when the task is executed, for
    example, a particular time of day or day of the week, you can use
    the :class:`~celery.schedules.crontab` schedule type:

    .. code-block:: python

        from celery.schedules import crontab

        app.conf.beat_schedule = {
            # Executes every Monday morning at 7:30 a.m.
            'add-every-monday-morning': {
                'task': 'tasks.add',
                'schedule': crontab(hour=7, minute=30, day_of_week=1),
                'args': (16, 16),
            },
        }

    The syntax of these Crontab expressions are very flexible.

    Some examples:

    +-----------------------------------------+--------------------------------------------+
    | **Example**                             | **Meaning**                                |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab()``                           | Execute every minute.                      |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute=0, hour=0)``           | Execute daily at midnight.                 |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute=0, hour='*/3')``       | Execute every three hours:                 |
    |                                         | midnight, 3am, 6am, 9am,                   |
    |                                         | noon, 3pm, 6pm, 9pm.                       |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute=0,``                   | Same as previous.                          |
    |         ``hour='0,3,6,9,12,15,18,21')`` |                                            |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute='*/15')``              | Execute every 15 minutes.                  |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(day_of_week='sunday')``       | Execute every minute (!) at Sundays.       |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute='*',``                 | Same as previous.                          |
    |         ``hour='*',``                   |                                            |
    |         ``day_of_week='sun')``          |                                            |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute='*/10',``              | Execute every ten minutes, but only        |
    |         ``hour='3,17,22',``             | between 3-4 am, 5-6 pm, and 10-11 pm on    |
    |         ``day_of_week='thu,fri')``      | Thursdays or Fridays.                      |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute=0, hour='*/2,*/3')``   | Execute every even hour, and every hour    |
    |                                         | divisible by three. This means:            |
    |                                         | at every hour *except*: 1am,               |
    |                                         | 5am, 7am, 11am, 1pm, 5pm, 7pm,             |
    |                                         | 11pm                                       |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute=0, hour='*/5')``       | Execute hour divisible by 5. This means    |
    |                                         | that it is triggered at 3pm, not 5pm       |
    |                                         | (since 3pm equals the 24-hour clock        |
    |                                         | value of "15", which is divisible by 5).   |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(minute=0, hour='*/3,8-17')``  | Execute every hour divisible by 3, and     |
    |                                         | every hour during office hours (8am-5pm).  |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(0, 0, day_of_month='2')``     | Execute on the second day of every month.  |
    |                                         |                                            |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(0, 0,``                       | Execute on every even numbered day.        |
    |         ``day_of_month='2-30/2')``      |                                            |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(0, 0,``                       | Execute on the first and third weeks of    |
    |         ``day_of_month='1-7,15-21')``   | the month.                                 |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(0, 0, day_of_month='11',``    | Execute on the eleventh of May every year. |
    |          ``month_of_year='5')``         |                                            |
    +-----------------------------------------+--------------------------------------------+
    | ``crontab(0, 0,``                       | Execute every day on the first month       |
    |         ``month_of_year='*/3')``        | of every quarter.                          |
    +-----------------------------------------+--------------------------------------------+

    See :class:`celery.schedules.crontab` for more documentation.

.. _beat-solar:

Solar 调度
=================

Solar schedules

.. tab:: 中文

    如果你有一个任务需要根据日出、日落、黎明或黄昏时间执行，可以使用
    :class:`~celery.schedules.solar` 调度类型：
    
    .. code-block:: python
    
        from celery.schedules import solar
    
        app.conf.beat_schedule = {
            # 在墨尔本日落时执行
            'add-at-melbourne-sunset': {
                'task': 'tasks.add',
                'schedule': solar('sunset', -37.81753, 144.96715),
                'args': (16, 16),
            },
        }
    
    该调用的参数格式为：``solar(event, latitude, longitude)``
    
    请确保纬度和经度的正负号使用正确：
    
    .. list-table:: 纬度和经度符号说明
       :header-rows: 1
    
       * - **符号**
         - **参数**
         - **含义**
       * - ``+``
         - ``latitude``
         - 北纬
       * - ``-``
         - ``latitude``
         - 南纬
       * - ``+``
         - ``longitude``
         - 东经
       * - ``-``
         - ``longitude``
         - 西经
    
    可用的事件类型如下：
    
    .. list-table:: 可用太阳事件类型
       :header-rows: 1
    
       * - **事件**
         - **含义**
       * - ``dawn_astronomical``
         - 在天空不再完全黑暗的那一刻执行，即太阳位于地平线下 18 度时。
       * - ``dawn_nautical``
         - 当有足够阳光以辨认地平线和一些物体时执行，形式上为太阳位于地平线下 12 度。
       * - ``dawn_civil``
         - 有足够光线让人辨别物体、可以开始户外活动时执行，形式上为太阳位于地平线下 6 度。
       * - ``sunrise``
         - 太阳上缘出现在东方地平线上的那一刻执行。
       * - ``solar_noon``
         - 太阳当天在天空中最高点时执行。
       * - ``sunset``
         - 太阳下缘落入西方地平线下的那一刻执行。
       * - ``dusk_civil``
         - 民用暮光结束时执行，此时仍可辨别物体，可见部分星体，形式上为太阳位于地平线下 6 度。
       * - ``dusk_nautical``
         - 太阳位于地平线下 12 度时执行，此时不可辨认物体，肉眼无法看见地平线。
       * - ``dusk_astronomical``
         - 天空完全变暗的那一刻执行，形式上为太阳位于地平线下 18 度。
    
    所有太阳事件均使用 UTC 进行计算，因此不会受到你所在时区的影响。
    
    在极地地区，太阳可能不会每天升起或落下。调度器能够处理这类情况（例如，若当天没有日出事件，则不会运行该事件）。
    唯一的例外是 ``solar_noon``，它正式定义为太阳过中天（穿越天球子午线）时的时刻，即便太阳在地平线以下也会每日发生。
    
    暮光（twilight）被定义为黎明与日出之间、以及日落与黄昏之间的时间段。
    你可以根据“暮光”时间调度事件，取决于你选择的暮光类型（民用、航海、天文）以及你希望事件在暮光的开始或结束执行，
    可使用上面列表中的相应事件类型。
    
    参见 :class:`celery.schedules.solar` 获取更多文档信息。

.. tab:: 英文

    If you have a task that should be executed according to sunrise,
    sunset, dawn or dusk, you can use the
    :class:`~celery.schedules.solar` schedule type:

    .. code-block:: python

        from celery.schedules import solar

        app.conf.beat_schedule = {
            # Executes at sunset in Melbourne
            'add-at-melbourne-sunset': {
                'task': 'tasks.add',
                'schedule': solar('sunset', -37.81753, 144.96715),
                'args': (16, 16),
            },
        }

    The arguments are simply: ``solar(event, latitude, longitude)``

    Be sure to use the correct sign for latitude and longitude:

    +---------------+-------------------+----------------------+
    | **Sign**      | **Argument**      | **Meaning**          |
    +---------------+-------------------+----------------------+
    | ``+``         | ``latitude``      | North                |
    +---------------+-------------------+----------------------+
    | ``-``         | ``latitude``      | South                |
    +---------------+-------------------+----------------------+
    | ``+``         | ``longitude``     | East                 |
    +---------------+-------------------+----------------------+
    | ``-``         | ``longitude``     | West                 |
    +---------------+-------------------+----------------------+

    Possible event types are:

    +-----------------------------------------+--------------------------------------------+
    | **Event**                               | **Meaning**                                |
    +-----------------------------------------+--------------------------------------------+
    | ``dawn_astronomical``                   | Execute at the moment after which the sky  |
    |                                         | is no longer completely dark. This is when |
    |                                         | the sun is 18 degrees below the horizon.   |
    +-----------------------------------------+--------------------------------------------+
    | ``dawn_nautical``                       | Execute when there's enough sunlight for   |
    |                                         | the horizon and some objects to be         |
    |                                         | distinguishable; formally, when the sun is |
    |                                         | 12 degrees below the horizon.              |
    +-----------------------------------------+--------------------------------------------+
    | ``dawn_civil``                          | Execute when there's enough light for      |
    |                                         | objects to be distinguishable so that      |
    |                                         | outdoor activities can commence;           |
    |                                         | formally, when the Sun is 6 degrees below  |
    |                                         | the horizon.                               |
    +-----------------------------------------+--------------------------------------------+
    | ``sunrise``                             | Execute when the upper edge of the sun     |
    |                                         | appears over the eastern horizon in the    |
    |                                         | morning.                                   |
    +-----------------------------------------+--------------------------------------------+
    | ``solar_noon``                          | Execute when the sun is highest above the  |
    |                                         | horizon on that day.                       |
    +-----------------------------------------+--------------------------------------------+
    | ``sunset``                              | Execute when the trailing edge of the sun  |
    |                                         | disappears over the western horizon in the |
    |                                         | evening.                                   |
    +-----------------------------------------+--------------------------------------------+
    | ``dusk_civil``                          | Execute at the end of civil twilight, when |
    |                                         | objects are still distinguishable and some |
    |                                         | stars and planets are visible. Formally,   |
    |                                         | when the sun is 6 degrees below the        |
    |                                         | horizon.                                   |
    +-----------------------------------------+--------------------------------------------+
    | ``dusk_nautical``                       | Execute when the sun is 12 degrees below   |
    |                                         | the horizon. Objects are no longer         |
    |                                         | distinguishable, and the horizon is no     |
    |                                         | longer visible to the naked eye.           |
    +-----------------------------------------+--------------------------------------------+
    | ``dusk_astronomical``                   | Execute at the moment after which the sky  |
    |                                         | becomes completely dark; formally, when    |
    |                                         | the sun is 18 degrees below the horizon.   |
    +-----------------------------------------+--------------------------------------------+

    All solar events are calculated using UTC, and are therefore
    unaffected by your timezone setting.

    In polar regions, the sun may not rise or set every day. The scheduler
    is able to handle these cases (i.e., a ``sunrise`` event won't run on a day
    when the sun doesn't rise). The one exception is ``solar_noon``, which is
    formally defined as the moment the sun transits the celestial meridian,
    and will occur every day even if the sun is below the horizon.

    Twilight is defined as the period between dawn and sunrise; and between
    sunset and dusk. You can schedule an event according to "twilight"
    depending on your definition of twilight (civil, nautical, or astronomical),
    and whether you want the event to take place at the beginning or end
    of twilight, using the appropriate event from the list above.

    See :class:`celery.schedules.solar` for more documentation.

.. _beat-starting:

启动调度程序
======================

Starting the Scheduler

.. tab:: 中文

    要启动 :program:`celery beat` 服务：
    
    .. code-block:: console
    
        $ celery -A proj beat
    
    你也可以通过启用 worker 的 :option:`-B <celery worker -B>` 选项将 `beat` 嵌入到 worker 中。
    这在你只运行一个 worker 节点时较为方便，但由于不是常规用法，不推荐在生产环境中使用：
    
    .. code-block:: console
    
        $ celery -A proj worker -B
    
    Beat 需要在本地数据库文件中存储任务的最后运行时间（默认文件名为 `celerybeat-schedule`），
    因此需要当前目录具有写权限，或者你可以为该文件指定一个自定义路径：
    
    .. code-block:: console
    
        $ celery -A proj beat -s /home/celery/var/run/celerybeat-schedule
    
    .. note::
    
        如需将 beat 守护化运行，请参阅 :ref:`daemonizing`。

.. tab:: 英文

    To start the :program:`celery beat` service:

    .. code-block:: console

        $ celery -A proj beat

    You can also embed `beat` inside the worker by enabling the
    workers :option:`-B <celery worker -B>` option, this is convenient if you'll
    never run more than one worker node, but it's not commonly used and for that
    reason isn't recommended for production use:

    .. code-block:: console

        $ celery -A proj worker -B

    Beat needs to store the last run times of the tasks in a local database
    file (named `celerybeat-schedule` by default), so it needs access to
    write in the current directory, or alternatively you can specify a custom
    location for this file:

    .. code-block:: console

        $ celery -A proj beat -s /home/celery/var/run/celerybeat-schedule


    .. note::

        To daemonize beat see :ref:`daemonizing`.

.. _beat-custom-schedulers:

使用自定义调度程序类
------------------------------

Using custom scheduler classes

.. tab:: 中文

    你可以在命令行上指定自定义调度器类（使用 :option:`--scheduler <celery beat --scheduler>` 参数）。
    
    默认调度器为 :class:`celery.beat.PersistentScheduler`，它会使用本地 :mod:`shelve` 数据库文件记录任务的最后运行时间。
    
    此外还有 :pypi:`django-celery-beat` 扩展，它会将调度数据存储在 Django 数据库中，并提供便捷的管理界面以在运行时管理定期任务。
    
    要安装并使用该扩展：
    
    #. 使用 :command:`pip` 安装该软件包：
    
       .. code-block:: console
    
           $ pip install django-celery-beat
    
    #. 在你的 Django 项目的 :file:`settings.py` 文件中将 ``django_celery_beat`` 添加至 ``INSTALLED_APPS``::
    
            INSTALLED_APPS = (
                ...,
                'django_celery_beat',
            )
    
       注意：模块名中使用的是下划线（underscore），不是破折号。
    
    #. 应用 Django 数据库迁移，以创建所需的数据表：
    
       .. code-block:: console
    
           $ python manage.py migrate
    
    #. 使用 ``django_celery_beat.schedulers:DatabaseScheduler`` 启动 :program:`celery beat` 服务：
    
       .. code-block:: console
    
           $ celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    
       注意：你也可以将此调度器类配置为 :setting:`beat_scheduler` 设置项。
    
    #. 访问 Django 管理界面，创建一些周期性任务。


.. tab:: 英文

    Custom scheduler classes can be specified on the command-line (the
    :option:`--scheduler <celery beat --scheduler>` argument).
    
    The default scheduler is the :class:`celery.beat.PersistentScheduler`,
    that simply keeps track of the last run times in a local :mod:`shelve`
    database file.
    
    There's also the :pypi:`django-celery-beat` extension that stores the schedule
    in the Django database, and presents a convenient admin interface to manage
    periodic tasks at runtime.
    
    To install and use this extension:
    
    #. Use :command:`pip` to install the package:
    
       .. code-block:: console
    
           $ pip install django-celery-beat
    
    #. Add the ``django_celery_beat`` module to ``INSTALLED_APPS`` in your
       Django project' :file:`settings.py`::
    
            INSTALLED_APPS = (
                ...,
                'django_celery_beat',
            )
    
       Note that there is no dash in the module name, only underscores.
    
    #. Apply Django database migrations so that the necessary tables are created:
    
       .. code-block:: console
       
           $ python manage.py migrate
    
    #. Start the :program:`celery beat` service using the ``django_celery_beat.schedulers:DatabaseScheduler`` scheduler:
    
       .. code-block:: console
    
           $ celery -A proj beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
    
       Note:  You may also add this as the :setting:`beat_scheduler` setting directly.
    
    #. Visit the Django-Admin interface to set up some periodic tasks.
