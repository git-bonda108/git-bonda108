#!/bin/bash
# Setup script for Multi-Agent Data Analysis System

echo "🚀 Setting up Multi-Agent Data Analysis System..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << 'EOF'
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here
EOF
    echo "✅ .env file created. Please add your OPENAI_API_KEY!"
else
    echo "✅ .env file exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your OPENAI_API_KEY"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the app: streamlit run data-insights.py"
echo ""



