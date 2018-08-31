# Server Sent Events reflector for the DOME

Uses Docker to conjure up an SSE server with nginx.

For it to work, you will need a copy of dome.js in this directory (or a symlink)

Run `docker-compose up` to make it go - serves on port 8080 with two endpoints, `/pub` to send updates and `/sub` to receive them.
You should probably secure this....

