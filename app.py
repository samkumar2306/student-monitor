import os
import requests
from flask import Flask, request, jsonify, render_template
from database import init_db, get_members, get_all_members, add_member, delete_member

app = Flask(__name__)

N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL", "")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/members', methods=['GET'])
def list_members():
    return jsonify(get_all_members())

@app.route('/api/members', methods=['POST'])
def add():
    data = request.json
    name = data.get('name', '').strip()
    phone = data.get('phone', '').strip()
    group = data.get('group', '').strip()
    if not name or not phone or not group:
        return jsonify({"error": "All fields required"}), 400
    add_member(name, phone, group)
    return jsonify({"status": "added"})

@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def remove(member_id):
    delete_member(member_id)
    return jsonify({"status": "deleted"})

@app.route('/api/send', methods=['POST'])
def send():
    data = request.json
    group = data.get('group', '').strip()
    message = data.get('message', '').strip()

    if not group or not message:
        return jsonify({"error": "Group and message required"}), 400

    members = get_members(group)
    if not members:
        return jsonify({"error": f"No members in group: {group}"}), 404

    if not N8N_WEBHOOK_URL:
        return jsonify({"error": "N8N_WEBHOOK_URL not configured"}), 500

    payload = {
        "group": group,
        "message": message,
        "members": members
    }

    try:
        resp = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=15)
        resp.raise_for_status()
        return jsonify({"status": "sent", "count": len(members)})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)