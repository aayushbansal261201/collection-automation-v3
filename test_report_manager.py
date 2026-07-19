from modules.report_manager import ReportManager

manager = ReportManager()

reports = manager.load_reports()

print("\nLoaded Reports:")

for report in reports:
    print(report)