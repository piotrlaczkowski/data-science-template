
## Docker Cheat-sheet

Here is a list of the basic Docker commands from this page, and some related ones if you’d like to explore a bit before moving on [Docker Docs](https://docs.docker.com/get-started/part2/#recap-and-cheat-sheet-optional).

```docker
docker build -t friendlyhello .  # Create image using this directory's Dockerfile
docker run -p 4000:80 friendlyhello  # Run "friendlyname" mapping port 4000 to 80
docker run -d -p 4000:80 friendlyhello         # Same thing, but in detached mode
docker container ls                                # List all running containers
docker container ls -a             # List all containers, even those not running
docker container stop <hash>           # Gracefully stop the specified container
docker container kill <hash>         # Force shutdown of the specified container
docker container rm <hash>        # Remove specified container from this machine
docker container rm $(docker container ls -a -q)         # Remove all containers
docker image ls -a                             # List all images on this machine
docker image rm <image id>            # Remove specified image from this machine
docker image rm $(docker image ls -a -q)   # Remove all images from this machine
docker login             # Log in this CLI session using your Docker credentials
docker tag <image> username/repository:tag  # Tag <image> for upload to registry
docker push username/repository:tag            # Upload tagged image to registry
docker run username/repository:tag                   # Run image from a registry
```

and some Docker Hacks [hacks.](https://codefresh.io/docker-tutorial/everyday-hacks-docker/)

## Scheduling Dockers 

One-shot dockers description [Docker Scheduling Tuto](https://blog.alexellis.io/containers-on-swarm/)

>Description of options for scheduling a one-shot container on Docker Swarm. We'll look at some use-cases, a comparison to legacy Swarm (prior to 1.12) and then move onto some working examples of short-lived containers with Swarm Services.


and a specialized tool: [Jobs as a Service ](https://github.com/alexellis/jaas)

>This project provides a simple Golang CLI tool that binds to the Docker Swarm API to create an ad-hoc/one-shot Service and then poll until it exits. Service logs can also be retrieved if the Docker daemon API version is greater than 1.29 or if the experimental feature is enabled on the Docker daemon.