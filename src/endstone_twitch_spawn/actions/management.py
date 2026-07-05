from endstone import Logger
from pathlib import Path
from .models import Workflow
from .parser import parse_workflow_file

class WorkflowManager:
    def __init__(self, folder: Path, logger: Logger):
        self.folder = folder
        self.folder.mkdir(parents=True, exist_ok=True)
        self._logger = logger
        self.workflows: list[Workflow] = []

    def scan_for_workflows(self):
        workflow_files = [
            file for file in self.folder.iterdir()
            if file.suffix.lower() in [".yml", ".yaml"]
        ]

        self.workflows.clear()
        for file in workflow_files:
            try:
                self.workflows.append(parse_workflow_file(file))
            except Exception as e:
                self._logger.error(f"Error while parsing workflow {file.name}:\n{e}")