import gradio as gr
import json

# Load your data
with open('scraped_data.json', 'r') as f:
    data = json.load(f)

# HTML template for displaying cards
def card_html(entry):
    points_or_type = entry.get("Points", entry.get("Type", "N/A"))  # Fallback to "N/A" if neither is present
    return f"""
    <div class='card' onclick='showDetails("{entry['Title'].replace('"', "&quot;")}", "{entry['Details'].replace('"', "&quot;")}", "{points_or_type}", "{entry['URL']}", "{entry['Source']}")'>
        <h2>{entry['Title']}</h2>
        <p>{points_or_type}</p>
    </div>
    """

# Convert all entries to HTML cards
cards = ''.join([card_html(entry) for entry in data])

# Custom CSS for the webpage
css = """
body { background-color: #000; font-family: 'Montserrat', sans-serif; color: white; }
.card { background-color: #333; padding: 20px; margin-bottom: 10px; cursor: pointer; border-radius: 8px; transition: transform 0.3s ease; }
.card:hover { transform: scale(1.05); }
.card h2, .card p { margin: 0; }
.modal { display: none; position: fixed; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.8); }
.modal-content { margin: 10% auto; padding: 20px; width: 50%; background-color: #222; border-radius: 10px; }
.close { float: right; font-size: 28px; font-weight: bold; color: #fff; }
.close:hover, .close:focus { color: #f00; cursor: pointer; }
"""

# Custom JavaScript for interactive behavior
js = """
function showDetails(title, details, points_or_type, url, source) {
    document.getElementById('title').textContent = title;
    document.getElementById('details').textContent = details;
    document.getElementById('points_or_type').textContent = points_or_type;
    document.getElementById('url').textContent = url;
    document.getElementById('source').textContent = source;
    document.getElementById('details_modal').style.display = 'block';
}
window.onclick = function(event) {
    if (event.target == document.getElementById('details_modal')) {
        document.getElementById('details_modal').style.display = 'none';
    }
}
"""

with gr.Blocks(css=css, js=js) as app:
    gr.Markdown(cards)
    gr.HTML("""
        <div id="details_modal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="document.getElementById('details_modal').style.display='none'">&times;</span>
                <h1 id="title"></h1>
                <p id="details"></p>
                <p id="points_or_type"></p>
                <p id="url"></p>
                <p id="source"></p>
            </div>
        </div>
    """)

app.launch()
