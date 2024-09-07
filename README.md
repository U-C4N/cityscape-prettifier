# Prettymaps Generator

Prettymaps Generator is a web application that creates stylized maps of cities and locations using OpenStreetMap data. Built on the Python Flask framework, this application utilizes the Prettymaps library to produce visually appealing maps.

![Prettymaps Generator Screenshot](readme.jpg)

## Features

- Generate maps by entering city names or coordinates
- Easy location search with autocomplete functionality
- Three different map styles: Minimalist, Vintage, and Colorful
- Wide-area maps showing the entire city
- Modern and user-friendly interface

## Installation

Follow these steps to run the project on your local machine:

1. Clone the repository:
   ```
   git clone https://github.com/U-C4N/prettymaps-generator.git
   cd prettymaps-generator
   ```

2. Create and activate a virtual Python environment:
   ```
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000/` to start using the application.

## Usage

1. On the main page, enter the name of the city or coordinates for which you want to create a map.
2. You can select one of the suggested locations using the autocomplete feature.
3. Choose a map style (Minimalist, Vintage, or Colorful).
4. Click the "Generate Map" button.
5. The generated map will be displayed at the bottom of the page.


## Acknowledgments

- [Prettymaps](https://github.com/marceloprates/prettymaps) - Map generation library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [OpenStreetMap](https://www.openstreetmap.org/) - Map data
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework

## Author

<p align="left">
<b>Umutcan Edizaslan:</b>
<a href="https://github.com/U-C4N" target="blank"><img align="center" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Github-Dark.svg" alt="TutTrue" height="30" width="40" /></a>
<a href="https://x.com/UEdizaslan" target="blank"><img align="center" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Twitter.svg" height="30" width="40" /></a>
<a href="https://discord.gg/2Tutcj6u" target="blank"><img align="center" src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Discord.svg" height="30" width="40" /></a>
</p>
