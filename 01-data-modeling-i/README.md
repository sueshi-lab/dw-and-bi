# 1. Running Docker
```
cd 01-data-modeling-i
docker-compose up
```

# 2. Creating tables and ETL
```
pip install psycopg2

cd 01-data-modeling-i
python create-tables.py
python etl.py
```

# 3. How about data model?
5 tables: actors, repos, orgs, events and event_types

## actors
| name | type | note |
| :---- | :---- | :---- |
| id | int | PK |
| login | text |  |
| display_login | text |  |
| url | text |  |
| avatar_url | text |  |

* เนื่องจาก gravatar_id เป็น empty string ทั้งหมด จึงนำออก

## repos
| name | type | note |
| :---- | :---- | :---- |
| id | int | PK |
| name | text |  |
| url | text |  |

## orgs
| name | type | note |
| :---- | :---- | :---- |
| id | int | PK |
| login | text |  |
| url | text |  |
| avatar_url | text |  |

* เนื่องจาก gravatar_id เป็น empty string ทั้งหมด จึงนำออก

## events
| name | type | note |
| :---- | :---- | :---- |
| id | bigint | PK |
| created_at | timestamp |  |
| type_id | int | FK |
| actor_id | int | FK |
| repo_id | int | FK |
| org_id | int | FK |

* มี id บางตัวที่เกินขอบเขตของ int จึงเลือกใช้ bigint ที่ขนาดใหญ่กว่าแทน
* public เป็น true เสมอ จึงนำออก

## event_types
| name | type | note |
| :---- | :---- | :---- |
| id | int | PK |
| name | text |  |

* เนื่องจากชื่อ type มีความซ้ำซ้อนในตาราง event จึงขอแยกออกมาเป็นอีกตารางค่ะ
* มีทั้งหมด 11 types ในชุดข้อมูล ได้แก่
    * IssueCommentEvent
    * PushEvent
    * CreateEvent
    * IssuesEvent
    * ReleaseEvent
    * DeleteEvent
    * PublicEvent
    * WatchEvent
    * PullRequestReviewEvent
    * PullRequestReviewCommentEvent
    * PullRequestEvent