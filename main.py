import asyncio
from flask import Flask, request, jsonify
from log_to_sheet import log_to_sheet
from send_email import send_email 

app = Flask(__name__)

def get_json_or_400():
    data = request.get_json()
    if not data:
        return None, jsonify({"result": "No data provided"}), 400
    return data, None, None

@app.route('/webhook', methods=['POST'])
def handle_call_report():
    data, error_response, status_code = get_json_or_400()
    if error_response:
        return error_response, status_code

    message = data.get("message")
    if not message or message.get("type") != "end-of-call-report":
        return jsonify({"result": "Invalid or missing 'end-of-call-report' message"}), 400

    print("📞 Logging end-of-call report...")

    try:
        log_to_sheet(message)
        return jsonify({"result": "Call report logged to Google Sheet."}), 200
    except Exception as e:
        print(f"❌ Error logging call report: {e}")
        return jsonify({"result": f"Failed to log call report: {str(e)}"}), 500


@app.route('/tools/webhook', methods=['POST'])
def handle_tool_calls():
    data, error_response, status_code = get_json_or_400()
    if error_response:
        return error_response, status_code

    message = data.get("message")
    if not message or message.get("type") != "tool-calls":
        return jsonify({"result": "Invalid or missing 'tool-calls' message"}), 400

    tool_calls = message.get("toolCalls", [])
    if not tool_calls:
        return jsonify({"result": "No tool calls found."}), 400

    for tool_call in tool_calls:
        args = tool_call.get("function", {}).get("arguments", {})
        to_email = args.get("to_email")
        subject = args.get("subject")
        body = args.get("body")

        print(f"🛠️ Tool call arguments: {args}")

        if not all([to_email, subject, body]):
            return jsonify({"result": "Missing 'to_email', 'subject', or 'body' in tool call"}), 400

        print(f"📤 Sending email to {to_email} with subject '{subject}'")

        try:
            success = run_async(send_email(to_email, subject, body))
        except Exception as e:
            print(f"❌ Email send error: {e}")
            return jsonify({"result": f"Failed to send the email: {str(e)}"}), 500

        if success:
            return jsonify({"result": "Your email has been sent."}), 200
        else:
            return jsonify({"result": "Failed to send the email."}), 500

    return jsonify({"result": "No valid tool calls processed."}), 400

def run_async(coro):
    """Run an async coroutine safely in a new event loop."""
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    finally:
        loop.close()

if __name__ == '__main__':
    app.run(debug=True)
