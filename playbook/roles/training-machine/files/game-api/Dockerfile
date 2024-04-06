FROM php:8-apache

RUN apt-get update \
    && apt-get install -y libpq-dev git libyaml-dev zlib1g-dev mariadb-client libzip-dev \
    && docker-php-ext-install pdo_mysql pdo_pgsql \
    && pecl install xdebug \
    && docker-php-ext-enable xdebug

ADD php.ini /usr/local/etc/php/
ADD php-http.ini /usr/local/etc/php/conf.d/php-http.ini

#YAML
RUN pecl install yaml-2.2.2 redis

# Redis
RUN docker-php-source extract
RUN git clone https://github.com/phpredis/phpredis.git
RUN docker-php-ext-enable redis
