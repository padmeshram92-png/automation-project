export function renderPromptInput(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = `
        <p class="section-description">Describe what you want to automate in natural language</p>

        <div class="input-group">
            <label for="prompt-input">Your Workflow Description</label>
            <textarea
                id="prompt-input"
                class="prompt-textarea"
                placeholder="Example: Send email summary when new orders arrive and classify them by type"
                rows="4"></textarea>
        </div>

        <div class="button-group">
            <button id="generate-btn" class="btn btn-primary">
                Generate Workflow
            </button>
            <button id="reset-btn" class="btn btn-secondary">
                Reset
            </button>
        </div>

        <div id="status-message" class="status-message"></div>
    `;
}
