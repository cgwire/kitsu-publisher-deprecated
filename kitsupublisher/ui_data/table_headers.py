"""
Module with the header names of the table.
The keys are the task attributes we want to display, the values are the names
the columns will have in the table.
"""
from kitsupublisher.utils.pyversion import python_version

if python_version() >= (3, 6, 0):
    tab_columns = {
        "project_name": "Prod",
        "task_type_name": "Type",
        "entity_name": "Entity",
        "task_estimation": "Est.",
        "task_duration": "Dur.",
        "task_due_date": "Due date",
        "task_status_short_name": "Status",
    }
else:
    from collections import OrderedDict
    tab_columns = OrderedDict(
        [
            ("project_name", "Prod"),
            ("task_type_name", "Type"),
            ("entity_name", "Entity"),
            ("task_estimation", "Est."),
            ("task_duration", "Dur."),
            ("task_due_date", "Due date"),
            ("task_status_short_name", "Status"),
        ]
    )
