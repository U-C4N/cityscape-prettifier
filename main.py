from flask import Flask, render_template_string, request, jsonify
import prettymaps
from matplotlib import pyplot as plt
import io
import base64
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import osmnx as ox

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prettymaps Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="container mx-auto p-8 bg-white rounded-lg shadow-lg">
        <h1 class="text-3xl font-bold mb-6 text-center text-indigo-600">Prettymaps Generator</h1>
        {% if error %}
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span class="block sm:inline">{{ error }}</span>
        </div>
        {% endif %}
        <form method="post" autocomplete="off" class="space-y-4">
            <div class="relative">
                <label for="location" class="block text-sm font-medium text-gray-700">Location (City name or Latitude,Longitude):</label>
                <input type="text" id="location" name="location" required class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
            </div>
            
            <div>
                <label for="style" class="block text-sm font-medium text-gray-700">Map Style:</label>
                <select id="style" name="style" required class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    <option value="minimalist">Minimalist</option>
                    <option value="vintage">Vintage</option>
                    <option value="colorful">Colorful</option>
                </select>
            </div>
            
            <button type="submit" class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                Generate Map
            </button>
        </form>
        
        {% if image_data %}
        <div class="mt-8 text-center">
            <h2 class="text-2xl font-semibold mb-4">Generated Map for {{ location }}</h2>
            <img src="data:image/png;base64,{{ image_data }}" alt="Generated Map" class="mx-auto rounded-lg shadow-lg">
        </div>
        {% endif %}
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
    <script>
    $(function() {
        $("#location").autocomplete({
            source: function(request, response) {
                $.ajax({
                    url: "https://nominatim.openstreetmap.org/search",
                    dataType: "json",
                    data: {
                        q: request.term,
                        format: "json",
                        limit: 5
                    },
                    success: function(data) {
                        response($.map(data, function(item) {
                            return {
                                label: item.display_name,
                                value: item.display_name
                            }
                        }));
                    }
                });
            },
            minLength: 2,
            select: function(event, ui) {
                console.log("Selected: " + ui.item.value);
            }
        });
    });
    </script>
</body>
</html>
"""

def create_prettymaps(location, output_style):
    fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)

    styles = {
        "minimalist": {
            "background": {"fc": "#F2F4F5", "ec": "#dadbc1", "hatch": "ooo..."},
            "perimeter": {"fc": "#F2F4F5", "ec": "#000000", "lw": 5},
            "water": {"fc": "#a1e3ff", "ec": "#2F3737", "hatch": "ooo..."},
            "green": {"fc": "#D0F1BF", "ec": "#2F3737", "lw": 1},
            "forest": {"fc": "#64B96A", "ec": "#2F3737", "lw": 1},
            "building": {"palette": ["#FFC857", "#E9724C", "#C5283D"], "ec": "#2F3737", "lw": 0.5},
        },
        "vintage": {
            "background": {"fc": "#F8F6E9", "ec": "#2F3737", "hatch": "ooo..."},
            "perimeter": {"fc": "#F8F6E9", "ec": "#2F3737", "lw": 4},
            "water": {"fc": "#B6D9DE", "ec": "#2F3737", "hatch": "ooo..."},
            "green": {"fc": "#8AAB92", "ec": "#2F3737", "lw": 1},
            "forest": {"fc": "#64855E", "ec": "#2F3737", "lw": 1},
            "building": {"palette": ["#C8AE9B", "#9A8978", "#7C6A58"], "ec": "#2F3737", "lw": 0.5},
        },
        "colorful": {
            "background": {"fc": "#F9E79F", "ec": "#2F3737", "hatch": "ooo..."},
            "perimeter": {"fc": "#F9E79F", "ec": "#2F3737", "lw": 4},
            "water": {"fc": "#5DADE2", "ec": "#2F3737", "hatch": "ooo..."},
            "green": {"fc": "#ABEBC6", "ec": "#2F3737", "lw": 1},
            "forest": {"fc": "#27AE60", "ec": "#2F3737", "lw": 1},
            "building": {"palette": ["#E74C3C", "#8E44AD", "#3498DB"], "ec": "#2F3737", "lw": 0.5},
        }
    }

    style = styles.get(output_style, styles["minimalist"])

    try:
        gdf = ox.geocode_to_gdf(location)
        boundary = gdf.geometry.iloc[0]
        plot = prettymaps.plot(
            boundary,
            ax=ax,
            style=style
        )
    except:
        plot = prettymaps.plot(
            location,
            ax=ax,
            style=style
        )

    plt.title(f"Map of {location}", fontsize=16, fontweight='bold')
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
    img_buffer.seek(0)
    return img_buffer

def is_coordinates(location):
    try:
        lat, lon = map(float, location.split(','))
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except:
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form['location']
        style = request.form['style']
        
        try:
            if not is_coordinates(location):
                geolocator = Nominatim(user_agent="prettymaps_app")
                location_info = geolocator.geocode(location, exactly_one=False, limit=1)
                if not location_info:
                    raise ValueError("Location not found")
                location = location_info[0].address
            
            img_buffer = create_prettymaps(location, style)
            img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            
            return render_template_string(HTML_TEMPLATE, image_data=img_str, location=location)
        except Exception as e:
            error_message = str(e)
            return render_template_string(HTML_TEMPLATE, error=error_message)
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)