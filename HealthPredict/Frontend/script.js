// -------- I18N --------
const translations = {
    bs: {
        language_label: "Jezik:",
        bs: "Bosanski",
        en: "Engleski",
        predict_title: "Predikcija bolesti srca",
        age: "Starost",
        sex: "Spol",
        select: "Odaberi",
        male: "Muški",
        female: "Ženski",
        cp: "Tip angine",
        trestbps: "Krvni pritisak u mirovanju",
        chol: "Holesterol",
        fbs: "Šećer u krvi na prazan stomak",
        restecg: "EKG u mirovanju",
        thalach: "Maksimalni puls",
        exang: "Angina izazvana vježbom",
        oldpeak: "Oldpeak",
        slope: "Nagib ST segmenta",
        ca: "CA",
        thal: "Thal",
        predict_btn: "Predvidi Rizik",
        add_patient_title: "Dodaj Novog Pacijenta",
        add_patient_btn: "Dodaj Pacijenta",
        retrain_title: "Retreniraj Model",
        retrain_text: "Koristi novododate podatke za ponovno treniranje ML modela",
        retrain_btn: "Retreniraj Model",
        yes: "Da",
        no: "Ne",
        upsloping: "rastući",
        flat: "ravan",
        downsloping: "opadajući",
        normal: "normalno",
        lv_hypertrophy: "LV hipertrofija",
        stt: "ST-T valni poremećaj",
        fixed_defect: "fiksni defekt",
        reversable_defect: "reverzibilni defekt",
        footer_text: "© 2025 HealthPredict. Sva prava zadržana."
    },
    en: {
        language_label: "Language:",
        bs: "Bosnian",
        en: "English",
        predict_title: "Heart Disease Prediction",
        age: "Age",
        sex: "Sex",
        select: "Select",
        male: "Male",
        female: "Female",
        cp: "Chest Pain Type",
        trestbps: "Resting BP",
        chol: "Cholesterol",
        fbs: "Fasting Blood Sugar",
        restecg: "Resting ECG",
        thalach: "Max Heart Rate",
        exang: "Exercise Induced Angina",
        oldpeak: "Oldpeak",
        slope: "Slope",
        ca: "CA",
        thal: "Thal",
        predict_btn: "Predict Risk",
        add_patient_title: "Add New Patient",
        add_patient_btn: "Add Patient",
        retrain_title: "Retrain Model",
        retrain_text: "Use newly added data to retrain the ML model.",
        retrain_btn: "Retrain Model",
        yes: "Yes",
        no: "No",
        upsloping: "upsloping",
        flat: "flat",
        downsloping: "downsloping",
        normal: "normal",
        lv_hypertrophy: "lv hypertrophy",
        stt: "ST-T wave abnormality",
        fixed_defect: "fixed defect",
        reversable_defect: "reversable defect",
        footer_text: "© 2025 HealthPredict. All rights reserved."
    }
};

const languageSelect = document.getElementById("languageSelect");

languageSelect.addEventListener("change", () => {
    const lang = languageSelect.value;

    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[lang][key]) {
            if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
                el.placeholder = translations[lang][key];
            } else {
                el.innerText = translations[lang][key];
            }
        }
    });

    document.querySelectorAll("select option[data-i18n]").forEach(opt => {
        const key = opt.getAttribute("data-i18n");
        if (translations[lang][key]) {
            opt.innerText = translations[lang][key];
        }
    });
});

// -------- PREDICTION --------
document.getElementById("predictBtn").addEventListener("click", async () => {
    const data = {
        age: parseFloat(document.getElementById("age").value),
        sex: parseInt(document.getElementById("sex").value),
        cp: document.getElementById("cp").value,
        trestbps: parseFloat(document.getElementById("trestbps").value),
        chol: parseFloat(document.getElementById("chol").value),
        fbs: parseInt(document.getElementById("fbs").value),
        restecg: document.getElementById("restecg").value,
        thalach: parseFloat(document.getElementById("thalach").value),
        exang: parseInt(document.getElementById("exang").value),
        oldpeak: parseFloat(document.getElementById("oldpeak").value),
        slope: document.getElementById("slope").value,
        ca: parseInt(document.getElementById("ca").value),
        thal: document.getElementById("thal").value
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById("result").innerHTML = `
            <strong>${translations[languageSelect.value].predict_title}:</strong> ${result.result.prediction ? "Heart Disease Risk" : "Low Risk"}<br>
            <strong>Probability:</strong> ${(result.result.probability*100).toFixed(2)}%<br>
            <strong>Top Features:</strong> ${result.top_features.map(f => f[0] + " (" + (f[1]*100).toFixed(1) + "%)").join(", ")}
        `;
    } catch (error) {
        console.error(error);
        document.getElementById("result").innerText = "Error connecting to backend.";
    }
});

// -------- ADD NEW DATA --------
document.getElementById("addBtn").addEventListener("click", async () => {
    const data = {
        age: parseFloat(document.getElementById("add_age").value),
        sex: parseInt(document.getElementById("add_sex").value),
        cp: document.getElementById("add_cp").value,
        trestbps: parseFloat(document.getElementById("add_trestbps").value),
        chol: parseFloat(document.getElementById("add_chol").value),
        fbs: parseInt(document.getElementById("add_fbs").value),
        restecg: document.getElementById("add_restecg").value,
        thalch: parseFloat(document.getElementById("add_thalch").value),
        exang: parseInt(document.getElementById("add_exang").value),
        oldpeak: parseFloat(document.getElementById("add_oldpeak").value),
        slope: document.getElementById("add_slope").value,
        ca: parseInt(document.getElementById("add_ca").value),
        thal: document.getElementById("add_thal").value
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById("addResult").innerText = `${result.status}: ${result.message}`;
    } catch (error) {
        console.error(error);
        document.getElementById("addResult").innerText = "Error adding data. Check backend.";
    }
});

// -------- RETRAIN MODEL --------
document.getElementById("retrainBtn").addEventListener("click", async () => {
    document.getElementById("retrainResult").innerText = "Retraining model, please wait...";
    try {
        const response = await fetch("http://127.0.0.1:5000/retrain", {
            method: "POST"
        });
        const result = await response.json();
        document.getElementById("retrainResult").innerText = `${result.status}: ${result.message}`;
    } catch (error) {
        console.error(error);
        document.getElementById("retrainResult").innerText = "Error retraining model. Check backend.";
    }
});
