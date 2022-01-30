<div align="center">

  <h3 align="center">Youtube Trim and Download</h3>

  <p align="center">
    Web app to trim and download Youtube Videos. Using Flask, Celery, Redis and Docker.
  </p>
</div>

### Live Demo
https://youtube-trim-dl.herokuapp.com/

## About The Project

You can trim and download Youtube Videos via app's frontend.

Trimming tasks are queued through Celery and Redis. Once the task is complete and the file is ready for download, download button becomes enabled.

Rate limited by ip address. There can only be one active task per ip.

### Run project with Docker

- ```sh
  docker-compose up --build
  ```

### Run project on localhost (Redis server required)

1. Clone the repo
    ```sh
    git clone https://github.com/martymfly/youtube-trim-download
    ````

    ```sh
    cd youtube-trim-download
    ```

2. Create virtual environment and activate

   Windows

   ```sh
   python -m venv venv
   cd venv & cd scripts & activate
   ```

   Linux

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python packages with pip and requirements.txt

   Windows

   ```sh
   pip install -r requirements.txt
   ```

   Linux

   ```sh
   pip3 install -r requirements.txt
   ```

4. Run Flask app within app root folder
   ```sh
   python app.py
   ```
5. Run worker from worker folder
   ```sh
   celery -A tasks worker --pool=solo -l info
   ```
6. Run Flower - Celery monitoring tool from worker folder
   ```sh
   celery -A tasks flower
   ```

### Deploy to Heroku

1. Install Heroku Redis add-on

2. Add ffmpeg build pack in Settings > Buildpacks - **https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git**

3. Add below environment variables in Settings > Config Vars

   - **ON_HEROKU** = 1
   - **UPLOAD_SECRET_KEY** = your_secret_key_change_this
   - **UPLOAD_URL** = https://**your-heroku-app-name**.herokuapp.com/uploadfromworker

4. Run below command on heroku-cli
   ```sh
   heroku ps:scale worker=1
   ```

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request.

You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
