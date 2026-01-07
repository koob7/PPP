cd "kontener 1"
docker run -d -p 5000:8080 kontener_1
cd ../"kontener 2"
docker run -d -p 5001:8080 kontener_2
cd ../"kontener 3"
docker run -d -p 5002:8080 kontener_3
cd ../"kontener 4"
docker run -d -p 5003:8080 kontener_4
cd ..
traefik.exe --configfile=traefik-config.toml
timeout /t 10