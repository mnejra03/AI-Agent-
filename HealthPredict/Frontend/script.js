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
        fbs: "Šećeeer u krvi na prazan stomak",
        restecg: "EKG u mirovanju",
        thalach: "Maksimalni puls",
        exang: "Angina izazvana vježbom",
        oldpeak: "Oldpeak",
        slope: "Nagib ST segmenta",
        ca: "CA",
        thal: "Thal",
        predict_btn: "Predvidi rizik",
        add_patient_title: "Dodaj novog pacijenta",
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
        typical_angina: "tipična angina",
        asymptomatic: "asimptomatska",
        nonanginal: "ne-anginalna",
        atypical_angina: "atipična angina",
        oldpeakOpis: "Oldpeak pokazuje koliko se EKG promijenio kada je srce bilo pod opterećenjem. Mjeri se u milimetrima (mm). Predstavlja razliku između ST-segmenta u mirovanju i tokom napora.",
        nagibStSegmenta: "Nagib opisuje da li ST segment ide gore, dolje ili je ravan. ST segment je dio EKG zapisa: nalazi se između QRS kompleksa i T talasa; predstavlja fazu kada su komore srca potpuno depolarizirane; normalno treba biti ravan i na istoj liniji kao osnovna (izoelektrična) linija.",
        caOpis: "CA pokazuje koliko velikih krvnih sudova koji vode krv do srca je vidljivo / blokirano na osnovu koronarografije. 0 -- Nema blokiranih sudova (najbolje stanje); 1 -- Jedna arterija zahvaćena; 2 -- Dvije arterije zahvaćene; 3 -- Tri arterije zahvaćene.",
        thalOpis: "Thal opisuje rezultat thallium stres testa srca, koji se koristi za procjenu prokrvljenosti srčanog mišića.",
        rezultat: "Ovdje će biti prikazan rezultat procjene rizika za srčane bolesti."
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
        typical_angina: "typical angina",
        asymptomatic: "asymptomatic",
        nonanginal: "nonanginal",
        atypical_angina: "atypical angina",
        oldpeakOpis: "Oldpeak shows how much the ECG changed when the heart was under stress. It is measured in millimeters (mm). It represents the difference between the ST-segment at rest and during exertion.",
        nagibStSegmenta: "The slope describes whether the ST segment is going up, down, or flat. The ST segment is a part of the ECG trace: it is located between the QRS complex and the T wave; represents the phase when the heart's ventricles are completely depolarized; normally it should be flat and on the same line as the baseline (isoelectric) line.",
        caOpis: "CA shows how many of the large blood vessels that carry blood to the heart are visible/blocked based on coronary angiography. 0 -- No blocked vessels (best condition); 1 -- One artery involved; 2 -- Two arteries involved; 3 -- Three arteries involved.",
        thalOpis: "Thal describes the result of a thallium cardiac stress test, which is used to assess blood flow to the heart muscle.",
        rezultat: "The result of the heart disease risk assessment will be displayed here."
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
        if (el.dataset.ignoreI18n === "true") return;
    });

    document.querySelectorAll("select option[data-i18n]").forEach(opt => {
        const key = opt.getAttribute("data-i18n");
        if (translations[lang][key]) {
            opt.innerText = translations[lang][key];
        }
    });
}

updateLanguage(languageSelect.value);
languageSelect.addEventListener("change", () => updateLanguage(languageSelect.value));

const featureLabels = {
    bs: {
        num: null,
        id: null,

        thalch: "Maksimalni puls",
        "cp_atypical angina": "Atipična angina",
        "cp_typical angina": "Tipična angina",
        "cp_non-anginal": "Ne-anginalni bol u prsima",
        exang_True: "Angina izazvana fizičkom aktivnošću",
        exang_False: "Nema angine pri naporu",
        oldpeak: "ST depresija (Oldpeak)",
        ca: "Broj zahvaćenih krvnih sudova",
        thal_normal: "Normalan thallium test",
        "thal_reversable defect": "Reverzibilni defekt (thal)"
    },

    en: {
        num: null,
        id: null,

        thalch: "Maximum heart rate",
        "cp_atypical angina": "Atypical angina",
        "cp_typical angina": "Typical angina",
        "cp_non-anginal": "Non-anginal chest pain",
        exang_True: "Exercise-induced angina",
        exang_False: "No exercise-induced angina",
        oldpeak: "ST depression (Oldpeak)",
        ca: "Number of affected vessels",
        thal_normal: "Normal thallium test",
        "thal_reversable defect": "Reversible thallium defect"
    }
};

const medicalExplanation = {
    bs: {
        LOW_RISK: "Na osnovu dostupnih zdravstvenih parametara ne postoje značajni pokazatelji povećanog kardiovaskularnog rizika...",
        REVIEW: "Procjena ukazuje na umjeren nivo rizika ili nesigurnost modela...",
        HIGH_RISK: "Identifikovani su značajni faktori koji su u medicinskoj praksi povezani s povećanim rizikom od srčanih oboljenja..."
    },
    en: {
        LOW_RISK: "Based on the available health indicators, there are no strong signs of elevated cardiovascular risk...",
        REVIEW: "The assessment indicates a moderate risk level or model uncertainty...",
        HIGH_RISK: "Significant risk factors commonly associated with cardiovascular disease have been identified..."
    }
};

function getDisplayRisk(risk, decision) {
    if (decision === "HIGH_RISK") {
        return Math.max(70, Math.round(risk * 100));
    }
    if (decision === "REVIEW") {
        return Math.max(40, Math.round(risk * 100));
    }
    return Math.round(risk * 100);
}


document.getElementById("predictBtn").addEventListener("click", async () => {
    const resultDiv = document.getElementById("result");
    const lang = languageSelect.value;

    resultDiv.innerText = lang === "bs"
        ? "Procjena u toku..."
        : "Predicting...";

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

        const queued = await response.json();
        const requestId = queued.request_id;

        resultDiv.innerText = lang === "bs"
            ? "Agent obrađuje podatke..."
            : "Agent is processing...";

        let result = null;

        while (result === null) {
            await new Promise(r => setTimeout(r, 1000));

            const res = await fetch(`http://127.0.0.1:5000/result/${requestId}`);
            const resData = await res.json();

            if (resData.status !== "processing") {
                result = resData;
            }
        }

        const decisionClass = result.decision.toLowerCase();

        const decisionLabels = {
            LOW_RISK: lang === "bs" ? "NIZAK RIZIK" : "LOW RISK",
            REVIEW: lang === "bs" ? "Potrebna dodatna provjera" : "Needs review",
            HIGH_RISK: lang === "bs" ? "VISOK RIZIK" : "HIGH RISK"
        };

        const riskPercent = getDisplayRisk(result.decision, result.risk);

        const riskFactors = detectRiskFactors(data, lang);


        let clinicalColor = "#28a745";
        if (result.decision === "HIGH_RISK") clinicalColor = "#dc3545";
        if (result.decision === "REVIEW") clinicalColor = "#007bff";

        resultDiv.innerHTML = `
    <h3>🩺 ${lang === "bs" ? "Procjena rizika" : "Risk Assessment"}</h3>

    <p><strong>
        ${lang === "bs" ? "Klinička odluka agenta:" : "Agent clinical decision:"}
    </strong></p>
    <div style="background:#eee;border-radius:8px;overflow:hidden;margin-bottom:10px;">
        <div style="
            width:100%;
            background:${clinicalColor};
            color:white;
            padding:8px;
            text-align:center;
            font-weight:bold;">
            ${decisionLabels[result.decision]}
        </div>
    </div>

    <p>
        <strong>
            ${lang === "bs"
                ? "Statistička vjerovatnoća (ML model):"
                : "Statistical probability (ML model):"}
        </strong>
        ${riskPercent}%
    </p>
    <div style="background:#eee;border-radius:8px;overflow:hidden;">
        <div style="
            width:${riskPercent}%;
            background:#007bff;
            height:18px;">
        </div>
    </div>

    <small style="display:block;margin-top:8px;color:#555;">
        ℹ️ ${
            lang === "bs"
                ? "Klinički rizik se određuje kombinacijom medicinskih pravila i modela, dok procenat predstavlja statističku vjerovatnoću."
                : "Clinical risk is determined using a combination of medical rules and the model, while the percentage represents statistical probability."
        }
    </small>


    <p style="margin-top:12px; font-style:italic;">
    🩺 ${getMedicalComment(result.decision, riskFactors, lang)}
</p>`;

    } catch (error) {
        console.error(error);
        resultDiv.innerText = lang === "bs"
            ? "Greška u komunikaciji s agentom."
            : "Agent communication error.";
    }

});

function getMedicalComment(decision, factors, lang) {
    let baseText = "";

    if (decision === "LOW_RISK") {
        baseText =
            lang === "bs"
                ? "Na osnovu dostupnih podataka, trenutno nema značajnih pokazatelja povišenog kardiovaskularnog rizika."
                : "Based on the available data, there are no significant indicators of elevated cardiovascular risk.";
    }

    if (decision === "REVIEW") {
        baseText =
            lang === "bs"
                ? "Prisutan je umjeren nivo rizika. Neki faktori zahtijevaju dodatno praćenje i oprez."
                : "A moderate level of risk is present. Certain factors require closer monitoring and caution.";
    }

    if (decision === "HIGH_RISK") {
        baseText =
            lang === "bs"
                ? "Uočena je kombinacija više klinički značajnih faktora koji ukazuju na povišen rizik.<br>"
                : "A combination of multiple clinically significant factors indicates an elevated risk.<br>";
    }

    if (factors && factors.length > 0) {
        baseText +=
            lang === "bs"
                ? `<br><strong>Mogući razlozi:</strong> ${factors.join(", ")}.<br>`
                : `<br><strong>Possible contributing factors:</strong> ${factors.join(", ")}.<br>`;
    }

    if (decision === "HIGH_RISK") {
        baseText +=
            lang === "bs"
                ? "<br><strong>Preporuka:</strong> Savjetuje se što skoriji pregled kod ljekara."
                : "<br><strong>Recommendation:</strong> Prompt medical consultation is strongly recommended.";
    }

    if (decision === "REVIEW") {
        baseText +=
            lang === "bs"
                ? "<br><strong>Preporuka:</strong> Nastaviti praćenje i razmotriti dodatne dijagnostičke pretrage."
                : "<br><strong>Recommendation:</strong> Continued monitoring and additional diagnostic evaluation may be beneficial.";
    }

    return baseText;
}

function getDisplayRisk(decision, rawRisk) {
    if (decision === "LOW_RISK") {
        return Math.min(35, Math.max(10, Math.round(rawRisk * 100)));
    }

    if (decision === "REVIEW") {
        return Math.min(65, Math.max(40, Math.round(rawRisk * 100)));
    }

    if (decision === "HIGH_RISK") {
        return Math.min(95, Math.max(70, Math.round(rawRisk * 100)));
    }

    return Math.round(rawRisk * 100);
}

function detectRiskFactors(data, lang) {
    const factors = [];

    if (data.trestbps >= 140)
        factors.push(lang === "bs" ? "povišen krvni pritisak" : "high blood pressure");

    if (data.chol >= 240)
        factors.push(lang === "bs" ? "povišen holesterol" : "high cholesterol");

    if (data.fbs === 1)
        factors.push(lang === "bs" ? "povišen šećer u krvi" : "high fasting blood sugar");

    if (data.exang === 1)
        factors.push(lang === "bs" ? "angina pri fizičkom naporu" : "exercise-induced angina");

    if (data.oldpeak >= 2)
        factors.push(lang === "bs" ? "značajne EKG promjene pri naporu" : "significant ECG changes under stress");

    if (data.ca >= 2)
        factors.push(lang === "bs" ? "više zahvaćenih krvnih sudova" : "multiple affected blood vessels");

    if (data.thal.includes("reversable"))
        factors.push(lang === "bs" ? "abnormalan thallium stres test" : "abnormal thallium stress test");

    return factors;
}
/*
document.getElementById("addBtn").addEventListener("click", async () => {
    const addResultDiv = document.getElementById("addResult");
    const lang = languageSelect.value;

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

    for (const key in data) {
        if (data[key] === "" || data[key] === null || data[key] === undefined) {
            addResultDiv.style.backgroundColor = "#ffcccc";
            addResultDiv.innerText = lang === "bs"
                ? "Molimo popunite sva polja prije dodavanja pacijenta."
                : "Please fill in all fields before adding a patient.";
            addResultDiv.classList.remove("hide");
            return;
        }
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === "success") {
            addResultDiv.style.backgroundColor = "#ccffcc";
            addResultDiv.innerHTML = lang === "bs"
                ? `
            <strong>Pacijent uspješno dodan.</strong><br>
            ⚠️ <em>Za ažuriranje predikcija potrebno je pokrenuti ponovno treniranje modela.</em>
          `
                : `
            <strong>Patient successfully added.</strong><br>
            ⚠️ <em>To update predictions, model retraining is required.</em>
          `;
        }
        document.getElementById("retrainBtn").style.border = "2px solid orange";
        document.getElementById("retrainBtn").scrollIntoView({ behavior: "smooth" });


        addResultDiv.classList.remove("hide");


    } catch (error) {
        console.error(error);
        addResultDiv.style.backgroundColor = "#ffcccc";
        addResultDiv.innerText = lang === "bs" ? "Greška prilikom dodavanja pacijenta." : "Error adding patient.";
        addResultDiv.classList.remove("hide");
    }
});
*/
document.getElementById("addBtn").addEventListener("click", async () => {
    const addResultDiv = document.getElementById("addResult");
    const lang = languageSelect.value;

    addResultDiv.classList.remove("hide");
    addResultDiv.style.opacity = 1;
    addResultDiv.style.display = "block";


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

    for (const key in data) {
        if (!data[key]) {
            addResultDiv.style.display = "block";
            addResultDiv.style.backgroundColor = "#f8d7da";
            addResultDiv.innerText =
                lang === "bs"
                    ? "Molimo popunite sva polja prije dodavanja pacijenta."
                    : "Please fill in all fields before adding a patient.";
            return;
        }
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === "success") {
            addResultDiv.style.backgroundColor = "#d4edda";
            addResultDiv.innerHTML =
                lang === "bs"
                    ? `<strong>Pacijent uspješno dodan.</strong><br>
                       ⚠️ <em>Za primjenu novih podataka potrebno je pokrenuti ponovno treniranje modela.</em>`
                    : `<strong>Patient successfully added.</strong><br>
                       ⚠️ <em>To apply new data, model retraining is required.</em>`;

            // vizualni hint za retrain
            const retrainBtn = document.getElementById("retrainBtn");
            retrainBtn.style.border = "2px solid #fd7e14";
            retrainBtn.scrollIntoView({ behavior: "smooth" });
        } else {
            throw new Error("Add failed");
        }

    } catch (error) {
        addResultDiv.style.backgroundColor = "#f8d7da";
        addResultDiv.innerText =
            lang === "bs"
                ? "Greška prilikom dodavanja pacijenta."
                : "Error adding patient.";
    }
});


document.getElementById("retrainBtn").addEventListener("click", async () => {
    const retrainDiv = document.getElementById("retrainResult");
    const lang = languageSelect.value;

    retrainDiv.style.display = "block";
    retrainDiv.style.backgroundColor = "#fff3cd";
    retrainDiv.innerText =
        lang === "bs"
            ? "Ponovno treniranje modela, molimo sačekajte..."
            : "Retraining model, please wait...";

    try {
        const response = await fetch("http://127.0.0.1:5000/retrain", {
            method: "POST"
        });

        const result = await response.json();

        if (result.status === "success") {
            retrainDiv.style.backgroundColor = "#ccffcc";
            retrainDiv.innerText =
                lang === "bs"
                    ? result.message_bs
                    : result.message_en;
        } else {
            retrainDiv.style.backgroundColor = "#ffcccc";
            retrainDiv.innerText =
                lang === "bs"
                    ? "Greška prilikom retreniranja."
                    : "Retraining failed.";
        }

    } catch (error) {
        retrainDiv.style.backgroundColor = "#ffcccc";
        retrainDiv.innerText =
            lang === "bs"
                ? "Greška – backend nije dostupan."
                : "Error – backend not reachable.";
    }
});


document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("age").value = 61;
    document.getElementById("sex").value = "0";
    document.getElementById("cp").value = "asymptomatic";
    document.getElementById("trestbps").value = 160;
    document.getElementById("chol").value = 320;
    document.getElementById("fbs").value = "0";
    document.getElementById("restecg").value = "ST-T wave abnormality";
    document.getElementById("thalach").value = 95;
    document.getElementById("exang").value = "0";
    document.getElementById("oldpeak").value = 3.5;
    document.getElementById("slope").value = "downsloping";
    document.getElementById("ca").value = 3;
    document.getElementById("thal").value = "reversable defect";
});
