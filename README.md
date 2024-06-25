# Prettymaps Generator

Prettymaps Generator is a web application that creates stylized maps of cities and locations using OpenStreetMap data. Built on the Python Flask framework, this application utilizes the Prettymaps library to produce visually appealing maps.

![Prettymaps Generator Screenshot](screenshot.png)

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
   git clone https://github.com/yourusername/prettymaps-generator.git
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

## Contributing

We welcome contributions! To contribute:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

Your Name - [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/yourusername/prettymaps-generator](https://github.com/yourusername/prettymaps-generator)

## Acknowledgments

- [Prettymaps](https://github.com/marceloprates/prettymaps) - Map generation library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [OpenStreetMap](https://www.openstreetmap.org/) - Map data
- [Tailwind CSS](https://tailwindcss.com/) - CSS framework
