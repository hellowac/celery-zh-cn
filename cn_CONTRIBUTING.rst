.. _contributing:

==============
贡献
==============

Contributing

.. tab:: 中文

    欢迎！

    本文档内容相当详尽，但对于一些小型贡献，你其实无需深入阅读全部内容；

        最重要的规则是：贡献应该是轻松的，
        社区应当友好，且不应在细枝末节上吹毛求疵，
        比如代码风格问题。

    如果你要报告一个 bug，请阅读下方的 “报告 Bug” 一节，以确保你的报告中包含足够的信息，以便我们能成功诊断问题；
    如果你要贡献代码，建议你尽量遵循你所修改代码周围已有的编码习惯，
    但最终，合并变更的人会清理所有补丁内容，因此不必过于担心细节。

.. tab:: 英文

    Welcome!

    This document is fairly extensive and you aren't really expected
    to study this in detail for small contributions;

        The most important rule is that contributing must be easy
        and that the community is friendly and not nitpicking on details,
        such as coding style.

    If you're reporting a bug you should read the Reporting bugs section
    below to ensure that your bug report contains enough information
    to successfully diagnose the issue, and if you're contributing code
    you should try to mimic the conventions you see surrounding the code
    you're working on, but in the end all patches will be cleaned up by
    the person merging the changes so don't worry too much.

.. _community-code-of-conduct:

社区行为准则
=========================

Community Code of Conduct

.. tab:: 中文

    我们的目标是维护一个对所有人都友好和谐的多元社区。
    因此，我们非常希望所有参与社区建设和互动的人都能遵守这份《行为准则》。

    《行为准则》适用于我们作为社区成员的各种行为，包括但不限于论坛、邮件列表、Wiki、网站、IRC 聊天、公开会议或私下通信等场合。

    本《行为准则》大量参考了 `Ubuntu Code of Conduct`_ 和 `Pylons Code of Conduct`_。

.. tab:: 英文

    The goal is to maintain a diverse community that's pleasant for everyone.
    That's why we would greatly appreciate it if everyone contributing to and
    interacting with the community also followed this Code of Conduct.

    The Code of Conduct covers our behavior as members of the community,
    in any forum, mailing list, wiki, website, Internet relay chat (IRC), public
    meeting or private correspondence.

    The Code of Conduct is heavily based on the `Ubuntu Code of Conduct`_, and
    the `Pylons Code of Conduct`_.

.. _`Ubuntu Code of Conduct`: https://www.ubuntu.com/community/conduct
.. _`Pylons Code of Conduct`: https://pylonsproject.org/community-code-of-conduct.html

体谅他人
--------------

Be considerate

.. tab:: 中文

    你的工作将被他人使用，同时你也将依赖他人的工作。
    你所做的每个决策都会影响用户和同事，因此我们希望你在做决定时能考虑其后果。
    即使后果在当下并不明显，我们对 Celery 的贡献都可能影响他人的工作。
    例如，在发布过程中对代码、基础设施、策略、文档或翻译的更改，都有可能对他人的工作造成负面影响。

.. tab:: 英文

    Your work will be used by other people, and you in turn will depend on the
    work of others. Any decision you take will affect users and colleagues, and
    we expect you to take those consequences into account when making decisions.
    Even if it's not obvious at the time, our contributions to Celery will impact
    the work of others. For example, changes to code, infrastructure, policy,
    documentation and translations during a release may negatively impact
    others' work.

尊重他人
-------------

Be respectful

.. tab:: 中文

    Celery 社区及其成员彼此尊重。
    每个人都可以为 Celery 做出有价值的贡献。
    我们可能意见不合，但这并不构成表现不当或缺乏礼貌的理由。
    我们都可能偶尔感到沮丧，但不能让这种情绪演变成对他人的人身攻击。
    必须牢记，一个让人感到不适或受到威胁的社区是缺乏生产力的。
    我们希望 Celery 社区的成员在与其他贡献者、项目外部人士以及 Celery 用户打交道时，都能保持尊重。

.. tab:: 英文

    The Celery community and its members treat one another with respect. Everyone
    can make a valuable contribution to Celery. We may not always agree, but
    disagreement is no excuse for poor behavior and poor manners. We might all
    experience some frustration now and then, but we cannot allow that frustration
    to turn into a personal attack. It's important to remember that a community
    where people feel uncomfortable or threatened isn't a productive one. We
    expect members of the Celery community to be respectful when dealing with
    other contributors as well as with people outside the Celery project and with
    users of Celery.

合作共事
----------------

Be collaborative

.. tab:: 中文

    协作是 Celery 和整个自由软件社区的核心。
    我们应始终对协作持开放态度。
    你的工作应该是透明进行的，并且补丁应当在完成时及时回馈给社区，而不是等到发布版本才公布。
    如果你希望为上游已有项目开发新功能，至少应让该项目了解你的想法与进展。
    你未必能从上游或你的同事那里获得一致意见或认可，因此也无需在开始前强求达成一致，
    但至少要让外部世界知道你在做什么，并以允许外部人员测试、讨论和参与的方式发布你的成果。

.. tab:: 英文

    Collaboration is central to Celery and to the larger free software community.
    We should always be open to collaboration. Your work should be done
    transparently and patches from Celery should be given back to the community
    when they're made, not just when the distribution releases. If you wish
    to work on new code for existing upstream projects, at least keep those
    projects informed of your ideas and progress. It many not be possible to
    get consensus from upstream, or even from your colleagues about the correct
    implementation for an idea, so don't feel obliged to have that agreement
    before you begin, but at least keep the outside world informed of your work,
    and publish your work in a way that allows outsiders to test, discuss, and
    contribute to your efforts.

意见不合时，请咨询他人
---------------------------------

When you disagree, consult others

.. tab:: 中文

    分歧——无论是政治上的还是技术上的——都时常发生，Celery 社区也不例外。
    我们认为，应通过社区及其流程以建设性的方式解决分歧与意见不合。
    如果你确实想要另辟蹊径，我们鼓励你基于 Celery 所做的工作，
    创建一个衍生发行版或替代性的软件包集合，同时尽可能复用通用核心。

.. tab:: 英文

    Disagreements, both political and technical, happen all the time and
    the Celery community is no exception. It's important that we resolve
    disagreements and differing views constructively and with the help of the
    community and community process. If you really want to go a different
    way, then we encourage you to make a derivative distribution or alternate
    set of packages that still build on the work we've done to utilize as common
    of a core as possible.

不确定时，请寻求帮助
--------------------------------

When you're unsure, ask for help

.. tab:: 中文

    没人知道所有的事情，也没有人被期望做到完美。提问可以避免许多后续的问题，因此我们鼓励提问。被提问的人应当给予回应和帮助。然而，提问时也应注意选择合适的交流渠道。

.. tab:: 英文

    Nobody knows everything, and nobody is expected to be perfect. Asking
    questions avoids many problems down the road, and so questions are
    encouraged. Those who are asked questions should be responsive and helpful.
    However, when asking a question, care must be taken to do so in an appropriate
    forum.

谨慎行事
-----------------------

Step down considerately

.. tab:: 中文

    每个项目的开发者都可能来来去去，Celery 也不例外。当你离开项目或部分地停止参与时，我们希望你能以最小化项目干扰的方式进行。这意味着你应当告知他人你将退出，并采取适当措施，确保他人可以在你离开后接续你的工作。

.. tab:: 英文

    Developers on every project come and go and Celery is no different. When you
    leave or disengage from the project, in whole or in part, we ask that you do
    so in a way that minimizes disruption to the project. This means you should
    tell people you're leaving and take the proper steps to ensure that others
    can pick up where you left off.

.. _reporting-bugs:


报告错误
==============

Reporting Bugs

.. _vulnsec:

安全
--------

Security

.. tab:: 中文

    你 **绝不能** 将涉及安全的问题、漏洞或包含敏感信息的错误报告到 Bug 追踪器或其他公共平台。此类敏感 Bug 应通过电子邮件发送至 ``security@celeryproject.org``。

    如果你希望加密发送信息，我们的 PGP 公钥如下::

        -----BEGIN PGP PUBLIC KEY BLOCK-----
        Version: GnuPG v1.4.15 (Darwin)

        mQENBFJpWDkBCADFIc9/Fpgse4owLNvsTC7GYfnJL19XO0hnL99sPx+DPbfr+cSE
        9wiU+Wp2TfUX7pCLEGrODiEP6ZCZbgtiPgId+JYvMxpP6GXbjiIlHRw1EQNH8RlX
        cVxy3rQfVv8PGGiJuyBBjxzvETHW25htVAZ5TI1+CkxmuyyEYqgZN2fNd0wEU19D
        +c10G1gSECbCQTCbacLSzdpngAt1Gkrc96r7wGHBBSvDaGDD2pFSkVuTLMbIRrVp
        lnKOPMsUijiip2EMr2DvfuXiUIUvaqInTPNWkDynLoh69ib5xC19CSVLONjkKBsr
        Pe+qAY29liBatatpXsydY7GIUzyBT3MzgMJlABEBAAG0MUNlbGVyeSBTZWN1cml0
        eSBUZWFtIDxzZWN1cml0eUBjZWxlcnlwcm9qZWN0Lm9yZz6JATgEEwECACIFAlJp
        WDkCGwMGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEOArFOUDCicIw1IH/26f
        CViDC7/P13jr+srRdjAsWvQztia9HmTlY8cUnbmkR9w6b6j3F2ayw8VhkyFWgYEJ
        wtPBv8mHKADiVSFARS+0yGsfCkia5wDSQuIv6XqRlIrXUyqJbmF4NUFTyCZYoh+C
        ZiQpN9xGhFPr5QDlMx2izWg1rvWlG1jY2Es1v/xED3AeCOB1eUGvRe/uJHKjGv7J
        rj0pFcptZX+WDF22AN235WYwgJM6TrNfSu8sv8vNAQOVnsKcgsqhuwomSGsOfMQj
        LFzIn95MKBBU1G5wOs7JtwiV9jefGqJGBO2FAvOVbvPdK/saSnB+7K36dQcIHqms
        5hU4Xj0RIJiod5idlRC5AQ0EUmlYOQEIAJs8OwHMkrdcvy9kk2HBVbdqhgAREMKy
        gmphDp7prRL9FqSY/dKpCbG0u82zyJypdb7QiaQ5pfPzPpQcd2dIcohkkh7G3E+e
        hS2L9AXHpwR26/PzMBXyr2iNnNc4vTksHvGVDxzFnRpka6vbI/hrrZmYNYh9EAiv
        uhE54b3/XhXwFgHjZXb9i8hgJ3nsO0pRwvUAM1bRGMbvf8e9F+kqgV0yWYNnh6QL
        4Vpl1+epqp2RKPHyNQftbQyrAHXT9kQF9pPlx013MKYaFTADscuAp4T3dy7xmiwS
        crqMbZLzfrxfFOsNxTUGE5vmJCcm+mybAtRo4aV6ACohAO9NevMx8pUAEQEAAYkB
        HwQYAQIACQUCUmlYOQIbDAAKCRDgKxTlAwonCNFbB/9esir/f7TufE+isNqErzR/
        aZKZo2WzZR9c75kbqo6J6DYuUHe6xI0OZ2qZ60iABDEZAiNXGulysFLCiPdatQ8x
        8zt3DF9BMkEck54ZvAjpNSern6zfZb1jPYWZq3TKxlTs/GuCgBAuV4i5vDTZ7xK/
        aF+OFY5zN7ciZHkqLgMiTZ+RhqRcK6FhVBP/Y7d9NlBOcDBTxxE1ZO1ute6n7guJ
        ciw4hfoRk8qNN19szZuq3UU64zpkM2sBsIFM9tGF2FADRxiOaOWZHmIyVZriPFqW
        RUwjSjs7jBVNq0Vy4fCu/5+e+XLOUBOoqtM5W7ELt0t1w9tXebtPEetV86in8fU2
        =0chn
        -----END PGP PUBLIC KEY BLOCK-----

.. tab:: 英文

    You must never report security related issues, vulnerabilities or bugs
    including sensitive information to the bug tracker, or elsewhere in public.
    Instead sensitive bugs must be sent by email to ``security@celeryproject.org``.

    If you'd like to submit the information encrypted our PGP key is::

        -----BEGIN PGP PUBLIC KEY BLOCK-----
        Version: GnuPG v1.4.15 (Darwin)

        mQENBFJpWDkBCADFIc9/Fpgse4owLNvsTC7GYfnJL19XO0hnL99sPx+DPbfr+cSE
        9wiU+Wp2TfUX7pCLEGrODiEP6ZCZbgtiPgId+JYvMxpP6GXbjiIlHRw1EQNH8RlX
        cVxy3rQfVv8PGGiJuyBBjxzvETHW25htVAZ5TI1+CkxmuyyEYqgZN2fNd0wEU19D
        +c10G1gSECbCQTCbacLSzdpngAt1Gkrc96r7wGHBBSvDaGDD2pFSkVuTLMbIRrVp
        lnKOPMsUijiip2EMr2DvfuXiUIUvaqInTPNWkDynLoh69ib5xC19CSVLONjkKBsr
        Pe+qAY29liBatatpXsydY7GIUzyBT3MzgMJlABEBAAG0MUNlbGVyeSBTZWN1cml0
        eSBUZWFtIDxzZWN1cml0eUBjZWxlcnlwcm9qZWN0Lm9yZz6JATgEEwECACIFAlJp
        WDkCGwMGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEOArFOUDCicIw1IH/26f
        CViDC7/P13jr+srRdjAsWvQztia9HmTlY8cUnbmkR9w6b6j3F2ayw8VhkyFWgYEJ
        wtPBv8mHKADiVSFARS+0yGsfCkia5wDSQuIv6XqRlIrXUyqJbmF4NUFTyCZYoh+C
        ZiQpN9xGhFPr5QDlMx2izWg1rvWlG1jY2Es1v/xED3AeCOB1eUGvRe/uJHKjGv7J
        rj0pFcptZX+WDF22AN235WYwgJM6TrNfSu8sv8vNAQOVnsKcgsqhuwomSGsOfMQj
        LFzIn95MKBBU1G5wOs7JtwiV9jefGqJGBO2FAvOVbvPdK/saSnB+7K36dQcIHqms
        5hU4Xj0RIJiod5idlRC5AQ0EUmlYOQEIAJs8OwHMkrdcvy9kk2HBVbdqhgAREMKy
        gmphDp7prRL9FqSY/dKpCbG0u82zyJypdb7QiaQ5pfPzPpQcd2dIcohkkh7G3E+e
        hS2L9AXHpwR26/PzMBXyr2iNnNc4vTksHvGVDxzFnRpka6vbI/hrrZmYNYh9EAiv
        uhE54b3/XhXwFgHjZXb9i8hgJ3nsO0pRwvUAM1bRGMbvf8e9F+kqgV0yWYNnh6QL
        4Vpl1+epqp2RKPHyNQftbQyrAHXT9kQF9pPlx013MKYaFTADscuAp4T3dy7xmiwS
        crqMbZLzfrxfFOsNxTUGE5vmJCcm+mybAtRo4aV6ACohAO9NevMx8pUAEQEAAYkB
        HwQYAQIACQUCUmlYOQIbDAAKCRDgKxTlAwonCNFbB/9esir/f7TufE+isNqErzR/
        aZKZo2WzZR9c75kbqo6J6DYuUHe6xI0OZ2qZ60iABDEZAiNXGulysFLCiPdatQ8x
        8zt3DF9BMkEck54ZvAjpNSern6zfZb1jPYWZq3TKxlTs/GuCgBAuV4i5vDTZ7xK/
        aF+OFY5zN7ciZHkqLgMiTZ+RhqRcK6FhVBP/Y7d9NlBOcDBTxxE1ZO1ute6n7guJ
        ciw4hfoRk8qNN19szZuq3UU64zpkM2sBsIFM9tGF2FADRxiOaOWZHmIyVZriPFqW
        RUwjSjs7jBVNq0Vy4fCu/5+e+XLOUBOoqtM5W7ELt0t1w9tXebtPEetV86in8fU2
        =0chn
        -----END PGP PUBLIC KEY BLOCK-----

其他错误
----------

Other bugs

.. tab:: 中文

    你也可以在 :ref:`mailing-list` 中描述 Bug，但确保及时回应和跟进的最佳方式是使用问题追踪器。

    1) **创建 GitHub 账号**

    你需要 `创建一个 GitHub 账号`_ 才能创建新的 Issue 并参与讨论。

    2) **确认你报告的问题确实是 Bug**

    如果你是请求支持，而不是报告 Bug，请使用 :ref:`mailing-list` 或 :ref:`irc-channel`。如果你仍然需要通过 GitHub 提问，请在标题前加上 ``[QUESTION]``。

    3) **确保该 Bug 尚未被报告过**

    请在相关 Issue 追踪器中搜索是否已有类似问题，如果找到，请确认是否可以提供更多新信息来帮助开发者修复该问题。

    4) **检查你是否使用的是最新版本**

    有些 Bug 可能已在后续修复中被解决，但没有被单独报告。请确保你使用的是 celery、billiard、kombu、amqp 和 vine 的最新版本。

    5) **收集与 Bug 相关的信息**

    为了尽可能高效地重现问题，我们需要完整的触发条件。大多数情况下是 Python 的回溯信息，但也可能是设计、拼写或网站/文档/代码中的其他错误。

        A) 如果是 Python 异常，请将回溯信息包含在报告中。

        B) 我们还需要知道你所使用的平台（Windows、macOS、Linux 等）、Python 解释器的版本、Celery 及其依赖包的版本。

        C) 如果你报告的是竞争条件或死锁，这类错误的回溯信息可能难以获取，或没有帮助。请尽可能收集进程诊断信息。例如：

        * 启用 Celery 的 :ref:`breakpoint signal <breakpoint_signal>`，用于检查进程状态，并打开 :mod:`pdb` 会话。
        * 使用如下工具收集追踪信息： `strace`_ （Linux）、 :command:`dtruss`（macOS）、 :command:`ktrace` （BSD）、 `ltrace`_、 `lsof`_。

        D) 包含 :command:`celery report` 命令的输出：

            .. code-block:: console

                $ celery -A proj report

            这将包括你的配置设定，并尝试清除已知敏感键的值。但请在提交前确认这些信息不包含如 API Token 和认证凭据等机密信息。

        E) 你的 Issue 可能会被标记为 `Needs Test Case`。测试用例代表复现问题所需的所有信息，可能是最小复现代码或完整的复现步骤和配置参数。

    6) **提交 Bug**

    默认情况下，`GitHub`_ 会在你的 Bug 有新评论时通过邮件通知你。如果你关闭了这个功能，请记得定期查看 Issue，以免错过开发者可能提出的问题。


.. tab:: 英文

    Bugs can always be described to the :ref:`mailing-list`, but the best
    way to report an issue and to ensure a timely response is to use the
    issue tracker.

    1) **Create a GitHub account**.

    You need to `create a GitHub account`_ to be able to create new issues
    and participate in the discussion.

    2) **Determine if your bug is really a bug**.

    You shouldn't file a bug if you're requesting support. For that you can use
    the :ref:`mailing-list`, or :ref:`irc-channel`. If you still need support
    you can open a github issue, please prepend the title with ``[QUESTION]``.

    3) **Make sure your bug hasn't already been reported**.

    Search through the appropriate Issue tracker. If a bug like yours was found,
    check if you have new information that could be reported to help
    the developers fix the bug.

    4) **Check if you're using the latest version**.

    A bug could be fixed by some other improvements and fixes - it might not have an
    existing report in the bug tracker. Make sure you're using the latest releases of
    celery, billiard, kombu, amqp, and vine.

    5) **Collect information about the bug**.

    To have the best chance of having a bug fixed, we need to be able to easily
    reproduce the conditions that caused it. Most of the time this information
    will be from a Python traceback message, though some bugs might be in design,
    spelling or other errors on the website/docs/code.

        A) If the error is from a Python traceback, include it in the bug report.

        B) We also need to know what platform you're running (Windows, macOS, Linux,
        etc.), the version of your Python interpreter, and the version of Celery,
        and related packages that you were running when the bug occurred.

        C) If you're reporting a race condition or a deadlock, tracebacks can be
        hard to get or might not be that useful. Try to inspect the process to
        get more diagnostic data. Some ideas:

        * Enable Celery's :ref:`breakpoint signal <breakpoint_signal>` and use it
            to inspect the process's state. This will allow you to open a
            :mod:`pdb` session.
        * Collect tracing data using `strace`_(Linux),
            :command:`dtruss` (macOS), and :command:`ktrace` (BSD),
            `ltrace`_, and `lsof`_.

        D) Include the output from the :command:`celery report` command:

            .. code-block:: console

                $ celery -A proj report

            This will also include your configuration settings and it will try to
            remove values for keys known to be sensitive, but make sure you also
            verify the information before submitting so that it doesn't contain
            confidential information like API tokens and authentication
            credentials.

        E) Your issue might be tagged as `Needs Test Case`. A test case represents
        all the details needed to reproduce what your issue is reporting.
        A test case can be some minimal code that reproduces the issue or
        detailed instructions and configuration values that reproduces
        said issue.

    6) **Submit the bug**.

    By default `GitHub`_ will email you to let you know when new comments have
    been made on your bug. In the event you've turned this feature off, you
    should check back on occasion to ensure you don't miss any questions a
    developer trying to fix the bug might ask.

.. _`创建一个 GitHub 账号`: https://github.com/signup/free

.. _`create a GitHub account`: https://github.com/signup/free

.. _`GitHub`: https://github.com
.. _`strace`: https://en.wikipedia.org/wiki/Strace
.. _`ltrace`: https://en.wikipedia.org/wiki/Ltrace
.. _`lsof`: https://en.wikipedia.org/wiki/Lsof

.. _issue-trackers:

问题跟踪器
--------------

Issue Trackers

.. tab:: 中文

    Celery 生态系统中的软件包如果出现错误，应将其报告到相应的问题跟踪器。

    * :pypi:`celery`: https://github.com/celery/celery/issues/
    * :pypi:`kombu`: https://github.com/celery/kombu/issues
    * :pypi:`amqp`: https://github.com/celery/py-amqp/issues
    * :pypi:`vine`: https://github.com/celery/vine/issues
    * :pypi:`pytest-celery`: https://github.com/celery/pytest-celery/issues
    * :pypi:`librabbitmq`: https://github.com/celery/librabbitmq/issues
    * :pypi:`django-celery-beat`: https://github.com/celery/django-celery-beat/issues
    * :pypi:`django-celery-results`: https://github.com/celery/django-celery-results/issues

    如果你不确定错误的来源，可以在 :ref:`mailing-list` 上提问，或者直接使用 Celery 的问题跟踪器。

.. tab:: 英文

    Bugs for a package in the Celery ecosystem should be reported to the relevant
    issue tracker.

    * :pypi:`celery`: https://github.com/celery/celery/issues/
    * :pypi:`kombu`: https://github.com/celery/kombu/issues
    * :pypi:`amqp`: https://github.com/celery/py-amqp/issues
    * :pypi:`vine`: https://github.com/celery/vine/issues
    * :pypi:`pytest-celery`: https://github.com/celery/pytest-celery/issues
    * :pypi:`librabbitmq`: https://github.com/celery/librabbitmq/issues
    * :pypi:`django-celery-beat`: https://github.com/celery/django-celery-beat/issues
    * :pypi:`django-celery-results`: https://github.com/celery/django-celery-results/issues

    If you're unsure of the origin of the bug you can ask the
    :ref:`mailing-list`, or just use the Celery issue tracker.

代码库贡献者指南
===================================

Contributors guide to the code base

.. tab:: 中文

    另有一个专门部分介绍内部实现细节，
    包括代码库细节和编码风格指南。

    阅读 :ref:`internals-guide` 获取更多信息！

.. tab:: 英文

    There's a separate section for internal details,
    including details about the code base and a style guide.

    Read :ref:`internals-guide` for more!

.. _versions:

版本
========

Versions

.. tab:: 中文

    版本号由主版本号、次版本号和发行号组成。
    自 2.1.0 版本以来，我们采用 SemVer 所描述的版本语义：
    http://semver.org。

    稳定版本会发布到 PyPI，
    而开发版本仅作为 GitHub 上的标签存在于 git 仓库中。
    所有版本标签都以 "v" 开头，例如版本 0.8.0 的标签是 v0.8.0。

.. tab:: 英文

    Version numbers consists of a major version, minor version and a release number.
    Since version 2.1.0 we use the versioning semantics described by
    SemVer: http://semver.org.

    Stable releases are published at PyPI
    while development releases are only available in the GitHub git repository as tags.
    All version tags starts with “v”, so version 0.8.0 has the tag v0.8.0.

.. _git-branches:

分支
========

Branches

.. tab:: 中文

    当前活跃的版本分支有：

    * dev（Git 称其为 "main"）(https://github.com/celery/celery/tree/main)
    * 4.5 (https://github.com/celery/celery/tree/v4.5)
    * 3.1 (https://github.com/celery/celery/tree/3.1)

    你可以通过查看 Changelog 来了解任意分支的状态：

        https://github.com/celery/celery/blob/main/Changelog.rst

    如果某个分支处于活跃开发中，其顶部的版本信息应包含如下元数据：

    .. code-block:: restructuredtext

        4.3.0
        ======
        :release-date: TBA
        :status: DEVELOPMENT
        :branch: dev (git calls this main)

    ``status`` 字段可以是以下几种之一：

    * ``PLANNING``
        分支当前处于实验性阶段，正在规划中。

    * ``DEVELOPMENT``
        分支处于活跃开发中，但测试套件应当能够通过，产品应可正常运行，供用户测试。

    * ``FROZEN``
        分支已被冻结，不再接受新特性。
        当分支冻结后，开发重点转向对该版本的尽可能多的测试，以准备发布。

.. tab:: 英文

    Current active version branches:

    * dev (which git calls "main") (https://github.com/celery/celery/tree/main)
    * 4.5 (https://github.com/celery/celery/tree/v4.5)
    * 3.1 (https://github.com/celery/celery/tree/3.1)

    You can see the state of any branch by looking at the Changelog:

        https://github.com/celery/celery/blob/main/Changelog.rst

    If the branch is in active development the topmost version info should
    contain meta-data like:

    .. code-block:: restructuredtext

        4.3.0
        ======
        :release-date: TBA
        :status: DEVELOPMENT
        :branch: dev (git calls this main)

    The ``status`` field can be one of:

    * ``PLANNING``
        The branch is currently experimental and in the planning stage.

    * ``DEVELOPMENT``
        The branch is in active development, but the test suite should
        be passing and the product should be working and possible for users to test.

    * ``FROZEN``
        The branch is frozen, and no more features will be accepted.
        When a branch is frozen the focus is on testing the version as much
        as possible before it is released.

开发分支
----------

dev branch

.. tab:: 中文

    dev 分支（Git 称其为 "main"）是用于开发下一个版本的主干分支。

.. tab:: 英文

    The dev branch (called "main" by git), is where development of the next
    version happens.

维护分支
--------------------

Maintenance branches

.. tab:: 中文

    维护分支根据版本命名 —— 例如，
    2.2.x 系列的维护分支命名为 ``2.2``。

    此前这些分支的命名方式为 ``releaseXX-maint``。

    当前我们维护的版本如下：

    * 4.2

      当前主力系列。

    * 4.1

      停止对 Python 2.6 的支持。新增对 Python 3.4、3.5 和 3.6 的支持。

    * 3.1

      官方支持 Python 2.6、2.7 和 3.3，同时也支持 PyPy。

.. tab:: 英文

    Maintenance branches are named after the version -- for example,
    the maintenance branch for the 2.2.x series is named ``2.2``.
    
    Previously these were named ``releaseXX-maint``.
    
    The versions we currently maintain is:
    
    * 4.2
    
      This is the current series.
    
    * 4.1
    
      Drop support for python 2.6. Add support for python 3.4, 3.5 and 3.6.
    
    * 3.1
    
      Official support for python 2.6, 2.7 and 3.3, and also supported on PyPy.

已归档分支
-----------------

Archived branches

.. tab:: 中文

    归档分支仅用于保留历史记录，
    理论上如果有人依赖已不再官方支持的系列，也可以为这些分支提交补丁。

    归档版本的命名格式为 ``X.Y-archived``。

    为了保持更简洁的提交历史并放弃兼容性以继续改进项目，
    我们 **当前没有任何归档版本**。

.. tab:: 英文

    Archived branches are kept for preserving history only,
    and theoretically someone could provide patches for these if they depend
    on a series that's no longer officially supported.

    An archived version is named ``X.Y-archived``.

    To maintain a cleaner history and drop compatibility to continue improving
    the project, we **do not have any archived version** right now.

功能分支
----------------

Feature branches

.. tab:: 中文

    重大新特性会在专门的分支中开发。
    这些分支的命名没有严格要求。

    特性分支在合并到发行分支后会被删除。

.. tab:: 英文

    Major new features are worked on in dedicated branches.
    There's no strict naming requirement for these branches.

    Feature branches are removed once they've been merged into a release branch.

标签
====

Tags

.. tab:: 中文

    - 标签专门用于标记发行版本。一个发布标签的命名格式为 ``vX.Y.Z`` —— 例如 ``v2.3.1``。

    - 实验性版本会包含额外的标识符 ``vX.Y.Z-id`` —— 例如 ``v3.0.0-rc1``。

    - 实验性标签可能会在正式版本发布后被移除。

.. tab:: 英文

    - Tags are used exclusively for tagging releases. A release tag is
      named with the format ``vX.Y.Z`` -- for example ``v2.3.1``.

    - Experimental releases contain an additional identifier ``vX.Y.Z-id`` --
      for example ``v3.0.0-rc1``.

    - Experimental tags may be removed after the official release.

.. _contributing-changes:

功能和补丁开发
=============================

Working on Features & Patches

.. tab:: 中文

    .. note::

        为 Celery 做贡献应当尽可能简单，
        所以这些步骤都不是强制性的。

        如果你更喜欢通过电子邮件提交补丁，我们也完全支持。
        我们不会因此对你另眼相看，任何贡献我们都感激不尽！

        不过，遵循这些流程可以让维护者的工作更轻松，
        也可能让你的改动更快被接纳。

.. tab:: 英文

    .. note::

        Contributing to Celery should be as simple as possible,
        so none of these steps should be considered mandatory.

        You can even send in patches by email if that's your preferred
        work method. We won't like you any less, any contribution you make
        is always appreciated!

        However, following these steps may make maintainer's life easier,
        and may mean that your changes will be accepted sooner.

分叉和设置代码库
-------------------------------------

Forking and setting up the repository

.. tab:: 中文

    首先你需要 fork Celery 的代码仓库；GitHub 指南中有一篇很好的入门教程：`Fork a Repo`_。

    在克隆仓库之后，你应该将代码检出到本地目录：

    .. code-block:: console

        $ git clone git@github.com:username/celery.git

    仓库克隆完成后，进入该目录并设置对上游仓库的便捷访问：

    .. code-block:: console

        $ cd celery
        $ git remote add upstream git@github.com:celery/celery.git
        $ git fetch upstream

    如果你需要从上游拉取更新，请始终使用 ``--rebase`` 选项执行 ``git pull``：

    .. code-block:: console

        git pull --rebase upstream main

    使用该选项可以避免在提交历史中添加多余的合并记录。
    参见 `Rebasing merge commits in git`_。
    如想了解更多有关 rebase 的内容，请阅读 GitHub 指南中的 `Rebase`_ 部分。

    如果你需要切换到 Git 默认 ``main`` 之外的其他分支，可以通过如下方式获取并检出远程分支::

        git checkout --track -b 5.0-devel upstream/5.0-devel

    **注意：** 任何特性分支或修复分支都应从 ``upstream/main`` 创建。


.. tab:: 英文

    First you need to fork the Celery repository; a good introduction to this
    is in the GitHub Guide: `Fork a Repo`_.

    After you have cloned the repository, you should checkout your copy
    to a directory on your machine:

    .. code-block:: console

        $ git clone git@github.com:username/celery.git

    When the repository is cloned, enter the directory to set up easy access
    to upstream changes:

    .. code-block:: console

        $ cd celery
        $ git remote add upstream git@github.com:celery/celery.git
        $ git fetch upstream

    If you need to pull in new changes from upstream you should
    always use the ``--rebase`` option to ``git pull``:

    .. code-block:: console

        git pull --rebase upstream main

    With this option, you don't clutter the history with merging
    commit notes. See `Rebasing merge commits in git`_.
    If you want to learn more about rebasing, see the `Rebase`_
    section in the GitHub guides.

    If you need to work on a different branch than the one git calls ``main``, you can
    fetch and checkout a remote branch like this::

        git checkout --track -b 5.0-devel upstream/5.0-devel

    **Note:** Any feature or fix branch should be created from ``upstream/main``.

.. _`Fork a Repo`: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo
.. _`Rebasing merge commits in git`:
    https://web.archive.org/web/20150627054345/http://marketblog.envato.com/general/rebasing-merge-commits-in-git/
.. _`Rebase`: https://docs.github.com/en/get-started/using-git/about-git-rebase

.. _contributing-docker-development:

使用 Docker 进行开发和测试
----------------------------------

Developing and Testing with Docker

.. tab:: 中文

    由于 Celery 包含多个组件，如 broker 和 backend，
    可以使用 `Docker`_ 和 `docker-compose`_ 来极大地简化开发与测试流程。
    这里的 Docker 配置要求至少使用 Docker 版本 17.13.0 和 `docker-compose` 1.13.0 以上版本。

    Docker 相关组件位于 :file:`docker/` 目录中，可以使用以下命令构建 Docker 镜像：

    .. code-block:: console

        $ docker compose build celery

    并通过以下命令运行：

    .. code-block:: console

        $ docker compose run --rm celery <command>

    其中 <command> 是要在 Docker 容器中执行的命令。`--rm` 参数表示容器在退出后将被自动删除，
    这有助于防止不必要的容器堆积。

    一些有用的命令如下：

    * ``bash``
        进入容器内的交互式 shell 环境

    * ``make test``
        运行测试套件。
        **注意：** 默认将使用 Python 3.12 运行测试。

    * ``tox``
        使用 tox 在多个配置下运行测试。
        **注意：** 此命令会运行 :file:`tox.ini` 中定义的所有环境下的测试，耗时较长。

    * ``pyenv exec python{3.8,3.9,3.10,3.11,3.12} -m pytest t/unit``
        使用 pytest 运行单元测试。

        **注意：** ``{3.8,3.9,3.10,3.11,3.12}`` 表示你可以使用这些版本中的任意一个。
        例如：``pyenv exec python3.12 -m pytest t/unit``

    * ``pyenv exec python{3.8,3.9,3.10,3.11,3.12} -m pytest t/integration``
        使用 pytest 运行集成测试。

        **注意：** ``{3.8,3.9,3.10,3.11,3.12}`` 表示你可以使用这些版本中的任意一个。
        例如：``pyenv exec python3.12 -m pytest t/unit``

    默认情况下，docker-compose 会将 Celery 和测试目录挂载到 Docker 容器中，
    这样可以在容器内实时看到代码修改和测试结果。
    broker 与 backend 等环境变量也在 :file:`docker/docker-compose.yml` 文件中定义。

    运行 ``docker compose build celery`` 命令后，将构建出一个名为 ``celery/celery:dev`` 的镜像。
    该镜像已安装所有开发所需依赖，并使用 ``pyenv`` 安装了多个 Python 版本，
    支持 Python 3.8、3.9、3.10、3.11 和 3.12。
    默认的 Python 版本为 3.12。

    :file:`docker-compose.yml` 文件定义了运行集成测试所需的环境变量。
    ``celery`` 服务还会挂载代码库，并将 ``PYTHONPATH`` 环境变量设置为 ``/home/developer/celery``。
    通过设置 ``PYTHONPATH``，该服务允许将挂载的代码库作为全局模块供开发使用。
    你也可以使用 ``python -m pip install -e .`` 命令以开发模式安装代码。

    如果你希望运行一个 Django 或独立项目以手动测试或调试某个功能，
    可以使用 `docker compose` 构建出的镜像并挂载你的自定义代码。
    以下是一个示例：

    假设目录结构如下：

    .. code-block:: console

        + celery_project
        + celery # 仓库克隆在此处
        + my_project
            - manage.py
            + my_project
            - views.py

    .. code-block:: yaml

        version: "3"

        services:
            celery:
                image: celery/celery:dev
                environment:
                    TEST_BROKER: amqp://rabbit:5672
                    TEST_BACKEND: redis://redis
                volumes:
                    - ../../celery:/home/developer/celery
                    - ../my_project:/home/developer/my_project
                depends_on:
                    - rabbit
                    - redis
            rabbit:
                image: rabbitmq:latest
            redis:
                image: redis:latest

    在上述示例中，我们使用的是通过当前仓库构建的镜像，并同时挂载了 celery 源码与自定义项目代码。


.. tab:: 英文

    Because of the many components of Celery, such as a broker and backend,
    `Docker`_ and `docker-compose`_ can be utilized to greatly simplify the
    development and testing cycle. The Docker configuration here requires a
    Docker version of at least 17.13.0 and `docker-compose` 1.13.0+.

    The Docker components can be found within the :file:`docker/` folder and the
    Docker image can be built via:

    .. code-block:: console

        $ docker compose build celery

    and run via:

    .. code-block:: console

        $ docker compose run --rm celery <command>

    where <command> is a command to execute in a Docker container. The `--rm` flag
    indicates that the container should be removed after it is exited and is useful
    to prevent accumulation of unwanted containers.

    Some useful commands to run:

    * ``bash``
        To enter the Docker container like a normal shell

    * ``make test``
        To run the test suite.
        **Note:** This will run tests using python 3.12 by default.

    * ``tox``
        To run tox and test against a variety of configurations.
        **Note:** This command will run tests for every environment defined in :file:`tox.ini`.
        It takes a while.

    * ``pyenv exec python{3.8,3.9,3.10,3.11,3.12} -m pytest t/unit``
        To run unit tests using pytest.

        **Note:** ``{3.8,3.9,3.10,3.11,3.12}`` means you can use any of those options.
        e.g. ``pyenv exec python3.12 -m pytest t/unit``

    * ``pyenv exec python{3.8,3.9,3.10,3.11,3.12} -m pytest t/integration``
        To run integration tests using pytest

        **Note:** ``{3.8,3.9,3.10,3.11,3.12}`` means you can use any of those options.
        e.g. ``pyenv exec python3.12 -m pytest t/unit``

    By default, docker-compose will mount the Celery and test folders in the Docker
    container, allowing code changes and testing to be immediately visible inside
    the Docker container. Environment variables, such as the broker and backend to
    use are also defined in the :file:`docker/docker-compose.yml` file.

    By running ``docker compose build celery`` an image will be created with the
    name ``celery/celery:dev``. This docker image has every dependency needed
    for development installed. ``pyenv`` is used to install multiple python
    versions, the docker image offers python 3.8, 3.9, 3.10, 3.11 and 3.12.
    The default python version is set to 3.12.

    The :file:`docker-compose.yml` file defines the necessary environment variables
    to run integration tests. The ``celery`` service also mounts the codebase
    and sets the ``PYTHONPATH`` environment variable to ``/home/developer/celery``.
    By setting ``PYTHONPATH`` the service allows to use the mounted codebase
    as global module for development. If you prefer, you can also run
    ``python -m pip install -e .`` to install the codebase in development mode.

    If you would like to run a Django or stand alone project to manually test or
    debug a feature, you can use the image built by `docker compose` and mount
    your custom code. Here's an example:

    Assuming a folder structure such as:

    .. code-block:: console

        + celery_project
        + celery # repository cloned here.
        + my_project
            - manage.py
            + my_project
            - views.py

    .. code-block:: yaml

        version: "3"

        services:
            celery:
                image: celery/celery:dev
                environment:
                    TEST_BROKER: amqp://rabbit:5672
                    TEST_BACKEND: redis://redis
                    volumes:
                        - ../../celery:/home/developer/celery
                        - ../my_project:/home/developer/my_project
                    depends_on:
                        - rabbit
                        - redis
                rabbit:
                    image: rabbitmq:latest
                redis:
                    image: redis:latest

    In the previous example, we are using the image that we can build from
    this repository and mounting the celery code base as well as our custom
    project.

.. _`Docker`: https://www.docker.com/
.. _`docker-compose`: https://docs.docker.com/compose/

.. _contributing-testing:

运行单元测试套件
---------------------------

Running the unit test suite

.. tab:: 中文

    如果你喜欢使用虚拟环境或希望在 Docker 外部进行开发，
    请确保你已安装所有必要的依赖。
    我们提供了多个 requirements 文件以便安装所有依赖。
    你无需使用每个 requirements 文件，但必须使用 `default.txt`：

    .. code-block:: console

    # pip install -U -r requirements/default.txt

    要运行 Celery 测试套件，还需安装 :file:`requirements/test.txt`：

    .. code-block:: console

        $ pip install -U -r requirements/test.txt
        $ pip install -U -r requirements/default.txt

    安装好所需依赖后，就可以使用 :pypi:`pytest <pytest>` 来执行测试套件：

    .. code-block:: console

        $ pytest t/unit
        $ pytest t/integration

    :command:`pytest` 的一些常用选项如下：

    * ``-x``
        一旦测试失败，立即停止运行后续测试。

    * ``-s``
        不捕获输出。

    * ``-v``
        输出更详细的测试信息。

    如果你只想运行某个特定测试文件的测试，可以这样做：

    .. code-block:: console

        $ pytest t/unit/worker/test_worker.py

.. tab:: 英文

    If you like to develop using virtual environments or just outside docker,
    you must make sure all necessary dependencies are installed.
    There are multiple requirements files to make it easier to install all dependencies.
    You do not have to use every requirements file but you must use `default.txt`.

    .. code-block:: console

    # pip install -U -r requirements/default.txt

    To run the Celery test suite you need to install
    :file:`requirements/test.txt`.

    .. code-block:: console

        $ pip install -U -r requirements/test.txt
        $ pip install -U -r requirements/default.txt

    After installing the dependencies required, you can now execute
    the test suite by calling :pypi:`pytest <pytest>`:

    .. code-block:: console

        $ pytest t/unit
        $ pytest t/integration

    Some useful options to :command:`pytest` are:

    * ``-x``
        Stop running the tests at the first test that fails.

    * ``-s``
        Don't capture output

    * ``-v``
        Run with verbose output.

    If you want to run the tests for a single test file only
    you can do so like this:

    .. code-block:: console

        $ pytest t/unit/worker/test_worker.py

.. _contributing-coverage:

计算测试覆盖率
~~~~~~~~~~~~~~~~~~~~~~~~~

Calculating test coverage

.. tab:: 中文

    要计算测试覆盖率，首先需要安装 :pypi:`pytest-cov` 模块。

    安装 :pypi:`pytest-cov` 模块：

    .. code-block:: console

        $ pip install -U pytest-cov

.. tab:: 英文

    To calculate test coverage you must first install the :pypi:`pytest-cov` module.

    Installing the :pypi:`pytest-cov` module:

    .. code-block:: console

        $ pip install -U pytest-cov

HTML 格式的代码覆盖率
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code coverage in HTML format

.. tab:: 中文

    #. 使用 ``--cov-report=html`` 参数运行 :command:`pytest`：

        .. code-block:: console

            $ pytest --cov=celery --cov-report=html

    #. 然后，覆盖率输出将位于 :file:`htmlcov/` 目录中：

        .. code-block:: console

            $ open htmlcov/index.html

.. tab:: 英文

    #. Run :command:`pytest` with the ``--cov-report=html`` argument enabled:

        .. code-block:: console

            $ pytest --cov=celery --cov-report=html

    #. The coverage output will then be located in the :file:`htmlcov/` directory:

        .. code-block:: console

            $ open htmlcov/index.html

XML 格式的代码覆盖率（Cobertura 风格）
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Code coverage in XML (Cobertura-style)

.. tab:: 中文

    #. 使用 ``--cov-report=xml`` 参数运行 :command:`pytest`：

    .. code-block:: console

        $ pytest --cov=celery --cov-report=xml

    #. 然后，覆盖率的 XML 输出将位于 :file:`coverage.xml` 文件中。

.. tab:: 英文

    #. Run :command:`pytest` with the ``--cov-report=xml`` argument enabled:

    .. code-block:: console

        $ pytest --cov=celery --cov-report=xml

    #. The coverage XML output will then be located in the :file:`coverage.xml` file.

.. _contributing-tox:

在所有支持的 Python 版本上运行测试
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Running the tests on all supported Python versions

.. tab:: 中文

    在分发的顶级目录中有一个 :pypi:`tox` 配置文件。

    要为所有支持的 Python 版本运行测试，只需执行：

    .. code-block:: console

        $ tox

    如果只想测试特定的 Python 版本，可以使用 ``tox -e`` 选项：

    .. code-block:: console

        $ tox -e 3.7

.. tab:: 英文

    There's a :pypi:`tox` configuration file in the top directory of the
    distribution.

    To run the tests for all supported Python versions simply execute:

    .. code-block:: console

        $ tox

    Use the ``tox -e`` option if you only want to test specific Python versions:

    .. code-block:: console

        $ tox -e 3.7

构建文档
--------------------------

Building the documentation

.. tab:: 中文

    要构建文档，需要安装 :file:`requirements/docs.txt` 和 :file:`requirements/default.txt` 中列出的依赖项：

    .. code-block:: console

        $ pip install -U -r requirements/docs.txt
        $ pip install -U -r requirements/default.txt

    此外，为了无警告地构建文档，你还需要安装以下软件包：

    .. code-block:: console

    $ apt-get install texlive texlive-latex-extra dvipng

    安装这些依赖项后，你应该能够通过以下命令构建文档：

    .. code-block:: console

        $ cd docs
        $ rm -rf _build
        $ make html

    确保构建输出中没有错误或警告。
    构建成功后，文档将位于 :file:`_build/html` 中。

.. tab:: 英文

    To build the documentation, you need to install the dependencies
    listed in :file:`requirements/docs.txt` and :file:`requirements/default.txt`:

    .. code-block:: console

        $ pip install -U -r requirements/docs.txt
        $ pip install -U -r requirements/default.txt

    Additionally, to build with no warnings, you will need to install
    the following packages:

    .. code-block:: console

    $ apt-get install texlive texlive-latex-extra dvipng

    After these dependencies are installed, you should be able to
    build the docs by running:

    .. code-block:: console

        $ cd docs
        $ rm -rf _build
        $ make html

    Make sure there are no errors or warnings in the build output.
    After building succeeds, the documentation is available at :file:`_build/html`.

.. _contributing-verify:

使用 Docker 构建文档
------------------------------------

Build the documentation using Docker

.. tab:: 中文

    通过运行以下命令来构建文档：

    .. code-block:: console

        $ docker compose -f docker/docker-compose.yml up --build docs

    该服务将在 ``:7000`` 启动一个本地文档服务器。该服务器使用了 ``sphinx-autobuild`` 并启用了 ``--watch`` 选项，
    因此你可以实时编辑文档。检查 :file:`docker/docker-compose.yml` 中的附加选项和配置。

.. tab:: 英文

    Build the documentation by running:

    .. code-block:: console

        $ docker compose -f docker/docker-compose.yml up --build docs

    The service will start a local docs server at ``:7000``. The server is using
    ``sphinx-autobuild`` with the ``--watch`` option enabled, so you can live
    edit the documentation. Check the additional options and configs in
    :file:`docker/docker-compose.yml`

验证您的贡献
---------------------------

Verifying your contribution

.. tab:: 中文

    要使用这些工具，你需要安装一些依赖项。这些依赖项可以在 :file:`requirements/pkgutils.txt` 中找到。

    安装依赖项：

    .. code-block:: console

        $ pip install -U -r requirements/pkgutils.txt

.. tab:: 英文

    To use these tools, you need to install a few dependencies. These dependencies
    can be found in :file:`requirements/pkgutils.txt`.

    Installing the dependencies:

    .. code-block:: console

        $ pip install -U -r requirements/pkgutils.txt

pyflakes 和 PEP-8
~~~~~~~~~~~~~~~~

pyflakes & PEP-8

.. tab:: 中文

    为了确保你的更改符合 :pep:`8` 标准并运行 pyflakes，执行：

    .. code-block:: console

        $ make flakecheck

    如果你不希望此命令失败时返回负的退出码，可以改用 ``flakes`` 目标：

    .. code-block:: console

        $ make flakes

.. tab:: 英文

    To ensure that your changes conform to :pep:`8` and to run pyflakes
    execute:

    .. code-block:: console

        $ make flakecheck

    To not return a negative exit code when this command fails, use
    the ``flakes`` target instead:

    .. code-block:: console

        $ make flakes

API 参考
~~~~~~~~~~~~~

API reference

.. tab:: 中文

    为了确保所有模块在 API 参考文档中都有相应的部分，请执行：

    .. code-block:: console

        $ make apicheck

    如果文件缺失，你可以通过复制现有的参考文件来添加它们。

    如果模块是内部模块，它应该是位于 :file:`docs/internals/reference/` 中的内部参考的一部分。
    如果模块是公共模块，它应该位于 :file:`docs/reference/` 中。

    例如，如果 ``celery.worker.awesome`` 模块缺少参考，而该模块被视为公共 API 的一部分，请按照以下步骤操作：

    使用现有文件作为模板：

    .. code-block:: console

        $ cd docs/reference/
        $ cp celery.schedules.rst celery.worker.awesome.rst

    使用你喜欢的编辑器编辑文件：

    .. code-block:: console

        $ vim celery.worker.awesome.rst

            # 将文件中所有的 ``celery.schedules`` 替换为
            # ``celery.worker.awesome``


    使用你喜欢的编辑器编辑索引文件：

    .. code-block:: console

        $ vim index.rst

            # 将 ``celery.worker.awesome`` 添加到索引中。


    提交更改：

    .. code-block:: console

        # 将文件添加到 git 中
        $ git add celery.worker.awesome.rst
        $ git add index.rst
        $ git commit celery.worker.awesome.rst index.rst \
            -m "添加 celery.worker.awesome 的参考文档"


.. tab:: 英文

    To make sure that all modules have a corresponding section in the API
    reference, please execute:

    .. code-block:: console

        $ make apicheck

    If files are missing, you can add them by copying an existing reference file.

    If the module is internal, it should be part of the internal reference
    located in :file:`docs/internals/reference/`. If the module is public,
    it should be located in :file:`docs/reference/`.

    For example, if reference is missing for the module ``celery.worker.awesome``
    and this module is considered part of the public API, use the following steps:


    Use an existing file as a template:

    .. code-block:: console

        $ cd docs/reference/
        $ cp celery.schedules.rst celery.worker.awesome.rst

    Edit the file using your favorite editor:

    .. code-block:: console

        $ vim celery.worker.awesome.rst

            # change every occurrence of ``celery.schedules`` to
            # ``celery.worker.awesome``


    Edit the index using your favorite editor:

    .. code-block:: console

        $ vim index.rst

            # Add ``celery.worker.awesome`` to the index.


    Commit your changes:

    .. code-block:: console

        # Add the file to git
        $ git add celery.worker.awesome.rst
        $ git add index.rst
        $ git commit celery.worker.awesome.rst index.rst \
            -m "Adds reference for celery.worker.awesome"

Isort
~~~~~~

Isort

.. tab:: 中文

.. tab:: 英文

`Isort`_ is a python utility to help sort imports alphabetically and separated into sections.
The Celery project uses isort to better maintain imports on every module.
Please run isort if there are any new modules or the imports on an existent module
had to be modified.

.. code-block:: console

   $ isort my_module.py # Run isort for one file
   $ isort -rc . # Run it recursively
   $ isort m_module.py --diff # Do a dry-run to see the proposed changes

.. _`Isort`: https://isort.readthedocs.io/en/latest/

.. _contributing-pull-requests:

创建拉取请求
----------------------

Creating pull requests

.. tab:: 中文

    当你的功能/修复完成后，你可能希望提交一个拉取请求（pull request），以便让维护者进行审查。

    在提交拉取请求之前，请确保按照以下清单检查，确保维护者能够更容易地接受你提出的更改：

    - [ ] 确保任何更改或新功能都有单元测试和/或集成测试。
          如果没有编写测试，你的 PR 将被标记为 ``Needs Test Coverage``。

    - [ ] 确保单元测试覆盖率没有下降。
          ``pytest -xv --cov=celery --cov-report=xml --cov-report term``。
          你可以在此查看当前的测试覆盖率： https://codecov.io/gh/celery/celery

    - [ ] 在代码上运行 ``pre-commit``。以下命令是有效且等效的：

          .. code-block:: console

              $ pre-commit run --all-files
              $ tox -e lint

    - [ ] 构建 API 文档以确保一切正常。以下命令是有效且等效的：

          .. code-block:: console

              $ make apicheck
              $ cd docs && sphinx-build -b apicheck -d _build/doctrees . _build/apicheck
              $ tox -e apicheck

    - [ ] 构建 configcheck。以下命令是有效且等效的：

          .. code-block:: console

              $ make configcheck
              $ cd docs && sphinx-build -b configcheck -d _build/doctrees   . _build/configcheck
              $ tox -e configcheck

    - [ ] 运行 ``bandit`` 以确保没有安全问题。以下命令是有效且等效的：

          .. code-block:: console

              $ pip install -U bandit
              $ bandit -b bandit.json celery/
              $ tox -e bandit

    - [ ] 对每个 Python 版本运行单元和集成测试。以下命令是有效且等效的：

          .. code-block:: console

             $ tox -v

    - [ ] 确认所有新导入或修改的导入文件通过了 ``isort`` 检查：

          .. code-block:: console

            $ isort my_module.py --diff

    创建拉取请求非常简单，它们还可以让你追踪你贡献的进展。
    阅读 GitHub 指南中的 `Pull Requests`_ 部分，了解如何完成这项操作。

    你还可以通过以下步骤将拉取请求附加到现有的问题： https://bit.ly/koJoso

    你也可以使用 `hub`_ 创建拉取请求。示例：https://theiconic.tech/git-hub-fbe2e13ef4d1

.. tab:: 英文

    When your feature/bugfix is complete, you may want to submit
    a pull request, so that it can be reviewed by the maintainers.

    Before submitting a pull request, please make sure you go through this checklist to
    make it easier for the maintainers to accept your proposed changes:

    - [ ] Make sure any change or new feature has a unit and/or integration test.
          If a test is not written, a label will be assigned to your PR with the name
          ``Needs Test Coverage``.

    - [ ] Make sure unit test coverage does not decrease.
          ``pytest -xv --cov=celery --cov-report=xml --cov-report term``.
          You can check the current test coverage here: https://codecov.io/gh/celery/celery

    - [ ] Run ``pre-commit`` against the code. The following commands are valid
          and equivalent.:

          .. code-block:: console

              $ pre-commit run --all-files
              $ tox -e lint

    - [ ]  Build api docs to make sure everything is OK. The following commands are valid
          and equivalent.:

          .. code-block:: console

              $ make apicheck
              $ cd docs && sphinx-build -b apicheck -d _build/doctrees . _build/apicheck
              $ tox -e apicheck

    - [ ] Build configcheck. The following commands are valid
          and equivalent.:

          .. code-block:: console

              $ make configcheck
              $ cd docs && sphinx-build -b configcheck -d _build/doctrees   . _build/configcheck
              $ tox -e configcheck

    - [ ] Run ``bandit`` to make sure there's no security issues. The following commands are valid
          and equivalent.:

          .. code-block:: console

              $ pip install -U bandit
              $ bandit -b bandit.json celery/
              $ tox -e bandit

    - [ ] Run unit and integration tests for every python version. The following commands are valid
          and equivalent.:

          .. code-block:: console

             $ tox -v

    - [ ] Confirm ``isort`` on any new or modified imports:

          .. code-block:: console

            $ isort my_module.py --diff

    Creating pull requests is easy, and they also let you track the progress
    of your contribution. Read the `Pull Requests`_ section in the GitHub
    Guide to learn how this is done.

    You can also attach pull requests to existing issues by following
    the steps outlined here: https://bit.ly/koJoso

    You can also use `hub`_ to create pull requests. Example: https://theiconic.tech/git-hub-fbe2e13ef4d1

.. _`Pull Requests`: http://help.github.com/send-pull-requests/

.. _`hub`: https://hub.github.com/

状态标签
~~~~~~~~~~~~~~

Status Labels

.. tab:: 中文
    
    有一些 `不同的标签`_ 用于轻松管理 GitHub 问题和 PR。
    这些标签中的大多数可以轻松地对每个问题进行分类并附加重要细节。
    例如，你可能会看到一个 ``Component:canvas`` 标签出现在某个问题或 PR 上。
    ``Component:canvas`` 标签意味着该问题或 PR 与画布功能相关。
    这些标签由维护者设置，大多数情况下，外部贡献者不需要担心它们。部分标签以 **Status:** 开头。
    通常，**Status:** 标签显示了问题或 PR 所需的关键操作。
    以下是这些状态的总结：
    
    - **Status: Cannot Reproduce**
    
      一个或多个 Celery 核心团队成员无法重现该问题。
    
    - **Status: Confirmed**
    
      一个或多个 Celery 核心团队成员已确认该问题或 PR。
    
    - **Status: Duplicate**
    
      重复的问题或 PR。
    
    - **Status: Feedback Needed**
    
      一个或多个 Celery 核心团队成员要求就该问题或 PR 提供反馈。
    
    - **Status: Has Testcase**
    
      已确认该问题或 PR 包含一个测试用例。
      这对于正确编写新功能或修复的测试尤为重要。
    
    - **Status: In Progress**
    
      PR 仍在进行中。
    
    - **Status: Invalid**
    
      报告的问题或 PR 对项目无效。
    
    - **Status: Needs Documentation**
    
      PR 没有包含所提出的功能或修复的文档。
    
    - **Status: Needs Rebase**
    
      PR 尚未与 ``main`` 进行变基。变基非常重要，因为它可以在合并到 ``main`` 之前解决任何合并冲突。
    
    - **Status: Needs Test Coverage**
    
      Celery 使用 `codecov`_ 来验证代码覆盖率。请确保 PR 不会降低代码覆盖率。此标签将标识需要代码覆盖率的 PR。
    
    - **Status: Needs Test Case**
    
      该问题或 PR 需要一个测试用例。测试用例可以是一个最小的代码片段，用于重现问题，或者是一个详细的指令集和配置值，用于重现报告的问题。如果可能，测试用例可以作为 PR 提交给 Celery 的集成套件。在修复 bug 之前，测试用例将标记为失败。当测试用例无法由 Celery 的集成套件运行时，最好在问题本身中进行描述。
    
    - **Status: Needs Verification**
    
      该标签用于通知其他用户，我们需要验证报告者提供的测试用例，和/或我们需要将该测试包含到我们的集成套件中。
    
    - **Status: Not a Bug**
    
      已决定报告的问题不是 bug。
    
    - **Status: Won't Fix**
    
      已决定不修复该问题。遗憾的是，Celery 项目没有无限的资源，有时必须做出这个决定。
      尽管如此，任何外部贡献者都被邀请参与，即使问题或 PR 被标记为 ``Status: Won't Fix``。
    
    - **Status: Works For Me**
    
      一个或多个 Celery 核心团队成员已确认报告的问题对他们有效。

.. tab:: 英文

    There are `different labels`_ used to easily manage github issues and PRs.
    Most of these labels make it easy to categorize each issue with important
    details. For instance, you might see a ``Component:canvas`` label on an issue or PR.
    The ``Component:canvas`` label means the issue or PR corresponds to the canvas functionality.
    These labels are set by the maintainers and for the most part external contributors
    should not worry about them. A subset of these labels are prepended with **Status:**.
    Usually the **Status:** labels show important actions which the issue or PR needs.
    Here is a summary of such statuses:

    - **Status: Cannot Reproduce**

      One or more Celery core team member has not been able to reproduce the issue.

    - **Status: Confirmed**

      The issue or PR has been confirmed by one or more Celery core team member.

    - **Status: Duplicate**

      A duplicate issue or PR.

    - **Status: Feedback Needed**

      One or more Celery core team member has asked for feedback on the issue or PR.

    - **Status: Has Testcase**

      It has been confirmed the issue or PR includes a test case.
      This is particularly important to correctly write tests for any new
      feature or bug fix.

    - **Status: In Progress**

      The PR is still in progress.

    - **Status: Invalid**

      The issue reported or the PR is not valid for the project.

    - **Status: Needs Documentation**

      The PR does not contain documentation for the feature or bug fix proposed.

    - **Status: Needs Rebase**

      The PR has not been rebased with ``main``. It is very important to rebase
      PRs before they can be merged to ``main`` to solve any merge conflicts.

    - **Status: Needs Test Coverage**

      Celery uses `codecov`_ to verify code coverage. Please make sure PRs do not
      decrease code coverage. This label will identify PRs which need code coverage.

    - **Status: Needs Test Case**

      The issue or PR needs a test case. A test case can be a minimal code snippet
      that reproduces an issue or a detailed set of instructions and configuration values
      that reproduces the issue reported. If possible a test case can be submitted in
      the form of a PR to Celery's integration suite. The test case will be marked
      as failed until the bug is fixed. When a test case cannot be run by Celery's
      integration suite, then it's better to describe in the issue itself.

    - **Status: Needs Verification**

      This label is used to notify other users we need to verify the test case offered
      by the reporter and/or we need to include the test in our integration suite.

    - **Status: Not a Bug**

      It has been decided the issue reported is not a bug.

    - **Status: Won't Fix**

      It has been decided the issue will not be fixed. Sadly the Celery project does
      not have unlimited resources and sometimes this decision has to be made.
      Although, any external contributors are invited to help out even if an
      issue or PR is labeled as ``Status: Won't Fix``.

    - **Status: Works For Me**

      One or more Celery core team members have confirmed the issue reported works
      for them.

.. _`different labels`: https://github.com/celery/celery/labels
.. _`codecov`: https://codecov.io/gh/celery/celery

.. _coding-style:

编码风格
============

Coding Style

.. tab:: 中文

    你应该能够从周围的代码中获得编码风格，但了解以下约定是个好主意。

    * 所有 Python 代码必须遵循 :pep:`8` 指南。

    :pypi:`pep8` 是一个可以用来验证你的代码是否符合约定的工具。

    * 文档字符串必须遵循 :pep:`257` 指南，并使用以下风格。
        这样做：

        .. code-block:: python

            def method(self, arg):
                """简短描述。

                更多详细信息。

                """

        或者：

        .. code-block:: python

            def method(self, arg):
                """简短描述。"""


        但不要这样做：

        .. code-block:: python

            def method(self, arg):
                """
                简短描述。
                """

    * 行长度不应超过 78 列。

      你可以通过在 :command:`vim` 中设置 ``textwidth`` 选项来强制执行：

      .. code-block:: vim

            set textwidth=78

      如果遵守此限制会使代码变得不易读，则可以多用一个字符。这意味着 78 是软限制，79 是硬限制 :)

    * 导入顺序

        * Python 标准库（`import xxx`）
        * Python 标准库（`from xxx import`）
        * 第三方包。
        * 当前包的其他模块。

        或者，如果代码使用 Django：

        * Python 标准库（`import xxx`）
        * Python 标准库（`from xxx import`）
        * 第三方包。
        * Django 包。
        * 当前包的其他模块。

        在这些部分中，导入应按模块名排序。

        示例：

        .. code-block:: python

            import threading
            import time

            from collections import deque
            from Queue import Queue, Empty

            from .platforms import Pidfile
            from .utils.time import maybe_timedelta

    * 不得使用通配符导入（`from xxx import *`）。

    * 对于支持 Python 2.5 的最早版本的分发，适用以下额外规则：
        * 每个模块的顶部必须启用绝对导入::

            from __future__ import absolute_import

        * 如果模块使用 :keyword:`with` 语句并且必须兼容 Python 2.5（celery 不需要），则还必须启用它::

            from __future__ import with_statement

        * 每个未来导入必须单独写在一行，因为早期的 Python 2.5 版本不支持在同一行导入多个特性::

            # 好
            from __future__ import absolute_import
            from __future__ import with_statement

            # 不好
            from __future__ import absolute_import, with_statement

         （注意，如果包不包括对 Python 2.5 的支持，则此规则不适用）


    * 请注意，当分发版不支持 Python 2.5 以下版本时，我们使用 "新风格" 的相对导入。
        这需要 Python 2.5 或更高版本：

        .. code-block:: python

            from . import submodule

.. tab:: 英文

    You should probably be able to pick up the coding style
    from surrounding code, but it is a good idea to be aware of the
    following conventions.

    * All Python code must follow the :pep:`8` guidelines.

    :pypi:`pep8` is a utility you can use to verify that your code
    is following the conventions.

    * Docstrings must follow the :pep:`257` conventions, and use the following
      style.

      Do this:
  
      .. code-block:: python
      
          def method(self, arg):
              """Short description.
  
              More details.
  
              """
  
      or:
  
      .. code-block:: python
      
          def method(self, arg):
              """Short description."""
  
  
      but not this:
  
      .. code-block:: python
      
          def method(self, arg):
              """
              Short description.
              """

    * Lines shouldn't exceed 78 columns.

      You can enforce this in :command:`vim` by setting the ``textwidth`` option:

      .. code-block:: vim

            set textwidth=78

      If adhering to this limit makes the code less readable, you have one more
      character to go on. This means 78 is a soft limit, and 79 is the hard
      limit :)

    * Import order
        * Python standard library (`import xxx`)
        * Python standard library (`from xxx import`)
        * Third-party packages.
        * Other modules from the current package.

        or in case of code using Django:

        * Python standard library (`import xxx`)
        * Python standard library (`from xxx import`)
        * Third-party packages.
        * Django packages.
        * Other modules from the current package.

        Within these sections the imports should be sorted by module name.

        Example:

        .. code-block:: python

            import threading
            import time

            from collections import deque
            from Queue import Queue, Empty

            from .platforms import Pidfile
            from .utils.time import maybe_timedelta

    * Wild-card imports must not be used (`from xxx import *`).

    * For distributions where Python 2.5 is the oldest support version,
      additional rules apply:
        * Absolute imports must be enabled at the top of every module::

            from __future__ import absolute_import

        * If the module uses the :keyword:`with` statement and must be compatible
          with Python 2.5 (celery isn't), then it must also enable that::

            from __future__ import with_statement

        * Every future import must be on its own line, as older Python 2.5
          releases didn't support importing multiple features on the
          same future import line::

            # Good
            from __future__ import absolute_import
            from __future__ import with_statement

            # Bad
            from __future__ import absolute_import, with_statement

         (Note that this rule doesn't apply if the package doesn't include
         support for Python 2.5)


    * Note that we use "new-style" relative imports when the distribution
      doesn't support Python versions below 2.5
        This requires Python 2.5 or later:

        .. code-block:: python

            from . import submodule


.. _feature-with-extras:

贡献需要额外库的功能
====================================================

Contributing features requiring additional libraries

.. tab:: 中文

    某些功能，如新的结果后端，可能需要用户安装额外的库。

    我们使用 setuptools `extra_requires` 来处理这个问题，所有需要第三方库的新可选功能都必须添加。

    1) 在 `requirements/extras` 中添加一个新的要求文件

        对于 Cassandra 后端，这是 :file:`requirements/extras/cassandra.txt`，该文件内容如下：

        .. code-block:: text

            pycassa

        这些是 pip 要求文件，因此你可以包含版本指定符，并且多个包通过换行分隔。一个更复杂的示例如下：

        .. code-block:: text

            # pycassa 2.0 会破坏 Foo
            pycassa>=1.0,<2.0
            thrift

    2) 修改 ``setup.py``

        添加要求文件后，你需要将其作为选项添加到 :file:`setup.py` 的 ``extras_require`` 部分::

            extra['extras_require'] = {
                # ...
                'cassandra': extras('cassandra.txt'),
            }

    3) 在 :file:`docs/includes/installation.txt` 中记录新功能

        你必须将你的功能添加到 :file:`docs/includes/installation.txt` 文件中的 :ref:`bundles` 部分。

        在你对该文件进行更改后，需要渲染分发版 :file:`README` 文件：

        .. code-block:: console

            $ pip install -U -r requirements/pkgutils.txt
            $ make readme


    以上是你需要做的全部工作，但请记住，如果你的功能添加了额外的配置选项，则这些选项需要在 :file:`docs/configuration.rst` 中进行文档化。此外，所有设置都需要添加到 :file:`celery/app/defaults.py` 模块中。

    结果后端需要在 :file:`docs/configuration.rst` 文件中单独的章节进行记录。


.. tab:: 英文

    Some features like a new result backend may require additional libraries
    that the user must install.

    We use setuptools `extra_requires` for this, and all new optional features
    that require third-party libraries must be added.

    1) Add a new requirements file in `requirements/extras`

        For the Cassandra backend this is
        :file:`requirements/extras/cassandra.txt`, and the file looks like this:

        .. code-block:: text

            pycassa

        These are pip requirement files, so you can have version specifiers and
        multiple packages are separated by newline. A more complex example could
        be:

        .. code-block:: text

            # pycassa 2.0 breaks Foo
            pycassa>=1.0,<2.0
            thrift

    2) Modify ``setup.py``

        After the requirements file is added, you need to add it as an option
        to :file:`setup.py` in the ``extras_require`` section::

            extra['extras_require'] = {
                # ...
                'cassandra': extras('cassandra.txt'),
            }

    3) Document the new feature in :file:`docs/includes/installation.txt`

        You must add your feature to the list in the :ref:`bundles` section
        of :file:`docs/includes/installation.txt`.

        After you've made changes to this file, you need to render
        the distro :file:`README` file:

        .. code-block:: console

            $ pip install -U -r requirements/pkgutils.txt
            $ make readme


    That's all that needs to be done, but remember that if your feature
    adds additional configuration options, then these needs to be documented
    in :file:`docs/configuration.rst`. Also, all settings need to be added to the
    :file:`celery/app/defaults.py` module.

    Result backends require a separate section in the :file:`docs/configuration.rst`
    file.

.. _contact_information:

联系方式
========

Contacts

.. tab:: 中文

    这是可以联系的人员列表，适用于有关官方 Git 仓库、PyPI 包
    和 Read the Docs 页面的问题。

    如果问题不是紧急的，最好是 :ref:`报告一个问题 <reporting-bugs>`。

.. tab:: 英文

    This is a list of people that can be contacted for questions
    regarding the official git repositories, PyPI packages
    Read the Docs pages.

    If the issue isn't an emergency then it's better
    to :ref:`report an issue <reporting-bugs>`.


Committers
----------

Ask Solem
~~~~~~~~~

:github: https://github.com/ask
:twitter: https://twitter.com/#!/asksol

Asif Saif Uddin
~~~~~~~~~~~~~~~

:github: https://github.com/auvipy
:twitter: https://twitter.com/#!/auvipy

Dmitry Malinovsky
~~~~~~~~~~~~~~~~~

:github: https://github.com/malinoff
:twitter: https://twitter.com/__malinoff__

Ionel Cristian Mărieș
~~~~~~~~~~~~~~~~~~~~~

:github: https://github.com/ionelmc
:twitter: https://twitter.com/ionelmc

Mher Movsisyan
~~~~~~~~~~~~~~

:github: https://github.com/mher
:twitter: https://twitter.com/#!/movsm

Omer Katz
~~~~~~~~~
:github: https://github.com/thedrow
:twitter: https://twitter.com/the_drow

Steeve Morin
~~~~~~~~~~~~

:github: https://github.com/steeve
:twitter: https://twitter.com/#!/steeve

Josue Balandrano Coronel
~~~~~~~~~~~~~~~~~~~~~~~~~

:github: https://github.com/xirdneh
:twitter: https://twitter.com/eusoj_xirdneh

Tomer Nosrati
~~~~~~~~~~~~~
:github: https://github.com/Nusnus
:twitter: https://x.com/tomer_nosrati

Website
-------

The Celery Project website is run and maintained by

Mauro Rocco
~~~~~~~~~~~

:github: https://github.com/fireantology
:twitter: https://twitter.com/#!/fireantology

with design by:

Jan Henrik Helmers
~~~~~~~~~~~~~~~~~~

:web: http://www.helmersworks.com
:twitter: https://twitter.com/#!/helmers


.. _packages:

Packages
========

``celery``
----------

:git: https://github.com/celery/celery
:CI: https://travis-ci.org/#!/celery/celery
:Windows-CI: https://ci.appveyor.com/project/ask/celery
:PyPI: :pypi:`celery`
:docs: https://docs.celeryq.dev

``kombu``
---------

Messaging library.

:git: https://github.com/celery/kombu
:CI: https://travis-ci.org/#!/celery/kombu
:Windows-CI: https://ci.appveyor.com/project/ask/kombu
:PyPI: :pypi:`kombu`
:docs: https://kombu.readthedocs.io

``amqp``
--------

Python AMQP 0.9.1 client.

:git: https://github.com/celery/py-amqp
:CI: https://travis-ci.org/#!/celery/py-amqp
:Windows-CI: https://ci.appveyor.com/project/ask/py-amqp
:PyPI: :pypi:`amqp`
:docs: https://amqp.readthedocs.io

``vine``
--------

Promise/deferred implementation.

:git: https://github.com/celery/vine/
:CI: https://travis-ci.org/#!/celery/vine/
:Windows-CI: https://ci.appveyor.com/project/ask/vine
:PyPI: :pypi:`vine`
:docs: https://vine.readthedocs.io

``pytest-celery``
-----------------

Pytest plugin for Celery.

:git: https://github.com/celery/pytest-celery
:PyPI: :pypi:`pytest-celery`
:docs: https://pytest-celery.readthedocs.io

``billiard``
------------

Fork of multiprocessing containing improvements
that'll eventually be merged into the Python stdlib.

:git: https://github.com/celery/billiard
:CI: https://travis-ci.org/#!/celery/billiard/
:Windows-CI: https://ci.appveyor.com/project/ask/billiard
:PyPI: :pypi:`billiard`

``django-celery-beat``
----------------------

Database-backed Periodic Tasks with admin interface using the Django ORM.

:git: https://github.com/celery/django-celery-beat
:CI: https://travis-ci.org/#!/celery/django-celery-beat
:Windows-CI: https://ci.appveyor.com/project/ask/django-celery-beat
:PyPI: :pypi:`django-celery-beat`

``django-celery-results``
-------------------------

Store task results in the Django ORM, or using the Django Cache Framework.

:git: https://github.com/celery/django-celery-results
:CI: https://travis-ci.org/#!/celery/django-celery-results
:Windows-CI: https://ci.appveyor.com/project/ask/django-celery-results
:PyPI: :pypi:`django-celery-results`

``librabbitmq``
---------------

Very fast Python AMQP client written in C.

:git: https://github.com/celery/librabbitmq
:PyPI: :pypi:`librabbitmq`

``cell``
--------

Actor library.

:git: https://github.com/celery/cell
:PyPI: :pypi:`cell`

``cyme``
--------

Distributed Celery Instance manager.

:git: https://github.com/celery/cyme
:PyPI: :pypi:`cyme`
:docs: https://cyme.readthedocs.io/


Deprecated
----------

- ``django-celery``

:git: https://github.com/celery/django-celery
:PyPI: :pypi:`django-celery`
:docs: https://docs.celeryq.dev/en/latest/django

- ``Flask-Celery``

:git: https://github.com/ask/Flask-Celery
:PyPI: :pypi:`Flask-Celery`

- ``celerymon``

:git: https://github.com/celery/celerymon
:PyPI: :pypi:`celerymon`

- ``carrot``

:git: https://github.com/ask/carrot
:PyPI: :pypi:`carrot`

- ``ghettoq``

:git: https://github.com/ask/ghettoq
:PyPI: :pypi:`ghettoq`

- ``kombu-sqlalchemy``

:git: https://github.com/ask/kombu-sqlalchemy
:PyPI: :pypi:`kombu-sqlalchemy`

- ``django-kombu``

:git: https://github.com/ask/django-kombu
:PyPI: :pypi:`django-kombu`

- ``pylibrabbitmq``

Old name for :pypi:`librabbitmq`.

:git: :const:`None`
:PyPI: :pypi:`pylibrabbitmq`

.. _release-procedure:


发布流程
=================

Release Procedure

更新版本号
---------------------------

Updating the version number

.. tab:: 中文

    版本号必须在三个地方进行更新：

        * :file:`celery/__init__.py`
        * :file:`docs/include/introduction.txt`
        * :file:`README.rst`

    对前述文件的更改可以使用 [`bumpversion` 命令行工具]
    (https://pypi.org/project/bumpversion/) 来处理。相应的配置文件位于
    :file:`.bumpversion.cfg`。进行必要的更改，运行：

    .. code-block:: console

        $ bumpversion

    在更改了这些文件后，您必须渲染
    :file:`README` 文件。这里有一个脚本可以将 sphinx 语法
    转换为通用的 reStructured Text 语法，`make readme` 目标会为您完成此操作：

    .. code-block:: console

        $ make readme

    现在提交这些更改：

    .. code-block:: console

        $ git commit -a -m "Bumps version to X.Y.Z"

    并创建一个新的版本标签：

    .. code-block:: console

        $ git tag vX.Y.Z
        $ git push --tags

.. tab:: 英文

    The version number must be updated in three places:

        * :file:`celery/__init__.py`
        * :file:`docs/include/introduction.txt`
        * :file:`README.rst`

    The changes to the previous files can be handled with the [`bumpversion` command line tool]
    (https://pypi.org/project/bumpversion/). The corresponding configuration lives in
    :file:`.bumpversion.cfg`. To do the necessary changes, run:

    .. code-block:: console

        $ bumpversion

    After you have changed these files, you must render
    the :file:`README` files. There's a script to convert sphinx syntax
    to generic reStructured Text syntax, and the make target `readme`
    does this for you:

    .. code-block:: console

        $ make readme

    Now commit the changes:

    .. code-block:: console

        $ git commit -a -m "Bumps version to X.Y.Z"

    and make a new version tag:

    .. code-block:: console

        $ git tag vX.Y.Z
        $ git push --tags

发布
---------

Releasing

.. tab:: 中文

    发布新的公共稳定版本的命令：

    .. code-block:: console

        $ make distcheck  # 检查 pep8、自动文档索引、运行测试等
        $ make dist  # 注意：执行 git clean -xdf 并删除未在仓库中的文件。
        $ python setup.py sdist upload --sign --identity='Celery Security Team'
        $ python setup.py bdist_wheel upload --sign --identity='Celery Security Team'

    如果这是一个新的发布系列，则还需要执行以下操作：

    * 进入 Read The Docs 管理界面：
        https://readthedocs.org/projects/celery/?fromdocs=celery

    * 选择“编辑项目”

        将默认分支更改为此系列的分支，例如，使用
        ``2.4`` 分支用于 2.4 系列。

    * 还需要在“版本”选项卡下添加前一个版本。

.. tab:: 英文

    Commands to make a new public stable release:

    .. code-block:: console

        $ make distcheck  # checks pep8, autodoc index, runs tests and more
        $ make dist  # NOTE: Runs git clean -xdf and removes files not in the repo.
        $ python setup.py sdist upload --sign --identity='Celery Security Team'
        $ python setup.py bdist_wheel upload --sign --identity='Celery Security Team'

    If this is a new release series then you also need to do the
    following:

    * Go to the Read The Docs management interface at:
        https://readthedocs.org/projects/celery/?fromdocs=celery

    * Enter "Edit project"

        Change default branch to the branch of this series, for example, use
        the ``2.4`` branch for the 2.4 series.

    * Also add the previous version under the "versions" tab.

.. _`mailing-list`: https://groups.google.com/group/celery-users

.. _`irc-channel`: https://docs.celeryq.dev/en/latest/getting-started/resources.html#irc

.. _`internals-guide`: https://docs.celeryq.dev/en/latest/internals/guide.html

.. _`bundles`: https://docs.celeryq.dev/en/latest/getting-started/introduction.html#bundles

.. _`report an issue`: https://docs.celeryq.dev/en/latest/contributing.html#reporting-bugs

