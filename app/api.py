from flask import Blueprint, jsonify
from app.models import Conversation, WarrantyClaim, User, db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint("api", __name__)


@bp.route("/stats", methods=["GET"])
def stats():
    """Summary stats for analytics dashboard."""
    total_convs = Conversation.query.count()
    total_users = User.query.count()
    resolved = Conversation.query.filter_by(resolved=True).count()
    resolution_rate = round((resolved / total_convs * 100) if total_convs else 0, 1)

    # Today's stats
    today = datetime.utcnow().date()
    today_convs = Conversation.query.filter(
        func.date(Conversation.timestamp) == today
    ).count()

    # Open warranty claims
    open_claims = WarrantyClaim.query.filter_by(status="open").count()

    return jsonify({
        "total_conversations": total_convs,
        "total_users": total_users,
        "resolution_rate": resolution_rate,
        "today_conversations": today_convs,
        "open_warranty_claims": open_claims,
    })


@bp.route("/intents", methods=["GET"])
def intents():
    """Intent distribution."""
    results = db.session.query(
        Conversation.intent,
        func.count(Conversation.id).label("count")
    ).group_by(Conversation.intent).all()

    return jsonify([{"intent": r.intent, "count": r.count} for r in results])


@bp.route("/languages", methods=["GET"])
def languages():
    """Language distribution."""
    results = db.session.query(
        Conversation.language,
        func.count(Conversation.id).label("count")
    ).group_by(Conversation.language).all()

    return jsonify([{"language": r.language, "count": r.count} for r in results])


@bp.route("/recent", methods=["GET"])
def recent():
    """Recent conversations (last 20)."""
    convs = Conversation.query.order_by(
        Conversation.timestamp.desc()
    ).limit(20).all()

    return jsonify([{
        "phone": c.phone[-4:].rjust(len(c.phone), "*"),  # mask number
        "intent": c.intent,
        "language": c.language,
        "resolved": c.resolved,
        "timestamp": c.timestamp.isoformat(),
    } for c in convs])


@bp.route("/warranty-claims", methods=["GET"])
def warranty_claims():
    """All warranty claims."""
    claims = WarrantyClaim.query.order_by(WarrantyClaim.created_at.desc()).limit(50).all()
    return jsonify([{
        "ticket_id": c.ticket_id,
        "model_no": c.model_no,
        "complaint": c.complaint,
        "status": c.status,
        "created_at": c.created_at.isoformat(),
    } for c in claims])
