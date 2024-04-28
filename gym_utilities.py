from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import pandas as pd
import yaml


def in_week(date: datetime, week: datetime = None) -> bool:
    """Return True iff <date> is in the same week as <week>.

    A week is defined as the period from Monday 0:00 to Sunday 23:59.
    Return True if no week is provided.

    Hint: You may find this helper function useful in your own code.

    >>> # Note: You can create a datetime that has only year, month, day, or
    >>> # you can optionally specify hour, minute, etc.
    >>> in_week(datetime(2022, 9, 1, 12, 0), datetime(2022, 8, 31))
    True
    >>> in_week(datetime(2022, 9, 1, 12, 0), datetime(2022, 9, 7))
    False
    >>> in_week(datetime(2022, 9, 1, 12, 0), datetime(202, 9, 8))
    False
    >>> in_week(datetime(2023, 1, 1), datetime(2022, 12, 31))
    True
    >>> in_week(datetime(2023, 1, 1))
    True
    """
    if not week:
        return True
    # find the first and last day of the calendar week containing <week>.
    week = week.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = week - timedelta(days=week.weekday())
    week_end = week_start + timedelta(days=6)
    week_end = week_end.replace(hour=23, minute=59, second=59, microsecond=0)
    # return True iff <date> is between <week_start> and <week_end>
    # return (week_start <= date) and (date <= week_end)  # pyTA complains
    return week_start <= date <= week_end


def create_offering_dict(date: str,
                         time: str,
                         workout_class_name: str,
                         room_name: str,
                         num_registered_participants: int,
                         num_available_seats: int,
                         instructor_name: str) -> dict[str, str | int]:
    """Return a dictionary that represents all the given attributes of a workout
    offering in a standardized format.

    Hint: You should use this helper function in the <offerings_at> method.
    """
    return {
        'Date': date,
        'Time': time,
        'Class': workout_class_name,
        'Room': room_name,
        'Registered': num_registered_participants,
        'Available': num_available_seats,
        'Instructor': instructor_name
    }


def write_schedule_to_html(df: pd.DataFrame, filename: str) -> None:
    """Use the data in <df> to produce an HTML file called <filename>.

    You do not have to use or understand this function. It is used by a method
    that we have provided.
    """
    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>
    header_style = '"text-align:center;font-family:sans-serif;"'
    h_link = '<link rel="stylesheet" ' \
             'type="text/css" href="table_style.css"/>'
    html_string = f'''
                <html>
                  <head><title>Schedule</title></head>

                  {h_link}
                  <body>
                    <p>
                    <h1 style={header_style}>Workout Class Schedule</h1>
                    </p>
                    TABLE
                  </body>
                </html>.
                '''
    # Write an HTML file
    with open(filename, 'w') as f:
        f.write(html_string.replace("TABLE", df.to_html(classes='mystyle',
                                                        index=False)))


class NoAliasDumper(yaml.Dumper):
    """A "YAML Dumper" that does not use aliases.

    You do not have to use or understand this class. It is used by a method
    that we have provided.

    Credit: https://github.com/yaml/pyyaml/issues/103
    """
    def ignore_aliases(self, data: Any) -> bool:
        return True


def write_yaml_file(filename: str, yaml_object: dict[str, Any]) -> None:
    """Write <yaml_object> to the YAML file named <filename>.

    See the doc tests below for examples of simple python objects in YAML
    format.

    You do not have to use or understand this function. It is used by a method
    that we have provided.

    >>> write_yaml_file('test.yaml', {'a': 1, 'b': 2})
    >>> data = open('test.yaml').read()
    >>> print(data.strip())
    a: 1
    b: 2
    >>> write_yaml_file('test.yaml', {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4}})
    >>> data = open('test.yaml').read()
    >>> print(data.strip())
    a: 1
    b: 2
    c:
      d: 3
      e: 4
    >>> write_yaml_file('test.yaml', {'a': [1,2, {'b': 3, 'c': [3,4]}], 'd': 5})
    >>> data = open('test.yaml').read()
    >>> print(data.strip())
    a:
    - 1
    - 2
    - b: 3
      c:
      - 3
      - 4
    d: 5
    """
    with open(filename, 'w') as f:
        yaml.dump(yaml_object, f, Dumper=NoAliasDumper)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'datetime', 'pandas', 'yaml',
                                   '__future__'],
        'allowed-io': ['write_schedule_to_html', 'write_yaml_file'],
        'disable': ['R0913'],
        'output-format': 'python_ta.reporters.ColorReporter'
    })

    import doctest
    doctest.testmod()
