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

    # Already in dashboard directory, no need to change

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
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from PIL import Image
        import io

        print("\n🤖 Attempting automated screenshots...")

        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:8501")

        # Wait for page to load
        print("⏳ Waiting for dashboard to load...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        time.sleep(3)  # Additional wait for dynamic content

        images_dir = os.path.join(os.path.dirname(__file__), '..', 'images')

        # Screenshot 1: KPI Cards (top section)
        try:
            # Get the main content area
            main_content = driver.find_element(By.CLASS_NAME, "main")
            screenshot = main_content.screenshot_as_png
            image = Image.open(io.BytesIO(screenshot))

            # Crop to show KPI cards (top portion)
            width, height = image.size
            kpi_region = image.crop((0, 0, width, min(height, 400)))
            kpi_path = os.path.join(images_dir, 'dashboard_kpi.png')
            kpi_region.save(kpi_path)
            print(f"✅ Saved KPI cards screenshot: dashboard_kpi.png")
        except Exception as e:
            print(f"⚠️  Could not capture KPI cards: {e}")

        # Screenshot 2: Regional Analysis
        try:
            # Scroll to regional analysis section
            driver.execute_script("arguments[0].scrollIntoView();",
                driver.find_element(By.XPATH, "//*[contains(text(), 'Regional Performance')]"))

            time.sleep(2)
            main_content = driver.find_element(By.CLASS_NAME, "main")
            screenshot = main_content.screenshot_as_png
            image = Image.open(io.BytesIO(screenshot))

            # Save regional analysis view
            regional_path = os.path.join(images_dir, 'dashboard_regional.png')
            image.save(regional_path)
            print(f"✅ Saved regional analysis screenshot: dashboard_regional.png")
        except Exception as e:
            print(f"⚠️  Could not capture regional analysis: {e}")

        # Screenshot 3: Performance Matrix (Heatmap)
        try:
            # Scroll to heatmap section
            driver.execute_script("arguments[0].scrollIntoView();",
                driver.find_element(By.XPATH, "//*[contains(text(), 'Performance Matrix')]"))

            time.sleep(2)
            main_content = driver.find_element(By.CLASS_NAME, "main")
            screenshot = main_content.screenshot_as_png
            image = Image.open(io.BytesIO(screenshot))

            # Save heatmap view
            heatmap_path = os.path.join(images_dir, 'dashboard_heatmap.png')
            image.save(heatmap_path)
            print(f"✅ Saved heatmap screenshot: dashboard_heatmap.png")
        except Exception as e:
            print(f"⚠️  Could not capture heatmap: {e}")

        # Screenshot 4: Time Series
        try:
            # Scroll to time series section
            driver.execute_script("arguments[0].scrollIntoView();",
                driver.find_element(By.XPATH, "//*[contains(text(), 'Sales Trends')]"))

            time.sleep(2)
            main_content = driver.find_element(By.CLASS_NAME, "main")
            screenshot = main_content.screenshot_as_png
            image = Image.open(io.BytesIO(screenshot))

            # Save time series view
            timeseries_path = os.path.join(images_dir, 'dashboard_timeseries.png')
            image.save(timeseries_path)
            print(f"✅ Saved time series screenshot: dashboard_timeseries.png")
        except Exception as e:
            print(f"⚠️  Could not capture time series: {e}")

        driver.quit()
        print("✅ Automated screenshot capture completed!")
        return True

    except Exception as e:
        print(f"❌ Automated screenshots failed: {e}")
        print("Falling back to manual method...")
        return False

def create_placeholder_screenshots():
    """Create placeholder screenshots for testing"""
    from PIL import Image, ImageDraw, ImageFont
    import textwrap

    images_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    # Create placeholder images
    placeholders = [
        ('dashboard_kpi.png', 'KPI Cards View\n\nTotal Units Sold\nTotal Revenue (£)\nTotal Profit (£)\nAvg Profit Margin'),
        ('dashboard_regional.png', 'Regional Performance Analysis\n\nInteractive bar chart showing\nprofit by UK region\n\nScotland: £926.3K\nWales: £718.4K\nJersey: £899.0K\nN. Ireland: £740.5K\nEngland: £677.2K'),
        ('dashboard_heatmap.png', 'Performance Matrix Heatmap\n\nProfit Margin % by Region × Product\n\nDark Green = High Margin\nDark Red = Low Margin\n\nInteractive hover tooltips'),
        ('dashboard_timeseries.png', 'Monthly Sales Trends\n\nTime series chart with\nregional filtering\n\nUnits Sold over time\nby region\n\nInteractive legends')
    ]

    for filename, text in placeholders:
        # Create image
        img = Image.new('RGB', (800, 400), color='#f0f2f6')
        draw = ImageDraw.Draw(img)

        # Try to use default font
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()

        # Draw text
        y_position = 50
        for line in text.split('\n'):
            if line.strip():
                # Handle text wrapping
                wrapped_lines = textwrap.wrap(line, width=40)
                for wrapped_line in wrapped_lines:
                    draw.text((50, y_position), wrapped_line, fill='black', font=font)
                    y_position += 25
            else:
                y_position += 15

        # Save image
        img_path = os.path.join(images_dir, filename)
        img.save(img_path)
        print(f"📄 Created placeholder: {filename}")

def main():
    """Main function"""
    print("📸 Dashboard Screenshot Capture Tool")
    print("=" * 50)

    # Check if images directory exists (in parent directory)
    images_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print("📁 Created images directory")

    # Ask user what they want to do
    print("\nChoose an option:")
    print("1. 🚀 Start dashboard and capture real screenshots (requires Chrome)")
    print("2. 📄 Create placeholder screenshots for testing")
    print("3. 📋 Show manual screenshot instructions")

    try:
        choice = input("\nEnter your choice (1-3): ").strip()
    except:
        choice = "2"  # Default to placeholders if input fails

    if choice == "1":
        # Check requirements
        if not check_requirements():
            return

        # Start dashboard
        dashboard_process = start_dashboard()
        if not dashboard_process:
            return

        try:
            # Try automated screenshots
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

    elif choice == "2":
        print("\n📄 Creating placeholder screenshots...")
        create_placeholder_screenshots()
        print("✅ Placeholder screenshots created in images/ directory")

    else:
        print("\n📋 MANUAL SCREENSHOT INSTRUCTIONS:")
        print("=" * 50)
        take_screenshots_guide()

if __name__ == "__main__":
    main()
