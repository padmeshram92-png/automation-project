import time
import threading
import requests
from datetime import datetime
from backend.utils.logger import log_info, log_error
from backend.database.db import get_connection

# Global variables for automation
active_workflows = []
automation_thread = None
running = False

class TriggerMonitor:
    """Monitors triggers and executes workflows automatically"""

    def __init__(self):
        self.last_email_check = datetime.now()
        self.last_order_check = datetime.now()
        self.webhook_data = {}

    def check_new_email(self):
        """Check for new emails (placeholder - integrate with Gmail API)"""
        try:
            # Placeholder for email checking
            # In real implementation, use Gmail API or IMAP
            log_info("Checking for new emails...")

            # Simulate email check (replace with real API)
            # For now, return False (no new emails)
            return False

        except Exception as e:
            log_error(f"Error checking emails: {str(e)}")
            return False

    def check_new_order(self):
        """Check for new orders (placeholder - integrate with e-commerce API)"""
        try:
            # Placeholder for order checking
            # In real implementation, use Shopify, WooCommerce API, etc.
            log_info("Checking for new orders...")

            # Simulate order check (replace with real API)
            # For now, return False (no new orders)
            return False

        except Exception as e:
            log_error(f"Error checking orders: {str(e)}")
            return False

    def check_webhook_trigger(self, webhook_id):
        """Check if webhook was triggered"""
        if webhook_id in self.webhook_data:
            data = self.webhook_data[webhook_id]
            del self.webhook_data[webhook_id]  # Clear after use
            return data
        return None

    def execute_workflow_for_trigger(self, workflow, trigger_data=None):
        """Execute workflow when trigger fires"""
        try:
            log_info(f"🔥 Trigger fired! Executing workflow: {workflow.name}")

            # Import here to avoid circular import
            from backend.services.automation_engine import run_workflow

            # Run the workflow
            result = run_workflow(workflow)

            log_info(f"✅ Workflow executed automatically: {result}")

            return result

        except Exception as e:
            log_error(f"❌ Error executing automated workflow: {str(e)}")
            return {"status": "error", "message": str(e)}

# Global trigger monitor instance
trigger_monitor = TriggerMonitor()

def check_trigger(trigger_type, workflow=None):
    """
    Check if a trigger condition is met
    Used for manual workflow execution
    """
    if trigger_type == "manual_trigger":
        return True

    elif trigger_type == "new_email":
        return trigger_monitor.check_new_email()

    elif trigger_type == "new_order":
        return trigger_monitor.check_new_order()

    elif trigger_type == "webhook":
        # For manual check, webhook triggers need external data
        return False

    else:
        return False

def start_automation_engine():
    """Start the background automation engine"""
    global automation_thread, running

    if running:
        log_info("Automation engine already running")
        return

    running = True
    automation_thread = threading.Thread(target=automation_loop, daemon=True)
    automation_thread.start()

    log_info("🚀 Automation engine started - workflows will run automatically!")

def stop_automation_engine():
    """Stop the background automation engine"""
    global running
    running = False
    log_info("🛑 Automation engine stopped")

def automation_loop():
    """Main automation loop that runs in background"""
    log_info("🔄 Starting automation monitoring loop...")

    while running:
        try:
            # Check all active workflows for triggers
            for workflow in active_workflows[:]:  # Copy list to avoid modification issues
                try:
                    trigger_type = workflow.trigger.type

                    # Check trigger based on type
                    trigger_fired = False
                    trigger_data = None

                    if trigger_type == "new_email":
                        trigger_fired = trigger_monitor.check_new_email()

                    elif trigger_type == "new_order":
                        trigger_fired = trigger_monitor.check_new_order()

                    elif trigger_type == "webhook":
                        trigger_data = trigger_monitor.check_webhook_trigger(workflow.id)
                        trigger_fired = trigger_data is not None

                    elif trigger_type == "schedule":
                        # For scheduled workflows (every X minutes/hours)
                        # This would need more complex scheduling logic
                        pass

                    # Execute workflow if trigger fired
                    if trigger_fired:
                        trigger_monitor.execute_workflow_for_trigger(workflow, trigger_data)

                except Exception as e:
                    log_error(f"Error checking workflow {workflow.id}: {str(e)}")

            # Wait before next check (adjust polling interval)
            time.sleep(30)  # Check every 30 seconds

        except Exception as e:
            log_error(f"Error in automation loop: {str(e)}")
            time.sleep(60)  # Wait longer on error

def add_workflow_to_automation(workflow):
    """Add a workflow to automatic monitoring"""
    if workflow not in active_workflows:
        active_workflows.append(workflow)
        log_info(f"📝 Workflow '{workflow.name}' added to automation monitoring")

def remove_workflow_from_automation(workflow_id):
    """Remove a workflow from automatic monitoring"""
    global active_workflows
    active_workflows = [w for w in active_workflows if w.id != workflow_id]
    log_info(f"🗑️ Workflow {workflow_id} removed from automation")

def trigger_webhook(workflow_id, data=None):
    """Manually trigger a webhook for a workflow"""
    trigger_monitor.webhook_data[workflow_id] = data or {}
    log_info(f"🪝 Webhook triggered for workflow {workflow_id}")

def get_active_workflows():
    """Get list of workflows being monitored"""
    return active_workflows

def get_automation_status():
    """Get automation engine status"""
    return {
        "running": running,
        "active_workflows_count": len(active_workflows),
        "monitored_workflows": [w.name for w in active_workflows]
    }

