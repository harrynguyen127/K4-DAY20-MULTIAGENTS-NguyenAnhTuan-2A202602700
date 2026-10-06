### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool call: glob
{"pattern": "**/*.py"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/test_bookings.py']

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: read_file
{"file_path": "workspace/README.md"}

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-5 of 5 @@
# bookings

Small package. Run the tests from the `workspace/` folder:

    cd workspace && python -m pytest tests -q

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q 2>&1 | tail -30"}

### Tool result
[stderr] 'tail' is not recognized as an internal or external command,
[stderr] operable program or batch file.

Exit code: 255
[Command failed with exit code 255]

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q"}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\anyio\_core\_eventloop.py", line 204, in get_async_backend
[stderr]     return loaded_backends[asynclib_name]
[stderr]            ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
[stderr] KeyError: 'asyncio'
[stderr] 
[stderr] During handling of the above exception, another exception occurred:
[stderr] 
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(pytest.console_main())
[stderr]                      ^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\config\__init__.py", line 201, in console_main
[stderr]     code = main()
[stderr]            ^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\config\__init__.py", line 156, in main
[stderr]     config = _prepareconfig(args, plugins)
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\config\__init__.py", line 342, in _prepareconfig
[stderr]     config = pluginmanager.hook.pytest_cmdline_parse(
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\L

### Tool call: execute
{"command": "cd workspace && python -m pytest tests -q -p no:anyio -p no:cacheprovider"}

### Tool result
[stderr] Traceback (most recent call last):
[stderr]   File "<frozen runpy>", line 198, in _run_module_as_main
[stderr]   File "<frozen runpy>", line 88, in _run_code
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\pytest\__main__.py", line 9, in <module>
[stderr]     raise SystemExit(pytest.console_main())
[stderr]                      ^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\config\__init__.py", line 201, in console_main
[stderr]     code = main()
[stderr]            ^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\config\__init__.py", line 156, in main
[stderr]     config = _prepareconfig(args, plugins)
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\_pytest\config\__init__.py", line 342, in _prepareconfig
[stderr]     config = pluginmanager.hook.pytest_cmdline_parse(
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\pluggy\_hooks.py", line 512, in __call__
[stderr]     return self._hookexec(self.name, self._hookimpls.copy(), kwargs, firstresult)
[stderr]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "~\AppData\Local\Programs\Python\Python311\Lib\site-packages\pluggy\_manager.py", line 120, in _hookexec
[stderr]     re

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q"}

### Tool result
FF.                                                                      [100%]
================================== FAILURES ===================================
______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

~\MyStorage\VinUniAI\Phase2\K4-DAY20-MULTIAGENTS-NguyenAnhTuan-2A202602700\tasks\code-eval\workspace\tests\test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
bookings\schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
bookings\schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45    # a bare number means minutes
        Surrounding whitespace is ignored.
        """
        m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
        if not m:
>           raise ValueError(f"bad duration: {text!r}")
E           ValueError: bad duration: '2h'

bookings\timeutil.py:18: ValueError
_

### Tool call: ls
{"path": "."}

### Tool call: glob
{"pattern": "**/*"}

### Tool result
['/.tools/', '/workspace/']

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/__init__.cpython-311.pyc', '/workspace/bookings/__pycache__/billing.cpython-311.pyc', '/workspace/bookings/__pycache__/calendar_export.cpython-311.pyc', '/workspace/bookings/__pycache__/schedule.cpython-311.pyc', '/workspace/bookings/__pycache__/timeutil.cpython-311.pyc', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-8.4.2.pyc', '/workspace/tests/__pycache__/test_bookings.cpython-311-pytest-9.1.1.pyc', '/workspace/tests/test_bookings.py']

### Tool call: ls
{"path": ".tools"}

### Tool result
['/.tools/cat.cmd', '/.tools/env.cmd', '/.tools/ls.cmd', '/.tools/which.cmd']

### Assistant
Now I understand the failures. Let me fix each module according to its docstring.

### Tool call: edit_file
{"file_path": "workspace/bookings/timeutil.py", "old_string": "    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))", "new_string": "    Supported formats:\n      \"1h30m\" -> 90\n      \"2h\"    -> 120\n      \"45m\"   -> 45\n      \"1:30\"  -> 90\n      \"45\"    -> 45    # a bare number means minutes\n    Surrounding whitespace is ignored.\n    \"\"\"\n    text = text.strip()\n\n    match = re.fullmatch(r\"(\\d+):(\\d{1,2})\", text)\n    if match:\n        return int(match.group(1)) * 60 + int(match.group(2))\n\n    match = re.fullmatch(r\"(\\d+)h(?:(\\d+)m)?\", text)\n    if match:\n        return int(match.group(1)) * 60 + int(match.group(2) or 0)\n\n    match = re.fullmatch(r\"(\\d+)m\", text)\n    if match:\n        return int(match.group(1))\n\n    match = re.fullmatch(r\"(\\d+)\", text)\n    if match:\n        return int(match.group(1))\n\n    raise ValueError(f\"bad duration: {text!r}\")"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    return round(minutes / block)", "new_string": "    A partial block is billed as a full block (always round UP):\n    16 minutes with 15-minute blocks -> 2 blocks.\n    `minutes` must be >= 0; a negative value raises ValueError.\n    \"\"\"\n    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return -(-minutes // block)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: edit_file
{"file_path": "workspace/bookings/schedule.py", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    return [*slots, slot]", "old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q"}

### Tool call: execute
{"command": "cd workspace && python -c \"from bookings.timeutil import parse_duration as p; from bookings.billing import billable_blocks as b; from bookings.schedule import add_slot, total_minutes; print(p('1h30m'), p('2h'), p('45m'), p('1:30'), p('45'), p(' 1h30m ')); print(b(20), b(45), b(16), b(0), b(15)); print(add_slot('a'), add_slot('b'), add_slot('b',['a']))\ntry:\n    b(-1)\nexcept ValueError as e: print('neg ok')\ntry:\n    p('garbage')\nexcept ValueError as e: print('bad ok')\nprint(total_minutes(['1h30m','2h']))\""}

### Tool result
...                                                                      [100%]
3 passed in 0.02s

[Command succeeded with exit code 0]

### Tool result
90 120 45 90 45 90
2 3 2 0 1
['a'] ['b'] ['a', 'b']

[Command succeeded with exit code 0]

### Tool call: execute
{"command": "cd workspace && python -c \"from bookings.billing import billable_blocks as b; from bookings.timeutil import parse_duration as p; import sys\nfor fn,arg in ((b,-1),(p,'garbage'),(p,''),(p,'1:30:00')):\n    try:\n        fn(arg); print('NO RAISE', fn.__name__, repr(arg))\n    except ValueError: print('raised ok', fn.__name__, repr(arg))\nprint('total', __import__('bookings.schedule', fromlist=['total_minutes']).total_minutes(['45','1:30','2h']))\""}

### Tool result
<no output>
[Command succeeded with exit code 0]

### Tool call: write_file
{"file_path": "workspace/_check.py", "content": "from bookings.billing import billable_blocks\nfrom bookings.timeutil import parse_duration\nfrom bookings.schedule import total_minutes, add_slot\nfrom bookings.calendar_export import slot_end\n\nfor fn, arg in ((billable_blocks, -1), (parse_duration, \"garbage\"),\n                (parse_duration, \"\"), (parse_duration, \"1:30:00\")):\n    try:\n        fn(arg)\n        print(\"NO RAISE\", fn.__name__, repr(arg))\n    except ValueError:\n        print(\"raised ok\", fn.__name__, repr(arg))\n\nprint(\"total\", total_minutes([\"45\", \"1:30\", \"2h\"]))\nprint(\"slot_end\", slot_end(480, \"1h30m\"))\nprint(\"add\", add_slot(\"a\"), add_slot(\"b\"), add_slot(\"b\", [\"a\"]))\n"}

### Tool result
Updated file /workspace/_check.py

### Tool call: execute
{"command": "cd workspace && python _check.py"}

### Tool result
raised ok billable_blocks -1
raised ok parse_duration 'garbage'
raised ok parse_duration ''
raised ok parse_duration '1:30:00'
total 255
slot_end 570
add ['a'] ['b'] ['a', 'b']

[Command succeeded with exit code 0]

### Tool call: edit_file
{"file_path": "workspace/bookings/billing.py", "old_string": "    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return -(-minutes // block)", "new_string": "    if minutes < 0:\n        raise ValueError(f\"minutes must be >= 0, got {minutes!r}\")\n    return (minutes + block - 1) // block"}

### Tool call: delete
{"file_path": "workspace/_check.py"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool result
Deleted /workspace/_check.py

### Tool call: read_file
{"file_path": "workspace/CHANGELOG.md"}

### Tool result
@@ lines 1-6 of 6 @@
# Changelog

## Unreleased

## 1.4.2
- initial import

### Tool call: edit_file
{"file_path": "workspace/CHANGELOG.md", "new_string": "## Unreleased\n- `parse_duration`: support the documented `\"2h\"`, `\"45m\"`, `\"1:30\"` and bare-minute formats.\n- `billable_blocks`: round partial blocks up and reject negative minutes.\n- `add_slot`: stop sharing mutable default state so each call returns a new list.\n\n## 1.4.2", "old_string": "## Unreleased\n\n## 1.4.2"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/CHANGELOG.md'

### Tool call: execute
{"command": "cd workspace && set PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 && python -m pytest tests -q"}

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
...                                                                      [100%]
3 passed in 0.02s

[Command succeeded with exit code 0]

### Tool result
@@ lines 1-34 of 34 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    text = text.strip()

    match = re.fullmatch(r"(\d+):(\d{1,2})", text)
    if match:
        return int(match.group(1)) * 60 + int(match.group(2))

    match = re.fullmatch(r"(\d+)h(?:(\d+)m)?", text)
    if match:
        return int(match.group(1)) * 60 + int(match.group(2) or 0)

    match = re.fullmatch(r"(\d+)m", text)
    if match:
        return int(match.group(1))

    match = re.fullmatch(r"(\d+)", text)
    if match:
        return int(match.group(1))

    raise ValueError(f"bad duration: {text!r}")

### Tool result
@@ lines 1-13 of 13 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    if minutes < 0:
        raise ValueError(f"minutes must be >= 0, got {minutes!r}")
    return (minutes + block - 1) // block

### Tool result
@@ lines 1-18 of 18 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=None):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    if slots is None:
        slots = []
    return [*slots, slot]

### Assistant
The test suite passes. Here's what I fixed and why:

**`bookings/timeutil.py` — `parse_duration`**
The old regex only matched the `"1h30m"` form, so any other documented format raised `ValueError`. It now handles every format named in the docstring: `"1h30m"`, `"2h"` (minutes optional), `"45m"`, `"1:30"`, and bare minutes `"45"`, still stripping surrounding whitespace and raising `ValueError` for junk input.

**`bookings/billing.py` — `billable_blocks`**
It used `round(...)`, which rounds to nearest (20 → 1, 45 → 3), not up. It now rounds up with `(minutes + block - 1) // block` and raises `ValueError` for negative `minutes`, as the docstring requires.

**`bookings/schedule.py` — `add_slot`**
It had a mutable default argument (`slots=[]`), so state leaked between calls. It now defaults to `None`, builds a fresh list, and returns a new list (also leaving the caller's list untouched), matching the "return a NEW list" contract.

**`CHANGELOG.md`**
Added an Unreleased entry documenting the three fixes.

`calendar_export.slot_end` and `schedule.total_minutes` were already correct once `parse_duration` was fixed. No test files were modified.