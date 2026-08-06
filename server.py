"""Generated MCP server for BioMatrixReport.

Do not hand-edit the tool functions below if you plan to regenerate this
project later - edit the source repo and regenerate instead. auth.py and
config.py are safe (and expected) to tune by hand, especially
TARGET_APP_BASE_URL / PUBLIC_BASE_URL and any OAuth client credentials.
"""

import contextlib

import httpx
from fastapi import FastAPI
from mcp.server.fastmcp import Context, FastMCP

from config import settings

mcp = FastMCP("BioMatrixReport")


def _clean(params: dict) -> dict | None:
    cleaned = {k: v for k, v in params.items() if v is not None}
    return cleaned or None


def _safe_body(resp: httpx.Response):
    try:
        return resp.json()
    except ValueError:
        return resp.text


@mcp.tool()
async def get_employee_details(
    employeeId: str,
) -> dict:
    """Fetches an employee's details (name, email, department, manager, active status, etc.) from the external HRIS/Employee API by employee code. Returns the raw JSON employee record."""
    path = f"/get-details"
    query_params = {
        "employeeId": employeeId,
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "GET", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def send_weekly_email(
    SendEmails: str | None = None,
    EmpCode: str | None = None,
) -> dict:
    """Triggers sending of the weekly Work-From-Office (WFO) attendance report email to active employees (and their managers). Validates that attendance data exists for the last Mon/Tue/Wed before sending; if data is missing, sends an alert email instead and returns an error."""
    path = f"/sendWeeklyEmail"
    query_params = {
        "SendEmails": SendEmails,
        "EmpCode": EmpCode,
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def send_monthly_email(
    SendEmails: str | None = None,
    EmpCode: str | None = None,
) -> dict:
    """Triggers sending of the monthly WFO attendance report email (with 6-month trend chart and pattern analysis) to active employees for the previous calendar month."""
    path = f"/sendMonthlyEmail"
    query_params = {
        "SendEmails": SendEmails,
        "EmpCode": EmpCode,
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def send_monthly_report(
    month: int | None = None,
    year: int | None = None,
) -> dict:
    """Generates and emails a company-wide monthly WFO compliance report to the engineering head, including department/band breakdowns, compliance distribution, day-of-week analysis, manager leaderboard, and 6-month trends. Defaults to the previous month if month/year are not supplied."""
    path = f"/api/EngineeringHeadReport/sendMonthlyReport"
    query_params = {
        "month": month,
        "year": year,
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def sync_employees_from_hris(
) -> dict:
    """Syncs employee master data from the external HRIS API into the local database, creating new employee records (default SendEmail='No') or updating existing ones (preserving SendEmail preference). Returns counts of new/updated records and any per-record errors."""
    path = f"/api/EmployeeSync/syncFromHRIS"
    query_params = {
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def upload_attendance_csv(
    files: str,
) -> dict:
    """Uploads one or more CSV files containing biometric attendance data (employee ID, datetime, IN/OUT status) and inserts the records into the database."""
    path = f"/api/UserData/upload"
    query_params = {
    }
    json_body = {
        "files": files,
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def send_monthly_attendance_email(
) -> dict:
    """Generates an Excel (xlsx) attendance report for all active employees for the previous month and emails it as an attachment to HR."""
    path = f"/sendMonthlyAttendanceEmail"
    query_params = {
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def send_weekly_attendance_email(
) -> dict:
    """Generates a CSV attendance report for the prior complete week and emails it as an attachment to HR."""
    path = f"/sendWeeklyAttendanceEmail"
    query_params = {
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

@mcp.tool()
async def trigger_attendance_sync(
    date: str | None = None,
) -> dict:
    """Manually triggers a sync of biometric attendance transactions (in/out punches) for a given date from the external iClock biometric device API into the AttendanceRecords table. Returns the date synced and the number of records upserted."""
    path = f"/api/attendance-sync/trigger"
    query_params = {
        "date": date,
    }
    json_body = {
    }
    headers: dict = {}
    async with httpx.AsyncClient(base_url=settings.target_app_base_url, timeout=30.0) as client:
        resp = await client.request(
            "POST", path, params=_clean(query_params), json=(json_body or None), headers=headers
        )
    return {"status_code": resp.status_code, "body": _safe_body(resp)}

# streamable_http_app() must be created before referencing mcp.session_manager
# below (it's what initializes it), and its lifespan (which starts that
# session manager's task group) has to be wired into our own FastAPI app
# explicitly - Starlette doesn't propagate a mounted sub-app's lifespan to
# the parent automatically, so without this every request would fail with
# "Task group is not initialized".
mcp_asgi_app = mcp.streamable_http_app()


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(title="BioMatrixReport MCP Server", lifespan=lifespan)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


# Mounted at "/" (not "/mcp") because streamable_http_app() already serves
# itself at "/mcp" internally - mounting it under "/mcp" too would make the
# real path "/mcp/mcp". Registered last so the explicit routes above win.
app.mount("/", mcp_asgi_app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.port)
