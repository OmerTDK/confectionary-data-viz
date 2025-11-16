#!/usr/bin/env python3
"""
Script to help capture dashboard screenshots
This script provides guidance and automation for taking dashboard screenshots
"""

import os
import time
import webbrowser
import subprocess
import sys

def check_requirements():
    """Check if required packages are installed"""
    try:
        import streamlit
        import selenium
        print("✅ Streamlit and Selenium available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Install with: pip install selenium")
        return False

def start_dashboard():
    """Start the Streamlit dashboard in background"""
    print("🚀 Starting Streamlit dashboard...")

    # Change to dashboard directory
    dashboard_dir = os.path.join(os.path.dirname(__file__), 'dashboard')
    os.chdir(dashboard_dir)

    # Start streamlit in background
    try:
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
        print("✅ Dashboard started at http://localhost:8501")
        return process
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        return None

def open_browser():
    """Open dashboard in default browser"""
    print("🌐 Opening dashboard in browser...")
    time.sleep(3)  # Wait for streamlit to start
    webbrowser.open('http://localhost:8501')

def take_screenshots_guide():
    """Provide manual screenshot guide"""
    print("\n📸 MANUAL SCREENSHOT GUIDE:")
    print("=" * 50)
    print("1. Dashboard will open in your browser")
    print("2. Take screenshots of these views:")
    print()
    print("   📊 KPI Cards View:")
    print("      - Default view with all filters selected")
    print("      - Save as: images/dashboard_kpi.png")
    print()
    print("   🏆 Regional Analysis:")
    print("      - Scroll to 'Regional Performance' section")
    print("      - Save as: images/dashboard_regional.png")
    print()
    print("   🍫 Product Heatmap:")
    print("      - Scroll to 'Regional Product Performance Matrix'")
    print("      - Save as: images/dashboard_heatmap.png")
    print()
    print("   📈 Time Series:")
    print("      - Scroll to 'Sales Trends Over Time' section")
    print("      - Save as: images/dashboard_timeseries.png")
    print()
    print("3. Use browser's screenshot tool (F12 → Device Toolbar)")
    print("   or external screenshot tools like Snip & Sketch")
    print()
    print("💡 Pro Tips:")
    print("   - Use full browser width for best results")
    print("   - Capture only the chart areas, not the entire page")
    print("   - PNG format with high quality (150+ DPI)")

def automated_screenshots():
    """Attempt automated screenshots using Selenium"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from PIL import Image
        import io

        print("\n🤖 Attempting automated screenshots...")

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:8501")

        # Wait for page to load
        time.sleep(5)

        # Take full page screenshot
        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))

        # Save full screenshot
        image.save("images/dashboard_full.png")
        print("✅ Saved full dashboard screenshot: images/dashboard_full.png")

        driver.quit()
        return True

    except Exception as e:
        print(f"❌ Automated screenshots failed: {e}")
        print("Falling back to manual method...")
        return False

def main():
    """Main function"""
    print("📸 Dashboard Screenshot Capture Tool")
    print("=" * 50)

    # Check if images directory exists
    if not os.path.exists('images'):
        os.makedirs('images')
        print("📁 Created images directory")

    # Check requirements
    if not check_requirements():
        return

    # Start dashboard
    dashboard_process = start_dashboard()
    if not dashboard_process:
        return

    try:
        # Try automated screenshots first
        if automated_screenshots():
            print("✅ Automated screenshots completed!")
        else:
            # Fall back to manual guide
            open_browser()
            take_screenshots_guide()

        print("\n🎉 Screenshot capture process completed!")
        print("Press Ctrl+C to stop the dashboard when done.")

        # Keep dashboard running
        dashboard_process.wait()

    except KeyboardInterrupt:
        print("\n🛑 Stopping dashboard...")
        dashboard_process.terminate()

if __name__ == "__main__":
    main()
