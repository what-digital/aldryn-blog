CHANGELOG
=========

0.4.7 (2019-03-17)
------------------

* add support for django 1.7
* moved migrations to 'south_migrations' folder django<1.7
* make one native migration for django>=1.7
* fix 'get_query_set' method
* add fields = '__all__' for PostForm