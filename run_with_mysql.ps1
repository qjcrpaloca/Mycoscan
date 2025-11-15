# Run MycoScan with local MySQL (Docker) and apply migrations
# Usage: from project root run `powershell -ExecutionPolicy Bypass -File .\run_with_mysql.ps1`

Write-Host "Setting environment variables for local MySQL..."
$env:DATABASE_URL = "mysql+pymysql://myuser:mypass@127.0.0.1:3306/mycoscan"
$env:SECRET_KEY = "change-me"
$env:FLASK_APP = "main:create_app"
$env:FLASK_ENV = "development"

Write-Host "Installing Python requirements (if needed)..."
pip install -r requirements.txt

if (!(Test-Path -Path ".\migrations")) {
    Write-Host "Initializing migrations (migrations folder not found)..."
    flask db init
}

Write-Host "Creating migration script..."
flask db migrate -m "init"

Write-Host "Applying migrations..."
flask db upgrade

Write-Host "Starting MycoScan app..."
python run_app.py
