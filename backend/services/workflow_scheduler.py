"""
Workflow Scheduler - Runs workflows automatically like n8n
"""
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
from backend.utils.logger import log_info, log_error
from backend.services.automation_engine import run_workflow
from backend.services.trigger_service import check_trigger
from backend.models.workflow_model import Workflow


class WorkflowScheduler:
    """Background scheduler that runs workflows automatically"""

    def __init__(self):
        self.running_workflows: Dict[str, Workflow] = {}
        self.workflow_threads: Dict[str, threading.Thread] = {}
        self.is_running = False
        self.check_interval = 30  # seconds

    def start_scheduler(self):
        """Start the background scheduler"""
        if self.is_running:
            log_info("Scheduler already running")
            return

        self.is_running = True
        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        scheduler_thread.start()
        log_info("Workflow scheduler started")

    def stop_scheduler(self):
        """Stop the background scheduler"""
        self.is_running = False
        log_info("Workflow scheduler stopped")

    def add_workflow(self, workflow: Workflow):
        """Add a workflow to be monitored and executed automatically"""
        workflow_id = workflow.id or str(hash(workflow.name))

        if workflow_id in self.running_workflows:
            log_info(f"Workflow {workflow.name} already running")
            return

        self.running_workflows[workflow_id] = workflow

        # Start monitoring thread for this workflow
        thread = threading.Thread(
            target=self._monitor_workflow,
            args=(workflow,),
            daemon=True
        )
        self.workflow_threads[workflow_id] = thread
        thread.start()

        log_info(f"Added workflow to scheduler: {workflow.name}")

    def remove_workflow(self, workflow_id: str):
        """Remove a workflow from automatic execution"""
        if workflow_id in self.running_workflows:
            del self.running_workflows[workflow_id]
            log_info(f"Removed workflow from scheduler: {workflow_id}")

    def list_active_workflows(self) -> List[Workflow]:
        """Get list of currently active workflows"""
        return list(self.running_workflows.values())

    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.is_running:
            try:
                # Check all running workflows
                for workflow_id, workflow in list(self.running_workflows.items()):
                    if not self.is_running:
                        break

                    try:
                        # Check if workflow trigger conditions are met
                        if self._should_run_workflow(workflow):
                            self._execute_workflow_async(workflow)
                    except Exception as e:
                        log_error(f"Error checking workflow {workflow.name}: {str(e)}")

            except Exception as e:
                log_error(f"Scheduler loop error: {str(e)}")

            time.sleep(self.check_interval)

    def _monitor_workflow(self, workflow: Workflow):
        """Monitor a specific workflow for trigger conditions"""
        workflow_id = workflow.id or str(hash(workflow.name))

        while self.is_running and workflow_id in self.running_workflows:
            try:
                if self._should_run_workflow(workflow):
                    self._execute_workflow_async(workflow)

                # Check every 10 seconds for this workflow
                time.sleep(10)

            except Exception as e:
                log_error(f"Error monitoring workflow {workflow.name}: {str(e)}")
                time.sleep(30)  # Wait longer on error

    def _should_run_workflow(self, workflow: Workflow) -> bool:
        """Check if a workflow should be executed based on its trigger"""
        trigger_type = workflow.trigger.type

        # Skip manual triggers - they should be run manually
        if trigger_type == "manual_trigger":
            return False

        # Check trigger conditions
        return check_trigger(trigger_type)

    def _execute_workflow_async(self, workflow: Workflow):
        """Execute a workflow asynchronously"""
        def run_async():
            try:
                log_info(f"Auto-executing workflow: {workflow.name}")
                result = run_workflow(workflow)
                log_info(f"Workflow {workflow.name} completed: {result}")
            except Exception as e:
                log_error(f"Error executing workflow {workflow.name}: {str(e)}")

        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()


# Global scheduler instance
workflow_scheduler = WorkflowScheduler()


def start_workflow_scheduler():
    """Start the global workflow scheduler"""
    workflow_scheduler.start_scheduler()


def stop_workflow_scheduler():
    """Stop the global workflow scheduler"""
    workflow_scheduler.stop_scheduler()


def add_workflow_to_scheduler(workflow: Workflow):
    """Add workflow to automatic execution"""
    workflow_scheduler.add_workflow(workflow)


def remove_workflow_from_scheduler(workflow_id: str):
    """Remove workflow from automatic execution"""
    workflow_scheduler.remove_workflow(workflow_id)


def get_active_workflows():
    """Get list of automatically running workflows"""
    return workflow_scheduler.list_active_workflows()


def get_scheduler():
    """Get the global workflow scheduler instance"""
    return workflow_scheduler
