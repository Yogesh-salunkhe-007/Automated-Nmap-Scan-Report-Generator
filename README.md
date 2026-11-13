# Automated Nmap Scan Report Generator

# Project Overview
A Python-based VAPT automation project that parses Nmap XML scan results and generates structured JSON and HTML reports.

# Objectives
- Parse Nmap XML files using Python.
- Extract discovered hosts and IP addresses.
- Identify open ports and detected services.
- Generate JSON reports.
- Generate HTML reports for easy review.

# Technologies Used
- Python 3
- Nmap
- XML ElementTree
- JSON
- HTML
- pathlib
- datetime

# Project Structure

day40-nmap-report-generator/
├── src/
│   └── report_generator.py
├── reports/
├── evidence/
├── docs/
├── README.md
└── .gitignore


# How to Run

First, generate an Nmap XML file against your authorized lab target:

bash:-
nmap -sV -oX reports/lab-scan.xml YOUR_LAB_IP


Then run the Python script:

bash:-
python3 src/report_generator.py reports/lab-scan.xml


The script generates JSON and HTML reports in the reports/nmap directory relative to its configured project root.

# Learning Outcomes
- Python XML parsing
- File handling
- Nmap automation
- JSON report generation
- HTML report generation
- Basic security assessment reporting

# Disclaimer
This project is intended only for authorized security testing and isolated lab environments.