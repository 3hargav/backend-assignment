from flask import Blueprint, request, jsonify
from sqlalchemy import desc

from app import db, ApiKeys, Videos

main = Blueprint('main', __name__)


@main.route('/videos', methods=['GET'])
def fetch_videos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    videos = Videos.query.order_by(desc(Videos.published_at)).paginate(page=page, per_page=per_page, error_out=False)

    result = {
        'videos': [{
            'id': video.id,
            'title': video.title,
            'description': video.description,
            'published_at': video.published_at.strftime('%Y-%m-%dT%H:%M:%S')
        } for video in videos.items],
        'page': page,
        'per_page': per_page,
        'total_pages': videos.pages,
        'total_items': videos.total
    }

    return jsonify(result), 200


@main.route("/search_videos", methods=['GET'])
def search_videos():
    query = request.args.get('query', '')
    videos = Videos.query.filter((Videos.title.ilike(f'%{query}%')) | (Videos.description.ilike(f'%{query}%'))).all()
    result = [{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'published_at': video.published_at.strftime('%Y-%m-%dT%H:%M:%S')
    } for video in videos]

    return jsonify(result), 200


@main.route('/api_key', methods=['POST'])
def update_api_key():
    data = request.get_json()

    if 'key' not in data:
        return jsonify({'error': 'Missing key field in request'}), 400

    existing_api_key = ApiKeys.query.filter_by(key=data['key']).first()

    if existing_api_key:
        db.session.delete(existing_api_key)
        db.session.commit()

    new_api_key = ApiKeys(key=data['key'], is_quota_exceeded=False)
    db.session.add(new_api_key)
    db.session.commit()

    return jsonify({'message': 'API key updated successfully'}), 200


@main.route('/admin/videos', methods=['GET'])
def get_dashboard_videos():
    title_filter = request.args.get('title')
    description_filter = request.args.get('description')
    sort_by = request.args.get('sort_by', 'published_at')
    sort_order = request.args.get('sort_order', 'desc')

    query = Videos.query
    if title_filter:
        query = query.filter(Videos.title.ilike(f'%{title_filter}%'))
    if description_filter:
        query = query.filter(Videos.description.ilike(f'%{description_filter}%'))

    if sort_by == 'published_at':
        if sort_order == 'asc':
            query = query.order_by(Videos.published_at)
        else:
            query = query.order_by(desc(Videos.published_at))
    elif sort_by == 'title':
        if sort_order == 'asc':
            query = query.order_by(Videos.title)
        else:
            query = query.order_by(desc(Videos.title))

    videos = query.all()

    result = [{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'published_at': video.published_at.strftime('%Y-%m-%dT%H:%M:%S')
    } for video in videos]

    return jsonify(result), 200
