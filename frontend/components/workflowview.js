export function renderWorkflowView(containerId, workflow) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!workflow) {
        container.innerHTML = '<div class="empty-state"><p>Generate a workflow to see preview</p></div>';
        return;
    }

    const triggerValue = workflow.trigger?.type || workflow.trigger || "N/A";
    const aiValue = workflow.ai_step?.type || workflow.ai_step || "N/A";
    const actionValue = workflow.action?.type || workflow.action || "N/A";

    container.innerHTML = `
        <div class="workflow-diagram">
            <div class="workflow-step trigger">
                <div class="step-icon">Trigger</div>
                <div class="step-title">Trigger</div>
                <div class="step-value">${triggerValue}</div>
            </div>

            <div class="workflow-arrow">-&gt;</div>

            <div class="workflow-step ai">
                <div class="step-icon">AI</div>
                <div class="step-title">AI Step</div>
                <div class="step-value">${aiValue}</div>
            </div>

            <div class="workflow-arrow">-&gt;</div>

            <div class="workflow-step action">
                <div class="step-icon">Action</div>
                <div class="step-title">Action</div>
                <div class="step-value">${actionValue}</div>
            </div>
        </div>
    `;
}
