FROM perl:5.30.2

#RUN apt update \
# && apt -y clean \
# && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/app

WORKDIR /home/app

ENV PATH /home/app/local/bin:${PATH}
ENV PERL5LIB /home/app/local/lib/perl5:${PATH}

ADD ./app/cpanfile /home/app/cpanfile

RUN cpanm Carton \
    && carton install

ADD ./app/api-debug.pl /home/app/api-debug.pl

CMD [ "hypnotoad", "-f", "./api-debug.pl" ]

