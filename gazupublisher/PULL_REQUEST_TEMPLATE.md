**Problem**
The user needs to see its to-do tasks and to add comments.

**Solution**
A class TasksTab was added, that stocks all the to-do tasks of the current user. It contains methods to empty it and fill it.
Its last column contains buttons, that open a comment window (class CommentWindow) when clicked. This dialog window asks the user for its comment, pass it to gazu, and the reloads the table.