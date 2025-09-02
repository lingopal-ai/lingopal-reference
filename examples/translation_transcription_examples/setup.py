#!/usr/bin/env python3
"""
Setup script for Transcribe and Translate Client
This script helps you set up your environment configuration
"""

import os
import sys

def create_env_file():
    """Create a .env file from the template"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    # Read the example file
    example_file = 'env_example.txt'
    if not os.path.exists(example_file):
        print(f"❌ {example_file} not found!")
        return False
    
    with open(example_file, 'r') as f:
        content = f.read()
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ Created .env file from template")
    print("📝 Please edit .env file with your actual values:")
    print("   - API_BASE_URL: Your deployed API URL")
    print("   - API_KEY: Your API key (if required)")
    print("   - AUDIO_FILE: Path to your audio file")
    print("   - TRANSLATION_LANGUAGES: Target languages (comma-separated)")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_client.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("🔧 Transcribe and Translate Client Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('transcribe_and_translate.py'):
        print("❌ Please run this script from the translation_transcription_examples directory")
        print("   cd translation_transcription_examples && python setup.py")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    print()
    
    # Create .env file
    if create_env_file():
        print()
        print("🎉 Setup completed!")
        print()
        print("Next steps:")
        print("1. Edit the .env file with your configuration")
        print("2. Run: python transcribe_and_translate.py")
        print()
        print("For examples, see: example_usage.py")
        print("For documentation, see: README_client.md")
    else:
        print("❌ Setup failed!")

if __name__ == "__main__":
    main()
