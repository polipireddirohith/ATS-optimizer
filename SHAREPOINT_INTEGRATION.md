# SharePoint Integration Guide for ATS Optimizer

This guide details how to integrate the **ATS Resume Optimizer** into your **Microsoft SharePoint** environment. The application is designed to be embedded or linked, accepting user identity automatically to streamline the HR workflow.

---

## 🚀 Integration Options

### Option 1: The "Embed" Web Part (Iframe)
The simplest way to display the ATS directly within a SharePoint page.

**Prerequisites:**
1. Host the ATS application on a server (e.g., `http://ats-internal-server`).
2. Ensure the server enables `X-Frame-Options: ALLOW-FROM https://yourcompany.sharepoint.com` (or remove the header).

**Steps:**
1. Edit your SharePoint Page.
2. Add an **Embed** web part.
3. Use the following iframe code:
   ```html
   <iframe 
     src="http://ats-internal-server/?user=HR_User" 
     width="100%" 
     height="900px" 
     style="border:none;">
   </iframe>
   ```
   *Note: To pass the dynamic current user, you may need a custom SPFx component or use the simple Link approach below.*

### Option 2: Azure AD App Proxy (Recommended for SSO)
If you publish this app via **Azure AD Application Proxy**, SharePoint users can access it securely without logging in again.

**Backend Configuration:**
The ATS automatically looks for these headers (standard in Azure AD Proxy):
- `X-User-Name` or `X-Remote-User` (The user's name/email)
- `X-User-Role` (The user's group/role)

**How it works:**
1. User clicks "Launch ATS" in SharePoint.
2. Azure AD authenticates them.
3. Azure passes `X-User-Name: Jane Doe` to the ATS Python backend.
4. **ATS Behavior:** The interface shows "ATS User Detected: Jane Doe" and **skips the 'Enter Recruiter Name' prompt** entirely.

### Option 3: Quick Link with Parameters
Create a tile or link in SharePoint that passes user context (if internal security allows).

**URL Pattern:**
`http://ats-server/?user=JaneDoe&role=HR_Manager`

---

## 🔧 Technical Details for IT

### API Endpoints
The application exposes the following endpoints which can be called by SharePoint workflows (via Power Automate) if needed:

- **POST** `/api/analyze`: Submit a resume + JD for scoring.
- **POST** `/api/source/generate`: Find candidates (X-Ray Search).
- **GET** `/api/shortlist/all`: Retrieve the JSON list of shortlisted candidates.

### Security
- **API Keys:** If using the *Sourcing* feature, configure the Google API key in the UI or set it as an environment variable on the server.
- **Data Storage:** All shortlist data is stored in `data/shortlisted_candidates.json` on the server. Ensure this directory is backed up.

---

## 🎨 Branding
The application uses a neutral, modern enterprise theme (`Inter` font, clean layout) that blends well with SharePoint's default styling.
