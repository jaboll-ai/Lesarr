
<p align="center">
  <img src="frontend/public/assets/lesarr.svg" alt="Lesarr Logo" width="200"/>
</p>

> [!WARNING]
> Doesn't work behind a VPN... yet.. maybe soon(tm). The scraping sometimes, repeatedly fails... just try again until it works. 

> [!CAUTION]
> This project is really experimental and might not work/break something on your system. There will be dragons!

> [!NOTE]  
> I know the CSS sucks. I know there is no download all button for an author yet. Shoot me a PR tho :)

# Lesarr

Lesarr is a FastAPI-based application for scraping book metadata from Thalia.de, managing authors, series, and editions in a SQLite database via SQLModel, and integrating NZB downloading through SABnzbd. It follows a somewhat clean architecture, so if you are interested in contributing, please do so! 

## Features

- **Web Scraping**  
  Fetch book editions, author information, and search results using BeautifulSoup and playwright yourself. Because german metadata for books sucks.
- **RESTful API**  
  Routes organized into `tapi`, `api`, and `nzbapi` for scraping, middleware imports, database access, and NZB handling.
- **Database Integration**  
  SQLite database powered by SQLModel, with automatic table creation and session management.
- **NZB Downloading**  
  Indexer and downloader services integrated with SABnzbd's API to search and queue downloads. If you want other downloaders, write the bridge yourself :)
- **File Management**  
  Background polling of finished downloads, moving files into organized folders by `author/series/book` structure. Following ABS schemes by default. Currently no custimization options

## Getting Started

**RECOMMENDED: Docker Compose**  
   Uncomment and adjust volume mounts as needed in `docker-compose.yml`:
   ```yaml
    version: '3.8'
    services:
    lesarr:
        container_name: lesarr
        build: https://github.com/jaboll-ai/Lesarr.git#main
        image: lesarr
        ports:
        - "8000:8000"
        # volumes:
        # - <on-host-config>:/config
        # - <on-host-data>:/data
  ```
**ALTERNATIVE: Run the application locally (please don't)** 
1. **Build the frontend assets**  
   ```bash
   cd frontend && npm install && npm run build && cd ..
   ```
   **Optional: Build the Docker image**  
   ```bash
   docker build . -t lesarr
   ```
 2. **Start**
    ```bash
    pip install -r requirements.txt
    python entry.py
    ```

## Contributing

Again, contributions are welcome! Please open issues and submit pull requests.

## License

This project is licensed under the MIT License.
