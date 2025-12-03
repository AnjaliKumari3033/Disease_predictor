from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = 'disease_model_xgb.pkl'
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
else:
    model = None  # Placeholder

# Dummy symptom list (replace with your actual one)
SYMPTOM_LIST = [
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
]

# Dummy disease info (replace with full descriptions)
DISEASE_INFO = {
" Acne" :"Acne is a prevalent skin condition marked by pimples, blackheads, and inflamed areas, often appearing on the face, back, and shoulders. It arises from clogged hair follicles and oil glands. Effective management involves good skin care and sometimes medical therapies to prevent scarring.",
"AIDS":"Acquired Immune Deficiency Syndrome is a chronic, life-altering illness caused by the Human Immunodeficiency Virus (HIV). It deteriorates the immune system, making the person extremely vulnerable to infections and certain cancers. Regular monitoring and antiretroviral treatment are vital to extend lifespan and improve quality of life.",
"Alcoholic Hepatitis":"Alcoholic hepatitis is liver inflammation due to excessive alcohol intake over time. It can cause symptoms like jaundice, nausea, abdominal pain, and fatigue. If untreated or if alcohol use continues, it can lead to permanent liver damage or failure.",
"Allergy":"Allergies are abnormal immune responses to substances such as pollen, foods, or animal dander. Reactions may range from mild sneezing and rashes to severe anaphylaxis. Management focuses on avoidance, symptom relief, and, in some cases, immunotherapy.",
"Arthritis":"Arthritis describes joint inflammation that leads to pain, swelling, stiffness, and reduced mobility. There are many types, affecting both young and older adults, and treatment depends on the cause and severity. It can impact daily activities if not managed properly.",
"Bronchial Asthma":"Bronchial asthma is a chronic lung disorder characterized by airway inflammation and narrowing. It causes recurrent wheezing, shortness of breath, chest tightness, and coughing. With proper inhaler use and avoiding triggers, most people live normal lives.",
"Cervical Spondylosis":"Cervical spondylosis is age-associated wear and tear affecting the spinal discs in the neck. It often leads to neck pain and stiffness, and can sometimes cause nerve problems like numbness or weakness in the arms. Treatment includes physiotherapy and medications to manage pain.",
"Chickenpox":"Chickenpox is a highly contagious viral disease causing an itchy, blistering skin rash accompanied by fever, tiredness, and headache. It typically affects children but can be more severe in adults. Vaccination offers excellent protection.",
"Chronic Cholestasis":"Chronic cholestasis occurs when bile flow from the liver is blocked over a sustained period, leading to symptoms such as jaundice, itching, and digestive disturbances. It can be due to liver diseases or bile duct obstruction, and may require long-term management and monitoring.",
"Common Cold":"The common cold is a mild, self-limited viral infection affecting the upper respiratory tract. Symptoms often include a runny nose, sore throat, sneezing, cough, and mild fever. Rest and supportive care usually result in recovery within a week.",
"Dengue":"Dengue is a mosquito-borne viral illness characterized by high fever, severe joint and muscle pain, headache, rash, and in serious cases, bleeding and shock. Prompt medical attention and fluid management are essential to reduce serious complications.",
"Diabetes":"Diabetes mellitus is a lifelong metabolic disorder in which the body cannot properly regulate blood sugar levels, leading to symptoms like increased thirst, urination, fatigue, and delayed healing. Complications can affect eyes, nerves, and organs if not controlled.",
"Dimorphic Hemmorhoids (piles)":"This condition, also called piles, involves swollen and inflamed veins in the rectum or anus. Patients may experience pain, itching, or bleeding during bowel movements. Lifestyle changes and treatments help manage symptoms and prevent recurrence.",
"Drug Reaction":"A drug reaction refers to unwanted effects that can occur with medication use, ranging from mild skin rashes to life-threatening allergic reactions. Early recognition and reporting to a physician are critical for appropriate management and safety.",
"Fungal Infection":"Fungal infections can affect the skin, nails, lungs or other organs. Symptoms depend on location, such as itching, redness, or scaling on the skin. Antifungal medicines are generally effective, but maintaining hygiene helps prevent recurrence.",
"Gastroenteritis":"Gastroesophageal Reflux Disease is a chronic condition where stomach acids flow back up into the esophagus, causing symptoms like heartburn, regurgitation, and discomfort after meals. Lifestyle changes and medications usually help relieve symptoms and prevent complications.",
"GERD":"Gastroenteritis is an inflammation of the lining of the stomach and intestines, typically from viral or bacterial infection. It causes vomiting, diarrhea, abdominal cramps, and dehydration. Most cases resolve with rest and hydration, but severe or persistent cases require medical care.",
"Heart Attack":"A heart attack, or myocardial infarction, occurs when blood supply to part of the heart muscle is stopped, often by a blocked artery. Symptoms include chest pain, shortness of breath, and nausea. Immediate medical attention saves lives and reduces complications.",
"Hepatitis A":"Hepatitis A is a viral liver infection spread through contaminated food or water. It causes jaundice, fatigue, abdominal pain, and loss of appetite but usually resolves fully with supportive care. Vaccination is available for prevention.",
"Hepatitis B":"Hepatitis B is a viral infection that aggressively attacks the liver and can cause both acute and chronic illness. It spreads via contact with infected blood or body fluids. Vaccination is highly effective, and treatment may include antiviral medications for chronic cases.",
"Hepatitis C":"Hepatitis C is mostly a bloodborne liver infection, frequently becoming chronic and leading to liver scarring or cancer over time. Early stages may cause few symptoms. Modern direct antiviral medications offer very high cure rates.",
"Hepatitis D": "This rare liver infection only occurs in those already infected with hepatitis B. It can worsen liver disease severity and is found in certain high-risk populations. Preventing hepatitis B is key for limiting hepatitis D.",
"Hepatitis E":"Hepatitis E is an acute viral liver infection often spread by contaminated water, mainly prevalent in developing regions. It usually resolves on its own but can be severe in pregnant women or those with weakened immune systems.",
"Hypertension ":"Hypertension, or high blood pressure, is a common condition that often causes no symptoms but dramatically raises the risk of stroke, heart attack, and kidney disease if uncontrolled. Management relies on lifestyle modification and, if needed, medication.",
"Hyperthyroidism":"Hyperthyroidism is the excessive production of thyroid hormone, causing symptoms such as weight loss, rapid heartbeat, sweating, and anxiety. Treatment options include medication, radioactive iodine, or surgery, depending on severity and cause.",
"Hypoglycemia":"Hypoglycemia means abnormally low blood sugar, most often seen in people with diabetes due to medication or skipping meals. Symptoms include shakiness, confusion, sweating, and in severe cases, loss of consciousness. Prompt treatment with sugar restores normal levels.",
"Hypothyroidism":"Hypothyroidism is when the thyroid gland doesn’t produce enough hormones, resulting in fatigue, weight gain, cold intolerance, and slowed metabolism. It is generally managed with daily thyroid hormone replacement.",
"Impetigo":"Impetigo is a contagious bacterial skin infection appearing as red sores or blisters, common in young children. It spreads easily in schools and daycares. Quick treatment with topical or oral antibiotics leads to a complete cure.",
"Jaundice":"Jaundice causes yellowing of the skin and eyes, resulting from increased bilirubin levels in the blood. It signals problems with the liver, bile ducts, or red blood cells. Identifying and treating the underlying cause is essential for recovery.",
"Malaria":"Malaria is a life-threatening disease transmitted by mosquito bites, common in some tropical regions. It leads to fever, chills, and flu-like symptoms, and can be fatal without prompt diagnosis and treatment with antimalarial drugs.",
"Migraine":"Migraine is a recurrent, often intense headache, sometimes accompanied by nausea, sensitivity to light/sound, and visual disturbances (“aura”). Triggers may include stress, foods, or hormonal changes. Individualized preventive and acute treatments are available.",
"Osteoarthritis":"Osteoarthritis is a degenerative disease causing the cartilage in joints to break down, leading to pain, stiffness, and limited movement, mostly in older adults. Weight management, exercise, and pain relief medicines optimize quality of life.",
"Paralysis (brain hemorrhage)":"Paralysis is the loss of voluntary muscle function in one or more parts of the body, usually from nerve or brain injury. Causes vary from stroke to trauma or infections. Early rehabilitation and medical care influence recovery and adaptation.",
"Peptic Ulcer Disease":"Peptic ulcer disease involves sores in the lining of the stomach or upper small intestine, often resulting from Helicobacter pylori infection or chronic anti-inflammatory use. Symptoms include burning stomach pain and nausea. Treatment targets infection and acid suppression.",
"Pneumonia":"Pneumonia is an infection of the lungs that fills air sacs with pus or fluid, leading to cough, fever, chest pain, and difficulty breathing. It can be caused by bacteria, viruses, or fungi and is more dangerous in infants, the elderly, or those with chronic illnesses.",
"Psoriasis":"Psoriasis is a long-term, immune-mediated skin disease that speeds up skin cell growth, resulting in red, scaly patches commonly on the elbows, scalp, or knees. Flare-ups can be triggered by stress, infections, or injuries. Treatment includes topical or systemic therapies.",
"Tuberculosis":"Tuberculosis (TB) is a bacterial infection mainly affecting the lungs but can spread to other organs. Symptoms include a chronic cough, weight loss, fever, and night sweats. Treatment is prolonged but highly effective if the full antibiotic course is completed.",
"Typhoid":"Typhoid is a serious bacterial infection, usually contracted through contaminated food or water. It causes prolonged fever, abdominal pain, diarrhea or constipation, and weakness. Vaccines and antibiotics are available to prevent and treat this disease.",
"Urinary Tract Infection":"UTIs are bacterial infections of the urinary system—bladder, urethra, or kidneys—causing frequent urination, discomfort, and cloudy urine. They are especially common in women and are treated effectively with antibiotics.",
"Varicose Veins":"Varicose veins are enlarged, twisted veins, most often appearing in the legs. They may cause aching, swelling, and skin color changes, especially after standing for long periods. Therapies include lifestyle changes, compression stockings, or surgical procedures.",
"Vertigo":"Vertigo is the sensation that you or your surroundings are spinning, often caused by problems with the inner ear. It may be accompanied by nausea or loss of balance. Treatment depends on the underlying cause and often involves medication or physical therapy."

}

predicted_disease_name = None  # Global to store last predicted disease

# Normalize DISEASE_INFO keys (strip spaces)
NORMALIZED_DISEASE_INFO = {k.strip(): v for k, v in DISEASE_INFO.items()}

def get_disease_info(disease_name):
    return NORMALIZED_DISEASE_INFO.get(disease_name.strip(), "No information available.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predictor')
def predictor():
    return render_template('predictor.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    selected_symptoms = data.get('symptoms', [])
    selected_symptoms = [s.strip().lower() for s in selected_symptoms]
    input_vector = [1 if symptom in selected_symptoms else 0 for symptom in SYMPTOM_LIST]

    probabilities = model.predict_proba([input_vector])[0]
    top3_indices = sorted(range(len(probabilities)), key=lambda i: probabilities[i], reverse=True)[:3]
    disease_labels = ['AIDS', 'Acne', 'Alcoholic Hepatitis', 'Allergy', 'Arthritis',
        'Bronchial Asthma', 'Cervical Spondylosis', 'Chickenpox','Chronic Cholestasis', 'Common Cold', 'Dengue', 'Diabetes',
        'Dimorphic Hemmorhoids (piles)', 'Drug Reaction', 'Fungal Infection',
        'GERD', 'Gastroenteritis', 'Heart Attack', 'Hepatitis A',
        'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
        'Hypertension', 'Hyperthyroidism', 'Hypoglycemia', 'Hypothyroidism',
        'Impetigo', 'Jaundice', 'Malaria', 'Migraine', 'Osteoarthritis',
        'Paralysis (brain hemorrhage)', 'Peptic Ulcer Disease', 'Pneumonia','Psoriasis', 'Tuberculosis', 'Typhoid', 'Urinary Tract Infection',
        'Varicose Veins', 'Vertigo']
    top3_diseases = [disease_labels[i] for i in top3_indices]
    top3_probs = [float(round(float(probabilities[i]) * 100, 2)) for i in top3_indices]

    # Use the helper to get info for each disease
    top3_info = [get_disease_info(d) for d in top3_diseases]

    return jsonify({'diseases': top3_diseases, 'info': top3_info, 'probs': top3_probs})

@app.route('/disease-info')
def disease_info():
    global predicted_disease_name
    info = DISEASE_INFO.get(predicted_disease_name, "No information available.")
    return render_template('info.html', disease=predicted_disease_name, info=info)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

