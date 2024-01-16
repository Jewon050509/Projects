from website import create_app

# create_app() from __init__.py
app = create_app()

# Check if running as the main script
if __name__ == '__main__':
    app.run(debug=False)