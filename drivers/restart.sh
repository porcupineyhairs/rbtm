docker stop drivers_server_1 experiment_server_1 &&  docker rm drivers_server_1 experiment_server_1 && cd ~/rbtm/drivers && docker-compose up -d &&  sleep 5 && cd ~/rbtm/experiment && docker-compose up -d