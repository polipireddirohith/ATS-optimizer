/**
 * ATS Resume Analyzer - Gamified Frontend Logic
 * Features: XP, Levels, Streaks, Daily Challenges, and Emotional Mascot.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements - Workspace
    const form = document.getElementById('atsForm');
    const fileInput = document.getElementById('resumeFile');
    const dropArea = document.getElementById('dropArea');
    const jdInput = document.getElementById('jdText');
    const charCount = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resumePreview = document.getElementById('resumePreview');
    const selectedFileName = document.getElementById('selectedFileName');

    // UI Sections
    const uploadSection = document.getElementById('uploadSection');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const sidebarItems = document.querySelectorAll('.sidebar-link');
    const navLinks = document.querySelectorAll('.nav-links a');

    // Gamification Elements
    const xpBar = document.getElementById('xpBar');
    const xpText = document.getElementById('xpText');
    const levelBadge = document.getElementById('levelBadge');
    const levelName = document.getElementById('levelName');
    const streakCount = document.getElementById('streakCount');
    const challengeText = document.getElementById('challengeText');
    const challengeDot = document.getElementById('challengeDot');
    const challengeStatus = document.getElementById('challengeStatus');
    const achievementsList = document.getElementById('achievementsList');

    // Core Results Widgets
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreRing = document.getElementById('scoreRing');
    const scoreStatus = document.getElementById('scoreStatus');
    const breakdownGrid = document.getElementById('breakdownGrid');
    const comparisonContainer = document.getElementById('comparisonContainer');
    const gapsContainer = document.getElementById('gapsContainer');
    const suitabilityVerdict = document.getElementById('suitabilityVerdict');
    const suitabilityRecommendation = document.getElementById('suitabilityRecommendation');
    const recruiterInsights = document.getElementById('recruiterInsights');
    const optimizedResume = document.getElementById('optimizedResume');
    const improvementsContainer = document.getElementById('improvementsContainer');

    // Buttons
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    const resetAnalysisBtn = document.getElementById('resetAnalysisBtn');
    const downloadReportBtn = document.getElementById('downloadReportBtn');
    const downloadResumeBtn = document.getElementById('downloadResumeBtn');
    const unlockBtn = document.getElementById('unlockBtn');
    const shortlistBtn = document.getElementById('shortlistBtn');
    const addNoteBtn = document.getElementById('addNoteBtn');
    const hrNewAnalysisBtn = document.getElementById('hrNewAnalysisBtn');

    // ==================== Gamification Core Removed ====================
    // HR Recruiter Mode Active
    // ==================== Logic ====================

    // Theme Management
    const themeBtns = document.querySelectorAll('[data-set-theme]');
    const savedTheme = localStorage.getItem('ats-theme-v2');

    if (savedTheme) applyTheme(savedTheme);

    themeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const theme = btn.dataset.setTheme;
            applyTheme(theme);
            localStorage.setItem('ats-theme-v2', theme);
        });
    });

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme === 'default' ? '' : theme);
    }

    // Gamification initialization removed

    // ==================== Workspace Interaction ====================

    dropArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
            geminiTalk("Awesome resume! Reading those professional secrets... 📄✨");
            // XP Award removed for HR Mode
            triggerSparkle();
        }
    });

    // Drag and Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => { e.preventDefault(); e.stopPropagation(); });
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('active'));
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('active'));
    });

    dropArea.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        handleFileSelect(file);
        // XP Removed
    });

    function handleFileSelect(file) {
        selectedFileName.textContent = `Selected: ${file.name}`;
        selectedFileName.style.display = 'block';
        const reader = new FileReader();
        reader.onload = (e) => {
            resumePreview.textContent = file.type === 'text/plain' ? e.target.result : `[ATS Analysis View: ${file.name} ready for bot-reading!]`;
        };
        reader.readAsText(file);
    }

    jdInput.addEventListener('input', () => {
        charCount.textContent = jdInput.value.length;
        if (jdInput.value.length === 100) geminiTalk("Detailed description! Robots love specifics. 👓");
    });

    // ==================== Analysis Logic ====================

    analyzeBtn.addEventListener('click', async () => {
        if (!fileInput.files.length) return alert('Upload a resume first, challenger! 🛡️');
        if (!jdInput.value.trim()) return alert('Paste a job description so we can match! 🔍');

        const formData = new FormData();
        formData.append('resume_file', fileInput.files[0]);
        formData.append('jd_text', jdInput.value);

        hideAll();
        loadingSection.style.display = 'flex';
        simulateProgress();
        geminiTalk("Judgment day! Sending to the robot overlords... 🧠⚡", 5000);

        try {
            const response = await fetch('/api/analyze', { method: 'POST', body: formData });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error);

            window.lastData = data;
            renderResults(data);

            // Gamification Progress removed for HR Mode
        } catch (error) {
            loadingSection.style.display = 'none';
            uploadSection.style.display = 'grid';
            geminiTalk("Whoa! Mascot catches it dramatically! Let's try again. 🧤✨", 5000);
            alert(`Error: ${error.message}`);
        }
    });

    function simulateProgress() {
        const steps = ["Scanning…", "Consulting the hiring oracle... 🔮", "Checking keywords... 🐝", "Finalizing bot verdict... 🤖"];
        const stepEl = document.getElementById('loadingStep');
        let idx = 0;
        const interval = setInterval(() => {
            if (idx < steps.length) stepEl.textContent = steps[idx++];
            else clearInterval(interval);
        }, 400);
    }

    // ==================== Results Rendering ====================

    // ==================== Role Management ====================
    window.setRole = function (role) {
        document.body.classList.remove('role-candidate', 'role-hr');
        document.body.classList.add(`role-${role}`);

        // Update Buttons
        document.querySelectorAll('.role-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.role === role);
        });

        // Toggle UI Elements
        if (role === 'hr') {
            document.body.classList.add('hr-mode');
            geminiTalk("HR Mode Active. Viewing as Recruiter. 👔");
            // Hide gamification, show professional controls
            if (window.lastData) updateHrControls(window.lastData);
        } else {
            document.body.classList.remove('hr-mode');
            geminiTalk("Candidate Mode. Let's optimize! 🚀");
        }

        localStorage.setItem('ats_role', role);
    };

    // Initialize Role
    const savedRole = localStorage.getItem('ats_role') || 'candidate';
    setRole(savedRole);

    function updateHrControls(data) {
        const controls = document.getElementById('hrControls');
        if (!controls) return;

        const hrMsg = document.getElementById('hrVisibilityMsg');
        if (!hrMsg) return;

        const vis = data.visibility_status || (data.score && data.score.visibility_status);
        if (!vis) return;

        const contactInfoContainer = document.getElementById('hrContactInfo');

        // Reset state
        if (contactInfoContainer) contactInfoContainer.innerHTML = '';
        if (unlockBtn) {
            unlockBtn.style.display = 'block';
            unlockBtn.disabled = true;
        }

        if (vis.contact_details_unlocked) {
            hrMsg.innerHTML = `<span class="vis-visible">✅ Perfect Match</span> Candidate details available.`;
            if (unlockBtn) unlockBtn.style.display = 'none';

            // Auto-show Contact Details
            if (contactInfoContainer) {
                const contact = data.resume_data.contact_info;
                contactInfoContainer.innerHTML = `
                    <div class="contact-details-inline">
                        <div class="c-row name">${contact.name}</div>
                        <div class="c-grid">
                            <div class="c-item">
                                <span class="label">Email</span>
                                <span class="value"><a href="mailto:${contact.email}">${contact.email || 'N/A'}</a></span>
                            </div>
                            <div class="c-item">
                                <span class="label">Phone</span>
                                <span class="value">${contact.phone || 'N/A'}</span>
                            </div>
                            <div class="c-item">
                                <span class="label">Location</span>
                                <span class="value">${contact.location || 'N/A'}</span>
                            </div>
                        </div>
                    </div>
                `;
            }
        } else if (vis.is_recruiter_visible) {
            hrMsg.innerHTML = `<span class="vis-limited">⚠ Potential Match</span> Contact details hidden.`;
            if (vis.missing_mandatory && vis.missing_mandatory.length > 0) {
                hrMsg.innerHTML += `<div style="font-size:0.7rem; color: #c2410c; margin-top:0.25rem;">Missing: ${vis.missing_mandatory.join(', ')}</div>`;
            }
            if (unlockBtn) {
                unlockBtn.disabled = true;
                unlockBtn.textContent = "Unlock (Score too low)";
            }
        } else {
            // Candidate is HIDDEN from HR - show professional message
            hrMsg.innerHTML = `<span class="vis-hidden">❌ Not Qualified</span> This candidate does not meet the minimum requirements.`;
            if (unlockBtn) unlockBtn.disabled = true;

            // Hide the detailed analysis panels for HR
            const hrSuitabilityPanel = document.getElementById('suitability');
            const hrKeywordPanel = document.getElementById('keyword-match');
            if (hrSuitabilityPanel) hrSuitabilityPanel.style.display = 'none';
            if (hrKeywordPanel) hrKeywordPanel.style.display = 'none';
        }
    }

    // ==================== Results Rendering ====================

    function renderResults(data) {
        loadingSection.style.display = 'none';
        resultsSection.style.display = 'grid';

        const finalScore = Math.round(data.total_score || data.score.total_score);

        // Store current candidate data globally for shortlist functionality
        window.currentCandidateData = data;

        // Reset panel visibility (in case they were hidden for a previous low-scoring candidate)
        const hrSuitabilityPanel = document.getElementById('suitability');
        const hrKeywordPanel = document.getElementById('keyword-match');
        if (hrSuitabilityPanel) hrSuitabilityPanel.style.display = '';
        if (hrKeywordPanel) hrKeywordPanel.style.display = '';

        // Update HR Controls if in HR mode
        if (document.body.classList.contains('role-hr')) {
            updateHrControls(data);
        }

        // 1. Score Widget Drama
        const scoreWidget = document.querySelector('.score-widget');
        scoreWidget.classList.add('drama-mode');

        setTimeout(() => {
            scoreWidget.classList.remove('drama-mode');
            animateScore(finalScore);
            updateScoreBadge(finalScore);

            if (finalScore >= 80) {
                triggerConfetti();
                geminiTalk("BOOM! This resume is illegal to ignore. 🚀🔥");
            } else if (finalScore >= 60) {
                geminiTalk("Not bad! ATS is nodding slowly. 🤖");
            } else {
                geminiTalk("Don’t panic. Even pro resumes start somewhere. 🎯");
            }
        }, 300);

        // 2. Breakdown
        breakdownGrid.innerHTML = '';
        Object.entries(data.score.breakdown).forEach(([key, val]) => {
            const row = document.createElement('div');
            row.className = 'breakdown-row';
            row.innerHTML = `<span class="row-label">${key.replace(/_/g, ' ')}</span><span class="row-val">${val.score} / 100</span>`;
            breakdownGrid.appendChild(row);
        });

        // 3. Requirements Comparison Grid
        if (comparisonContainer) {
            let comparisonHtml = '';

            // Skills Comparison
            const mandatorySkills = data.jd_data.mandatory_skills || [];
            const resumeSkills = data.resume_data.skills || [];
            const matchedSkills = data.suitability.matched_skills || [];
            const missingSkills = data.suitability.missing_skills || [];

            comparisonHtml += `
                <div class="comparison-row">
                    <div class="comparison-category">
                        <h4>💼 Technical Skills</h4>
                    </div>
                    <div class="comparison-content">
                        <div class="comparison-col">
                            <div class="col-header">Required by JD</div>
                            <div class="col-items">
                                ${mandatorySkills.length > 0 ? mandatorySkills.map(s => `<span class="req-item">${s}</span>`).join('') : '<span class="no-data">No specific skills required</span>'}
                            </div>
                        </div>
                        <div class="comparison-status">
                            <span class="status-badge ${matchedSkills.length === mandatorySkills.length && mandatorySkills.length > 0 ? 'status-match' : missingSkills.length > 0 ? 'status-partial' : 'status-none'}">
                                ${matchedSkills.length}/${mandatorySkills.length} Match
                            </span>
                        </div>
                        <div class="comparison-col">
                            <div class="col-header">Found in Resume</div>
                            <div class="col-items">
                                ${matchedSkills.length > 0 ? matchedSkills.map(s => `<span class="resume-item matched">✓ ${s}</span>`).join('') : ''}
                                ${missingSkills.length > 0 ? missingSkills.map(s => `<span class="resume-item missing">✗ ${s}</span>`).join('') : ''}
                                ${matchedSkills.length === 0 && missingSkills.length === 0 ? '<span class="no-data">No matching skills detected</span>' : ''}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Education Comparison
            const eduRequired = data.suitability.education_required || 'Not specified';
            const eduFound = data.suitability.resume_education || [];
            const eduMatch = data.suitability.education_match;

            comparisonHtml += `
                <div class="comparison-row">
                    <div class="comparison-category">
                        <h4>🎓 Education</h4>
                    </div>
                    <div class="comparison-content">
                        <div class="comparison-col">
                            <div class="col-header">Required by JD</div>
                            <div class="col-items">
                                <span class="req-item">${eduRequired}</span>
                            </div>
                        </div>
                        <div class="comparison-status">
                            <span class="status-badge ${eduMatch ? 'status-match' : eduRequired === 'Not specified' ? 'status-none' : 'status-no-match'}">
                                ${eduMatch ? '✓ Match' : eduRequired === 'Not specified' ? 'N/A' : '✗ No Match'}
                            </span>
                        </div>
                        <div class="comparison-col">
                            <div class="col-header">Found in Resume</div>
                            <div class="col-items">
                                ${eduFound.length > 0 ? eduFound.map(e => `<span class="resume-item ${eduMatch ? 'matched' : 'partial'}">${e}</span>`).join('') : '<span class="no-data">No education detected</span>'}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Certifications Comparison
            const certsRequired = data.jd_data.required_certifications || [];
            const certsMatched = data.suitability.matched_certifications || [];
            const certsMissing = data.suitability.missing_certifications || [];

            comparisonHtml += `
                <div class="comparison-row">
                    <div class="comparison-category">
                        <h4>📜 Certifications</h4>
                    </div>
                    <div class="comparison-content">
                        <div class="comparison-col">
                            <div class="col-header">Required by JD</div>
                            <div class="col-items">
                                ${certsRequired.length > 0 ? certsRequired.map(c => `<span class="req-item">${c}</span>`).join('') : '<span class="no-data">No certifications required</span>'}
                            </div>
                        </div>
                        <div class="comparison-status">
                            <span class="status-badge ${certsMatched.length === certsRequired.length && certsRequired.length > 0 ? 'status-match' : certsMissing.length > 0 ? 'status-partial' : 'status-none'}">
                                ${certsMatched.length}/${certsRequired.length} Match
                            </span>
                        </div>
                        <div class="comparison-col">
                            <div class="col-header">Found in Resume</div>
                            <div class="col-items">
                                ${certsMatched.length > 0 ? certsMatched.map(c => `<span class="resume-item matched">✓ ${c}</span>`).join('') : ''}
                                ${certsMissing.length > 0 ? certsMissing.map(c => `<span class="resume-item missing">✗ ${c}</span>`).join('') : ''}
                                ${certsMatched.length === 0 && certsMissing.length === 0 ? '<span class="no-data">No certifications detected</span>' : ''}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Experience Comparison
            const expRequired = data.jd_data.experience_required || 'Not specified';
            const expSummary = data.suitability.experience_summary || [];

            comparisonHtml += `
                <div class="comparison-row">
                    <div class="comparison-category">
                        <h4>💼 Experience</h4>
                    </div>
                    <div class="comparison-content">
                        <div class="comparison-col">
                            <div class="col-header">Required by JD</div>
                            <div class="col-items">
                                <span class="req-item">${expRequired}</span>
                            </div>
                        </div>
                        <div class="comparison-status">
                            <span class="status-badge status-none">
                                Review
                            </span>
                        </div>
                        <div class="comparison-col">
                            <div class="col-header">Found in Resume</div>
                            <div class="col-items">
                                ${expSummary.length > 0 ? expSummary.slice(0, 3).map(e => `<span class="resume-item partial">${e}</span>`).join('') : '<span class="no-data">No relevant experience detected</span>'}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            comparisonContainer.innerHTML = comparisonHtml;
        }

        // 4. Keywords
        gapsContainer.innerHTML = '';
        if (data.score.breakdown.skills_match.matched) {
            data.score.breakdown.skills_match.matched.forEach(skill => addKeywordPill(skill, 'matched'));
        }
        if (data.score.breakdown.skills_match.missing) {
            data.score.breakdown.skills_match.missing.forEach(skill => addKeywordPill(skill, 'missing'));
        }

        // 4. Suitability - ENHANCED HR VIEW
        suitabilityVerdict.textContent = data.suitability.verdict;
        suitabilityVerdict.style.color = data.suitability.color;
        suitabilityRecommendation.textContent = data.suitability.recommendation;

        // Build comprehensive HR report
        let hrHtml = `<div class="insight-list">`;

        // Insights
        data.suitability.recruiter_insights.forEach(i => {
            hrHtml += `<div class="insight-item"><span class="icon">💡</span> ${i}</div>`;
        });

        // Skills Matrix
        if (data.suitability.matched_skills && data.suitability.matched_skills.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Matched Skills (Verified)</h5><div class="skill-tags valid">`;
            data.suitability.matched_skills.forEach(s => hrHtml += `<span>✓ ${s}</span>`);
            hrHtml += `</div></div>`;
        }

        if (data.suitability.missing_skills && data.suitability.missing_skills.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Missing Critical Skills</h5><div class="skill-tags missing">`;
            data.suitability.missing_skills.forEach(s => hrHtml += `<span>✗ ${s}</span>`);
            hrHtml += `</div></div>`;
        }

        // Certifications Matrix
        if (data.suitability.matched_certifications && data.suitability.matched_certifications.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Verified Certifications</h5><div class="skill-tags valid">`;
            data.suitability.matched_certifications.forEach(c => hrHtml += `<span>📜 ${c}</span>`);
            hrHtml += `</div></div>`;
        }

        if (data.suitability.missing_certifications && data.suitability.missing_certifications.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Missing Certifications</h5><div class="skill-tags missing">`;
            data.suitability.missing_certifications.forEach(c => hrHtml += `<span>❓ ${c}</span>`);
            hrHtml += `</div></div>`;
        }

        // Education Matrix
        if (data.suitability.education_required !== 'Not specified') {
            const eduClass = data.suitability.education_match ? 'valid' : 'missing';
            const eduIcon = data.suitability.education_match ? '🎓' : '📚';
            const matchStatus = data.suitability.education_match ? 'MATCHED ✓' : 'NOT MATCHED ✗';
            const matchColor = data.suitability.education_match ? 'var(--accent-teal)' : '#ef4444';

            hrHtml += `<div class="hr-section"><h5>Academic Requirement</h5>`;
            hrHtml += `<div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">`;
            hrHtml += `<span style="font-size:0.7rem; font-weight:700; color:${matchColor}; background:${data.suitability.education_match ? 'rgba(20, 184, 166, 0.1)' : 'rgba(239, 68, 68, 0.1)'}; padding:0.25rem 0.5rem; border-radius:4px;">${matchStatus}</span>`;
            hrHtml += `</div>`;
            hrHtml += `<div class="skill-tags ${eduClass}">`;
            hrHtml += `<span>${eduIcon} Required: ${data.suitability.education_required}</span>`;
            hrHtml += `</div><div style="font-size:0.75rem; margin-top:0.5rem; color:var(--text-secondary);">Found: ${data.suitability.resume_education.join(', ') || 'None detected'}</div></div>`;
        } else {
            hrHtml += `<div class="hr-section"><h5>Academic Background</h5><div style="font-size:0.75rem; color:var(--text-secondary);">${data.suitability.resume_education.join(', ') || 'No specific education detected'}</div></div>`;
        }

        // Experience Evidence
        if (data.suitability.experience_summary && data.suitability.experience_summary.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Relevant Evidence Snippets</h5><ul>`;
            data.suitability.experience_summary.forEach(snip => hrHtml += `<li>"${snip}"</li>`);
            hrHtml += `</ul></div>`;
        }

        // --- NEW: Full Professional History for HR ---
        if (data.suitability.work_history && data.suitability.work_history.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Professional History</h5><div class="work-history-list">`;
            data.suitability.work_history.forEach(job => {
                hrHtml += `
                    <div class="work-item-mini" style="margin-bottom:0.75rem; padding-bottom:0.5rem; border-bottom:1px solid var(--border-color);">
                        <div style="font-weight:700; color:var(--text-primary); font-size:0.85rem;">${job.header}</div>
                        <ul style="margin:0.25rem 0 0 1rem; font-size:0.75rem; color:var(--text-secondary);">
                            ${job.bullets.slice(0, 2).map(b => `<li>${b}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
            hrHtml += `</div></div>`;
        }

        hrHtml += `</div>`;
        recruiterInsights.innerHTML = hrHtml;

        // 5. Optimization - Disabled for HR View
        // Optimization features are for candidates only.
    }

    function addKeywordPill(text, type) {
        const pill = document.createElement('div');
        pill.className = `keyword-pill ${type}`;
        pill.textContent = text;
        gapsContainer.appendChild(pill);
    }

    function animateScore(target) {
        let current = 0;
        const ring = scoreRing;
        const circumference = 2 * Math.PI * 45;
        const timer = setInterval(() => {
            if (current >= target) { current = target; clearInterval(timer); }
            scoreNumber.textContent = Math.round(current);
            ring.style.strokeDashoffset = circumference - (current / 100) * circumference;
            current += 1.5;
        }, 30);
    }

    function updateScoreBadge(score) {
        scoreStatus.className = 'score-verdict ' + (score >= 75 ? 'high' : (score >= 50 ? 'mid' : 'low'));
        scoreStatus.textContent = score >= 75 ? 'Strong Match' : (score >= 50 ? 'Potential Match' : 'Weak Match');
    }

    // "Optimize Below" button - scroll to editor
    newAnalysisBtn.addEventListener('click', () => {
        const editorSection = document.getElementById('editor');
        if (editorSection) {
            editorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });

    // "Start New Search" / "Analyze New Resume" button - reload page
    if (resetAnalysisBtn) {
        resetAnalysisBtn.addEventListener('click', () => {
            window.location.href = '/';
        });
    }

    // ==================== HR Actions ====================
    window.unlockContactDetails = function () {
        if (!window.lastData || !window.lastData.resume_data) return alert("Analyze a resume first!");

        const contact = window.lastData.resume_data.contact_info;
        const infoHtml = `
            <div class="contact-card-unlocked">
                <h3>🔓 Candidate Contact Details</h3>
                <p><strong>Name:</strong> ${contact.name}</p>
                <p><strong>Email:</strong> ${contact.email || 'Not found'}</p>
                <p><strong>Phone:</strong> ${contact.phone || 'Not found'}</p>
                <p><strong>Location:</strong> ${contact.location || 'Not found'}</p>
                <div style="margin-top:1rem; font-size:0.8rem; color:var(--accent-teal);">
                    Verified by ATS • High Match Score
                </div>
                <button onclick="this.closest('.contact-card-unlocked').nextElementSibling.remove(); this.closest('.contact-card-unlocked').remove()" 
                        style="margin-top:1.5rem; width:100%; padding:0.75rem; background:var(--bg-app); border:1px solid var(--border-color); border-radius:8px; cursor:pointer; font-weight:600; color:var(--text-primary);">
                    Close
                </button>
            </div>
            <div class="modal-backdrop" onclick="this.nextElementSibling.remove(); this.remove()"></div>
        `;

        const div = document.createElement('div');
        div.innerHTML = infoHtml;
        document.body.appendChild(div);

        // Disable button after unlock
        const unlockBtn = document.getElementById('unlockBtn');
        unlockBtn.textContent = "Details Unlocked ✅";
        unlockBtn.classList.add('btn-success');
        unlockBtn.disabled = true;
    };

    window.shortlistCandidate = async function () {
        const btn = document.getElementById('shortlistBtn');
        const isShortlisted = btn.classList.contains('active');

        if (isShortlisted) {
            // Remove from shortlist
            try {
                const response = await fetch('/api/shortlist/remove', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: window.currentCandidateData?.resume_data?.contact_info?.email
                    })
                });

                const result = await response.json();

                if (result.success) {
                    btn.classList.remove('active');
                    btn.textContent = "Shortlist Candidate";
                    btn.style.borderColor = "";
                    geminiTalk("Candidate removed from shortlist. ❌");
                } else {
                    alert('Failed to remove from shortlist: ' + result.message);
                }
            } catch (error) {
                alert('Error removing from shortlist: ' + error.message);
            }
        } else {
            // Add to shortlist
            try {
                let recruiterName;

                if (window.ATS_USER) {
                    recruiterName = window.ATS_USER;
                    localStorage.setItem('ats_recruiter_name', recruiterName);
                } else {
                    let storedName = localStorage.getItem('ats_recruiter_name') || '';
                    let recruiterNameInput = prompt("Processing Shortlist. Confirm Recruiter Name:", storedName);

                    if (recruiterNameInput) {
                        recruiterName = recruiterNameInput;
                        localStorage.setItem('ats_recruiter_name', recruiterName);
                    } else {
                        if (recruiterNameInput === null) return; // Abort if cancelled
                        recruiterName = storedName || 'Anonymous Recruiter';
                    }
                }

                const candidateData = {
                    candidate_name: window.currentCandidateData?.resume_data?.contact_info?.name,
                    email: window.currentCandidateData?.resume_data?.contact_info?.email,
                    phone: window.currentCandidateData?.resume_data?.contact_info?.phone,
                    total_score: window.currentCandidateData?.score?.total_score,
                    verdict: window.currentCandidateData?.suitability?.verdict,
                    matched_skills: window.currentCandidateData?.suitability?.matched_skills,
                    missing_skills: window.currentCandidateData?.suitability?.missing_skills,
                    education_match: window.currentCandidateData?.suitability?.education_match,
                    matched_certifications: window.currentCandidateData?.suitability?.matched_certifications,
                    job_title: 'Current Analysis',
                    recruiter_name: recruiterName
                };

                const response = await fetch('/api/shortlist/add', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(candidateData)
                });

                const result = await response.json();

                if (result.success) {
                    btn.classList.add('active');
                    btn.textContent = "Shortlisted ⭐";
                    btn.style.borderColor = "var(--accent-teal)";
                    triggerConfetti();
                    geminiTalk(result.message || "Candidate saved to shortlist. ⭐");
                } else {
                    alert(result.message || 'Failed to add to shortlist');
                }
            } catch (error) {
                alert('Error adding to shortlist: ' + error.message);
            }
        }
    };

    window.addInternalNote = function () {
        const note = prompt("Enter recruiter note for this candidate:");
        if (note) {
            const btn = document.getElementById('addNoteBtn');
            btn.textContent = "Note Added 📝";
            btn.title = note;
            geminiTalk("Note saved to candidate profile. 📝");
        }
    };

    // Bind HR Buttons
    if (unlockBtn) unlockBtn.onclick = window.unlockContactDetails;
    if (shortlistBtn) shortlistBtn.onclick = window.shortlistCandidate;
    if (addNoteBtn) addNoteBtn.onclick = window.addInternalNote;
    if (hrNewAnalysisBtn) hrNewAnalysisBtn.onclick = () => window.startOver();

    // ==================== UI Effects ====================

    function geminiTalk(message, duration = 3000) {
        let toast = document.getElementById('notification-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'notification-toast';
            toast.style.cssText = `
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                background: #1e293b;
                border: 1px solid #14b8a6;
                color: #f1f5f9;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                z-index: 10000;
                font-weight: 500;
                transition: opacity 0.3s ease;
                opacity: 0;
            `;
            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.style.display = 'block';
        // Force reflow
        void toast.offsetWidth;
        toast.style.opacity = '1';

        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 300);
        }, duration);
    }

    function triggerConfetti() {
        const popper = document.getElementById('successPopper');
        popper.style.display = 'block';
        setTimeout(() => popper.style.display = 'none', 4000);
    }

    function triggerSparkle() {
        const dropZone = document.getElementById('dropArea');
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle-drop';
        sparkle.innerHTML = '✨✨✨';
        Object.assign(sparkle.style, { left: '50%', top: '50%', fontSize: '3rem' });
        dropZone.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 1000);
    }

    function hideAll() {
        [uploadSection, resultsSection, loadingSection, document.getElementById('aboutSection')].forEach(s => { if (s) s.style.display = 'none'; });
    }

    // ==================== Navigation & Routing ====================

    function navigate(target) {
        hideAll();

        // Handle physical section visibility
        if (target === 'dashboard') {
            if (window.lastData) {
                resultsSection.style.display = 'grid';
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                uploadSection.style.display = 'grid';
            }
        } else if (target === 'about') {
            document.getElementById('aboutSection').style.display = 'flex';
        } else if (target === 'score') {
            if (!window.lastData) return alert("Analyze a resume first to see your score! 📊");
            resultsSection.style.display = 'grid';
            document.getElementById('suitability').scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else if (target === 'optimize') {
            if (!window.lastData) return alert("Analyze a resume first to unlock the optimization editor! 🚀");
            resultsSection.style.display = 'grid';
            document.getElementById('editor').scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        // Update active states
        [...navLinks, ...sidebarItems].forEach(el => {
            const text = el.textContent.trim().toLowerCase();
            const href = el.getAttribute('href') || '';
            const isActive = text.includes(target) || href.includes(target);
            el.classList.toggle('active', isActive);
        });
    }

    [...navLinks, ...sidebarItems].forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');

            // Allow external links (start with / or http) to behave normally
            if (!href || href.startsWith('/') || href.startsWith('http')) return;

            // Handle internal navigation for dashboard sections
            e.preventDefault();

            if (href === '#dashboard' || href.includes('dashboard')) navigate('dashboard');
            else if (href === '#score-info' || href.includes('score')) navigate('score');
            else if (href === '#optimize-info' || href.includes('optimize')) navigate('optimize');
            else if (href === '#about' || href.includes('about')) navigate('about');
        });
    });

    if (newAnalysisBtn) {
        newAnalysisBtn.onclick = () => window.startOver();
    }

    if (resetAnalysisBtn) {
        resetAnalysisBtn.onclick = () => window.startOver();
    }

    // ==================== Download Logic ====================

    if (downloadReportBtn) {
        downloadReportBtn.onclick = async () => {
            if (!window.lastData) return;
            try {
                const response = await fetch('/api/download-report', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(window.lastData)
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `ATS_Report_${new Date().getTime()}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                geminiTalk("PDF Report downloaded! You're ready for the big leagues. 📄⭐");
            } catch (e) {
                alert("Download failed. The server might be shy. 🙈");
            }
        };
    }

    if (downloadResumeBtn) {
        downloadResumeBtn.onclick = async () => {
            const text = optimizedResume.innerText;
            try {
                const response = await fetch('/api/download-resume', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ resume_text: text })
                });
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Optimized_Resume_${new Date().getTime()}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
                geminiTalk("Optimized resume exported as PDF! Go get 'em, tiger! 🐯🚀");
            } catch (e) {
                alert("Export failed. Let's try manual copy-paste? 📋");
            }
        };
    }

    // Follow Cursor logic
    document.addEventListener('mousemove', (e) => {
        const glow = document.getElementById('mouseGlow');
        if (glow) { glow.style.left = e.clientX + 'px'; glow.style.top = e.clientY + 'px'; }
        const aiCompanion = document.getElementById('aiCompanion');
        if (aiCompanion) {
            const x = (e.clientX / window.innerWidth - 0.5) * 40;
            const y = (e.clientY / window.innerHeight - 0.5) * 40;
            aiCompanion.style.transform = `translate(${x}px, ${y}px)`;
        }
    });

    // Start Over logic - Navigate to home page for new analysis
    window.startOver = function () {
        window.location.href = '/';
    };
});
