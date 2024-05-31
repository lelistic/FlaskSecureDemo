# webapp/bp_list_reports/__init__.py

from flask import Blueprint, jsonify, render_template, request
from flask_security import auth_required

list_reports = Blueprint('bp_list_reports', __name__)

# Static data for Bible Proverbs
proverbs = [
    {"chapter": 1, "verse": 7, "text": "The fear of the LORD is the beginning of knowledge, but fools despise wisdom and instruction."},
    {"chapter": 3, "verse": 5, "text": "Trust in the LORD with all your heart and lean not on your own understanding;"},
    {"chapter": 3, "verse": 6, "text": "in all your ways submit to him, and he will make your paths straight."},
    {"chapter": 4, "verse": 23, "text": "Above all else, guard your heart, for everything you do flows from it."},
    {"chapter": 10, "verse": 12, "text": "Hatred stirs up conflict, but love covers over all wrongs."},
    {"chapter": 12, "verse": 1, "text": "Whoever loves discipline loves knowledge, but whoever hates correction is stupid."},
    {"chapter": 13, "verse": 3, "text": "Those who guard their lips preserve their lives, but those who speak rashly will come to ruin."},
    {"chapter": 15, "verse": 1, "text": "A gentle answer turns away wrath, but a harsh word stirs up anger."},
    {"chapter": 16, "verse": 3, "text": "Commit to the LORD whatever you do, and he will establish your plans."},
    {"chapter": 16, "verse": 9, "text": "In their hearts humans plan their course, but the LORD establishes their steps."},
    {"chapter": 17, "verse": 22, "text": "A cheerful heart is good medicine, but a crushed spirit dries up the bones."},
    {"chapter": 18, "verse": 10, "text": "The name of the LORD is a fortified tower; the righteous run to it and are safe."},
    {"chapter": 19, "verse": 21, "text": "Many are the plans in a person’s heart, but it is the LORD’s purpose that prevails."},
    {"chapter": 22, "verse": 6, "text": "Start children off on the way they should go, and even when they are old they will not turn from it."},
    {"chapter": 27, "verse": 17, "text": "As iron sharpens iron, so one person sharpens another."},
    {"chapter": 28, "verse": 13, "text": "Whoever conceals their sins does not prosper, but the one who confesses and renounces them finds mercy."},
    {"chapter": 29, "verse": 25, "text": "Fear of man will prove to be a snare, but whoever trusts in the LORD is kept safe."}
]

@list_reports.route('/api/proverbs', methods=['GET'])
@auth_required()
def get_proverbs():
    return jsonify(proverbs)

@list_reports.route('/proverbs', methods=['GET'])
@auth_required()
def show_proverbs():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))
    start_index = (page - 1) * limit
    end_index = start_index + limit
    paginated_proverbs = proverbs[start_index:end_index]

    return render_template('bp_list_reports/show.html', proverbs=paginated_proverbs, page=page, limit=limit)