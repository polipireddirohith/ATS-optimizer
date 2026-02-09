/**
 * ATS Resume Optimizer - Frontend Logic
 * Handles file uploads, API communication, and UI updates
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const form = document.getElementById('atsForm');
    const fileInput = document.getElementById('resumeFile');
    const fileDisplay = document.querySelector('.file-upload-display');
    const fileNameDisplay = document.querySelector('.file-name');
    const jdInput = document.getElementById('jdText');
    const charCount = document.getElementById('charCount');
    const uploadSection = document.getElementById('uploadSection');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');

    // Result Elements
    const scoreNumber = document.getElementById('scoreNumber');
    const scoreStatus = document.getElementById('scoreStatus');
    const scoreRing = document.getElementById('scoreRing');
    const breakdownItems = document.getElementById('breakdownItems');
    const gapsContainer = document.getElementById('gapsContainer');
    const improvementsContainer = document.getElementById('improvementsContainer');
    const optimizedResume = document.getElementById('optimizedResume');

    // Buttons
    const downloadReportBtn = document.getElementById('downloadReportBtn');
    const downloadResumeBtn = document.getElementById('downloadResumeBtn');
    const mouseGlow = document.getElementById('mouseGlow');

    // Mouse Glow Tracking
    document.addEventListener('mousemove', (e) => {
        if (mouseGlow) {
            // Using requestAnimationFrame for better performance
            window.requestAnimationFrame(() => {
                mouseGlow.style.left = e.clientX + 'px';
                mouseGlow.style.top = e.clientY + 'px';
            });
        }
    });

    // Theme Switcher
    const themeBtns = document.querySelectorAll('[data-set-theme]');
    themeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const theme = btn.dataset.setTheme;
            document.documentElement.setAttribute('data-theme', theme === 'default' ? '' : theme);

            // Save preference
            localStorage.setItem('ats-theme', theme);
        });
    });

    // Load saved theme
    const savedTheme = localStorage.getItem('ats-theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme === 'default' ? '' : savedTheme);
    }

    // State
    let currentData = null;

    // ==================== Event Listeners ====================

    // File Input Change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            updateFileDisplay(file.name);
        }
    });

    // Drag and Drop
    fileDisplay.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileDisplay.style.borderColor = 'var(--primary-color)';
        fileDisplay.style.background = '#f0f4ff';
    });

    fileDisplay.addEventListener('dragleave', (e) => {
        e.preventDefault();
        fileDisplay.style.borderColor = 'var(--border-color)';
        fileDisplay.style.background = 'var(--bg-secondary)';
    });

    fileDisplay.addEventListener('drop', (e) => {
        e.preventDefault();
        fileDisplay.style.borderColor = 'var(--border-color)';
        fileDisplay.style.background = 'var(--bg-secondary)';

        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            updateFileDisplay(e.dataTransfer.files[0].name);
        }
    });

    // Character Count
    jdInput.addEventListener('input', (e) => {
        charCount.textContent = e.target.value.length;
    });

    // Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!fileInput.files.length) {
            alert('Please select a resume file');
            return;
        }

        if (!jdInput.value.trim()) {
            alert('Please enter a job description');
            return;
        }

        await analyzeResume();
    });

    // Tab Switching
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            const tabId = tab.dataset.tab;
            document.getElementById(`${tabId}Tab`).classList.add('active');
        });
    });

    // New Analysis
    newAnalysisBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
        uploadSection.style.display = 'block';
        form.reset();
        resetFileDisplay();
        window.scrollTo(0, 0);
    });

    // Download Buttons
    downloadReportBtn.addEventListener('click', downloadReport);
    downloadResumeBtn.addEventListener('click', downloadOptimizedResume);

    // ==================== Functions ====================

    function updateFileDisplay(filename) {
        fileNameDisplay.textContent = filename;
        fileNameDisplay.style.display = 'inline-block';
        document.querySelector('.upload-text').style.display = 'none';
        document.querySelector('.upload-icon').style.display = 'none';
    }

    function resetFileDisplay() {
        fileNameDisplay.style.display = 'none';
        document.querySelector('.upload-text').style.display = 'flex';
        document.querySelector('.upload-icon').style.display = 'block';
    }

    async function analyzeResume() {
        // Show loading state
        uploadSection.style.display = 'none';
        loadingSection.style.display = 'block';

        const formData = new FormData(form);

        try {
            // Simulate progress steps
            simulateLoading();

            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Analysis failed');
            }

            currentData = data;
            displayResults(data);

        } catch (error) {
            alert(`Error: ${error.message}`);
            loadingSection.style.display = 'none';
            uploadSection.style.display = 'block';
        }
    }

    function simulateLoading() {
        const steps = [
            'Parsing resume document...',
            'Extracting key skills and experience...',
            'Analyzing job description requirements...',
            'Calculating compatibility match...',
            'Identifying improvement opportunities...',
            'Generating optimized resume...'
        ];

        const loadingStep = document.getElementById('loadingStep');
        let stepIndex = 0;

        const interval = setInterval(() => {
            if (stepIndex < steps.length) {
                loadingStep.textContent = steps[stepIndex];
                stepIndex++;
            } else {
                clearInterval(interval);
            }
        }, 800);
    }

    function displayResults(data) {
        loadingSection.style.display = 'none';
        resultsSection.style.display = 'block';

        // Update Score
        animateScore(data.score.total_score);
        updateScoreStatus(data.score.total_score);

        // Update Breakdown
        renderBreakdown(data.score.breakdown);

        // Update Gaps
        renderGaps(data.gaps);

        // Update Improvements
        renderImprovements(data.improvements);

        // Update Recruiter Insights
        renderRecruiterInsights(data.suitability);

        // Update Optimized Resume
        optimizedResume.textContent = data.optimized_resume;

        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderRecruiterInsights(suitability) {
        const verdictValue = document.getElementById('suitabilityVerdict');
        const recommendationText = document.getElementById('suitabilityRecommendation');
        const insightsContainer = document.getElementById('recruiterInsights');

        verdictValue.textContent = suitability.verdict;
        verdictValue.style.backgroundColor = suitability.color;
        recommendationText.textContent = `HR Recommendation: ${suitability.recommendation}`;

        insightsContainer.innerHTML = '';
        suitability.recruiter_insights.forEach(insight => {
            const card = document.createElement('div');
            card.className = 'insight-card';
            card.innerHTML = `
                <div class="insight-icon">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div class="insight-content">${insight}</div>
            `;
            insightsContainer.appendChild(card);
        });
    }

    function animateScore(targetScore) {
        let currentScore = 0;
        const duration = 1500;
        const interval = 20;
        const increment = targetScore / (duration / interval);

        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
            }

            scoreNumber.textContent = Math.round(currentScore);

            // Update circle stroke
            const circumference = 2 * Math.PI * 85; // r=85
            const offset = circumference - (currentScore / 100) * circumference;
            scoreRing.style.strokeDasharray = `${circumference} ${circumference}`;
            scoreRing.style.strokeDashoffset = offset;

        }, interval);
    }

    function updateScoreStatus(score) {
        let statusHtml = '';
        let statusClass = '';

        if (score >= 80) {
            statusClass = 'excellent';
            statusHtml = `
                <div class="status-badge excellent">EXCELLENT MATCH</div>
                <p class="status-message">Your resume is highly optimized for this role. You have a strong chance of passing the ATS.</p>
            `;
        } else if (score >= 60) {
            statusClass = 'good';
            statusHtml = `
                <div class="status-badge good">GOOD MATCH</div>
                <p class="status-message">Good potential, but there are some important gaps to address to improve your ranking.</p>
            `;
        } else {
            statusClass = 'needs-improvement';
            statusHtml = `
                <div class="status-badge needs-improvement">NEEDS IMPROVEMENT</div>
                <p class="status-message">Your resume needs significant optimization to pass the ATS filters for this role.</p>
            `;
        }

        scoreStatus.innerHTML = statusHtml;
    }

    function renderBreakdown(breakdown) {
        breakdownItems.innerHTML = '';

        for (const [key, value] of Object.entries(breakdown)) {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            const html = `
                <div class="breakdown-item">
                    <div>
                        <span class="breakdown-label">${label}</span>
                        <span class="breakdown-weight">(${value.weight})</span>
                    </div>
                    <span class="breakdown-score">${value.score}/100</span>
                </div>
            `;
            breakdownItems.innerHTML += html;
        }
    }

    function renderGaps(gaps) {
        gapsContainer.innerHTML = '';

        // Critical Gaps
        if (gaps.critical && Object.keys(gaps.critical).length > 0) {
            let hasCritical = false;
            let html = `<div class="gap-section critical"><h4><span class="gap-badge critical">Critical</span> Missing Requirements</h4><ul class="gap-list">`;

            for (const [key, items] of Object.entries(gaps.critical)) {
                if (items && items.length > 0) {
                    hasCritical = true;
                    // Format key for display
                    const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                    items.forEach(item => {
                        html += `<li>Missing ${label}: <strong>${item}</strong></li>`;
                    });
                }
            }
            html += `</ul></div>`;

            if (hasCritical) gapsContainer.innerHTML += html;
        }

        // Important Gaps
        if (gaps.important && Object.keys(gaps.important).length > 0) {
            let hasImportant = false;
            let html = `<div class="gap-section important"><h4><span class="gap-badge important">Important</span> Optimization Opportunities</h4><ul class="gap-list">`;

            for (const [key, items] of Object.entries(gaps.important)) {
                if (items && items.length > 0) {
                    hasImportant = true;
                    items.forEach(item => {
                        html += `<li>${item}</li>`;
                    });
                }
            }
            html += `</ul></div>`;

            if (hasImportant) gapsContainer.innerHTML += html;
        }

        // Formatting Issues
        if (gaps.formatting_issues && gaps.formatting_issues.length > 0) {
            let html = `<div class="gap-section optional"><h4><span class="gap-badge optional">Formatting</span> ATS Readability Issues</h4><ul class="gap-list">`;
            gaps.formatting_issues.forEach(issue => {
                html += `<li>${issue}</li>`;
            });
            html += `</ul></div>`;
            gapsContainer.innerHTML += html;
        }

        if (gapsContainer.innerHTML === '') {
            gapsContainer.innerHTML = '<p>No significant gaps detected! Great job.</p>';
        }
    }

    function renderImprovements(improvements) {
        improvementsContainer.innerHTML = '';

        // Keyword Insertions
        if (improvements.keyword_insertions && improvements.keyword_insertions.length > 0) {
            let html = `<div class="improvement-section"><h4>Keyword Strategy</h4>`;
            improvements.keyword_insertions.forEach(item => {
                html += `
                    <div class="improvement-item">
                        <p><strong>Add "${item.keyword}"</strong> to ${item.location}</p>
                        <p class="text-sm text-muted">${item.suggestion}</p>
                    </div>
                `;
            });
            html += `</div>`;
            improvementsContainer.innerHTML += html;
        }

        // Bullet Rewrites
        if (improvements.bullet_point_rewrites && improvements.bullet_point_rewrites.length > 0) {
            let html = `<div class="improvement-section"><h4>Bullet Point Enhancements</h4>`;
            improvements.bullet_point_rewrites.forEach(item => {
                html += `
                    <div class="improvement-item">
                        <p class="text-muted strike">Original: ${item.original}</p>
                        <p><strong>Improved:</strong> ${item.improved}</p>
                        <p class="text-sm text-muted"><em>Why: ${item.reason}</em></p>
                    </div>
                `;
            });
            html += `</div>`;
            improvementsContainer.innerHTML += html;
        }
    }

    async function downloadReport() {
        if (!currentData) return;

        try {
            const response = await fetch('/api/download-report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(currentData)
            });

            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'ATS_Report.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            alert('Failed to download report');
        }
    }

    async function downloadOptimizedResume() {
        if (!currentData) return;

        try {
            const response = await fetch('/api/download-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ resume_text: currentData.optimized_resume })
            });

            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Optimized_Resume.txt';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

        } catch (error) {
            alert('Failed to download resume');
        }
    }
});
