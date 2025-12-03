// List of symptoms (should match your SYMPTOM_LIST in app.py)
const SYMPTOM_LIST = [
    "Fever", "Headache", "Cough", "Sore throat", "Runny nose", "Body aches", "Fatigue", "Nausea", "Vomiting", "Diarrhea",
    "Abdominal pain", "Chest pain", "Skin rash", "Shortness of breath", "Dizziness", "Joint pain", "Loss of appetite",
    "Weight loss", "Night sweats", "Chills", "Congestion", "Sneezing"
    // ...add all your symptoms here
];

const grid = document.getElementById('symptom-grid');
SYMPTOM_LIST.forEach(symptom => {
    const label = document.createElement('label');
    label.className = 'symptom-checkbox';
    label.innerHTML = `<input type="checkbox" value="${symptom}"> ${symptom}`;
    grid.appendChild(label);
});

const form = document.getElementById('symptom-form');
const resultDiv = document.getElementById('result');
const reportedDiv = document.getElementById('reported-symptoms');

form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const checked = Array.from(document.querySelectorAll('#symptom-grid input:checked')).map(cb => cb.value);
    // Show reported symptoms as tags
    if (checked.length > 0) {
        reportedDiv.style.display = '';
        reportedDiv.innerHTML = `<div class="reported-title">Your Reported Symptoms</div>` +
            checked.map(s => `<span class="symptom-tag">${s}</span>`).join(' ');
    } else {
        reportedDiv.style.display = 'none';
        reportedDiv.innerHTML = '';
    }
    resultDiv.textContent = 'Analyzing...';
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symptoms: checked })
        });
        const data = await response.json();
        if (data.diseases && data.diseases.length > 0) {
            let html = '<div class="result-card"><b>Top 3 Possible Diseases:</b><br>';
            data.diseases.forEach((disease, i) => {
                html += `<div style="margin-bottom:10px;">
                            <b>${disease}</b><br>
                            <span style="font-size:14px;white-space:pre-line;">${data.info ? data.info[i] : ''}</span>
                        </div>`;
            });
            html += '</div>';
            resultDiv.innerHTML = html;
        } else {
            resultDiv.innerHTML = '<div class="result-card">No diseases found.</div>';
        }
    } catch (err) {
        resultDiv.innerHTML = '<div class="result-card">Error predicting diseases.</div>';
    }
});
