from flask import Flask, render_template, request, jsonify
import prettymaps
from matplotlib import pyplot as plt
import io
import base64
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import osmnx as ox
from functools import lru_cache

app = Flask(__name__)

# Cache geocoding results to improve performance
@lru_cache(maxsize=100)
def geocode_location(location):
  geolocator = Nominatim(user_agent="prettymaps_app")
  return geolocator.geocode(location, exactly_one=True)

HTML_TEMPLATE = "templates/index.html"

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
      prettymaps.plot(boundary, ax=ax, style=style)
  except (GeocoderTimedOut, GeocoderUnavailable):
      raise
  except Exception as e:
      raise ValueError(f"Error generating map: {e}")

  plt.title(f"Map of {location}", fontsize=16, fontweight='bold')

  img_buffer = io.BytesIO()
  plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
  plt.close(fig)
  img_buffer.seek(0)
  return img_buffer

def is_coordinates(location):
  try:
      lat, lon = map(float, location.split(','))
      return -90 <= lat <= 90 and -180 <= lon <= 180
  except ValueError:
      return False

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
      location = request.form.get('location', '').strip()
      style = request.form.get('style', 'minimalist').strip().lower()

      if not location:
          return render_template(HTML_TEMPLATE, error="Location is required.")

      try:
          if not is_coordinates(location):
              geocoded = geocode_location(location)
              if not geocoded:
                  raise ValueError("Location not found.")
              location = geocoded.address

          img_buffer = create_prettymaps(location, style)
          img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

          return render_template(HTML_TEMPLATE, image_data=img_str, location=location)
      except (GeocoderTimedOut, GeocoderUnavailable):
          error_message = "Geocoding service is currently unavailable. Please try again later."
          return render_template(HTML_TEMPLATE, error=error_message)
      except ValueError as ve:
          return render_template(HTML_TEMPLATE, error=str(ve))
      except Exception as e:
          error_message = f"An unexpected error occurred: {e}"
          return render_template(HTML_TEMPLATE, error=error_message)

  return render_template(HTML_TEMPLATE)

if __name__ == '__main__':
  app.run(debug=True)
