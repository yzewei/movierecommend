from django.db import models


# Create your models here.


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class CbLikesSimilar(models.Model):
    uid = models.CharField(max_length=20, blank=True, null=True)
    mid = models.CharField(max_length=20, blank=True, null=True)
    similar = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cb_likes_similar'


class CbTagSimilar(models.Model):
    uid = models.CharField(max_length=20, blank=True, null=True)
    mid = models.CharField(max_length=20, blank=True, null=True)
    similar = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cb_tag_similar'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ManagerInfo(models.Model):
    manager_id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'manager_info'


class MoviesDetail(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    english_name = models.CharField(max_length=255, blank=True, null=True)
    directors = models.CharField(max_length=255, blank=True, null=True)
    writer = models.CharField(max_length=255, blank=True, null=True)
    actors = models.CharField(max_length=255, blank=True, null=True)
    rate = models.CharField(max_length=255, blank=True, null=True)
    style1 = models.CharField(max_length=255, blank=True, null=True)
    style2 = models.CharField(max_length=255, blank=True, null=True)
    style3 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    dataid = models.CharField(db_column='dataID', primary_key=True, max_length=255)  # Field name made lowercase.
    url = models.TextField(blank=True, null=True)
    pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies_detail'


class UserInfo(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    likes = models.TextField(blank=True, null=True)
    # db_column='createDate', blank=True, null=True
    createdate = models.DateTimeField()  # Field name made lowercase.
    updatedate = models.DateTimeField()  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_info'


class UserMovieCollect(models.Model):
    uid = models.CharField(max_length=20, blank=True, null=True)
    mid = models.CharField(max_length=20, blank=True, null=True)
    updatedate = models.DateTimeField(db_column='updateDate', blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_movie_collect'


class UserMovieScore(models.Model):
    uid = models.CharField(max_length=20, blank=True, null=True)
    mid = models.CharField(max_length=20, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    createdate = models.DateTimeField(db_column='createDate', blank=True, null=True)  # Field name made lowercase.
    updatedate = models.DateTimeField(db_column='updateDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_movie_score'


class WebUserLoginInfo(models.Model):
    uid = models.CharField(max_length=20)
    date = models.DateTimeField()
    ip = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'web_user_login_info'


class MaxDateMovie(models.Model):
    dataid = models.CharField(db_column='dataID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'max_date_movie'


class MaxRateMovie(models.Model):
    dataid = models.CharField(db_column='dataID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    rate = models.CharField(max_length=255, blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'max_rate_movie'
