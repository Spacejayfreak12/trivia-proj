@echo off
rem This script sets the environment variables needed for the persistent public URL
rem and then runs the application.

rem Default values
set PORT=5000
set AUTHTOKEN=
set SUBDOMAIN=

rem Parse command line arguments
:parse_args
if "%~1"=="" goto run_app
if "%~1"=="-p" set PORT=%~2 & shift & shift & goto parse_args
if "%~1"=="-a" set AUTHTOKEN=%~2 & shift & shift & goto parse_args
if "%~1"=="-s" set SUBDOMAIN=%~2 & shift & shift & goto parse_args
shift
goto parse_args

:run_app
rem Set environment variables if provided
if not "%AUTHTOKEN%"=="" (
    set NGROK_AUTHTOKEN=%AUTHTOKEN%
    echo Set NGROK_AUTHTOKEN from parameter
)

if not "%SUBDOMAIN%"=="" (
    set NGROK_SUBDOMAIN=%SUBDOMAIN%
    echo Set NGROK_SUBDOMAIN from parameter
)

rem Display info
echo Using port: %PORT%

rem Run the application
python app.py

rem Cleanup (optional)
rem set NGROK_AUTHTOKEN=
rem set NGROK_SUBDOMAIN=
rem set PORT= 