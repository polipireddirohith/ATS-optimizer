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
    const sidebarItems = document.querySelectorAll('.sidebar-item');
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

    // ==================== Gamification Core ====================

    const gameState = {
        xp: parseInt(localStorage.getItem('ats_xp') || '0'),
        level: parseInt(localStorage.getItem('ats_level') || '1'),
        streak: parseInt(localStorage.getItem('ats_streak') || '0'),
        lastVisit: localStorage.getItem('ats_last_visit'),
        achievements: JSON.parse(localStorage.getItem('ats_achievements') || '[]'),
        dailyChallengeDone: localStorage.getItem('ats_daily_done') === new Date().toDateString()
    };

    const levels = [
        { minXp: 0, name: "Resume Rookie" },
        { minXp: 500, name: "ATS Explorer" },
        { minXp: 1500, name: "Keyword Ninja" },
        { minXp: 3500, name: "Resume Pro" },
        { minXp: 7000, name: "Recruiter-Ready" }
    ];

    function saveState() {
        localStorage.setItem('ats_xp', gameState.xp);
        localStorage.setItem('ats_level', gameState.level);
        localStorage.setItem('ats_streak', gameState.streak);
        localStorage.setItem('ats_achievements', JSON.stringify(gameState.achievements));
    }

    function addXp(amount, reason) {
        gameState.xp += amount;
        if (reason) geminiTalk(`+${amount} XP: ${reason} ✨`, 2000);
        updateXpUi();
        checkLevelUp();
        saveState();
    }

    function updateXpUi() {
        const currentLevel = levels[gameState.level - 1];
        const nextLevel = levels[gameState.level] || { minXp: gameState.xp + 1000 };
        const progress = ((gameState.xp - currentLevel.minXp) / (nextLevel.minXp - currentLevel.minXp)) * 100;

        xpBar.style.width = `${Math.min(progress, 100)}%`;
        xpText.textContent = `${gameState.xp} / ${nextLevel.minXp} XP`;
        levelBadge.textContent = `Lv. ${gameState.level}`;
        levelName.textContent = currentLevel.name;
    }

    function checkLevelUp() {
        const nextLevel = levels[gameState.level];
        if (nextLevel && gameState.xp >= nextLevel.minXp) {
            gameState.level++;
            geminiTalk(`LEVEL UP! You are now a ${nextLevel.name}! 🎉`, 5000);
            triggerConfetti();
            updateXpUi();
        }
    }

    function unlockAchievement(id, title, icon) {
        if (gameState.achievements.find(a => a.id === id)) return;

        const achievement = { id, title, icon, date: new Date().toLocaleDateString() };
        gameState.achievements.unshift(achievement);
        renderAchievements();
        geminiTalk(`ACHIEVEMENT UNLOCKED: ${title} 🏆`, 4000);
        addXp(250, "Achievement Unlocked");
        saveState();
    }

    function renderAchievements() {
        if (!achievementsList) return;
        achievementsList.innerHTML = gameState.achievements.slice(0, 3).map(a => `
            <div class="achievement-mini-item">
                <div class="achievement-icon">${a.icon}</div>
                <div class="achievement-info">
                    <strong>${a.title}</strong>
                    <span>${a.date}</span>
                </div>
            </div>
        `).join('');
    }

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

    // Initialize UI
    updateXpUi();
    renderAchievements();

    // Streak & Daily
    const today = new Date().toDateString();
    if (gameState.lastVisit !== today) {
        if (gameState.lastVisit) {
            const lastDate = new Date(gameState.lastVisit);
            const diff = (new Date() - lastDate) / (1000 * 60 * 60 * 24);
            if (diff <= 1.5) {
                gameState.streak++;
            } else {
                geminiTalk("Your streak missed you yesterday! 🥺 Let's rebuild it.", 5000);
            }
        } else {
            gameState.streak = 1;
        }
        gameState.lastVisit = today;
        localStorage.setItem('ats_last_visit', today);
        saveState();
    }

    if (gameState.streak > 0) {
        document.getElementById('streakIndicator').style.display = 'flex';
        streakCount.textContent = gameState.streak;
    }

    if (gameState.dailyChallengeDone) {
        challengeDot.classList.add('completed');
        challengeStatus.textContent = "Completed";
    }

    // ==================== Workspace Interaction ====================

    dropArea.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
            geminiTalk("Awesome resume! Reading those professional secrets... 📄✨");
            addXp(50, "Resume Uploaded");
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
        addXp(50, "Resume Dropped");
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

            // Gamification Progress
            addXp(200, "Full Analysis Complete");
            if (!gameState.dailyChallengeDone) {
                gameState.dailyChallengeDone = true;
                localStorage.setItem('ats_daily_done', today);
                challengeDot.classList.add('completed');
                challengeStatus.textContent = "Completed";
                addXp(100, "Daily Challenge Met");
            }
            unlockAchievement('first_scan', 'First Optimization', '✨');
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

        const msg = document.getElementById('hrVisibilityMsg');
        if (!msg) return;

        const vis = data.visibility_status || (data.score && data.score.visibility_status);
        if (!vis) return;

        const contactInfoContainer = document.getElementById('hrContactInfo');

        // Reset state
        if (contactInfoContainer) contactInfoContainer.innerHTML = '';
        unlockBtn.style.display = 'block';
        unlockBtn.disabled = true;

        if (vis.contact_details_unlocked) {
            msg.innerHTML = `<span class="vis-visible">✅ Perfect Match</span> Candidate details available.`;
            unlockBtn.style.display = 'none'; // Hide unlock button since we show it directly

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
            msg.innerHTML = `<span class="vis-limited">⚠ Potential Match</span> Contact details hidden.`;
            if (vis.missing_mandatory && vis.missing_mandatory.length > 0) {
                msg.innerHTML += `<div style="font-size:0.7rem; color: #c2410c; margin-top:0.25rem;">Missing: ${vis.missing_mandatory.join(', ')}</div>`;
            }
            unlockBtn.disabled = true;
            unlockBtn.textContent = "Unlock (Score too low)";
        } else {
            msg.innerHTML = `<span class="vis-hidden">❌ Hidden</span> Score too low for visibility.`;
            unlockBtn.disabled = true;
        }
    }

    // ==================== Results Rendering ====================

    function renderResults(data) {
        loadingSection.style.display = 'none';
        resultsSection.style.display = 'grid';

        const finalScore = Math.round(data.total_score || data.score.total_score);

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
                unlockAchievement('top_tier', 'ATS Score 80+', '🚀');
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

        // 3. Keywords
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

        // Experience Evidence
        if (data.suitability.experience_summary && data.suitability.experience_summary.length > 0) {
            hrHtml += `<div class="hr-section"><h5>Contextual Evidence</h5><ul>`;
            data.suitability.experience_summary.forEach(snip => hrHtml += `<li>"${snip}"</li>`);
            hrHtml += `</ul></div>`;
        }

        hrHtml += `</div>`;
        recruiterInsights.innerHTML = hrHtml;

        // 5. Editor & Comprehensive Improvements
        optimizedResume.innerText = data.optimized_resume;
        improvementsContainer.innerHTML = '';

        const allSuggestions = [
            ...(data.improvements.keyword_insertions || []).map(i => ({ ...i, icon: '➕' })),
            ...(data.improvements.bullet_point_rewrites || []).map(i => ({ ...i, icon: '✍️', keyword: 'STAR Rewrite' })),
            ...(data.improvements.formatting_fixes || []).map(i => ({ keyword: 'Formatting', suggestion: i, icon: '🎨' }))
        ];

        if (allSuggestions.length > 0) {
            improvementsContainer.innerHTML = allSuggestions.slice(0, 8).map(i => `
                <div class="suggestion-card" onclick="window.applySuggestion('${i.suggestion.replace(/'/g, "\\'")}'); this.classList.add('applied');">
                    <span style="font-size:1.2rem; margin-right:0.5rem;">${i.icon}</span>
                    <div>
                        <strong>${i.keyword}</strong>
                        <p>${i.suggestion}</p>
                    </div>
                </div>
            `).join('');
        }

        window.applySuggestion = function (text) {
            // Focus editor and insert at cursor or just append if not focused
            optimizedResume.focus();
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                if (optimizedResume.contains(range.commonAncestorContainer)) {
                    range.deleteContents();
                    range.insertNode(document.createTextNode(text));
                    geminiTalk("Applied! Your resume is getting stronger. 💪");
                    return;
                }
            }
            // Fallback: Append
            optimizedResume.innerText += "\n\n" + text;
            geminiTalk("Added to optimized draft! ✏️");
        };
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

    newAnalysisBtn.addEventListener('click', () => {
        resultsSection.style.display = 'none';
        uploadSection.style.display = 'grid';
        form.reset();
        jdInput.value = '';
        window.scrollTo(0, 0);
    });

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

    window.shortlistCandidate = function () {
        const btn = document.getElementById('shortlistBtn');
        const isShortlisted = btn.classList.contains('active');

        if (isShortlisted) {
            btn.classList.remove('active');
            btn.textContent = "Shortlist Candidate";
            btn.style.borderColor = "";
            geminiTalk("Candidate removed from shortlist. ❌");
        } else {
            btn.classList.add('active');
            btn.textContent = "Shortlisted ⭐";
            btn.style.borderColor = "var(--accent-teal)";
            triggerConfetti();
            geminiTalk("Excellent choice! Candidate added to shortlist. ⭐");
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
    const unlockBtn = document.getElementById('unlockBtn');
    if (unlockBtn) unlockBtn.onclick = window.unlockContactDetails;

    const shortlistBtn = document.getElementById('shortlistBtn');
    if (shortlistBtn) shortlistBtn.onclick = window.shortlistCandidate;

    const addNoteBtn = document.getElementById('addNoteBtn');
    if (addNoteBtn) addNoteBtn.onclick = window.addInternalNote;

    // ==================== UI Effects ====================

    function geminiTalk(message, duration = 3000) {
        const aiCompanion = document.getElementById('aiCompanion');
        const aiStatusText = aiCompanion.querySelector('.status-bubble');
        aiStatusText.textContent = message;
        aiCompanion.classList.add('talking');
        setTimeout(() => aiCompanion.classList.remove('talking'), duration);
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
            el.classList.toggle('active', text.includes(target));
        });
    }

    [...navLinks, ...sidebarItems].forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const text = link.textContent.trim().toLowerCase();
            if (text.includes('dashboard')) navigate('dashboard');
            else if (text.includes('score')) navigate('score');
            else if (text.includes('optimize')) navigate('optimize');
            else if (text.includes('about')) navigate('about');
        });
    });

    if (newAnalysisBtn) {
        newAnalysisBtn.onclick = () => {
            if (resultsSection.style.display !== 'none') {
                navigate('optimize');
            } else {
                location.reload();
            }
        };
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

    // Start Over logic - Add a dedicated "New Analysis" button or handle specifically
    window.startOver = function () {
        if (confirm("Clear results and start a new analysis?")) {
            location.reload();
        }
    };
});
