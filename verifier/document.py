"""
Penn State LionPATH Student Card Document Generator
Generates realistic student verification documents as HTML and PNG screenshots.
"""

from playwright.sync_api import sync_playwright


def generate_html(first_name: str, last_name: str, school_id: str = "2565") -> str:
    """
    Generate Penn State LionPATH student card HTML.
    
    Args:
        first_name: Student's first name
        last_name: Student's last name
        school_id: PSU student ID (default: '2565')
    
    Returns:
        Full HTML string with Penn State LionPATH branding
    """
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LionPATH - Student Center</title>
    <style>
        :root {{
            --psu-blue: #1E407C;
            --psu-navy: #001E44;
            --psu-light-blue: #96BEE6;
            --psu-white: #FFFFFF;
            --border-color: #D6D6D6;
            --bg-gray: #F5F5F5;
            --text-dark: #333333;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Arial', 'Helvetica Neue', sans-serif;
            background-color: var(--bg-gray);
            color: var(--text-dark);
            line-height: 1.6;
        }}
        
        .header {{
            background-color: var(--psu-blue);
            color: var(--psu-white);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .header-left {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        
        .logo {{
            font-size: 24px;
            font-weight: bold;
            letter-spacing: -0.5px;
        }}
        
        .university-name {{
            font-size: 18px;
            font-weight: 500;
            padding-left: 20px;
            border-left: 2px solid var(--psu-light-blue);
        }}
        
        .header-right {{
            font-size: 14px;
        }}
        
        .nav-bar {{
            background-color: var(--psu-navy);
            padding: 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .nav-tabs {{
            display: flex;
            list-style: none;
            margin: 0;
            padding: 0;
        }}
        
        .nav-tabs li {{
            flex: 1;
        }}
        
        .nav-tabs a {{
            display: block;
            padding: 12px 20px;
            color: var(--psu-white);
            text-decoration: none;
            text-align: center;
            font-size: 14px;
            border-right: 1px solid var(--psu-blue);
            transition: background-color 0.2s;
        }}
        
        .nav-tabs a:hover {{
            background-color: var(--psu-blue);
        }}
        
        .nav-tabs a.active {{
            background-color: var(--psu-blue);
            font-weight: bold;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }}
        
        .page-title {{
            font-size: 28px;
            color: var(--psu-navy);
            margin-bottom: 20px;
            font-weight: 600;
        }}
        
        .card {{
            background-color: var(--psu-white);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        .card-header {{
            font-size: 20px;
            font-weight: 600;
            color: var(--psu-navy);
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--psu-blue);
        }}
        
        .student-info {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .info-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .info-label {{
            font-size: 12px;
            color: #666;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 5px;
            letter-spacing: 0.5px;
        }}
        
        .info-value {{
            font-size: 16px;
            color: var(--text-dark);
            font-weight: 500;
        }}
        
        .status-enrolled {{
            color: #28A745;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .status-enrolled::before {{
            content: '✓';
            font-weight: bold;
            font-size: 18px;
        }}
        
        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        
        .schedule-table thead {{
            background-color: var(--psu-blue);
            color: var(--psu-white);
        }}
        
        .schedule-table th {{
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .schedule-table tbody tr {{
            border-bottom: 1px solid var(--border-color);
        }}
        
        .schedule-table tbody tr:hover {{
            background-color: #F9F9F9;
        }}
        
        .schedule-table td {{
            padding: 12px 15px;
            font-size: 14px;
        }}
        
        .course-number {{
            color: var(--psu-blue);
            font-weight: 600;
        }}
        
        .footer {{
            background-color: var(--psu-navy);
            color: var(--psu-white);
            text-align: center;
            padding: 20px;
            margin-top: 40px;
            font-size: 13px;
        }}
        
        .footer a {{
            color: var(--psu-light-blue);
            text-decoration: none;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        .semester-info {{
            display: inline-block;
            background-color: var(--psu-light-blue);
            color: var(--psu-navy);
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-left">
            <div class="logo">LionPATH</div>
            <div class="university-name">PennState</div>
        </div>
        <div class="header-right">
            Student Center
        </div>
    </header>
    
    <nav class="nav-bar">
        <ul class="nav-tabs">
            <li><a href="#" class="active">Academics</a></li>
            <li><a href="#">Enrollment</a></li>
            <li><a href="#">Financial Account</a></li>
            <li><a href="#">Personal Information</a></li>
            <li><a href="#">Campus Services</a></li>
        </ul>
    </nav>
    
    <div class="container">
        <h1 class="page-title">Student Center</h1>
        
        <div class="card">
            <div class="card-header">Student Information</div>
            <div class="student-info">
                <div class="info-item">
                    <div class="info-label">Name</div>
                    <div class="info-value">{first_name} {last_name}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">PSU ID</div>
                    <div class="info-value">{school_id}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Academic Program</div>
                    <div class="info-value">Computer Science BS</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Enrollment Status</div>
                    <div class="info-value status-enrolled">Enrolled</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">Class Schedule</div>
            <div class="semester-info">Fall 2025 Semester</div>
            <table class="schedule-table">
                <thead>
                    <tr>
                        <th>Class Nbr</th>
                        <th>Course</th>
                        <th>Title</th>
                        <th>Days & Times</th>
                        <th>Room</th>
                        <th>Units</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>12345</td>
                        <td><span class="course-number">CMPSC 311</span></td>
                        <td>Introduction to Systems Programming</td>
                        <td>MWF 10:10 AM - 11:00 AM</td>
                        <td>Thomas 117</td>
                        <td>3.0</td>
                    </tr>
                    <tr>
                        <td>12346</td>
                        <td><span class="course-number">CMPSC 360</span></td>
                        <td>Discrete Mathematics for Computer Science</td>
                        <td>TuTh 1:15 PM - 2:30 PM</td>
                        <td>Willard 260</td>
                        <td>3.0</td>
                    </tr>
                    <tr>
                        <td>12347</td>
                        <td><span class="course-number">CMPSC 465</span></td>
                        <td>Data Structures and Algorithms</td>
                        <td>MWF 12:20 PM - 1:10 PM</td>
                        <td>Thomas 216</td>
                        <td>3.0</td>
                    </tr>
                    <tr>
                        <td>12348</td>
                        <td><span class="course-number">CMPSC 473</span></td>
                        <td>Operating Systems Design & Construction</td>
                        <td>TuTh 3:05 PM - 4:20 PM</td>
                        <td>Westgate E131</td>
                        <td>3.0</td>
                    </tr>
                    <tr>
                        <td>12349</td>
                        <td><span class="course-number">CMPSC 483W</span></td>
                        <td>Software Design Project</td>
                        <td>MW 4:40 PM - 5:55 PM</td>
                        <td>IST 222</td>
                        <td>3.0</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <footer class="footer">
        <p>&copy; 2025 The Pennsylvania State University. All Rights Reserved.</p>
        <p><a href="#">Privacy Policy</a> | <a href="#">Accessibility</a> | <a href="#">Contact Us</a></p>
    </footer>
</body>
</html>
"""


def generate_image(first_name: str, last_name: str, school_id: str = "2565") -> bytes:
    """
    Generate PNG screenshot of Penn State LionPATH student card.
    
    Args:
        first_name: Student's first name
        last_name: Student's last name
        school_id: PSU student ID (default: '2565')
    
    Returns:
        PNG image as bytes
    """
    html = generate_html(first_name, last_name, school_id)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        page = browser.new_page(viewport={'width': 1200, 'height': 900})
        page.set_content(html, wait_until='load')
        page.wait_for_timeout(500)
        screenshot_bytes = page.screenshot(type='png', full_page=True)
        browser.close()
    
    return screenshot_bytes
