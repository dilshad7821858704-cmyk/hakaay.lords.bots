from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

BOT_DATA = {
    "accounts": [
        {"igg_id": "123456789", "server": "1600", "status": "Active"}
    ]
}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lords Mobile Web Bot - IGG Connect</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #fff; padding: 15px; margin: 0; }
        .container { max-width: 600px; margin: auto; background: #1e293b; padding: 20px; border-radius: 10px; }
        h1 { text-align: center; color: #38bdf8; font-size: 20px; }
        .status { background: #0f172a; padding: 10px; border-radius: 6px; border-left: 4px solid #22c55e; margin-bottom: 15px; font-family: monospace; font-size: 13px; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; margin-bottom: 10px; font-size: 15px; }
        .btn-start { background: #22c55e; color: white; }
        .btn-stop { background: #ef4444; color: white; }
        .btn-save { background: #38bdf8; color: #0f172a; margin-top: 15px; }
        .section { background: #334155; padding: 12px; border-radius: 6px; margin-top: 15px; }
        h3 { margin-top: 0; color: #cbd5e1; font-size: 15px; border-bottom: 1px solid #475569; padding-bottom: 5px; }
        label { display: block; margin-bottom: 8px; font-size: 13px; cursor: pointer; }
        input[type="text"], input[type="password"] { width: 100%; padding: 6px; background: #0f172a; border: 1px solid #475569; color: #fff; border-radius: 4px; margin-top: 4px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Lords Mobile Web Bot</h1>
        <div class="status" id="status-msg">READY | Connect to IGG.</div>
        
        <div class="section">
            <h3>Connect IGG Account</h3>
            <label>IGG ID / Username: <input type="text" id="igg_id" placeholder="Enter IGG ID"></label>
            <label>IGG Password / Token: <input type="password" id="igg_pass" placeholder="Enter password"></label>
            <label>Server / Kingdom: <input type="text" id="igg_server" placeholder="e.g. 1600"></label>
            <button class="btn btn-save" onclick="addAccount()">CONNECT TO IGG</button>
        </div>

        <div class="section">
            <h3>Connected Accounts</h3>
            <pre id="acc-list" style="background: #0f172a; padding: 10px; border-radius: 4px; color: #38bdf8; font-size: 12px;">Loading...</pre>
        </div>

        <button class="btn btn-start" onclick="alert('Bot started for connected IGG accounts!')">START BOT 24/7</button>
        <button class="btn btn-stop" onclick="alert('Bot stopped.')">STOP BOT</button>
    </div>

    <script>
        function loadAccounts() {
            fetch('/api/accounts')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('acc-list').innerText = JSON.stringify(data, null, 2);
                });
        }

        function addAccount() {
            const igg_id = document.getElementById('igg_id').value;
            const server = document.getElementById('igg_server').value;
            
            fetch('/api/accounts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ igg_id: igg_id, server: server })
            })
            .then(res => res.json())
            .then(response => {
                document.getElementById('status-msg').innerText = "SUCCESS | Connected to IGG!";
                loadAccounts();
            });
        }

        loadAccounts();
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    return jsonify(BOT_DATA["accounts"])

@app.route("/api/accounts", methods=["POST"])
def add_account():
    new_acc = request.json
    if new_acc and new_acc.get("igg_id"):
        BOT_DATA["accounts"].append({
            "igg_id": new_acc.get("igg_id"),
            "server": new_acc.get("server", "Unknown"),
            "status": "Connected to IGG"
        })
        return jsonify({"status": "success", "message": "Connected successfully!"})
    return jsonify({"status": "error"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
