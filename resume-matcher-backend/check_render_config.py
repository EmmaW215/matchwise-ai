#!/usr/bin/env python3
"""
Render Configuration Checker
This script helps verify that all required environment variables are set.
Run this locally or check the output in Render logs.
"""

import os
import sys

def check_env_var(name, required=True, prefix=None):
    """Check if an environment variable is set"""
    value = os.getenv(name)
    if not value:
        if required:
            print(f"❌ {name}: NOT SET (REQUIRED)")
            return False
        else:
            print(f"⚠️  {name}: NOT SET (Optional)")
            return True
    else:
        # Mask sensitive values
        if prefix and value.startswith(prefix):
            masked = prefix + "..." + value[-4:]
        else:
            masked = "***" + value[-4:] if len(value) > 4 else "***"
        
        if required:
            print(f"✅ {name}: SET ({masked})")
        else:
            print(f"✅ {name}: SET ({masked}) - Optional")
        return True

def check_file_exists(filepath):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {filepath}: EXISTS")
        return True
    else:
        print(f"❌ {filepath}: NOT FOUND")
        return False

def main():
    print("=" * 60)
    print("Render Configuration Checker")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Required environment variables
    print("📋 Required Environment Variables:")
    print("-" * 60)
    all_ok &= check_env_var("XAI_API_KEY", required=True, prefix="xai-")
    all_ok &= check_env_var("OPENAI_API_KEY", required=True, prefix="sk-")
    all_ok &= check_env_var("STRIPE_SECRET_KEY", required=True, prefix="sk_")
    all_ok &= check_env_var("STRIPE_WEBHOOK_SECRET", required=True, prefix="whsec_")
    print()
    
    # Optional environment variables
    print("📋 Optional Environment Variables:")
    print("-" * 60)
    check_env_var("ALLOWED_ORIGINS", required=False)
    print()
    
    # File checks
    print("📁 Required Files:")
    print("-" * 60)
    file_ok = check_file_exists("serviceAccountKey.json")
    if not file_ok:
        print("   ⚠️  Note: serviceAccountKey.json may be configured via environment variables")
    all_ok &= file_ok
    print()
    
    # Summary
    print("=" * 60)
    if all_ok:
        print("✅ All required configurations are set!")
        return 0
    else:
        print("❌ Some required configurations are missing!")
        print("   Please check the RENDER_CONFIGURATION_CHECKLIST.md for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())