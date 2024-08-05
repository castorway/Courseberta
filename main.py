from website import create_app

# make the web app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # run the web app and update on every save
