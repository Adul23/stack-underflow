questions (not deleted): 5000
### search=deadlock (rare keyword)
rows returned: 12; execution time: 12.825 ms
```
Unique  (cost=240.86..240.93 rows=1 width=301) (actual time=12.648..12.662 rows=12 loops=1)
  Buffers: shared hit=197
  ->  Sort  (cost=240.86..240.87 rows=1 width=301) (actual time=12.647..12.649 rows=12 loops=1)
        Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
        Sort Method: quicksort  Memory: 29kB
        Buffers: shared hit=197
        ->  GroupAggregate  (cost=240.81..240.85 rows=1 width=301) (actual time=12.590..12.607 rows=12 loops=1)
              Group Key: questions_question.id, users_customuser.id
              Buffers: shared hit=197
              ->  Sort  (cost=240.81..240.82 rows=3 width=301) (actual time=12.577..12.580 rows=37 loops=1)
                    Sort Key: questions_question.id DESC, users_customuser.id
                    Sort Method: quicksort  Memory: 37kB
                    Buffers: shared hit=197
                    ->  Nested Loop Left Join  (cost=4.31..240.79 rows=3 width=301) (actual time=0.691..12.481 rows=37 loops=1)
                          Buffers: shared hit=197
                          ->  Nested Loop  (cost=0.00..226.02 rows=1 width=293) (actual time=0.647..12.152 rows=12 loops=1)
                                Join Filter: (questions_question.author_id = users_customuser.id)
                                Buffers: shared hit=137
                                ->  Seq Scan on questions_question  (cost=0.00..225.00 rows=1 width=168) (actual time=0.641..12.044 rows=12 loops=1)
                                      Filter: ((deleted_at IS NULL) AND ((upper((title)::text) ~~ '%DEADLOCK%'::text) OR (upper(description) ~~ '%DEADLOCK%'::text)))
                                      Rows Removed by Filter: 4988
                                      Buffers: shared hit=125
                                ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.002..0.002 rows=1 loops=12)
                                      Buffers: shared hit=12
                          ->  Bitmap Heap Scan on questions_question_tag  (cost=4.31..14.74 rows=3 width=16) (actual time=0.015..0.020 rows=3 loops=12)
                                Recheck Cond: (questions_question.id = question_id)
                                Heap Blocks: exact=36
                                Buffers: shared hit=60
                                ->  Bitmap Index Scan on questions_question_tag_question_id_4dda0a92  (cost=0.00..4.31 rows=3 width=0) (actual time=0.010..0.011 rows=3 loops=12)
                                      Index Cond: (question_id = questions_question.id)
                                      Buffers: shared hit=24
Planning:
  Buffers: shared hit=24
Planning Time: 0.398 ms
Execution Time: 12.825 ms
```
### search=django&tag=python (keyword + tag)
rows returned: 29; execution time: 11.723 ms
```
Unique  (cost=287.03..287.15 rows=2 width=301) (actual time=11.598..11.624 rows=29 loops=1)
  Buffers: shared hit=1950
  ->  Sort  (cost=287.03..287.03 rows=2 width=301) (actual time=11.597..11.601 rows=29 loops=1)
        Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
        Sort Method: quicksort  Memory: 33kB
        Buffers: shared hit=1950
        ->  GroupAggregate  (cost=286.98..287.02 rows=2 width=301) (actual time=11.503..11.545 rows=29 loops=1)
              Group Key: questions_question.id, users_customuser.id
              Buffers: shared hit=1950
              ->  Sort  (cost=286.98..286.98 rows=2 width=301) (actual time=11.494..11.500 rows=91 loops=1)
                    Sort Key: questions_question.id DESC, users_customuser.id
                    Sort Method: quicksort  Memory: 53kB
                    Buffers: shared hit=1950
                    ->  Nested Loop Left Join  (cost=8.62..286.97 rows=2 width=301) (actual time=0.235..11.419 rows=91 loops=1)
                          Buffers: shared hit=1950
                          ->  Nested Loop  (cost=4.31..272.20 rows=1 width=293) (actual time=0.212..11.227 rows=29 loops=1)
                                Join Filter: (questions_question.author_id = users_customuser.id)
                                Buffers: shared hit=1801
                                ->  Nested Loop  (cost=4.31..271.18 rows=1 width=168) (actual time=0.207..11.159 rows=29 loops=1)
                                      Join Filter: (t4.tag_id = t5.id)
                                      Rows Removed by Join Filter: 964
                                      Buffers: shared hit=1772
                                      ->  Nested Loop  (cost=4.31..269.30 rows=9 width=176) (actual time=0.108..10.881 rows=993 loops=1)
                                            Buffers: shared hit=1771
                                            ->  Seq Scan on questions_question  (cost=0.00..225.00 rows=3 width=168) (actual time=0.089..8.804 rows=332 loops=1)
                                                  Filter: ((deleted_at IS NULL) AND ((upper((title)::text) ~~ '%DJANGO%'::text) OR (upper(description) ~~ '%DJANGO%'::text)))
                                                  Rows Removed by Filter: 4668
                                                  Buffers: shared hit=125
                                            ->  Bitmap Heap Scan on questions_question_tag t4  (cost=4.31..14.74 rows=3 width=16) (actual time=0.003..0.004 rows=3 loops=332)
                                                  Recheck Cond: (questions_question.id = question_id)
                                                  Heap Blocks: exact=982
                                                  Buffers: shared hit=1646
                                                  ->  Bitmap Index Scan on questions_question_tag_question_id_4dda0a92  (cost=0.00..4.31 rows=3 width=0) (actual time=0.002..0.002 rows=3 loops=332)
                                                        Index Cond: (question_id = questions_question.id)
                                                        Buffers: shared hit=664
                                      ->  Materialize  (cost=0.00..1.61 rows=2 width=8) (actual time=0.000..0.000 rows=1 loops=993)
                                            Buffers: shared hit=1
                                            ->  Seq Scan on tags_tag t5  (cost=0.00..1.60 rows=2 width=8) (actual time=0.005..0.023 rows=1 loops=1)
                                                  Filter: ((upper((slug)::text) = 'PYTHON'::text) OR (upper((name)::text) = 'PYTHON'::text))
                                                  Rows Removed by Filter: 29
                                                  Buffers: shared hit=1
                                ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.000..0.000 rows=1 loops=29)
                                      Buffers: shared hit=29
                          ->  Bitmap Heap Scan on questions_question_tag  (cost=4.31..14.74 rows=3 width=16) (actual time=0.003..0.004 rows=3 loops=29)
                                Recheck Cond: (questions_question.id = question_id)
                                Heap Blocks: exact=91
                                Buffers: shared hit=149
                                ->  Bitmap Index Scan on questions_question_tag_question_id_4dda0a92  (cost=0.00..4.31 rows=3 width=0) (actual time=0.002..0.002 rows=3 loops=29)
                                      Index Cond: (question_id = questions_question.id)
                                      Buffers: shared hit=58
Planning:
  Buffers: shared hit=40
Planning Time: 0.807 ms
Execution Time: 11.723 ms
```
### tag=kubernetes (tag only)
rows returned: 476; execution time: 5.983 ms
```
Unique  (cost=996.69..1175.88 rows=2867 width=301) (actual time=5.555..5.872 rows=476 loops=1)
  Buffers: shared hit=317
  ->  Sort  (cost=996.69..1003.86 rows=2867 width=301) (actual time=5.555..5.580 rows=476 loops=1)
        Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
        Sort Method: quicksort  Memory: 173kB
        Buffers: shared hit=317
        ->  HashAggregate  (cost=803.38..832.05 rows=2867 width=301) (actual time=5.146..5.310 rows=476 loops=1)
              Group Key: questions_question.id, users_customuser.id
              Batches: 1  Memory Usage: 369kB
              Buffers: shared hit=317
              ->  Hash Right Join  (cost=457.57..781.88 rows=2867 width=301) (actual time=1.754..4.597 rows=1511 loops=1)
                    Hash Cond: (questions_question_tag.question_id = questions_question.id)
                    Buffers: shared hit=317
                    ->  Seq Scan on questions_question_tag  (cost=0.00..240.64 rows=14664 width=16) (actual time=0.005..1.059 rows=14664 loops=1)
                          Buffers: shared hit=94
                    ->  Hash  (cost=445.34..445.34 rows=978 width=293) (actual time=1.742..1.744 rows=476 loops=1)
                          Buckets: 1024  Batches: 1  Memory Usage: 157kB
                          Buffers: shared hit=223
                          ->  Nested Loop  (cost=228.58..445.34 rows=978 width=293) (actual time=0.307..1.502 rows=476 loops=1)
                                Join Filter: (questions_question.author_id = users_customuser.id)
                                Buffers: shared hit=223
                                ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.005..0.005 rows=1 loops=1)
                                      Buffers: shared hit=1
                                ->  Hash Join  (cost=228.58..432.11 rows=978 width=168) (actual time=0.300..1.422 rows=476 loops=1)
                                      Hash Cond: (questions_question.id = t4.question_id)
                                      Buffers: shared hit=222
                                      ->  Seq Scan on questions_question  (cost=0.00..175.00 rows=5000 width=168) (actual time=0.004..0.663 rows=5000 loops=1)
                                            Filter: (deleted_at IS NULL)
                                            Buffers: shared hit=125
                                      ->  Hash  (cost=216.35..216.35 rows=978 width=8) (actual time=0.291..0.292 rows=476 loops=1)
                                            Buckets: 1024  Batches: 1  Memory Usage: 27kB
                                            Buffers: shared hit=97
                                            ->  Nested Loop  (cost=8.07..216.35 rows=978 width=8) (actual time=0.044..0.233 rows=476 loops=1)
                                                  Buffers: shared hit=97
                                                  ->  Seq Scan on tags_tag t5  (cost=0.00..1.60 rows=2 width=8) (actual time=0.011..0.024 rows=1 loops=1)
                                                        Filter: ((upper((slug)::text) = 'KUBERNETES'::text) OR (upper((name)::text) = 'KUBERNETES'::text))
                                                        Rows Removed by Filter: 29
                                                        Buffers: shared hit=1
                                                  ->  Bitmap Heap Scan on questions_question_tag t4  (cost=8.07..102.49 rows=489 width=16) (actual time=0.031..0.163 rows=476 loops=1)
                                                        Recheck Cond: (tag_id = t5.id)
                                                        Heap Blocks: exact=94
                                                        Buffers: shared hit=96
                                                        ->  Bitmap Index Scan on questions_question_tag_tag_id_438f51e8  (cost=0.00..7.95 rows=489 width=0) (actual time=0.018..0.018 rows=476 loops=1)
                                                              Index Cond: (tag_id = t5.id)
                                                              Buffers: shared hit=2
Planning:
  Buffers: shared hit=40
Planning Time: 0.874 ms
Execution Time: 5.983 ms
```
### q=deadlock (legacy search box, LIMIT 50)
rows returned: 12; execution time: 36.972 ms
```
Limit  (cost=566.02..566.83 rows=13 width=301) (actual time=36.893..36.910 rows=12 loops=1)
  Buffers: shared hit=411
  ->  Unique  (cost=566.02..566.83 rows=13 width=301) (actual time=36.892..36.907 rows=12 loops=1)
        Buffers: shared hit=411
        ->  Sort  (cost=566.02..566.05 rows=13 width=301) (actual time=36.891..36.894 rows=12 loops=1)
              Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
              Sort Method: quicksort  Memory: 29kB
              Buffers: shared hit=411
              ->  GroupAggregate  (cost=565.52..565.78 rows=13 width=301) (actual time=36.845..36.880 rows=12 loops=1)
                    Group Key: questions_question.id, users_customuser.id
                    Buffers: shared hit=411
                    ->  Sort  (cost=565.52..565.55 rows=13 width=301) (actual time=36.835..36.843 rows=119 loops=1)
                          Sort Key: questions_question.id DESC, users_customuser.id
                          Sort Method: quicksort  Memory: 65kB
                          Buffers: shared hit=411
                          ->  Nested Loop Left Join  (cost=239.46..565.28 rows=13 width=301) (actual time=2.127..36.722 rows=119 loops=1)
                                Buffers: shared hit=411
                                ->  Nested Loop  (cost=239.18..563.38 rows=4 width=293) (actual time=2.114..36.498 rows=37 loops=1)
                                      Join Filter: (questions_question.author_id = users_customuser.id)
                                      Buffers: shared hit=221
                                      ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.005..0.006 rows=1 loops=1)
                                            Buffers: shared hit=1
                                      ->  Hash Right Join  (cost=239.18..562.32 rows=4 width=168) (actual time=2.107..36.476 rows=37 loops=1)
                                            Hash Cond: (t4.question_id = questions_question.id)
                                            Filter: ((upper((questions_question.title)::text) ~~ '%DEADLOCK%'::text) OR (upper(questions_question.description) ~~ '%DEADLOCK%'::text) OR (upper((t5.name)::text) ~~ '%DEADLOCK%'::text))
                                            Rows Removed by Filter: 14627
                                            Buffers: shared hit=220
                                            ->  Hash Left Join  (cost=1.68..286.25 rows=14664 width=14) (actual time=0.032..3.949 rows=14664 loops=1)
                                                  Hash Cond: (t4.tag_id = t5.id)
                                                  Buffers: shared hit=95
                                                  ->  Seq Scan on questions_question_tag t4  (cost=0.00..240.64 rows=14664 width=16) (actual time=0.005..1.138 rows=14664 loops=1)
                                                        Buffers: shared hit=94
                                                  ->  Hash  (cost=1.30..1.30 rows=30 width=14) (actual time=0.012..0.013 rows=30 loops=1)
                                                        Buckets: 1024  Batches: 1  Memory Usage: 10kB
                                                        Buffers: shared hit=1
                                                        ->  Seq Scan on tags_tag t5  (cost=0.00..1.30 rows=30 width=14) (actual time=0.004..0.007 rows=30 loops=1)
                                                              Buffers: shared hit=1
                                            ->  Hash  (cost=175.00..175.00 rows=5000 width=168) (actual time=1.149..1.149 rows=5000 loops=1)
                                                  Buckets: 8192  Batches: 1  Memory Usage: 1063kB
                                                  Buffers: shared hit=125
                                                  ->  Seq Scan on questions_question  (cost=0.00..175.00 rows=5000 width=168) (actual time=0.004..0.638 rows=5000 loops=1)
                                                        Filter: (deleted_at IS NULL)
                                                        Buffers: shared hit=125
                                ->  Index Scan using questions_question_tag_question_id_4dda0a92 on questions_question_tag  (cost=0.29..0.44 rows=3 width=16) (actual time=0.003..0.005 rows=3 loops=37)
                                      Index Cond: (question_id = questions_question.id)
                                      Buffers: shared hit=190
Planning:
  Buffers: shared hit=56
Planning Time: 0.986 ms
Execution Time: 36.972 ms
```
