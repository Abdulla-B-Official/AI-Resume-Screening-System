const presetRoles = {
    data_engineer: `Title: Senior Data Engineer
Location: Bengaluru (Hybrid)
 
About the role:
We are looking for a Senior Data Engineer to design and operate large-scale batch and streaming data pipelines that power our analytics and ML platforms. You will own pipeline reliability, data warehousing, and real-time ingestion.
 
Responsibilities:
- Design, build, and maintain scalable ETL/ELT pipelines.
- Build real-time streaming ingestion and processing.
- Own and optimize the cloud data warehouse serving analysts and data scientists.
- Ensure pipeline reliability, data quality, and performance at scale.
 
Required skills (must-have):
- 5+ years of data engineering experience
- Strong SQL and Python
- Apache Spark
- Apache Airflow
- Apache Kafka (streaming)
- Cloud data platform (AWS strongly preferred)
- ETL/ELT and data warehousing
 
Nice to have:
- Snowflake, dbt, Databricks
- Terraform / infrastructure-as-code`,

    data_analyst: `Title: Data Analyst – Business Intelligence
Location: Pune, India (Hybrid)
Experience Required: 2–5 Years

Required Skills (Must-Have):
* Bachelor's degree in Statistics, Mathematics, Computer Science, Economics, Business Analytics, or related field.
* 2+ years of experience as a Data Analyst or Business Intelligence Analyst.
* Strong proficiency in SQL, complex joins, window functions, CTEs.
* Hands-on experience with Power BI and/or Tableau for dashboard development and reporting.
* Advanced knowledge of Microsoft Excel (Pivot Tables, Power Query, Power Pivot).
* Understanding of A/B Testing, hypothesis testing, and statistical analysis.`
};

function setRole(roleKey) {
    const textarea = document.getElementById('jd_textarea');
    if (textarea && presetRoles[roleKey]) {
        textarea.value = presetRoles[roleKey];
    }
}

// Keep track of attached files in memory
let uploadedFilesData = new DataTransfer();

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('files');
    const dropzone = document.getElementById('dropzone');
    const fileLabelContent = document.getElementById('file-label-content');
    const selectedFilesContainer = document.getElementById('selected-files-container');
    const clearBtn = document.getElementById('clear-btn');
    const runBtn = document.getElementById('run-btn');
    const resultsSection = document.getElementById('results-section');
    const resultsTbody = document.getElementById('results-tbody');
    const errorBanner = document.getElementById('error-banner');
    const errorText = document.getElementById('error-text');

    if (!fileInput) return;

    // Handle file selection
    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        for (let i = 0; i < files.length; i++) {
            uploadedFilesData.items.add(files[i]);
        }
        fileInput.files = uploadedFilesData.files;
        updateFileListUI();
    });

    function updateFileListUI() {
        const files = uploadedFilesData.files;
        if (files.length > 0) {
            dropzone.classList.add('has-files');
            fileLabelContent.style.display = 'none';
            
            let html = `<div class="file-success-badge">✅ ${files.length} resume(s) attached</div><ul class="file-names-ul">`;
            for (let i = 0; i < files.length; i++) {
                html += `<li>📄 ${files[i].name}</li>`;
            }
            html += `</ul>`;
            selectedFilesContainer.innerHTML = html;
        } else {
            dropzone.classList.remove('has-files');
            fileLabelContent.style.display = 'flex';
            selectedFilesContainer.innerHTML = '';
        }
    }

    // Explicit Clear Button Click
    clearBtn.addEventListener('click', () => {
        uploadedFilesData = new DataTransfer();
        fileInput.files = uploadedFilesData.files;
        updateFileListUI();
        resultsSection.style.display = 'none';
        errorBanner.style.display = 'none';
    });

    // Run Screening via AJAX (Fetch) so files don't disappear
    runBtn.addEventListener('click', async () => {
        const files = uploadedFilesData.files;
        if (files.length === 0) {
            errorText.textContent = "⚠️ Please upload at least one resume before running screening.";
            errorBanner.style.display = 'block';
            return;
        }

        const jdText = document.getElementById('jd_textarea').value;
        const formData = new FormData();
        formData.append('jd_text', jdText);
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        runBtn.disabled = true;
        runBtn.textContent = "⏳ Screening Resumes...";
        errorBanner.style.display = 'none';

        try {
            const response = await fetch('/screen', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.error) {
                errorText.textContent = "⚠️ " + data.error;
                errorBanner.style.display = 'block';
                resultsSection.style.display = 'none';
            } else {
                renderResults(data.results);
            }
        } catch (err) {
            errorText.textContent = "⚠️ An error occurred during screening.";
            errorBanner.style.display = 'block';
        } finally {
            runBtn.disabled = false;
            runBtn.textContent = "⚡ Run Lightning Screening";
        }
    });

    function renderResults(results) {
        resultsTbody.innerHTML = '';
        results.forEach(res => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><span class="rank-badge rank-${res.rank}">#${res.rank}</span></td>
                <td class="file-name"><strong>${res.file_name}</strong></td>
                <td>
                    <div class="score-bar-wrapper">
                        <span class="score-text">${res.fit_score}%</span>
                        <div class="score-bar"><div class="score-fill" style="width: var(--score); --score: ${res.fit_score}%;"></div></div>
                    </div>
                </td>
                <td class="preview-text">${res.text.substring(0, 140)}...</td>
            `;
            resultsTbody.appendChild(tr);
        });
        resultsSection.style.display = 'block';
    }
});