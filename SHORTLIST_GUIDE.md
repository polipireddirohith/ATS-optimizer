# Shortlist Management System - Documentation

## 📋 Overview

The **Shortlist Management System** allows HR recruiters to save, track, and manage their top candidates throughout the hiring process. All shortlisted candidates are stored persistently and can be accessed anytime.

---

## 🎯 Key Features

### 1. **Persistent Storage**
- Candidates saved to `data/shortlisted_candidates.json`
- Data persists across sessions
- No database setup required

### 2. **Candidate Tracking**
- Store complete candidate information
- Track ATS scores and verdicts
- Monitor skills match and gaps
- Record education and certifications

### 3. **Status Management**
- **Shortlisted**: Initial status
- **Interviewed**: Candidate has been interviewed
- **Offered**: Job offer extended
- **Hired**: Candidate accepted offer
- **Rejected**: Candidate not moving forward

### 4. **Notes System**
- Add internal notes to candidates
- Track interview feedback
- Record hiring manager comments

---

## 🚀 How to Use

### **Adding Candidates to Shortlist**

#### From Single Analysis:
1. Analyze a resume against a job description
2. Review the results in HR mode
3. Click "Shortlist Candidate" button
4. Candidate is saved with all details

#### From Bulk Analysis:
1. Upload multiple resumes
2. Review ranked results
3. Click shortlist button on candidate cards
4. Selected candidates are saved

---

### **Viewing Shortlisted Candidates**

**Access:** Navigate to `http://localhost:5000/shortlist`

**What You See:**
```
┌─────────────────────────────────────────────────────────┐
│ ⭐ Shortlisted Candidates                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Statistics:                                             │
│ ┌──────────┬──────────┬──────────┐                     │
│ │ Total: 5 │ Avg: 85  │ Active:3 │                     │
│ └──────────┴──────────┴──────────┘                     │
│                                                         │
│ Candidate Table:                                        │
│ ┌──────────────────────────────────────────────────┐   │
│ │ Name    │ Email  │ Score │ Status    │ Actions  │   │
│ ├──────────────────────────────────────────────────┤   │
│ │ John    │ j@...  │ 92    │ OFFERED   │ [Update] │   │
│ │ Jane    │ ja...  │ 85    │ INTERVIEW │ [Update] │   │
│ │ Bob     │ b@...  │ 78    │ SHORTLIST │ [Update] │   │
│ └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

### **Managing Candidate Status**

1. Go to shortlist page (`/shortlist`)
2. Find the candidate in the table
3. Use the "Update Status" dropdown
4. Select new status:
   - Interviewed
   - Offered
   - Hired
   - Rejected
5. Status updates automatically

---

### **Removing Candidates**

1. Go to shortlist page
2. Click "Remove" button next to candidate
3. Confirm removal
4. Candidate is removed from shortlist

---

## 🔌 API Endpoints

### **Add to Shortlist**
```
POST /api/shortlist/add
Content-Type: application/json

{
  "candidate_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "total_score": 92,
  "verdict": "Perfect Match ✅",
  "matched_skills": ["Python", "React", "AWS"],
  "missing_skills": ["Kubernetes"],
  "education_match": true,
  "matched_certifications": ["AWS Solutions Architect"],
  "job_title": "Senior Developer"
}

Response:
{
  "success": true,
  "message": "Candidate shortlisted successfully",
  "entry": {
    "id": "SL-20260210001234",
    "shortlisted_at": "2026-02-10T00:12:34",
    ...
  }
}
```

### **Remove from Shortlist**
```
POST /api/shortlist/remove
Content-Type: application/json

{
  "email": "john@example.com"
}

Response:
{
  "success": true,
  "message": "Candidate removed from shortlist"
}
```

### **Get All Shortlisted**
```
GET /api/shortlist/all

Response:
{
  "success": true,
  "candidates": [...],
  "total": 5
}
```

### **Check Shortlist Status**
```
GET /api/shortlist/check/john@example.com

Response:
{
  "success": true,
  "is_shortlisted": true,
  "candidate": {...}
}
```

### **Update Status**
```
POST /api/shortlist/update-status
Content-Type: application/json

{
  "email": "john@example.com",
  "status": "interviewed"
}

Response:
{
  "success": true,
  "message": "Status updated to interviewed"
}
```

### **Add Note**
```
POST /api/shortlist/add-note
Content-Type: application/json

{
  "email": "john@example.com",
  "note": "Great technical skills, good culture fit"
}

Response:
{
  "success": true,
  "message": "Note added successfully"
}
```

### **Get Statistics**
```
GET /api/shortlist/statistics

Response:
{
  "success": true,
  "statistics": {
    "total_shortlisted": 5,
    "status_breakdown": {
      "shortlisted": 2,
      "interviewed": 2,
      "offered": 1
    },
    "average_score": 85.4
  }
}
```

---

## 📊 Data Structure

### Shortlisted Candidate Entry
```json
{
  "id": "SL-20260210001234",
  "shortlisted_at": "2026-02-10T00:12:34.567890",
  "candidate_name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "total_score": 92,
  "verdict": "Perfect Match ✅",
  "matched_skills": ["Python", "React", "AWS", "Docker"],
  "missing_skills": ["Kubernetes"],
  "education_match": true,
  "matched_certifications": ["AWS Solutions Architect"],
  "job_title": "Senior Developer",
  "notes": [
    {
      "text": "Great interview, strong technical skills",
      "added_at": "2026-02-10T10:30:00"
    }
  ],
  "status": "interviewed",
  "status_updated_at": "2026-02-10T10:00:00"
}
```

---

## 💡 Use Cases

### Use Case 1: Tracking Interview Pipeline
**Scenario:** HR manager wants to track 10 candidates through interview process

**Process:**
1. Shortlist 10 candidates from bulk analysis
2. Update status to "interviewed" after each interview
3. Add notes with interview feedback
4. Update to "offered" for top 3
5. Update to "hired" when candidate accepts

**Result:** Complete audit trail of hiring process

---

### Use Case 2: Multi-Position Hiring
**Scenario:** Company hiring for 3 different positions

**Process:**
1. Analyze resumes for Position A, shortlist top 5
2. Analyze resumes for Position B, shortlist top 5
3. Analyze resumes for Position C, shortlist top 5
4. View all 15 candidates in shortlist page
5. Filter by job_title or status

**Result:** Centralized candidate management

---

### Use Case 3: Collaborative Hiring
**Scenario:** Multiple recruiters working on same position

**Process:**
1. Recruiter A shortlists candidates
2. Recruiter B reviews shortlist
3. Recruiter B adds notes to each candidate
4. Hiring manager reviews shortlist with notes
5. Team decides on final candidates

**Result:** Shared candidate pool with feedback

---

## 📁 File Storage

### Location
```
data/shortlisted_candidates.json
```

### Backup
Recommended to backup this file regularly:
```bash
# Windows
copy data\shortlisted_candidates.json data\shortlisted_candidates_backup.json

# Linux/Mac
cp data/shortlisted_candidates.json data/shortlisted_candidates_backup.json
```

### Migration
To move shortlist to another system:
1. Copy `data/shortlisted_candidates.json`
2. Place in `data/` folder of new installation
3. Shortlist will load automatically

---

## 🔒 Security & Privacy

### Data Protection
- Stored locally on your server
- No external API calls
- No cloud storage
- Full data control

### Access Control
- Only accessible through your application
- Requires server access
- Can add authentication layer (future enhancement)

---

## 🚀 Future Enhancements

### Planned Features
1. **Export to Excel**: Download shortlist as spreadsheet
2. **Email Integration**: Send candidate info to hiring managers
3. **Calendar Integration**: Schedule interviews directly
4. **Advanced Filtering**: Filter by score range, skills, status
5. **Bulk Actions**: Update multiple candidates at once
6. **Candidate Comparison**: Side-by-side comparison view
7. **Interview Scheduling**: Built-in interview scheduler
8. **Offer Letter Generation**: Auto-generate offer letters

---

## ✅ Best Practices

### For Recruiters
1. **Shortlist Immediately**: Add candidates right after analysis
2. **Update Status Promptly**: Keep status current
3. **Add Detailed Notes**: Record interview insights
4. **Regular Review**: Check shortlist weekly
5. **Clean Up**: Remove rejected candidates periodically

### For System Admins
1. **Backup Regularly**: Daily backups recommended
2. **Monitor File Size**: Large shortlists may slow down
3. **Archive Old Data**: Move hired/rejected to archive
4. **Set Permissions**: Restrict file access appropriately

---

## 🐛 Troubleshooting

### Issue: Candidate not appearing in shortlist
**Solution:** Check browser console for errors, verify API response

### Issue: Status not updating
**Solution:** Ensure email is correct, check server logs

### Issue: Duplicate candidates
**Solution:** System prevents duplicates by email, check email format

### Issue: Shortlist file missing
**Solution:** File auto-creates on first shortlist, check folder permissions

---

## 📈 Analytics

### Track These Metrics
- **Shortlist Rate**: % of analyzed candidates shortlisted
- **Conversion Rate**: % of shortlisted candidates hired
- **Time to Hire**: Days from shortlist to hire
- **Average Score**: Quality of shortlisted candidates

---

## ✨ Conclusion

The Shortlist Management System provides:

1. **Persistent Candidate Tracking**: Never lose top candidates
2. **Status Management**: Track hiring pipeline
3. **Collaborative Features**: Share feedback with team
4. **Simple Integration**: Works seamlessly with ATS

**Your shortlisted candidates are now saved and managed professionally!**

---

*Last Updated: February 10, 2026*
