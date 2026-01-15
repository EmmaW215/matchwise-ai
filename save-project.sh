#!/bin/bash

# MatchWise AI Project Backup Script
# This script creates a complete backup of the project

echo "🚀 Starting MatchWise AI Project Backup..."

# Set backup directory
BACKUP_DIR="MatchWise_AI_Backup_$(date +%Y%m%d_%H%M%S)"
echo "📁 Creating backup directory: $BACKUP_DIR"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Copy frontend
echo "📱 Backing up frontend..."
cp -r resume-matcher-frontend "$BACKUP_DIR/"

# Copy backend
echo "🔧 Backing up backend..."
cp -r resume-matcher-backend "$BACKUP_DIR/"

# Copy root files
echo "📄 Backing up root files..."
cp README.md "$BACKUP_DIR/"
cp package*.json "$BACKUP_DIR/" 2>/dev/null || true

# Create deployment info
echo "📋 Creating deployment information..."
cat > "$BACKUP_DIR/DEPLOYMENT_INFO.md" << EOF
# MatchWise AI Deployment Information

## Backup Created: $(date)

## Live URLs
- Frontend: https://matchwise-ai.vercel.app/
- Backend: https://resume-matcher-backend-rrrw.onrender.com/

## Environment Variables Required

### Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://resume-matcher-backend-rrrw.onrender.com

### Backend (Render)
OPENAI_API_KEY=your_openai_api_key
XAI_API_KEY=your_xai_api_key
ALLOWED_ORIGINS=https://matchwise-ai.vercel.app

## Quick Start Commands

### Frontend
\`\`\`bash
cd resume-matcher-frontend
npm install
npm run dev
\`\`\`

### Backend
\`\`\`bash
cd resume-matcher-backend
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Features Included
- ✅ AI Resume Analysis
- ✅ Job Posting Scraping
- ✅ Matching Score Calculation
- ✅ Cover Letter Generation
- ✅ Visitor Counter
- ✅ Admin Dashboard
- ✅ Triple-layer AI System (OpenAI + xAI + Local Mock)
- ✅ PDF/DOCX Support
- ✅ Responsive Design
- ✅ Error Handling

## Version Information
- Next.js: 15.3.4
- FastAPI: Latest
- Python: 3.9+
- Node.js: 18+
EOF

# Create restore script
echo "🔧 Creating restore script..."
cat > "$BACKUP_DIR/restore.sh" << 'EOF'
#!/bin/bash

echo "🔄 Restoring MatchWise AI Project..."

# Check if we're in the backup directory
if [ ! -f "DEPLOYMENT_INFO.md" ]; then
    echo "❌ Error: Please run this script from the backup directory"
    exit 1
fi

# Create project directory
PROJECT_DIR="../h_MatchWise_AI_Restored"
echo "📁 Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"

# Copy all files
echo "📋 Copying project files..."
cp -r resume-matcher-frontend "$PROJECT_DIR/"
cp -r resume-matcher-backend "$PROJECT_DIR/"
cp DEPLOYMENT_INFO.md "$PROJECT_DIR/"
cp restore.sh "$PROJECT_DIR/"

echo "✅ Project restored to: $PROJECT_DIR"
echo "📖 See DEPLOYMENT_INFO.md for setup instructions"
EOF

chmod +x "$BACKUP_DIR/restore.sh"

# Create archive
echo "📦 Creating compressed archive..."
tar -czf "${BACKUP_DIR}.tar.gz" "$BACKUP_DIR"

# Clean up temporary directory
rm -rf "$BACKUP_DIR"

echo "✅ Backup completed successfully!"
echo "📦 Archive created: ${BACKUP_DIR}.tar.gz"
echo "📁 Size: $(du -h "${BACKUP_DIR}.tar.gz" | cut -f1)"
echo ""
echo "🎉 Your MatchWise AI project has been saved!"
echo "📖 To restore: tar -xzf ${BACKUP_DIR}.tar.gz && cd ${BACKUP_DIR} && ./restore.sh" 