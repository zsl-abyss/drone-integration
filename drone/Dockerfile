# Use this Dockefile to build an image to be used by the `launch-worker' step in
# the `.drone.yaml' file. The image needs to be tagged with:
#   325729004853.dkr.ecr.ap-southeast-2.amazonaws.com/ubuntu:22.04-for-launch-worker
# and pushed to ECR and then pulled to an instance running drone server/runner,
# so it is already available there.

FROM ubuntu:22.04
RUN apt-get update --yes
RUN apt-get install --yes \
    curl \
    jq \
    python3 \
    python3-pip \
    python3-yaml \
    unzip
RUN curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip
RUN unzip awscliv2.zip
RUN ./aws/install
