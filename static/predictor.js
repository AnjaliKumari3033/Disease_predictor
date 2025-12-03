// Full list of symptoms (should match SYMPTOM_LIST in app.py)
const SYMPTOM_LIST = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_ urination',
    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
    'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
    'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
    'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid',
    'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech',
    'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability',
    'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic _patches',
    'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
    'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
    'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum', 'prominent_veins_on_calf',
    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting',
    'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze'
];

const grid = document.getElementById('symptom-grid');
SYMPTOM_LIST.forEach(symptom => {
    const label = document.createElement('label');
    label.className = 'symptom-checkbox';
    label.innerHTML = `<input type="checkbox" value="${symptom}"> ${symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}`;
    grid.appendChild(label);
});

// Custom symptom logic
const addBtn = document.getElementById('add-custom-symptom');
const customInput = document.getElementById('custom-symptom-input');
addBtn.addEventListener('click', function() {
    let val = customInput.value.trim();
    if (!val) return;
    // Normalize for duplicate check
    let normalized = val.toLowerCase().replace(/\s+/g, '_');
    // Prevent duplicates
    if (Array.from(document.querySelectorAll('#symptom-grid input')).some(cb => cb.value.toLowerCase() === normalized)) {
        customInput.value = '';
        return;
    }
    const label = document.createElement('label');
    label.className = 'symptom-checkbox';
    label.innerHTML = `<input type="checkbox" value="${val}" checked> ${val.charAt(0).toUpperCase() + val.slice(1)}`;
    grid.appendChild(label);
    customInput.value = '';
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
            checked.map(s => `<span class="symptom-tag">${s.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>`).join(' ');
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
                const prob = data.probs && data.probs[i] !== undefined ? ` (${data.probs[i]}%)` : '';
                html += `<div style="margin-bottom:10px;">
                            <b>${disease}${prob}</b><br>
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