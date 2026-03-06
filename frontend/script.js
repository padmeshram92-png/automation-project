import { renderPromptInput } from "./components/promptinput.js";
import { renderTriggerActionUI } from "./components/triggeractionUI.js";

// ==================== Configuration ====================
const API_BASE_URL = "http://127.0.0.1:8001";
let currentWorkflow = null;
let savedWorkflows = [];

// ==================== Event Listeners ====================
function initializeEventListeners() {


document.getElementById("generate-btn").addEventListener("click", generateWorkflow);
document.getElementById("reset-btn").addEventListener("click", resetForm);
document.getElementById("save-btn").addEventListener("click", saveWorkflow);
document.getElementById("run-btn").addEventListener("click", runWorkflow);
document.getElementById("set-api-key-btn").addEventListener("click", setApiKey);
document.getElementById("list-api-keys-btn").addEventListener("click", listApiKeys);
document.querySelector(".close").addEventListener("click", closeModal);

window.addEventListener("click", (event) => {
    const modal = document.getElementById("modal");
    if (event.target === modal) {
        closeModal();
    }
    
});


}

// ==================== API Connection Check ====================
async function checkAPIConnection() {


try {

    const response = await fetch(`${API_BASE_URL}`);

    if (response.ok) {
        updateAPIStatus(true);
    } else {
        updateAPIStatus(false);
    }

} catch (error) {

    updateAPIStatus(false);

}


}

function updateAPIStatus(isConnected) {


const indicator = document.getElementById("api-status-indicator");
const text = document.getElementById("api-status-text");

if (isConnected) {

    indicator.classList.remove("disconnected");
    indicator.classList.add("connected");

    text.textContent = "API Connected ✓";

} else {

    indicator.classList.remove("connected");
    indicator.classList.add("disconnected");

    text.textContent = "API Disconnected ✗";

}


}

// ==================== Generate Workflow ====================
async function generateWorkflow() {

const promptInput = document.getElementById("prompt-input");
if (!promptInput) {
console.error("Prompt input element not found");
showStatus("Prompt input not found", "error");
return;
}

const prompt = promptInput.value.trim();

if (!prompt) {
showStatus("Please enter a workflow description", "error");
return;
}

showLoading(true);
showStatus("");

try {

const response = await fetch(`${API_BASE_URL}/api/prompt/generate-workflow`, {
method: "POST",
headers: { "Content-Type": "application/json" },
body: JSON.stringify({ prompt })
});

if (!response.ok) {
const text = await response.text();
throw new Error("API request failed: " + text);
}

const data = await response.json();
console.log("Workflow response:", data);

// backend sometimes returns {workflow:{...}} or directly {...}
const workflow = data.workflow ? data.workflow : data;

currentWorkflow = workflow;

displayWorkflow(workflow);
displayWorkflowDetails(workflow);

showStatus("Workflow generated successfully!", "success");

document.getElementById("save-btn").style.display = "inline-block";
document.getElementById("run-btn").style.display = "inline-block";

} catch (error) {
console.error("Generate workflow error:", error);
showStatus("Error generating workflow", "error");
} finally {
showLoading(false);
}

}


// ==================== Display Workflow ====================
function displayWorkflow(workflow) {


renderTriggerActionUI("workflow-container", workflow);


}

function displayWorkflowDetails(workflow) {


const container = document.getElementById("details-container");

const html = `
    <div class="details-grid">

        <div class="detail-item">
            <h4>Workflow Name</h4>
            <p>${workflow.name}</p>
        </div>

        <div class="detail-item">
            <h4>Status</h4>
            <span class="status-badge status-${workflow.status}">
                ${workflow.status.toUpperCase()}
            </span>
        </div>

        <div class="detail-item">
            <h4>Trigger</h4>
            <p>${workflow.trigger.type}</p>
        </div>

        <div class="detail-item">
            <h4>AI Step</h4>
            <p>${workflow.ai_step.type}</p>
        </div>

        <div class="detail-item">
            <h4>Action</h4>
            <p>${workflow.action.type}</p>
        </div>

    </div>
`;

container.innerHTML = html;


}

// ==================== Save Workflow ====================
async function saveWorkflow(){

if(!currentWorkflow){
showStatus("No workflow to save","error");
return;
}

try{

const response = await fetch(`${API_BASE_URL}/api/workflow/create`,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify(currentWorkflow)

});

if(!response.ok){
throw new Error("Save failed");
}

const data = await response.json();

console.log(data);

showStatus("Workflow saved successfully","success");

savedWorkflows.push(currentWorkflow);

displaySavedWorkflows();

}catch(error){

console.error(error);

showStatus("Error saving workflow","error");

}

}

// ==================== Run Workflow ====================
async function runWorkflow() {

console.log("RUN BUTTON CLICKED");
console.log("Workflow data:", currentWorkflow);


if (!currentWorkflow) {
    showStatus("No workflow to run", "error");
    return;
}
currentWorkflow.recipient = "yourgmail@gmail.com";
currentWorkflow.subject = "Workflow Test";
currentWorkflow.message = "Hello from automation";


try {

    const response = await fetch(`${API_BASE_URL}/api/workflow/run`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(currentWorkflow)

    });

    if (!response.ok) {
    throw new Error("API request failed");
   }
    console.log("Response status:", response.status);

    const data = await response.json();

    console.log("Response data:",data);
    
    if (data.result && data.result.status === "success") {
        showStatus("Workflow executed successfully", "success");
    } 
    else {
        showStatus("Workflow executed but skipped", "info");
    }

    

}

catch (error) {
    
    console.error(error);
    showStatus("Error running workflow", "error");

}


}

// ==================== Helpers ====================
function resetForm() {


document.getElementById("prompt-input").value = "";

document.getElementById("workflow-container").innerHTML =
    "<p>Generate workflow to see preview</p>";

document.getElementById("details-container").innerHTML =
    "<p>No workflow generated</p>";


}

function showStatus(message, type = "info") {


const status = document.getElementById("status-message");

status.textContent = message;
status.className = `status-${type}`;


}

function showLoading(show) {


const spinner = document.getElementById("loading-spinner");

spinner.style.display = show ? "flex" : "none";


}

function showModal(title, content) {


document.getElementById("modal-title").textContent = title;
document.getElementById("modal-body").innerHTML = content;

document.getElementById("modal").style.display = "block";


}

function closeModal() {


document.getElementById("modal").style.display = "none";


}
async function listApiKeys(){


console.log("List keys clicked")

const res = await fetch("http://127.0.0.1:8001/api/admin/api-keys")

const data = await res.json()

console.log(data)

const container = document.getElementById("api-keys-list")


container.style.display = "block"

container.innerHTML = data.api_keys
.map(key => `<p>${key}</p>`)
.join("")

}
async function setApiKey(){

const keyName = document.getElementById("api-key-name").value.trim();
const keyValue = document.getElementById("api-key-value").value.trim();

if(!keyName || !keyValue){
alert("Enter key name and value");
return;
}

const res = await fetch(`${API_BASE_URL}/api/admin/set-api-key`,{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
key_name:keyName,
key_value:keyValue
})
});

const data = await res.json();

console.log(data);

alert("API key saved successfully");

}

// ==================== Init ====================
document.addEventListener("DOMContentLoaded", () => {

renderPromptInput("prompt-input-component");

initializeEventListeners();

checkAPIConnection();


});

// Check API every 10 seconds
setInterval(() => {
checkAPIConnection();
}, 10000);
