This project sets up a **Voice AI Receptionist** that logs call reports and sends emails via a webhook. We use **ngrok** to expose the local server to the internet.

## Steps to Set Up

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <project_directory>
```

### 2. Set Up Vapi Account

1. Sign up on [Vapi](https://www.vapi.com/).
2. Follow the instructions to create your account and get the API key.

### 3. Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.developers.google.com/).
2. Enable **Google Sheets API**.
3. Create a **Service Account** and download the credentials JSON file.
4. Rename the file to `credentials.json` and place it in your project.

### 4. Install Dependencies

Run the following command to install required libraries:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file with:

```dotenv
GMAIL_USER=<your_gmail_username>
GMAIL_PASSWORD=<your_gmail_app_password>
SHEET_ID=<your_google_sheet_id>
VAPI_API_KEY=<your_vapi_api_key>
```

### 6. Run the Application

Run the Flask application:

```bash
python main.py
```

### 7. Expose with ngrok

Run **ngrok** to expose your app:

```bash
ngrok http 5000
```

Get the generated public URL, e.g., `http://<random_subdomain>.ngrok.io`.

### 8. Set Webhooks in Vapi

In Vapi, set the following webhook URLs:

* **Messaging Webhook URL**: `http://<random_subdomain>.ngrok.io/webhook`
* **Tool Webhook URL**: `http://<random_subdomain>.ngrok.io/tools/webhook`

### 9. Test

Run the tests:

```bash
pytest test_webhooks.py
```

Now your Voice AI Receptionist is ready to log call reports and send emails!
