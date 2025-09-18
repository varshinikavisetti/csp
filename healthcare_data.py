# Healthcare dataset — 50+ diseases (common, chronic, mental, rare)
# NOTE: Educational purposes only — not medical advice.

DISEASE_DB = {
    # 🔹 Infectious Diseases
    "influenza": {
        "aliases": ["flu", "influenza"],
        "symptoms": ["fever", "cough", "sore throat", "runny nose", "chills", "muscle aches"],
        "medicines": "Rest, fluids, paracetamol, antivirals in severe cases.",
        "precautions": "Vaccination, rest, hydration.",
        "specialist": "General Physician"
    },
    "covid-19": {
        "aliases": ["covid", "coronavirus", "covid-19"],
        "symptoms": ["fever", "dry cough", "loss of smell", "loss of taste", "fatigue", "breathing difficulty"],
        "medicines": "Supportive care, antivirals, oxygen support.",
        "precautions": "Isolation, mask, vaccination.",
        "specialist": "Pulmonologist"
    },
    "tuberculosis": {
        "aliases": ["tb", "tuberculosis"],
        "symptoms": ["persistent cough", "coughing blood", "night sweats", "weight loss", "fever"],
        "medicines": "Long-course antibiotics (DOTS therapy).",
        "precautions": "Seek medical care quickly, avoid close contact.",
        "specialist": "Infectious Disease Specialist"
    },
    "malaria": {
        "aliases": ["malaria"],
        "symptoms": ["fever", "chills", "headache", "nausea", "fatigue", "sweating"],
        "medicines": "Antimalarial drugs.",
        "precautions": "Mosquito nets, prophylaxis for travelers.",
        "specialist": "Infectious Disease Specialist"
    },
    "dengue": {
        "aliases": ["dengue fever"],
        "symptoms": ["high fever", "rash", "headache", "joint pain", "muscle pain", "eye pain"],
        "medicines": "Fluids, paracetamol (avoid NSAIDs).",
        "precautions": "Mosquito prevention.",
        "specialist": "General Physician"
    },
    "typhoid": {
        "aliases": ["typhoid", "enteric fever"],
        "symptoms": ["high fever", "abdominal pain", "headache", "constipation", "diarrhea"],
        "medicines": "Antibiotics (prescription).",
        "precautions": "Safe food and water, vaccination.",
        "specialist": "General Physician"
    },
    "hepatitis b": {
        "aliases": ["hepatitis b"],
        "symptoms": ["jaundice", "fatigue", "abdominal pain", "nausea"],
        "medicines": "Antivirals (doctor prescribed).",
        "precautions": "Avoid alcohol, vaccination available.",
        "specialist": "Gastroenterologist"
    },
    "chickenpox": {
        "aliases": ["chickenpox", "varicella"],
        "symptoms": ["itchy rash", "blisters", "fever", "tiredness"],
        "medicines": "Antihistamines, calamine lotion, antivirals if needed.",
        "precautions": "Isolation until blisters dry, vaccine available.",
        "specialist": "General Physician"
    },
    "measles": {
        "aliases": ["measles"],
        "symptoms": ["rash", "fever", "cough", "red eyes", "runny nose"],
        "medicines": "Supportive care, vitamin A.",
        "precautions": "MMR vaccination.",
        "specialist": "General Physician"
    },

    # 🔹 Respiratory Diseases
    "asthma": {
        "aliases": ["asthma", "wheezing"],
        "symptoms": ["shortness of breath", "wheezing", "coughing", "chest tightness"],
        "medicines": "Inhalers (bronchodilators, corticosteroids).",
        "precautions": "Avoid triggers, carry inhaler.",
        "specialist": "Pulmonologist"
    },
    "pneumonia": {
        "aliases": ["pneumonia"],
        "symptoms": ["fever", "cough", "chest pain", "breathing difficulty"],
        "medicines": "Antibiotics if bacterial, fluids.",
        "precautions": "Vaccination, see doctor urgently if severe.",
        "specialist": "Pulmonologist"
    },
    "bronchitis": {
        "aliases": ["bronchitis"],
        "symptoms": ["cough", "fatigue", "shortness of breath", "mucus"],
        "medicines": "Rest, fluids, antibiotics if bacterial.",
        "precautions": "Avoid smoking, hydrate.",
        "specialist": "Pulmonologist"
    },

    # 🔹 Chronic Diseases
    "diabetes": {
        "aliases": ["diabetes", "blood sugar"],
        "symptoms": ["frequent urination", "increased thirst", "weight loss", "blurred vision"],
        "medicines": "Insulin, metformin, diet changes.",
        "precautions": "Sugar monitoring, exercise, diet.",
        "specialist": "Endocrinologist"
    },
    "hypertension": {
        "aliases": ["high blood pressure", "hypertension"],
        "symptoms": ["headache", "dizziness", "chest pain", "vision problems"],
        "medicines": "Antihypertensives.",
        "precautions": "Low-salt diet, stress management.",
        "specialist": "Cardiologist"
    },
    "anemia": {
        "aliases": ["anemia", "low hemoglobin"],
        "symptoms": ["fatigue", "pale skin", "dizziness", "shortness of breath"],
        "medicines": "Iron supplements, vitamin B12, folic acid.",
        "precautions": "Diet rich in iron, doctor supervision.",
        "specialist": "Hematologist"
    },
    "arthritis": {
        "aliases": ["arthritis", "joint pain"],
        "symptoms": ["joint pain", "stiffness", "swelling", "mobility issues"],
        "medicines": "Painkillers, physiotherapy, disease-modifying drugs.",
        "precautions": "Regular exercise, weight management.",
        "specialist": "Rheumatologist"
    },
    "migraine": {
        "aliases": ["migraine", "severe headache"],
        "symptoms": ["headache", "nausea", "light sensitivity", "visual disturbances"],
        "medicines": "Painkillers, triptans.",
        "precautions": "Avoid triggers, rest in quiet space.",
        "specialist": "Neurologist"
    },
    "thyroid disorder": {
        "aliases": ["thyroid", "hypothyroidism", "hyperthyroidism"],
        "symptoms": ["weight change", "fatigue", "hair loss", "mood swings"],
        "medicines": "Thyroxine or antithyroid drugs.",
        "precautions": "Regular thyroid tests.",
        "specialist": "Endocrinologist"
    },

    # 🔹 Mental Health
    "depression": {
        "aliases": ["depression", "low mood"],
        "symptoms": ["sadness", "loss of interest", "sleep issues", "fatigue"],
        "medicines": "Antidepressants, therapy.",
        "precautions": "Counseling, support, lifestyle management.",
        "specialist": "Psychiatrist"
    },
    "anxiety disorder": {
        "aliases": ["anxiety", "gad"],
        "symptoms": ["excessive worry", "sweating", "palpitations", "restlessness"],
        "medicines": "SSRIs, therapy.",
        "precautions": "Relaxation, meditation.",
        "specialist": "Psychiatrist"
    },
    "bipolar disorder": {
        "aliases": ["bipolar"],
        "symptoms": ["mood swings", "mania", "depression", "irritability"],
        "medicines": "Mood stabilizers, therapy.",
        "precautions": "Medication adherence.",
        "specialist": "Psychiatrist"
    },
    "schizophrenia": {
        "aliases": ["schizophrenia"],
        "symptoms": ["hallucinations", "delusions", "disorganized speech"],
        "medicines": "Antipsychotics, therapy.",
        "precautions": "Regular treatment, family support.",
        "specialist": "Psychiatrist"
    },
    "ptsd": {
        "aliases": ["ptsd", "post traumatic stress disorder"],
        "symptoms": ["flashbacks", "nightmares", "avoidance", "anxiety"],
        "medicines": "Therapy, antidepressants.",
        "precautions": "Support groups, counseling.",
        "specialist": "Psychiatrist"
    },
    "ocd": {
        "aliases": ["ocd", "obsessive compulsive disorder"],
        "symptoms": ["repetitive thoughts", "compulsions", "anxiety"],
        "medicines": "SSRIs, therapy.",
        "precautions": "Stress management.",
        "specialist": "Psychiatrist"
    },

    # 🔹 Rare Diseases
    "als": {
        "aliases": ["als", "amyotrophic lateral sclerosis"],
        "symptoms": ["muscle weakness", "twitching", "speech difficulty", "breathing problems"],
        "medicines": "Riluzole, supportive care.",
        "precautions": "Therapy, assistive devices.",
        "specialist": "Neurologist"
    },
    "huntington's disease": {
        "aliases": ["huntington"],
        "symptoms": ["involuntary movements", "cognitive decline", "mood changes"],
        "medicines": "No cure, supportive care.",
        "precautions": "Therapy, counseling.",
        "specialist": "Neurologist"
    },
    "sickle cell anemia": {
        "aliases": ["sickle cell"],
        "symptoms": ["pain episodes", "fatigue", "infections", "delayed growth"],
        "medicines": "Hydroxyurea, transfusions.",
        "precautions": "Hydration, avoid infections.",
        "specialist": "Hematologist"
    }
}
