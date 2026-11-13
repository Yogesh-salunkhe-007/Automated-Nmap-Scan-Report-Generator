
import json
import html
import sys
import xml.etree.ElementTree as ET

from pathlib import Path
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def parse_xml_file(xml_file):
    xml_file = Path(xml_file)

    if not xml_file.is_file():
        raise FileNotFoundError(f"XML file not found: {xml_file}")

    root = ET.parse(xml_file).getroot()
    hosts = []

    for host in root.findall("host"):
        status_element = host.find("status")
        status = status_element.get("state", "unknown") if status_element is not None else "unknown"

        addresses = [
            {
                "ip": address.get("addr"),
                "type": address.get("addrtype")
            }
            for address in host.findall("address")
        ]

        ports = []

        for port_element in host.findall("./ports/port"):
            port_id = port_element.get("portid")

            if port_id is None:
                continue

            state_element = port_element.find("state")
            service_element = port_element.find("service")

            state = state_element.get("state", "unknown") if state_element is not None else "unknown"

            service = {}
            if service_element is not None:
                service = {
                    "name": service_element.get("name"),
                    "product": service_element.get("product"),
                    "version": service_element.get("version")
                }

            ports.append({
                "protocol": port_element.get("protocol"),
                "port": int(port_id),
                "state": state,
                "service": service
            })

        hosts.append({
            "status": status,
            "addresses": addresses,
            "ports": ports
        })

    return hosts


def generate_json_report(hosts):
    timestamp = datetime.now(timezone.utc)

    report = {
        "report_name": "Nmap Service Assessment",
        "generated_at": timestamp.isoformat(),
        "host_count": len(hosts),
        "open_port_count": sum(
            port["state"] == "open"
            for host in hosts
            for port in host["ports"]
        ),
        "hosts": hosts
    }

    filename = f"nmap-report-{timestamp:%Y%m%d-%H%M%S}.json"
    output_file = REPORT_DIR / filename

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"[+] JSON report saved: {output_file}")
    return report, filename


def generate_html_report(report, json_filename):
    rows = []

    for host in report["hosts"]:
        ips = [
            address["ip"]
            for address in host["addresses"]
            if address["type"] == "ipv4" and address["ip"]
        ]

        ip = ", ".join(ips) or "unknown"

        for port in host["ports"]:
            if port["state"] != "open":
                continue

            service = port["service"]

            rows.append(
                f"<tr>"
                f"<td>{html.escape(ip)}</td>"
                f"<td>{port['port']}/{html.escape(port.get('protocol') or '')}</td>"
                f"<td>{html.escape(service.get('name') or 'unknown')}</td>"
                f"<td>{html.escape(service.get('product') or '')}</td>"
                f"<td>{html.escape(service.get('version') or '')}</td>"
                f"</tr>"
            )

    table_rows = "\n".join(rows) or (
        '<tr><td colspan="5">No open ports found</td></tr>'
    )

    page = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nmap VAPT Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
            background: #f4f4f4;
        }}
        h1 {{
            color: #183153;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}
        th, td {{
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }}
        th {{
            background: #183153;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>Nmap Service Assessment Report</h1>
    <p>Generated: {html.escape(report['generated_at'])}</p>
    <p>Hosts discovered: {report['host_count']}</p>
    <p>Open ports: {report['open_port_count']}</p>

    <table>
        <tr>
            <th>IP Address</th>
            <th>Port</th>
            <th>Service</th>
            <th>Product</th>
            <th>Version</th>
        </tr>
        {table_rows}
    </table>

    <p>JSON evidence: {html.escape(json_filename)}</p>
</body>
</html>
"""

    timestamp = datetime.now(timezone.utc)
    filename = f"nmap-report-{timestamp:%Y%m%d-%H%M%S}.html"
    output_file = REPORT_DIR / filename

    output_file.write_text(page, encoding="utf-8")
    print(f"[+] HTML report saved: {output_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python report_generator.py <nmap-xml-file>")
        sys.exit(1)

    try:
        print("\n[*] Parsing Nmap XML file...")
        hosts = parse_xml_file(sys.argv[1])
        print(f"[+] Hosts processed: {len(hosts)}")

        print("[*] Generating JSON report...")
        report, json_filename = generate_json_report(hosts)

        print("[*] Generating HTML report...")
        generate_html_report(report, json_filename)

        print("\n[+] Report generation completed!")

    except (FileNotFoundError, ET.ParseError, OSError, ValueError) as error:
        print(f"\n[!] Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
