# This is the development environment
# FROM athackst/ros2:dashing-dev 

# COPY install_depends.sh /setup/install_depends.sh
# RUN /setup/install_depends.sh && rm -rf /var/lib/apt/lists/*

# # This Dockerfile adds a non-root 'vscode' user with sudo access. However, for Linux,
# # this user's GID/UID must match your local user UID/GID to avoid permission issues
# # with bind mounts. Update USER_UID / USER_GID if yours is not 1000. See
# # https://aka.ms/vscode-remote/containers/non-root-user for details.
# ARG USERNAME=vscode
# ARG USER_UID=1000
# ARG USER_GID=$USER_UID

# # Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
# RUN groupadd --gid $USER_GID $USERNAME \
#     && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
#     # [Optional] Add sudo support for the non-root user
#     && apt-get update \
#     && apt-get install -y sudo \
#     && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
#     && chmod 0440 /etc/sudoers.d/$USERNAME \
#     # Cleanup
#     && rm -rf /var/lib/apt/lists/*

# COPY entrypoint.sh /setup/entrypoint.sh
# ENTRYPOINT [ "/setup/entrypoint.sh" ]


FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
        apt-get -y upgrade && \
        apt-get -y install apt-utils locales && \
        rm -rf /var/lib/apt/lists/*


RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN apt-get update && \
        apt-get -y upgrade  && \
        apt-get -y install lsb-release bash-completion git cron  \
        sudo vim nano net-tools curl gdb gdbserver gnupg2 && \
        rm -rf /var/lib/apt/lists/*


# Installing Ros:Dashing
ENV ROS_DISTRO=dashing
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN sh -c 'echo "deb [arch=amd64,arm64] http://packages.ros.org/ros2/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros2-latest.list'

RUN apt-get update && \
        apt-get -y install python3-colcon-common-extensions python3-argcomplete \
        ros-$ROS_DISTRO-ros-base ros-$ROS_DISTRO-rclcpp-components ros-$ROS_DISTRO-ros2component \
        ros-$ROS_DISTRO-rosbag2 ros-$ROS_DISTRO-rosbag2-storage-default-plugins ros-$ROS_DISTRO-ros2bag ros-$ROS_DISTRO-launch*  \
        ros-$ROS_DISTRO-cv-bridge ros-$ROS_DISTRO-librealsense2 ros-$ROS_DISTRO-message-filters ros-$ROS_DISTRO-image-transport && \
        rm -rf /var/lib/apt/lists/*



# Installing OpenCV 4.1.1
RUN apt-get update && \
        apt-get -y upgrade && \
        apt-get install -y build-essential cmake \
        qt5-default libvtk6-dev \
        zlib1g-dev libjpeg-dev libwebp-dev libpng-dev libtiff5-dev libopenexr-dev libgdal-dev \
        libdc1394-22-dev libavcodec-dev libavformat-dev libswscale-dev libtheora-dev libvorbis-dev  \
        libxvidcore-dev libx264-dev yasm libopencore-amrnb-dev libopencore-amrwb-dev \
        libv4l-dev libxine2-dev libtbb-dev libeigen3-dev \
        python3-dev python3-tk python3-numpy locate \
        python-dev python-tk python-numpy locate \
        ant default-jdk \
        unzip wget && \
        wget https://github.com/opencv/opencv/archive/4.1.1.zip  && \
        unzip 4.1.1.zip && \
        rm 4.1.1.zip && \
        mv opencv-4.1.1 OpenCV && \
        cd OpenCV \
        && mkdir build \
        && cd build \
        && cmake -DWITH_QT=ON -DWITH_OPENGL=ON -DFORCE_VTK=ON -DWITH_TBB=ON -DWITH_GDAL=ON -DWITH_XINE=ON -DBUILD_EXAMPLES=ON -DENABLE_PRECOMPILED_HEADERS=OFF .. \
        && make -j4 \
        && make install \
        && ldconfig \
        &&  apt install libopencv-dev -y && \
        rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get -y install ros-dashing-rmw-opensplice-cpp && \
    rm -rf /var/lib/apt/lists/*
ENV RMW_IMPLEMENTATION=rmw_opensplice_cpp
ENV OSPL_URI=file:///module/ospl.xml

Installing Tensorflow & pytorch
RUN apt-get update && \
        apt-get install -y python3-pip && \
        pip3 install --upgrade pip && \
        python3 -m pip install pandas && \
        python3 -m pip install  --no-cache-dir tensorflow-gpu==1.14.0 && \
        python3 -m pip  install torch==1.2.0 torchvision==0.4.0 -f https://download.pytorch.org/whl/torch_stable.html  && \
        rm -rf /var/lib/apt/lists/*


ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID



# ARG WDIR=/module
# ARG UNAME=haval
# ARG HOST_UID=1000
# ARG HOST_GID=1000


# RUN groupadd -g $HOST_GID -o $UNAME
# RUN useradd -m -u $HOST_UID -g $HOST_GID -o -s /bin/bash $UNAME

# USER $UNAME

# RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
# # source module install on start (this only works if the module is built)
# RUN echo "source $WDIR/install/setup.bash" >> ~/.bashrc

# # EXPOSE 2000
# WORKDIR $WDIR

ENV ROS_DOMAIN_ID=0

CMD ["/bin/bash"]

# ensures unique image/container
ENV MODULE_NAME=perception