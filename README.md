# Automated Nmap Scan Report Generator

## Project Overview

A Python-based VAPT automation project that parses Nmap XML scan results and generates structured JSON and HTML reports. It helps security professionals review discovered hosts, open ports, and detected services in an organized format.

## Objectives

- Parse Nmap XML files using Python.
- Extract discovered hosts and IP addresses.
- Identify open ports and detected services.
- Generate structured JSON reports.
- Generate HTML reports for easy review.
- Maintain scan evidence and generated reports.

## Technologies Used

- Python 3
- Nmap
- XML ElementTree
- JSON
- HTML
- pathlib
- datetime

## Project Structure

```text
Automated-Nmap-Scan-Report-Generator/
│
├── evidence/
│   └── scan screenshots
│
├── nmap_scan/
│
├── reports/
│   ├── JSON reports
│   └── HTML reports
│
├── src/
│   └── report_generator.py
│
├── xml_parse/
│   └── config.xml
│
├── README.md
└── .gitignore
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Yogesh-salunkhe-007/Automated-Nmap-Scan-Report-Generator.git
```

### 2. Navigate to the project directory

```bash
cd Automated-Nmap-Scan-Report-Generator
```

### 3. Generate an Nmap XML scan

Run Nmap against your authorized lab target:

```bash
nmap -sV -oX xml_parse/config.xml YOUR_LAB_IP
```

### 4. Run the Python script

```bash
python src/report_generator.py xml_parse/config.xml
```

### 5. View generated reports

The script generates JSON and HTML reports inside the `reports/` directory.

## Features

- Nmap XML parsing
- Host and IP extraction
- Open port detection
- Service and version identification
- Automated JSON report generation
- Automated HTML report generation
- Error handling for invalid or missing XML files

## Learning Outcomes

- Python XML parsing
- File handling
- Nmap automation
- JSON report generation
- HTML report generation
- Basic security assessment reporting

## Disclaimer

This project is intended only for authorized security testing and isolated lab environments. Do not scan systems or networks without proper permission.
