# Generated by Django 3.2 on 2021-04-13 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("member", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("begin_time", models.DateTimeField(verbose_name="开始时间")),
                ("end_time", models.DateTimeField(verbose_name="结束时间")),
                ("description", models.TextField(max_length=200, verbose_name="简介")),
                ("content", models.TextField(verbose_name="介绍")),
                ("address", models.TextField(verbose_name="活动地点")),
                (
                    "poster",
                    models.CharField(
                        blank=True,
                        default="/media/upload/null-event-1.jpg",
                        max_length=255,
                        verbose_name="招贴画",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="名称")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("total_votes", models.PositiveIntegerField(default=0)),
                (
                    "total_favourites",
                    models.PositiveIntegerField(default=0, editable=False),
                ),
                (
                    "appearances",
                    models.ManyToManyField(
                        related_name="arrived_event", to="member.Member"
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="event_last_modified",
                        to="member.member",
                    ),
                ),
                (
                    "participants",
                    models.ManyToManyField(
                        related_name="joined_event", to="member.Member"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.FloatField(default=0, verbose_name="评分")),
                ("object_id", models.PositiveIntegerField()),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建日期"),
                ),
                ("item_raw", models.TextField(blank=True, verbose_name="item raw")),
                ("user_raw", models.TextField(blank=True, verbose_name="user raw")),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to={"model__in": ("topic", "event", "comment")},
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="vote_created",
                        to="member.member",
                        verbose_name="用户",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Topic",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(max_length=200, verbose_name="简介")),
                ("content", models.TextField(blank=True, verbose_name="内容")),
                ("html", models.TextField(blank=True, null=True, verbose_name="HTML")),
                ("content_type", models.CharField(default="html", max_length=30)),
                ("accepted", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255, verbose_name="名称")),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("total_votes", models.PositiveIntegerField(default=0)),
                (
                    "total_favourites",
                    models.PositiveIntegerField(default=0, editable=False),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="topic_created",
                        to="member.member",
                        verbose_name="演讲者",
                    ),
                ),
                (
                    "in_event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="topic_shown_in",
                        to="core.event",
                        verbose_name="已安排在此活动中",
                    ),
                ),
                (
                    "last_modified_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="topic_last_modified",
                        to="member.member",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="内容")),
                (
                    "content_type",
                    models.CharField(
                        default="html", max_length=80, verbose_name="内容格式"
                    ),
                ),
                ("title", models.CharField(max_length=512, verbose_name="标题")),
                ("summary", models.TextField(blank=True, verbose_name="摘要")),
                ("status", models.IntegerField(default=0)),
                (
                    "post_name",
                    models.CharField(
                        blank=True, max_length=256, verbose_name="短名称(引用url)"
                    ),
                ),
                (
                    "to_ping",
                    models.CharField(blank=True, max_length=512, verbose_name="Ping文章"),
                ),
                ("created_at", models.DateTimeField(verbose_name="创建时间")),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新时间"),
                ),
                (
                    "guid",
                    models.CharField(
                        blank=True, max_length=512, verbose_name="Canonical网址"
                    ),
                ),
                ("author", models.CharField(max_length=256, verbose_name="发表人")),
                ("comment_count", models.IntegerField(default=0, verbose_name="评论数量")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="post_created",
                        to="member.member",
                        verbose_name="创建人",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建日期"),
                ),
                ("item_raw", models.TextField(blank=True, verbose_name="item raw")),
                ("user_raw", models.TextField(blank=True, verbose_name="user raw")),
                (
                    "content_type",
                    models.ForeignKey(
                        limit_choices_to={"model__in": ("topic", "event", "comment")},
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="favourites",
                        to="member.member",
                        verbose_name="用户",
                    ),
                ),
            ],
        ),
    ]
