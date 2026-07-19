# Collection Automation V3

## Overview

Collection Automation V3 is a Python-based automation system that downloads reports, filters data based on user roles and branch access, generates personalized Excel reports, and automatically emails them to users.

The project is designed to reduce manual effort in report distribution by automating the complete workflow.

---

## Features

- Download reports automatically
- Load multiple reports into memory
- Filter reports based on user role and branch
- Generate personalized Excel reports
- Send reports via email
- Execution logging
- Summary generation
- Easy to configure for new users and reports

---

## Tech Stack

- Python 3.x
- Pandas
- OpenPyXL
- XlsxWriter
- SMTP (Email Automation)

---

## Project Structure

```
Collection-Automation-V3/
│
├── modules/
│   ├── download_reports.py
│   ├── report_manager.py
│   ├── filter_engine.py
│   ├── email_service.py
│   ├── summary.py
│   ├── logger.py
│   └── validator.py
│
├── config.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Collection-Automation-V3.git
cd Collection-Automation-V3
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Update the `config.py` file with:

- Email credentials
- SMTP server details
- Report locations
- User file path

> **Important:** Do not commit real credentials. Use environment variables or a `.env` file for sensitive information.

---

## Usage

Run the application:

```bash
python main.py
```

The automation will:

1. Validate the user file
2. Download reports
3. Load reports into memory
4. Filter reports for each user
5. Generate Excel reports
6. Email reports to users
7. Generate execution summary

---

## Future Improvements

- Scheduler integration
- Dashboard for execution status
- Email retry mechanism
- Database integration
- Cloud deployment
- Role-based configuration UI

---

## Author

**Aayush Bansal**

- Data Analyst
- Python | SQL | Power BI | Automation
