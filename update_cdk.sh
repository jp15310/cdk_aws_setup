#!/bin/bash

set -e

echo "🔄 Updating AWS CDK CLI globally..."
npm install -g aws-cdk

echo "✅ CDK CLI updated to version: $(cdk --version)"

echo "Opting out of AWS Telemetry Collection"
cdk cli-telemetry --disable

# Optional: recreate virtualenv
if [ -d ".venv" ]; then
    echo "⚠️ Deleting existing Python virtual environment (.venv)..."
    rm -rf .venv
fi

echo "🐍 Creating new Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "📥 Installing latest CDK Python libraries..."
pip install --upgrade aws-cdk-lib constructs

echo "✅ Python CDK packages installed:"
pip list | grep -E 'aws-cdk-lib|constructs'

echo "🚀 Done! Your CDK environment is fully updated."
