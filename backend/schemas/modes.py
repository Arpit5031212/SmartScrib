from enum import StrEnum
from typing import List, Optional
from pydantic import BaseModel


class Mode(StrEnum):
    MEETING = "meeting"
    NOTES = "notes"
    TASKS = "tasks"
    TIMESHEET = "timesheet"
    REWRITE = "rewrite"
    REPORT = "report"
    
class FieldType(StrEnum):
    STR = "str"
    NUMBER = "number"
    DATE = "datetime"
    LIST = "list"
    ENUM = "enum"
    
class FieldDefinitionModel(BaseModel):
    name: str
    description: str
    required: bool = False
    field_type: FieldType
    enum_values: Optional[List[str]] = None  # Only used if type is ENUM
    
meeting_fields = [
    FieldDefinitionModel(
        name="title",
        description="What is the title of the meeting?",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="date",
        description="What was the date and time of the meeting?",
        required=True,
        field_type=FieldType.DATE,
    ),
    FieldDefinitionModel(
        name="attendees",
        description="Who attended the meeting? Please list all participants.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="action_items",
        description="What were the tasks discussed in the meeting? Please list all the tasks.",
        required=True,
        field_type=FieldType.STR,
    ),
    FieldDefinitionModel(
        name="decisions",
        description="What were the decisions taken during the meeting regarding the issues or new tasks? Please list all the decisions?",
        required=False,
        field_type=FieldType.STR,
    ),
    FieldDefinitionModel(
        name="notes",
        description="What were the key points discussed in the meeting? Please list them.",
        required=False,
        field_type=FieldType.STR,
    ),
    FieldDefinitionModel(
        name="next_steps",
        description="If there is some details of date and time of the next meeting, or some deliverables like report or email to be shared as a followup. Please list them.",
        required=False,
        field_type=FieldType.STR
    )
]

note_fields = [
    FieldDefinitionModel(
        name="title",
        description="Title of the note.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="content",
        description="Content of the note.",
        required=True,
        field_type=FieldType.STR
    ), FieldDefinitionModel(
        name="date",
        description="Date of the note created.",
        required=True,
        field_type=FieldType.DATE
    ), FieldDefinitionModel(
        name="category",
        description="Category of the note.",
        required=False,
        field_type=FieldType.STR
    )
]


task_fields = [
    FieldDefinitionModel(
        name="task_name",
        description="Name of the task.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="task_detail",
        description="What needs to be done in task? Explain briefly.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="assignee",
        description="Name of person who assigned the task. If no information is present then set assignee to 'SELF'",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="deadline",
        description="Last date or time to complete the task.",
        required=False,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="status",
        description="What is the current status of the task?",
        required=True,
        field_type=FieldType.ENUM,
        enum_values=["TODO", "IN_PROGRESS", "DONE", "BLOCKED"]
    ),
    FieldDefinitionModel(
        name="notes",
        description="What are the points to keep in mind for this task? List them.",
        required=False,
        field_type=FieldType.STR
    )
]

timesheet_fields = [
    FieldDefinitionModel(
        name="task",
        description="Give me a brief or the task id of the task assigned.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="date",
        description="The date on which task is assigned.",
        required=True,
        field_type=FieldType.DATE
    ),
    FieldDefinitionModel(
        name="hours_spent",
        description="What were the hours spent on the task?",
        required=True,
        field_type=FieldType.NUMBER
    ),
    FieldDefinitionModel(
        name="assignee",
        description="What is the name of person who assigned the task?",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="current_status",
        description="What is the current status of the task?",
        required=True,
        field_type=FieldType.ENUM,
        enum_values=["TODO", "IN_PROGRESS", "DONE", "BLOCKED"]
    ),
    FieldDefinitionModel(
        name="assigned_to",
        description="What is the name of the person the task is assigned to?",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="deadline",
        description="What is the last date or time to complete the task?",
        required=False,
        field_type=FieldType.STR
    ),
]

rewrite_fields = [
    FieldDefinitionModel(
        name="original_content",
        description="What do you want to rewrite? Share the text with me and I will rewrite it for you.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="target_audience",
        description="What is the target audience for this (e.g., academic, management, technical)",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="tone",
        description="What tone do you want for the text? Will it be formal, casual or technical?",
        required=False,
        field_type=FieldType.ENUM,
        enum_values=["formal", "casual", "technical"]
    ),
    FieldDefinitionModel(
        name="output_format",
        description="Select the output format of the text?",
        required=False,
        field_type=FieldType.ENUM,
        enum_values=["PDF", "DOCS", "MARKDOWN"]
    ),
    FieldDefinitionModel(
        name="notes",
        description="What are the points to keep in mind for the rewrite? List them.",
        required=False,
        field_type=FieldType.STR,
    )
]

report_fields = [
    FieldDefinitionModel(
        name="title",
        description="What should be the title of the report? Or do I suggest one?",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="content",
        description="What should be the content of the report. If you already have material (notes, data, outline), paste it. I will convert it into a structured report.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="report_type",
        description="What type of report do you want to make? Is it formal, analytic, operation or some other type? List them.",
        required=True,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="output_format",
        description="Any required format/style?",
        required=False,
        field_type=FieldType.STR
    ),
    FieldDefinitionModel(
        name="notes",
        description="What points should I keep in mind for this report?",
        required=False,
        field_type=FieldType.STR
    ),
]
    
MODE_SCHEMAS: dict[Mode, List[FieldDefinitionModel]] = {
    Mode.MEETING: meeting_fields,
    Mode.NOTES:note_fields,
    Mode.TASKS: task_fields,
    Mode.TIMESHEET: timesheet_fields,
    Mode.REWRITE: rewrite_fields,
    Mode.REPORT: report_fields
}



