# Build --no-cache
docker build . -t investor-view-backend:local

# Stop and remove existing container
docker stop investor-view-backend 2>$null
docker rm investor-view-backend 2>$null

# Create Docker network (ignore error if it already exists)
docker network create investor-view-network 2>$null

# Start backend container
docker run -d --restart always --name investor-view-backend --network investor-view-network --network-alias backend-service -p "5010:5010" investor-view-backend:local
