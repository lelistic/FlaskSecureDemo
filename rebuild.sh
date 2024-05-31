docker compose -f docker-compose.dev.yml down
docker rmi -f lelis-web
docker compose -f docker-compose.dev.yml up -d --build
docker compose -f docker-compose.dev.yml logs
