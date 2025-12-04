#!/usr/bin/env python3
"""
Flask API Server for Repository Analysis
Integrates with main_agent.py to provide web API endpoints
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from main_agent import EnhancedASIOneRepoAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Global analyzer instance
analyzer = None

def initialize_analyzer():
    """Initialize the analyzer instance"""
    global analyzer
    try:
        analyzer = EnhancedASIOneRepoAnalyzer()
        logger.info("✅ Repository analyzer initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to initialize analyzer: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Repository Analysis API",
        "analyzer_ready": analyzer is not None
    })

@app.route('/api/analyze-repo', methods=['POST'])
def analyze_repository():
    """
    Analyze a GitHub repository and return feature suggestions
    Expected payload: {"repoUrl": "https://github.com/owner/repo"}
    """
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        repo_url = data.get('repoUrl') or data.get('repo_url')
        
        if not repo_url:
            return jsonify({
                "success": False,
                "error": "repoUrl or repo_url is required"
            }), 400
        
        # Validate GitHub URL format
        if not repo_url.startswith('https://github.com/'):
            return jsonify({
                "success": False,
                "error": "Invalid GitHub URL format"
            }), 400
        
        logger.info(f"🔍 Analyzing repository: {repo_url}")
        
        # Check if analyzer is initialized
        if not analyzer:
            logger.error("❌ Analyzer not initialized")
            return jsonify({
                "success": False,
                "error": "Analysis service not properly initialized"
            }), 500
        
        # Perform analysis
        result = analyzer.analyze_repository_and_create_issue(repo_url)
        
        if result.get('success'):
            logger.info(f"✅ Analysis completed for {repo_url}")
            
            # Format response for frontend
            response_data = {
                "success": True,
                "repository": result.get('repository'),
                "analysis_method": result.get('analysis_method'),
                "agents_discovered": result.get('agents_discovered', 0),
                "agents_used": result.get('agents_used', 0),
                "selected_agents": result.get('selected_agents', []),
                "synthesized_analysis": result.get('synthesized_analysis', {}),
                "github_payload": result.get('github_payload', {})
            }
            
            return jsonify(response_data)
        else:
            logger.error(f"❌ Analysis failed for {repo_url}: {result.get('error')}")
            return jsonify({
                "success": False,
                "error": result.get('error', 'Analysis failed')
            }), 500
            
    except Exception as e:
        logger.error(f"❌ Unexpected error in analyze_repository: {e}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/create-github-issue', methods=['POST'])
def create_github_issue():
    """
    Create a GitHub issue from analysis results
    Expected payload: {"owner": "owner", "repo": "repo", "issueData": {...}}
    """
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
        
        data = request.get_json()
        owner = data.get('owner')
        repo = data.get('repo')
        issue_data = data.get('issueData')
        
        if not all([owner, repo, issue_data]):
            return jsonify({
                "success": False,
                "error": "owner, repo, and issueData are required"
            }), 400
        
        logger.info(f"📝 Creating GitHub issue for {owner}/{repo}")
        
        if not analyzer:
            return jsonify({
                "success": False,
                "error": "Analysis service not properly initialized"
            }), 500
        
        # Create GitHub issue
        github_response = analyzer.create_github_issue(owner, repo, issue_data)
        
        logger.info(f"✅ GitHub issue created: #{github_response.get('number')}")
        
        return jsonify({
            "success": True,
            "issue": {
                "number": github_response.get('number'),
                "title": github_response.get('title'),
                "url": github_response.get('html_url'),
                "state": github_response.get('state')
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Error creating GitHub issue: {e}")
        return jsonify({
            "success": False,
            "error": f"Failed to create GitHub issue: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

def main():
    """Main function to run the Flask server"""
    print("🚀 Starting Repository Analysis API Server...")
    print("=" * 60)
    
    # Initialize analyzer
    if not initialize_analyzer():
        print("❌ Failed to initialize analyzer. Check your .env configuration.")
        return
    
    print("✅ Analyzer initialized successfully")
    print("🌐 Starting Flask server on http://localhost:5000")
    print("📡 Available endpoints:")
    print("  GET  /health - Health check")
    print("  POST /api/analyze-repo - Analyze repository")
    print("  POST /api/create-github-issue - Create GitHub issue")
    print("=" * 60)
    
    # Run Flask server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )

if __name__ == '__main__':
    main()
