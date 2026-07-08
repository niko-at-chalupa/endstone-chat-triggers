from endstone import Logger
from pathlib import Path
from .models import Workflow, FailedWorkflow
from .parser import parse_workflow


class WorkflowManager:
    workflows: list[Workflow]
    failed_workflows: list[FailedWorkflow]

    def __init__(self, folder: Path, logger: Logger):
        self.folder = folder
        self.folder.mkdir(parents=True, exist_ok=True)
        self._logger = logger
        self.workflows: list[Workflow] = []
        self.failed_workflows: list[FailedWorkflow] = []

    def scan_for_workflows(self):
        workflow_files = [
            file
            for file in self.folder.iterdir()
            if file.suffix.lower() in [".yml", ".yaml"]
        ]

        self.workflows.clear()
        self.failed_workflows.clear()
        
        for file in workflow_files:
            try:
                parsed_workflow = parse_workflow(file)
                match parsed_workflow:
                    case Workflow():
                        self.workflows.append(parsed_workflow)
                    case FailedWorkflow():
                        self.failed_workflows.append(parsed_workflow)
            except Exception as e:
                self._logger.error(f"Error while parsing workflow {file.name}:\n{e}")
