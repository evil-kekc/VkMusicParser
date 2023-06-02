## VK Music Parser

VK Music Parser is a Python script that retrieves all audio recordings from all playlists on a VK page and writes them
to text files.

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/evil-kekc/VkMusicParser
    ```
2. Install the required dependencies:

   ```shell
   pip install vk_api dotenv
   ```

3. Set up your VK credentials:

    * Create a new file named `.env` in the project directory.

    * Open the .env file and add the following lines, replacing `<your-login>` and `<your-password>` with your VK login
      and
      password:

   ```plaintext
   LOGIN=<your-login>
   PASSWORD=<your-password>
   ```

## Usage

1. Run the VkMusicParser script to retrieve audio recordings from playlists:

   ```shell
   python VkMusicParser.py

The script will authenticate with VK using the provided login and password from the `.env` file. It will then retrieve
the
playlists and save the audio recordings to text files in the data directory. Each playlist will have a separate text
file with the name of the playlist.

## Logging

The script logs its actions and any errors to a log file located at `logs/parser.log`. You can check this file for
information about the script's execution and any encountered issues.

Please note that this script is for educational purposes only. Use it responsibly and respect the terms of service of
the VK platform.