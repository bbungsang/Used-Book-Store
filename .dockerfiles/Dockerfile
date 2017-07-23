# ubuntu 에서 시작
FROM            ubuntu:16.04
# 관리자
MAINTAINER      bbungsang@gmail.com

# 현재 경로를 /srv/used-book-store 에 복사
# COPY            . /srv/used-book-store

# 해당 스크립트에서는 y/n 에 대해 대답할 수 없기 때문에 -y 옵션을 줘야한다
RUN             apt-get -y update
RUN             apt-get install -y python-pip
RUN             apt install -y git vim

##
# pyenv
##
RUN             apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
RUN             curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# working directory 변경
# WORKDIR         /srv/used-book-store

RUN             echo 'export PATH="/home/ubuntu/.pyenv/bin:$PATH"' >> ~/.bash_profile
RUN             echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
RUN             echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
RUN             . ~/.bash_profile
ENV             PATH /root/.pyenv/bin:$PATH

RUN             pyenv install 3.6.1

##
# zsh
##
RUN             apt-get -y install zsh
RUN             wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN             chsh -s /usr/bin/zsh

RUN             echo 'export PATH="/home/ubuntu/.pyenv/bin:$PATH"' >> ~/.zshrc
RUN             echo 'eval "$(pyenv init -)"' >> ~/.zshrc
RUN             echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zshrc

##
# Note : 명령어 한 줄 마다 레이어가 남는다.
##