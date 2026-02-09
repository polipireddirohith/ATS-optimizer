/**
 * ATS Resume Analyzer - Enterprise SaaS Frontend Logic
 * Inspired by Manatal and modern recruiter ATS systems.
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
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const navLinks = document.querySelectorAll('.nav-links a');

    // Core Results Widgets
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreRing = document.getElementById('scoreRing');
    const scoreStatus = document.getElementById('scoreStatus');
    const breakdownGrid = document.getElementById('breakdownGrid');
    const gapsContainer = document.getElementById('gapsContainer');
    const suitabilityVerdict = document.getElementById('suitabilityVerdict');
    const suitabilityRecommendation = document.getElementById('suitabilityRecommendation');
    const recruiterInsights = document.getElementById('recruiterInsights');
    const optimizedResume = document.getElementById('optimizedResume');
    const improvementsContainer = document.getElementById('improvementsContainer');

    // Buttons
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    const downloadReportBtn = document.getElementById('downloadReportBtn');
    const downloadResumeBtn = document.getElementById('downloadResumeBtn');

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

    // Particle Generation
    function createNodes() {
        const container = document.getElementById('particles');
        if (!container) return;

        for (let i = 0; i < 20; i++) {
            const node = document.createElement('div');
            Object.assign(node.style, {
                position: 'absolute',
                width: '3px',
                height: '3px',
                background: 'var(--accent-teal)',
                borderRadius: '50%',
                top: Math.random() * 100 + '%',
                left: Math.random() * 100 + '%',
                opacity: '0.1',
                pointerEvents: 'none',
                boxShadow: '0 0 10px var(--accent-teal)'
            });
            container.appendChild(node);

            node.animate([
                { transform: 'translate(0, 0)', opacity: 0.1 },
                { transform: `translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px)`, opacity: 0.3 }
            ], {
                duration: 5000 + Math.random() * 5000,
                iterations: Infinity,
                direction: 'alternate',
                easing: 'ease-in-out'
            });
        }
    }
    createNodes();

    // ==================== Workspace Logic ====================

    // Trigger file input
    dropArea.addEventListener('click', () => fileInput.click());

    // File selection handler
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Drag and Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('active'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('active'), false);
    });

    dropArea.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        handleFileSelect(file);
    });

    function handleFileSelect(file) {
        selectedFileName.textContent = `Selected: ${file.name}`;
        selectedFileName.style.display = 'block';

        // Simulating immediate text extraction preview
        const reader = new FileReader();
        reader.onload = (e) => {
            // Only preview text if it looks like a text-readable file (basic heuristic)
            if (file.type === 'text/plain') {
                resumePreview.textContent = e.target.result;
            } else {
                resumePreview.textContent = `[ATS View: ${file.name} - Ready for backend parsing. Professional ATS systems will extract keywords from this ${file.type.split('/')[1].toUpperCase()} document.]`;
            }
        };
        reader.readAsText(file);
    }

    // JD Character Count
    jdInput.addEventListener('input', () => {
        charCount.textContent = jdInput.value.length;
    });

    // Navigation Logic
    const aboutSection = document.getElementById('aboutSection');

    function hideAll() {
        uploadSection.style.display = 'none';
        resultsSection.style.display = 'none';
        loadingSection.style.display = 'none';
        if (aboutSection) aboutSection.style.display = 'none';
    }

    function showDashboard() {
        hideAll();
        if (window.lastData) {
            resultsSection.style.display = 'grid';
        } else {
            uploadSection.style.display = 'grid';
        }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function showInfo(subId) {
        hideAll();
        if (aboutSection) {
            aboutSection.style.display = 'flex';
            if (subId) {
                const target = document.getElementById(subId);
                if (target) {
                    // Slight delay to ensure display: flex is rendered before scrolling
                    setTimeout(() => target.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
                }
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
    }

    // Top Nav Links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const text = link.textContent.trim();
            if (text === 'Dashboard') showDashboard();
            else if (text === 'Resume Score') showInfo('scoreInfo');
            else if (text === 'Optimize') showInfo('optimizeInfo');
            else if (text === 'About') showInfo();
        });
    });

    // Logo Click
    document.querySelector('.nav-logo').addEventListener('click', () => {
        showDashboard();
        navLinks.forEach(l => l.classList.remove('active'));
        navLinks[0].classList.add('active');
    });

    // Sidebar Navigation
    sidebarItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const href = item.getAttribute('href');
            if (href.startsWith('#')) {
                // If we're in results, scroll to panel
                if (resultsSection.style.display !== 'none') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                } else if (href === '#analysis') {
                    e.preventDefault();
                    showDashboard();
                }
            }
            sidebarItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
    });

    // ==================== Analysis Logic ====================

    analyzeBtn.addEventListener('click', async () => {
        if (!fileInput.files.length) return alert('Please upload a resume first.');
        if (!jdInput.value.trim()) return alert('Please provide a job description.');

        const formData = new FormData();
        formData.append('resume_file', fileInput.files[0]);
        formData.append('jd_text', jdInput.value);

        // UI State: Loading
        uploadSection.style.display = 'none';
        loadingSection.style.display = 'flex';
        simulateProgress();

        try {
            const response = await fetch('/api/analyze', { method: 'POST', body: formData });
            const data = await response.json();

            if (!response.ok) throw new Error(data.error);

            window.lastData = data; // Store for downloads
            renderResults(data);
        } catch (error) {
            alert(`Error analyzing resume: ${error.message}`);
            loadingSection.style.display = 'none';
            uploadSection.style.display = 'grid';
        }
    });

    function simulateProgress() {
        const steps = [
            "Initializing ATS parsing engine...",
            "Extracting identity and contact metadata...",
            "Contextualizing professional experience...",
            "Running multi-layer skill match analysis...",
            "Evaluating document formatting compatibility...",
            "Finalizing recruiter suitability verdict..."
        ];
        const stepEl = document.getElementById('loadingStep');
        let idx = 0;
        const interval = setInterval(() => {
            if (idx < steps.length) {
                stepEl.textContent = steps[idx++];
            } else {
                clearInterval(interval);
            }
        }, 1200);
    }

    // ==================== Results Rendering ====================

    function renderResults(data) {
        loadingSection.style.display = 'none';
        resultsSection.style.display = 'grid';

        // Gemini Response
        const finalScore = Math.round(data.total_score || data.score.total_score);
        if (finalScore > 80) geminiTalk(`WOW! ${finalScore}% match! You're a superstar! 🌟`);
        else if (finalScore > 50) geminiTalk(`Solid match! Let's tweak it to perfection! 🛠️`);
        else geminiTalk("A bit of work to do, but we'll get there! 🎯");

        // 1. Score Widget
        const score = finalScore;
        animateScore(score);
        updateScoreBadge(score);

        // 2. Breakdown Grid
        breakdownGrid.innerHTML = '';
        Object.entries(data.score.breakdown).forEach(([key, val]) => {
            const row = document.createElement('div');
            row.className = 'breakdown-row';
            row.innerHTML = `<span class="row-label">${key.replace(/_/g, ' ').toUpperCase()}</span><span class="row-val">${val.score}%</span>`;
            breakdownGrid.innerHTML += row.outerHTML;
        });

        // 3. Keyword Mesh
        gapsContainer.innerHTML = '';
        // Extracting mandatory skills for the 'Matched' list
        const mandatory = data.jd_data.mandatory_skills;
        const found = data.suitability.recruiter_insights[1]?.match(/\d+\/\d+/) ? true : false; // Heuristic skill check

        // Simplified keyword display for professional UI
        data.score.breakdown.skills_match.matched?.forEach(skill => {
            addKeywordPill(skill, 'matched');
        });

        data.gaps.critical.skills?.forEach(skill => {
            addKeywordPill(skill, 'missing');
        });

        // 4. Suitability
        suitabilityVerdict.textContent = data.suitability.verdict;
        suitabilityVerdict.style.color = data.suitability.color;
        suitabilityRecommendation.textContent = data.suitability.recommendation;

        recruiterInsights.innerHTML = '';
        data.suitability.recruiter_insights.forEach(insight => {
            const div = document.createElement('div');
            div.className = 'insight-item';
            div.textContent = insight;
            recruiterInsights.appendChild(div);
        });

        // 5. Editor Workspace
        optimizedResume.textContent = data.optimized_resume;

        improvementsContainer.innerHTML = '';
        data.improvements.keyword_insertions.slice(0, 4).forEach(item => {
            const card = document.createElement('div');
            card.className = 'suggestion-card';
            card.innerHTML = `<strong>Add ${item.keyword}</strong> ${item.suggestion}`;
            improvementsContainer.appendChild(card);
        });

        // Sync editor changes back to data (optional for real apps)
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
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            scoreNumber.textContent = Math.round(current);
            const offset = circumference - (current / 100) * circumference;
            ring.style.strokeDashoffset = offset;
            current += 1.5;
        }, 30);
    }

    function updateScoreBadge(score) {
        scoreStatus.className = 'score-verdict ' + (score >= 75 ? 'high' : (score >= 50 ? 'mid' : 'low'));
        scoreStatus.textContent = score >= 75 ? 'Strong Match' : (score >= 50 ? 'Potential Match' : 'Weak Match');
    }

    // Re-launch analysis
    newAnalysisBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
        uploadSection.style.display = 'grid';
        form.reset();
        jdInput.value = '';
        resumePreview.textContent = 'No document uploaded yet...';
        selectedFileName.style.display = 'none';
        window.scrollTo(0, 0);
    });

    // ==================== Downloads ====================

    downloadResumeBtn.addEventListener('click', async () => {
        if (!window.lastData) return;
        try {
            const res = await fetch('/api/download-resume', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_text: optimizedResume.textContent })
            });
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ATS_Optimized_Resume.txt';
            a.click();
        } catch (e) { alert('Export error.'); }
    });

    downloadReportBtn.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/download-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(window.lastData || {})
            });
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ATS_Professional_Report.txt';
            a.click();
        } catch (e) { alert('Report generation error.'); }
    });

    // ==================== Gemini AI Interaction ====================
    const aiCompanion = document.getElementById('aiCompanion');
    const aiStatusText = aiCompanion.querySelector('.status-bubble');
    let geminiTimeout;

    function geminiTalk(message, duration = 3000) {
        if (!aiCompanion) return;
        clearTimeout(geminiTimeout);
        aiStatusText.textContent = message;
        aiCompanion.classList.add('talking');

        geminiTimeout = setTimeout(() => {
            aiCompanion.classList.remove('talking');
        }, duration);
    }

    // Initial greeting
    setTimeout(() => geminiTalk("Looking for a job? Let's optimize! 🚀"), 1500);

    // React to file upload
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            geminiTalk("Awesome resume! Let's see those skills... 📄✨");
            triggerSparkle();
        }
    });

    // React to JD typing
    jdInput.addEventListener('input', () => {
        if (jdInput.value.length > 50 && jdInput.value.length < 55) {
            geminiTalk("Reading the fine print... You've got this! 💪");
        }
    });

    // React to analysis start
    analyzeBtn.addEventListener('click', () => {
        if (fileInput.files.length && jdInput.value.trim()) {
            geminiTalk("Analysing... Gemini logic: ACTIVATED! 🧠⚡", 5000);
        }
    });

    // Follow Cursor logic for AI Orb
    document.addEventListener('mousemove', (e) => {
        if (!aiCompanion) return;
        const x = (e.clientX / window.innerWidth - 0.5) * 40;
        const y = (e.clientY / window.innerHeight - 0.5) * 40;
        aiCompanion.style.transform = `translate(${x}px, ${y}px)`;
    });

    function triggerSparkle() {
        const dropZone = document.getElementById('dropArea');
        const sparkle = document.createElement('div');
        sparkle.className = 'sparkle-drop';
        sparkle.innerHTML = '✨✨✨';
        Object.assign(sparkle.style, {
            left: '50%',
            top: '50%',
            fontSize: '3rem'
        });
        dropZone.appendChild(sparkle);
        setTimeout(() => sparkle.remove(), 1000);
    }

    // Update Gemini on results - Logic moved into renderResults directly
    // Logic was cleaned up here

    // ==================== Interactions ====================
    // Mouse Glow
    const glow = document.getElementById('mouseGlow');
    document.addEventListener('mousemove', (e) => {
        if (glow) {
            glow.style.left = e.clientX + 'px';
            glow.style.top = e.clientY + 'px';
        }
    });
});
