"""
Shortlist Management System

Stores and manages shortlisted candidates
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class ShortlistManager:
    """Manages candidate shortlisting with persistent storage"""
    
    def __init__(self, storage_file='data/shortlisted_candidates.json'):
        """Initialize shortlist manager"""
        self.storage_file = storage_file
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)
    
    def add_candidate(self, candidate_data: Dict) -> Dict:
        """
        Add a candidate to the shortlist
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            Updated candidate data with shortlist info
        """
        shortlist = self._load_shortlist()
        
        # Create shortlist entry
        entry = {
            'id': f"SL-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'shortlisted_at': datetime.now().isoformat(),
            'candidate_name': candidate_data.get('candidate_name', 'Unknown'),
            'email': candidate_data.get('email', ''),
            'phone': candidate_data.get('phone', ''),
            'total_score': candidate_data.get('total_score', 0),
            'verdict': candidate_data.get('verdict', ''),
            'matched_skills': candidate_data.get('matched_skills', []),
            'missing_skills': candidate_data.get('missing_skills', []),
            'education_match': candidate_data.get('education_match', False),
            'matched_certifications': candidate_data.get('matched_certifications', []),
            'job_title': candidate_data.get('job_title', 'Not specified'),
            'notes': candidate_data.get('notes', ''),
            'status': 'shortlisted'
        }
        
        # Check if already shortlisted
        existing = next((c for c in shortlist if c['email'] == entry['email']), None)
        if existing:
            return {'success': False, 'message': 'Candidate already shortlisted', 'entry': existing}
        
        shortlist.append(entry)
        self._save_shortlist(shortlist)
        
        return {'success': True, 'message': 'Candidate shortlisted successfully', 'entry': entry}
    
    def remove_candidate(self, candidate_email: str) -> Dict:
        """
        Remove a candidate from the shortlist
        
        Args:
            candidate_email: Email of the candidate to remove
            
        Returns:
            Success status
        """
        shortlist = self._load_shortlist()
        original_length = len(shortlist)
        
        shortlist = [c for c in shortlist if c['email'] != candidate_email]
        
        if len(shortlist) == original_length:
            return {'success': False, 'message': 'Candidate not found in shortlist'}
        
        self._save_shortlist(shortlist)
        return {'success': True, 'message': 'Candidate removed from shortlist'}
    
    def get_all_shortlisted(self) -> List[Dict]:
        """Get all shortlisted candidates"""
        return self._load_shortlist()
    
    def get_by_email(self, email: str) -> Dict:
        """Get a specific candidate by email"""
        shortlist = self._load_shortlist()
        candidate = next((c for c in shortlist if c['email'] == email), None)
        return candidate if candidate else {}
    
    def update_status(self, candidate_email: str, new_status: str) -> Dict:
        """
        Update candidate status
        
        Args:
            candidate_email: Email of the candidate
            new_status: New status (e.g., 'interviewed', 'offered', 'hired', 'rejected')
            
        Returns:
            Success status
        """
        shortlist = self._load_shortlist()
        
        for candidate in shortlist:
            if candidate['email'] == candidate_email:
                candidate['status'] = new_status
                candidate['status_updated_at'] = datetime.now().isoformat()
                self._save_shortlist(shortlist)
                return {'success': True, 'message': f'Status updated to {new_status}'}
        
        return {'success': False, 'message': 'Candidate not found'}
    
    def add_note(self, candidate_email: str, note: str) -> Dict:
        """
        Add a note to a candidate
        
        Args:
            candidate_email: Email of the candidate
            note: Note to add
            
        Returns:
            Success status
        """
        shortlist = self._load_shortlist()
        
        for candidate in shortlist:
            if candidate['email'] == candidate_email:
                if 'notes' not in candidate:
                    candidate['notes'] = []
                
                candidate['notes'].append({
                    'text': note,
                    'added_at': datetime.now().isoformat()
                })
                
                self._save_shortlist(shortlist)
                return {'success': True, 'message': 'Note added successfully'}
        
        return {'success': False, 'message': 'Candidate not found'}
    
    def get_statistics(self) -> Dict:
        """Get shortlist statistics"""
        shortlist = self._load_shortlist()
        
        status_counts = {}
        for candidate in shortlist:
            status = candidate.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            'total_shortlisted': len(shortlist),
            'status_breakdown': status_counts,
            'average_score': sum(c.get('total_score', 0) for c in shortlist) / len(shortlist) if shortlist else 0
        }
    
    def _load_shortlist(self) -> List[Dict]:
        """Load shortlist from file"""
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_shortlist(self, shortlist: List[Dict]):
        """Save shortlist to file"""
        with open(self.storage_file, 'w') as f:
            json.dump(shortlist, f, indent=2)
