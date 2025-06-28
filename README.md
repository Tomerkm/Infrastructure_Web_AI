# Infrastructure_Web_AI

## Installation Guide
#### Step 1: Clone the Repository
```bash
git clone https://github.com/Tomerkm/Infrastructure_Web_AI.git
cd Infrastructure_Web_AI
```

#### Step 2: Set Up Python Environment

```bash
python -m venv .venv
```

Activate the virtual environment:
- Windows (Command Prompt):
```cmd
.venv\Scripts\activate
```
- Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

#### Step 3: Install Dependencies
Install Python packages:
```bash
pip install -r requirements.txt
```

Install Browsers in playwright. 
```bash
playwright install --with-deps
```
Or you can install specific browsers by running:
```bash
playwright install chromium --with-deps
```



#### Step 4: Configure Environment
Open `.env` in your preferred text editor and add your API keys and other settings




