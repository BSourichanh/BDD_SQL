FROM php:8.1-fpm

# CONF PHP
RUN apt-get update && apt-get install -y zlib1g-dev libicu-dev g++ libmcrypt-dev locales libmagickwand-dev libcurl4-gnutls-dev zip unzip
RUN apt-get -y install libcurl4-openssl-dev pkg-config libssl-dev
RUN docker-php-ext-install pdo pdo_mysql intl
RUN docker-php-ext-configure intl
#RUN pecl install mongodb && docker-php-ext-enable mongodb

## NODE JS
RUN apt-get install -y curl \
  && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
  && apt-get install -y nodejs \
  && curl -L https://www.npmjs.com/install.sh | sh

# Install REDIS
#RUN pecl install redis \
#    && docker-php-ext-enable redis

# Install GIT
RUN apt-get update \
    && apt-get -y install git && apt-get install nodejs\
&& apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

#Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# LOCALES
RUN sed -i 's=# \(en_US.UTF-8\)=\1=g' /etc/locale.gen
RUN sed -i 's=# \(fr_FR.UTF-8\)=\1=g' /etc/locale.gen
RUN locale-gen
ADD /30-custom.ini /usr/local/etc/php/conf.d/app.ini

RUN mkdir -p /home/wwwroot
RUN mkdir -p /var/www/.composer
RUN mkdir -p /var/www/.npm
RUN mkdir -p /var/www/.config
RUN chown -R www-data.www-data /home/wwwroot
RUN chown -R  www-data.www-data /var/www/.composer
RUN chown -R  www-data.www-data /var/www/.npm
RUN chown -R  www-data.www-data /var/www/.config

#COPY startQuery.sh /
#RUN chmod +x /startQuery.sh
##RUN /startQuery.sh
#ENTRYPOINT ["/startQuery.sh"]
#USER www-data


WORKDIR /home/wwwroot

