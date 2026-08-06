# BioMatrixReport MCP Server

Generated automatically from the BioMatrixReport source repo. Exposes its API
as MCP tools so an AI assistant can call them via natural language.

## What's in here

- `server.py` - the MCP server (mounted at `/mcp`) plus one tool per API
  endpoint discovered in the source repo.
- `auth.py` / `session_store.py` - authentication. **Credentials and tokens
  never pass through the assistant** - sign-in always happens in a real
  browser page, and only an opaque session reference reaches the model.
- `config.py` - runtime settings, read from environment variables.

## 1. Configure environment variables

Copy `.env.example` to `.env` (locally) or set these in your hosting
platform's dashboard:

- `TARGET_APP_BASE_URL` - detected as `http://localhost:5183` from the source repo. **Confirm this is actually where BioMatrixReport is running** (dev/staging/prod may differ) and update it if not.

## 2. Deploy to Render

1. Push this folder to a new git repo (or use Render's "Deploy from a Blueprint"
   with the included `render.yaml`).
2. In the Render dashboard, create a new **Web Service** from that repo
   (Render will detect the `Dockerfile`), or use the Blueprint if you set one
   up from `render.yaml`.
3. Set the environment variables from step 1 in the Render dashboard.
4. Deploy. Render will give you a public URL like `https://your-service.onrender.com`.

## 3. Connect it to your AI assistant

Add the MCP server URL to your assistant as a remote MCP connector:

```
https://your-service.onrender.com/mcp
```


## Available tools

- `get_employee_details` (GET `/get-details`) - Fetches an employee's details (name, email, department, manager, active status, etc.) from the external HRIS/Employee API by employee code. Returns the raw JSON employee record.
- `send_weekly_email` (POST `/sendWeeklyEmail`) - Triggers sending of the weekly Work-From-Office (WFO) attendance report email to active employees (and their managers). Validates that attendance data exists for the last Mon/Tue/Wed before sending; if data is missing, sends an alert email instead and returns an error.
- `send_monthly_email` (POST `/sendMonthlyEmail`) - Triggers sending of the monthly WFO attendance report email (with 6-month trend chart and pattern analysis) to active employees for the previous calendar month.
- `send_monthly_report` (POST `/api/EngineeringHeadReport/sendMonthlyReport`) - Generates and emails a company-wide monthly WFO compliance report to the engineering head, including department/band breakdowns, compliance distribution, day-of-week analysis, manager leaderboard, and 6-month trends. Defaults to the previous month if month/year are not supplied.
- `sync_employees_from_hris` (POST `/api/EmployeeSync/syncFromHRIS`) - Syncs employee master data from the external HRIS API into the local database, creating new employee records (default SendEmail='No') or updating existing ones (preserving SendEmail preference). Returns counts of new/updated records and any per-record errors.
- `upload_attendance_csv` (POST `/api/UserData/upload`) - Uploads one or more CSV files containing biometric attendance data (employee ID, datetime, IN/OUT status) and inserts the records into the database.
- `send_monthly_attendance_email` (POST `/sendMonthlyAttendanceEmail`) - Generates an Excel (xlsx) attendance report for all active employees for the previous month and emails it as an attachment to HR.
- `send_weekly_attendance_email` (POST `/sendWeeklyAttendanceEmail`) - Generates a CSV attendance report for the prior complete week and emails it as an attachment to HR.
- `trigger_attendance_sync` (POST `/api/attendance-sync/trigger`) - Manually triggers a sync of biometric attendance transactions (in/out punches) for a given date from the external iClock biometric device API into the AttendanceRecords table. Returns the date synced and the number of records upserted.

## Notes from analysis

ASP.NET Core 6 app with no authentication/authorization configured anywhere (no [Authorize] attributes, no auth middleware registered in Program.cs), so all endpoints are unauthenticated. Base URL is only known from the local dev launchSettings.json (http://localhost:5183 / https://localhost:7083) - no deployed/production URL was found in config or docs. The app also calls several external third-party APIs (HRIS at app1.thepsi.com, an internal Employee API at 192.168.3.220:5000, a biometric iClock API, and a SendMail API) but those are outbound dependencies, not endpoints this app exposes, so they were excluded. The GET /get-details endpoint proxies to that internal Employee API.

## Local development

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in values
python server.py
```
