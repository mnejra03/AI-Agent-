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
        predict_btn: "Predvidi rizik",
        add_patient_title: "Dodaj nvog pacijenta",
        add_patient_btn: "Dodaj pacijenta",
        retrain_title: "Retreniraj model",
        retrain_text: "Koristi novododate podatke za ponovno treniranje ML modela",
        retrain_btn: "Retreniraj model",
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
        footer_text: "© 2025 HealthPredict. Sva prava zadržana.",
        typical_angina:"tipična angina",
        asymptomatic:"asimptomatska",
        nonanginal:"ne-anginalna",
        atypical_angina:"atipična angina",
        oldpeakOpis: "Oldpeak pokazuje koliko se EKG promijenio kada je srce bilo pod opterećenjem. Mjeri se u milimetrima (mm). Predstavlja razliku između ST-segmenta u mirovanju i tokom napora.",
        nagibStSegmenta:"Nagib opisuje da li ST segment ide gore, dolje ili je ravan. ST segment je dio EKG zapisa: nalazi se između QRS kompleksa i T talasa; predstavlja fazu kada su komore srca potpuno depolarizirane; normalno treba biti ravan i na istoj liniji kao osnovna (izoelektrična) linija.",
        caOpis:"CA pokazuje koliko velikih krvnih sudova koji vode krv do srca je vidljivo / blokirano na osnovu koronarografije. 0 -- Nema blokiranih sudova (najbolje stanje); 1 -- Jedna arterija zahvaćena; 2 -- Dvije arterije zahvaćene; 3 -- Tri arterije zahvaćene.",
        thalOpis:"Thal opisuje rezultat thallium stres testa srca, koji se koristi za procjenu prokrvljenosti srčanog mišića.",
        rezultat:"Ovdje će biti prikazan rezultat procjene rizika za srčane bolesti."
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
        footer_text: "© 2025 HealthPredict. All rights reserved.",
        typical_angina:"typical angina",
        asymptomatic:"asymptomatic",
        nonanginal:"nonanginal",
        atypical_angina:"atypical angina",
        oldpeakOpis:"Oldpeak shows how much the ECG changed when the heart was under stress. It is measured in millimeters (mm). It represents the difference between the ST-segment at rest and during exertion.",
        nagibStSegmenta:"The slope describes whether the ST segment is going up, down, or flat. The ST segment is a part of the ECG trace: it is located between the QRS complex and the T wave; represents the phase when the heart's ventricles are completely depolarized; normally it should be flat and on the same line as the baseline (isoelectric) line.",
        caOpis:"CA shows how many of the large blood vessels that carry blood to the heart are visible/blocked based on coronary angiography. 0 -- No blocked vessels (best condition); 1 -- One artery involved; 2 -- Two arteries involved; 3 -- Three arteries involved.",
        thalOpis:"Thal describes the result of a thallium cardiac stress test, which is used to assess blood flow to the heart muscle.",
        rezultat:"The result of the heart disease risk assessment will be displayed here."        
    }
};

const languageSelect = document.getElementById("languageSelect");

function updateLanguage(lang) {
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
}

// Inicijalno postavi jezik
updateLanguage(languageSelect.value);
languageSelect.addEventListener("change", () => updateLanguage(languageSelect.value));

// --- PREDICT ---
document.getElementById("predictBtn").addEventListener("click", async () => {
    const resultDiv = document.getElementById("result");
    const lang = languageSelect.value;

    // --- Prije predikcije ne mijenjamo boju, samo prikažemo tekst ---
    resultDiv.innerText = lang==="bs" ? "Procjena u toku..." : "Predicting...";

    const data = { 
        age: parseFloat(document.getElementById("age").value),
        sex: parseInt(document.getElementById("sex").value),
        cp: document.getElementById("cp").value,
        trestbps: parseFloat(document.getElementById("trestbps").value),
        chol: parseFloat(document.getElementById("chol").value),
        fbs: parseInt(document.getElementById("fbs").value),
        restecg: document.getElementById("restecg").value,
        thalch: parseFloat(document.getElementById("thalach").value),
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

        // --- Nakon predikcije mijenjamo boju prema riziku ---
        if(result.result.prediction) {
            resultDiv.style.backgroundColor = "#ffcccc"; // crveno za visok rizik
        } else {
            resultDiv.style.backgroundColor = "#ccffcc"; // zeleno za nizak rizik
        }

        resultDiv.innerHTML = `
            <strong>${translations[lang].predict_title}:</strong> ${result.result.prediction ? (lang==="bs"?"Visok rizik":"High Risk") : (lang==="bs"?"Nizak rizik":"Low Risk")}<br>
            <strong>Probability:</strong> ${(result.result.probability*100).toFixed(2)}%<br>
            <strong>Top Features:</strong> ${result.top_features.map(f => f[0] + " (" + (f[1]*100).toFixed(1) + "%)").join(", ")}
        `;
    } catch (error) { 
        console.error(error); 
        resultDiv.style.backgroundColor = "#f8d7da"; // crveno za grešku
        resultDiv.innerText = lang==="bs" ? "Greška prilikom predikcije." : "Error predicting."; 
    }
});


// --- ADD DATA ---
document.getElementById("addBtn").addEventListener("click", async () => {
    const addResultDiv = document.getElementById("addResult");
    const lang = languageSelect.value;

    // Prikupljanje inputa
    const data = {
        age: document.getElementById("add_age").value,
        sex: document.getElementById("add_sex").value,
        cp: document.getElementById("add_cp").value,
        trestbps: document.getElementById("add_trestbps").value,
        chol: document.getElementById("add_chol").value,
        fbs: document.getElementById("add_fbs").value,
        restecg: document.getElementById("add_restecg").value,
        thalch: document.getElementById("add_thalch").value,
        exang: document.getElementById("add_exang").value,
        oldpeak: document.getElementById("add_oldpeak").value,
        slope: document.getElementById("add_slope").value,
        ca: document.getElementById("add_ca").value,
        thal: document.getElementById("add_thal").value
    };

    // Provjera da li su sva obavezna polja popunjena
    for (const key in data) {
        if (data[key] === "" || data[key] === null || data[key] === undefined) {
            addResultDiv.style.backgroundColor = "#ffcccc";
            addResultDiv.innerText = lang === "bs" ? "Molimo popunite sva polja." : "Please fill in all required fields.";
            addResultDiv.classList.remove("hide");
            return; // prekida slanje zahtjeva
        }
    }

    // Ako je sve popunjeno, nastavlja se sa slanjem
    try {
        const response = await fetch("http://127.0.0.1:5000/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if(result.status === "success") {
            addResultDiv.style.backgroundColor = "#ccffcc"; 
            addResultDiv.innerText = lang === "bs" ? "Pacijent uspješno dodan." : "Patient added successfully.";
        } else {
            addResultDiv.style.backgroundColor = "#ffcccc"; 
            addResultDiv.innerText = lang === "bs" ? "Dodavanje pacijenta nije uspjelo." : "Failed to add patient.";
        }

        addResultDiv.classList.remove("hide");
        // Nestaje nakon 5 sekundi
        setTimeout(() => { addResultDiv.classList.add("hide"); }, 5000);

    } catch (error) {
        console.error(error);
        addResultDiv.style.backgroundColor = "#ffcccc";
        addResultDiv.innerText = lang === "bs" ? "Greška prilikom dodavanja pacijenta." : "Error adding patient.";
        addResultDiv.classList.remove("hide");
        setTimeout(() => { addResultDiv.classList.add("hide"); }, 5000);
    }
});




// --- RETRAIN MODEL ---
// --- RETRAIN MODEL ---
document.getElementById("retrainBtn").addEventListener("click", async () => {
    const lang = languageSelect.value;
    const retrainDiv = document.getElementById("retrainResult");
    const addResultDiv = document.getElementById("addResult");

    // Fade-out poruke dodavanja pacijenta
    addResultDiv.classList.add("hide");

    retrainDiv.classList.remove("success", "error", "hide");
    retrainDiv.style.display = "block";
    retrainDiv.style.opacity = 1;
    retrainDiv.style.color = "green";
    retrainDiv.innerText = lang === "bs" ? "Ponovno treniranje modela, molimo sačekajte..." : "Retraining model, please wait...";

    try {
        const response = await fetch("http://127.0.0.1:5000/retrain", { method: "POST" });
        const result = await response.json();

        retrainDiv.classList.remove("hide");

        if(result.status.toLowerCase() === "success") {
            retrainDiv.classList.add("success");
            retrainDiv.innerText = lang === "bs" ? result.message_bs : result.message_en;
        } else {
            retrainDiv.classList.add("error");
            retrainDiv.innerText = lang === "bs" ? (result.message_bs || "Greška prilikom retreniranja modela.") 
                                                 : (result.message_en || "Error retraining model.");
        }

    } catch (error) {
        retrainDiv.classList.remove("hide");
        retrainDiv.classList.add("error");
        retrainDiv.innerText = lang === "bs" ? "Greška prilikom retreniranja modela." : "Error retraining model. Check backend.";
    }
});



// --- DEFAULT EXAMPLE ON LOAD ---
document.addEventListener("DOMContentLoaded", () => {
    // Primjer: mlada osoba (23 godine)
    document.getElementById("age").value = 23;
    document.getElementById("sex").value = "0"; // Female
    document.getElementById("cp").value = "non-anginal";
    document.getElementById("trestbps").value = 110;
    document.getElementById("chol").value = 170;
    document.getElementById("fbs").value = "0"; // No
    document.getElementById("restecg").value = "normal";
    document.getElementById("thalach").value = 190;
    document.getElementById("exang").value = "0"; // No
    document.getElementById("oldpeak").value = 0;
    document.getElementById("slope").value = "upsloping";
    document.getElementById("ca").value = 0;
    document.getElementById("thal").value = "normal";
});
