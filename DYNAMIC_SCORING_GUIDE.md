# Dynamic Scoring System - Documentation

## 🎯 Overview

The ATS scoring system now uses **DYNAMIC WEIGHTING** based on what's actually required in the Job Description. This ensures fair, accurate scoring that reflects real requirements.

---

## ❌ **OLD SYSTEM (Fixed Weights)**

### Problems:
1. **Inflated Scores**: Candidates got points for things not required
2. **Unfair Advantage**: Someone with certifications scored higher even if JD didn't ask for them
3. **Hidden Criteria**: All 7 criteria always scored, even if irrelevant
4. **100/100 Possible**: Could get perfect score without meeting actual requirements

### Example:
```
JD: "Looking for Python developer with 3 years experience"
(No mention of certifications or specific education)

OLD SCORING:
- Domain: 30%
- Skills: 25%
- Keywords: 20%
- Experience: 10%
- Certifications: 5%  ← NOT REQUIRED but still scored!
- Education: 5%       ← NOT REQUIRED but still scored!
- Formatting: 5%

Result: Candidate with AWS cert gets 5% bonus even though JD didn't ask for it!
```

---

## ✅ **NEW SYSTEM (Dynamic Weights)**

### Features:
1. **Requirement Detection**: Analyzes JD to find what's actually required
2. **Dynamic Weighting**: Only scores criteria mentioned in JD
3. **Fair Redistribution**: Unused weight goes to relevant criteria
4. **Transparent Breakdown**: Shows only scored criteria

### How It Works:

#### **Step 1: Detect Requirements**
```python
has_cert_requirements = bool(jd_data.get('certifications_required'))
has_edu_requirements = jd_data.get('education_required') != 'Not specified'
has_skills_requirements = bool(jd_data.get('mandatory_skills'))
has_experience_requirements = bool(jd_data.get('experience_required'))
```

#### **Step 2: Assign Base Weights**
Always scored (65% total):
- **Domain Similarity**: 30% - Role fit
- **Keyword Match**: 25% - Content relevance
- **Formatting**: 10% - ATS compatibility

#### **Step 3: Distribute Optional Weight (35%)**
Split equally among required optional criteria:
- Skills (if JD mentions skills)
- Experience (if JD mentions years/experience)
- Education (if JD specifies degree)
- Certifications (if JD lists certs)

#### **Step 4: Calculate Score**
```python
total_score = (
    domain_score * weights['domain'] +
    keyword_score * weights['keyword'] +
    formatting_score * weights['formatting'] +
    (skills_score * weights.get('skills', 0)) +
    (experience_score * weights.get('experience', 0)) +
    (edu_score * weights.get('education', 0)) +
    (cert_score * weights.get('certifications', 0))
)
```

---

## 📊 **Scoring Examples**

### **Example 1: Minimal JD (No Optional Requirements)**
```
JD: "Looking for software developer to build web apps"
(No skills, experience, education, or certs mentioned)

DETECTED REQUIREMENTS:
- Domain: ✅ (always)
- Keywords: ✅ (always)
- Formatting: ✅ (always)
- Skills: ❌
- Experience: ❌
- Education: ❌
- Certifications: ❌

DYNAMIC WEIGHTS:
- Domain: 45% (30% + 15% redistribution)
- Keywords: 40% (25% + 15% redistribution)
- Formatting: 15% (10% + 5% redistribution)

BREAKDOWN SHOWN:
{
  "domain_similarity": {"score": 85, "weight": "45%", "required": true},
  "keyword_match": {"score": 70, "weight": "40%", "required": true},
  "formatting": {"score": 90, "weight": "15%", "required": true}
}

TOTAL: (85 * 0.45) + (70 * 0.40) + (90 * 0.15) = 79.25
```

---

### **Example 2: Skills + Experience Required**
```
JD: "5+ years Python developer with Django, AWS, Docker"

DETECTED REQUIREMENTS:
- Domain: ✅
- Keywords: ✅
- Formatting: ✅
- Skills: ✅ (Python, Django, AWS, Docker)
- Experience: ✅ (5+ years)
- Education: ❌
- Certifications: ❌

DYNAMIC WEIGHTS:
35% split between Skills and Experience = 17.5% each
- Domain: 30%
- Keywords: 25%
- Skills: 17.5%
- Experience: 17.5%
- Formatting: 10%

BREAKDOWN SHOWN:
{
  "domain_similarity": {"score": 90, "weight": "30%", "required": true},
  "keyword_match": {"score": 85, "weight": "25%", "required": true},
  "skills_match": {"score": 80, "weight": "17%", "required": true},
  "experience_alignment": {"score": 75, "weight": "17%", "required": true},
  "formatting": {"score": 95, "weight": "10%", "required": true}
}

TOTAL: (90*0.30) + (85*0.25) + (80*0.175) + (75*0.175) + (95*0.10) = 85.625
```

---

### **Example 3: All Requirements**
```
JD: "Senior Data Scientist with MS in CS, 7+ years ML experience, 
     AWS Certified, Python/TensorFlow/PyTorch skills"

DETECTED REQUIREMENTS:
- Domain: ✅
- Keywords: ✅
- Formatting: ✅
- Skills: ✅ (Python, TensorFlow, PyTorch)
- Experience: ✅ (7+ years)
- Education: ✅ (MS in CS)
- Certifications: ✅ (AWS Certified)

DYNAMIC WEIGHTS:
35% split among 4 optional criteria = 8.75% each
- Domain: 30%
- Keywords: 25%
- Skills: 8.75%
- Experience: 8.75%
- Education: 8.75%
- Certifications: 8.75%
- Formatting: 10%

BREAKDOWN SHOWN:
{
  "domain_similarity": {"score": 95, "weight": "30%", "required": true},
  "keyword_match": {"score": 90, "weight": "25%", "required": true},
  "skills_match": {"score": 85, "weight": "8%", "required": true},
  "experience_alignment": {"score": 90, "weight": "8%", "required": true},
  "education": {"score": 100, "weight": "8%", "required": true},
  "certifications": {"score": 100, "weight": "8%", "required": true},
  "formatting": {"score": 95, "weight": "10%", "required": true}
}

TOTAL: (95*0.30) + (90*0.25) + (85*0.0875) + (90*0.0875) + 
       (100*0.0875) + (100*0.0875) + (95*0.10) = 92.5625
```

---

## 🔍 **How Requirements Are Detected**

### **Certifications**
```python
# Looks for:
- "AWS Certified"
- "PMP certification"
- "Certified Scrum Master"
- Any cert from universal_skills.json

if jd_data.get('certifications_required'):
    has_cert_requirements = True
```

### **Education**
```python
# Looks for:
- "Bachelor's degree"
- "MS in Computer Science"
- "PhD required"
- "Engineering degree"

if jd_data.get('education_required') != 'Not specified':
    has_edu_requirements = True
```

### **Skills**
```python
# Looks for:
- Technical skills (Python, Java, React)
- Tools (Git, Docker, Kubernetes)
- Frameworks (Django, Spring, Angular)

if jd_data.get('mandatory_skills') or jd_data.get('preferred_skills'):
    has_skills_requirements = True
```

### **Experience**
```python
# Looks for:
- "5+ years"
- "3-5 years experience"
- "Senior level"
- "Mid-level developer"

if jd_data.get('experience_required'):
    has_experience_requirements = True
```

---

## 📈 **Benefits**

### **1. Fair Scoring**
- Only scored on what's actually required
- No bonus points for irrelevant qualifications
- Reflects true job fit

### **2. Transparent**
- Breakdown shows only scored criteria
- Each criterion marked as "required: true"
- Clear weight percentages

### **3. Accurate Rankings**
- Candidates ranked by actual requirements
- No inflation from unrelated qualifications
- Better hiring decisions

### **4. Flexible**
- Adapts to any JD
- Works for entry-level to executive roles
- Handles minimal to comprehensive JDs

---

## 🎯 **Use Cases**

### **Use Case 1: Entry-Level Position**
```
JD: "Junior developer needed. Will train."

SCORING:
- Domain: 45%
- Keywords: 40%
- Formatting: 15%

WHY: No specific requirements, so focus on role fit and content
```

### **Use Case 2: Specialized Role**
```
JD: "ML Engineer with PhD, 10+ years, TensorFlow certified"

SCORING:
- Domain: 30%
- Keywords: 25%
- Skills: 8.75%
- Experience: 8.75%
- Education: 8.75%
- Certifications: 8.75%
- Formatting: 10%

WHY: All requirements specified, so all criteria scored
```

### **Use Case 3: Skills-Focused Role**
```
JD: "Full-stack developer: React, Node.js, PostgreSQL, AWS"

SCORING:
- Domain: 30%
- Keywords: 25%
- Skills: 35%
- Formatting: 10%

WHY: Heavy emphasis on specific technical skills
```

---

## 🔧 **Technical Implementation**

### **Weight Distribution Algorithm**
```python
# Base weights (always present)
weights = {
    'domain': 0.30,
    'keyword': 0.25,
    'formatting': 0.10
}

# Remaining 35% for optional criteria
remaining_weight = 0.35
optional_criteria = []

if has_skills_requirements:
    optional_criteria.append('skills')
if has_experience_requirements:
    optional_criteria.append('experience')
if has_edu_requirements:
    optional_criteria.append('education')
if has_cert_requirements:
    optional_criteria.append('certifications')

# Distribute equally
if optional_criteria:
    weight_per_criterion = remaining_weight / len(optional_criteria)
    for criterion in optional_criteria:
        weights[criterion] = weight_per_criterion
else:
    # Redistribute to base criteria
    weights['domain'] += 0.15
    weights['keyword'] += 0.15
    weights['formatting'] += 0.05
```

---

## ✅ **Validation**

### **Test Scenario 1: No Certs in JD**
```
INPUT:
JD: "Python developer needed"
Resume: Has AWS certification

EXPECTED:
- Certification score: 0 (not calculated)
- Certification not in breakdown
- Weight redistributed to other criteria

RESULT: ✅ Pass
```

### **Test Scenario 2: All Requirements**
```
INPUT:
JD: "Senior role, MS required, AWS cert, 5+ years Python"
Resume: Meets all requirements

EXPECTED:
- All 7 criteria scored
- Weights sum to 100%
- High total score (85+)

RESULT: ✅ Pass
```

---

## 📝 **Migration Notes**

### **Breaking Changes**
- Breakdown structure changed
- Added `required` flag to each criterion
- Added `scoring_note` field
- Weights are now dynamic strings (e.g., "30%" vs "25%")

### **Backward Compatibility**
- Total score calculation unchanged
- Visibility logic unchanged
- API response structure mostly compatible

---

## 🚀 **Future Enhancements**

1. **Custom Weights**: Allow recruiters to set custom importance
2. **Industry Profiles**: Pre-defined weight profiles by industry
3. **ML-Based Detection**: Better requirement extraction from JD
4. **Scoring Explanations**: Natural language explanation of score
5. **Comparative Analysis**: Show how candidate compares to others

---

**Last Updated**: February 10, 2026  
**Version**: 2.0 (Dynamic Scoring)
