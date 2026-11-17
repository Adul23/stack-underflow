questions (not deleted): 5000
### search=deadlock (rare keyword)
rows returned: 12; execution time: 0.512 ms
```
Unique  (cost=276.44..277.00 rows=9 width=301) (actual time=0.373..0.401 rows=12 loops=1)
  Buffers: shared hit=99
  ->  Sort  (cost=276.44..276.46 rows=9 width=301) (actual time=0.373..0.376 rows=12 loops=1)
        Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
        Sort Method: quicksort  Memory: 29kB
        Buffers: shared hit=99
        ->  GroupAggregate  (cost=275.95..276.30 rows=9 width=301) (actual time=0.317..0.353 rows=12 loops=1)
              Group Key: questions_question.id, users_customuser.id
              Buffers: shared hit=99
              ->  Sort  (cost=275.95..276.01 rows=26 width=301) (actual time=0.310..0.315 rows=37 loops=1)
                    Sort Key: questions_question.id DESC, users_customuser.id
                    Sort Method: quicksort  Memory: 37kB
                    Buffers: shared hit=99
                    ->  Nested Loop Left Join  (cost=116.68..275.34 rows=26 width=301) (actual time=0.079..0.276 rows=37 loops=1)
                          Buffers: shared hit=99
                          ->  Nested Loop  (cost=112.37..142.43 rows=9 width=293) (actual time=0.067..0.145 rows=12 loops=1)
                                Join Filter: (users_customuser.id = questions_question.author_id)
                                Buffers: shared hit=39
                                ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.004..0.005 rows=1 loops=1)
                                      Buffers: shared hit=1
                                ->  Bitmap Heap Scan on questions_question  (cost=112.37..141.30 rows=9 width=168) (actual time=0.058..0.127 rows=12 loops=1)
                                      Recheck Cond: ((upper((title)::text) ~~ '%DEADLOCK%'::text) OR (upper(description) ~~ '%DEADLOCK%'::text))
                                      Filter: (deleted_at IS NULL)
                                      Heap Blocks: exact=12
                                      Buffers: shared hit=38
                                      ->  BitmapOr  (cost=112.37..112.37 rows=9 width=0) (actual time=0.047..0.048 rows=0 loops=1)
                                            Buffers: shared hit=26
                                            ->  Bitmap Index Scan on question_title_trgm_idx  (cost=0.00..56.16 rows=1 width=0) (actual time=0.020..0.020 rows=0 loops=1)
                                                  Index Cond: (upper((title)::text) ~~ '%DEADLOCK%'::text)
                                                  Buffers: shared hit=13
                                            ->  Bitmap Index Scan on question_description_trgm_idx  (cost=0.00..56.20 rows=8 width=0) (actual time=0.027..0.027 rows=12 loops=1)
                                                  Index Cond: (upper(description) ~~ '%DEADLOCK%'::text)
                                                  Buffers: shared hit=13
                          ->  Bitmap Heap Scan on questions_question_tag  (cost=4.31..14.74 rows=3 width=16) (actual time=0.005..0.007 rows=3 loops=12)
                                Recheck Cond: (questions_question.id = question_id)
                                Heap Blocks: exact=36
                                Buffers: shared hit=60
                                ->  Bitmap Index Scan on questions_question_tag_question_id_4dda0a92  (cost=0.00..4.31 rows=3 width=0) (actual time=0.003..0.003 rows=3 loops=12)
                                      Index Cond: (question_id = questions_question.id)
                                      Buffers: shared hit=24
Planning:
  Buffers: shared hit=26
Planning Time: 0.790 ms
Execution Time: 0.512 ms
```
### search=django&tag=python (keyword + tag)
rows returned: 29; execution time: 1.505 ms
```
Unique  (cost=564.40..571.77 rows=118 width=301) (actual time=1.388..1.414 rows=29 loops=1)
  Buffers: shared hit=378
  ->  Sort  (cost=564.40..564.69 rows=118 width=301) (actual time=1.388..1.392 rows=29 loops=1)
        Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
        Sort Method: quicksort  Memory: 33kB
        Buffers: shared hit=378
        ->  GroupAggregate  (cost=557.98..560.34 rows=118 width=301) (actual time=1.256..1.312 rows=29 loops=1)
              Group Key: questions_question.id, users_customuser.id
              Buffers: shared hit=378
              ->  Sort  (cost=557.98..558.27 rows=118 width=301) (actual time=1.250..1.257 rows=91 loops=1)
                    Sort Key: questions_question.id DESC, users_customuser.id
                    Sort Method: quicksort  Memory: 53kB
                    Buffers: shared hit=378
                    ->  Nested Loop Left Join  (cost=223.60..553.92 rows=118 width=301) (actual time=0.749..1.173 rows=91 loops=1)
                          Buffers: shared hit=378
                          ->  Nested Loop  (cost=223.31..435.41 rows=40 width=293) (actual time=0.734..1.037 rows=29 loops=1)
                                Buffers: shared hit=229
                                ->  Hash Join  (cost=223.18..434.02 rows=40 width=168) (actual time=0.713..0.998 rows=29 loops=1)
                                      Hash Cond: (t4.question_id = questions_question.id)
                                      Buffers: shared hit=227
                                      ->  Nested Loop  (cost=8.07..216.35 rows=978 width=8) (actual time=0.051..0.271 rows=509 loops=1)
                                            Buffers: shared hit=96
                                            ->  Seq Scan on tags_tag t5  (cost=0.00..1.60 rows=2 width=8) (actual time=0.007..0.026 rows=1 loops=1)
                                                  Filter: ((upper((slug)::text) = 'PYTHON'::text) OR (upper((name)::text) = 'PYTHON'::text))
                                                  Rows Removed by Filter: 29
                                                  Buffers: shared hit=1
                                            ->  Bitmap Heap Scan on questions_question_tag t4  (cost=8.07..102.49 rows=489 width=16) (actual time=0.041..0.178 rows=509 loops=1)
                                                  Recheck Cond: (tag_id = t5.id)
                                                  Heap Blocks: exact=93
                                                  Buffers: shared hit=95
                                                  ->  Bitmap Index Scan on questions_question_tag_tag_id_438f51e8  (cost=0.00..7.95 rows=489 width=0) (actual time=0.028..0.028 rows=509 loops=1)
                                                        Index Cond: (tag_id = t5.id)
                                                        Buffers: shared hit=2
                                      ->  Hash  (cost=212.54..212.54 rows=205 width=168) (actual time=0.650..0.651 rows=332 loops=1)
                                            Buckets: 1024  Batches: 1  Memory Usage: 75kB
                                            Buffers: shared hit=131
                                            ->  Bitmap Heap Scan on questions_question  (cost=78.76..212.54 rows=205 width=168) (actual time=0.125..0.568 rows=332 loops=1)
                                                  Recheck Cond: ((upper((title)::text) ~~ '%DJANGO%'::text) OR (upper(description) ~~ '%DJANGO%'::text))
                                                  Filter: (deleted_at IS NULL)
                                                  Heap Blocks: exact=113
                                                  Buffers: shared hit=131
                                                  ->  BitmapOr  (cost=78.76..78.76 rows=205 width=0) (actual time=0.111..0.111 rows=0 loops=1)
                                                        Buffers: shared hit=18
                                                        ->  Bitmap Index Scan on question_title_trgm_idx  (cost=0.00..39.84 rows=205 width=0) (actual time=0.103..0.103 rows=332 loops=1)
                                                              Index Cond: (upper((title)::text) ~~ '%DJANGO%'::text)
                                                              Buffers: shared hit=9
                                                        ->  Bitmap Index Scan on question_description_trgm_idx  (cost=0.00..38.82 rows=1 width=0) (actual time=0.007..0.007 rows=0 loops=1)
                                                              Index Cond: (upper(description) ~~ '%DJANGO%'::text)
                                                              Buffers: shared hit=9
                                ->  Memoize  (cost=0.14..0.21 rows=1 width=125) (actual time=0.001..0.001 rows=1 loops=29)
                                      Cache Key: questions_question.author_id
                                      Cache Mode: logical
                                      Hits: 28  Misses: 1  Evictions: 0  Overflows: 0  Memory Usage: 1kB
                                      Buffers: shared hit=2
                                      ->  Index Scan using users_customuser_pkey on users_customuser  (cost=0.12..0.20 rows=1 width=125) (actual time=0.014..0.014 rows=1 loops=1)
                                            Index Cond: (id = questions_question.author_id)
                                            Buffers: shared hit=2
                          ->  Index Scan using questions_question_tag_question_id_4dda0a92 on questions_question_tag  (cost=0.29..2.93 rows=3 width=16) (actual time=0.003..0.004 rows=3 loops=29)
                                Index Cond: (question_id = questions_question.id)
                                Buffers: shared hit=149
Planning:
  Buffers: shared hit=42
Planning Time: 0.971 ms
Execution Time: 1.505 ms
```
### tag=kubernetes (tag only)
rows returned: 476; execution time: 5.945 ms
```
Unique  (cost=996.69..1175.88 rows=2867 width=301) (actual time=5.540..5.859 rows=476 loops=1)
  Buffers: shared hit=317
  ->  Sort  (cost=996.69..1003.86 rows=2867 width=301) (actual time=5.539..5.566 rows=476 loops=1)
        Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
        Sort Method: quicksort  Memory: 173kB
        Buffers: shared hit=317
        ->  HashAggregate  (cost=803.38..832.05 rows=2867 width=301) (actual time=5.137..5.300 rows=476 loops=1)
              Group Key: questions_question.id, users_customuser.id
              Batches: 1  Memory Usage: 369kB
              Buffers: shared hit=317
              ->  Hash Right Join  (cost=457.57..781.88 rows=2867 width=301) (actual time=1.789..4.600 rows=1511 loops=1)
                    Hash Cond: (questions_question_tag.question_id = questions_question.id)
                    Buffers: shared hit=317
                    ->  Seq Scan on questions_question_tag  (cost=0.00..240.64 rows=14664 width=16) (actual time=0.005..1.012 rows=14664 loops=1)
                          Buffers: shared hit=94
                    ->  Hash  (cost=445.34..445.34 rows=978 width=293) (actual time=1.776..1.778 rows=476 loops=1)
                          Buckets: 1024  Batches: 1  Memory Usage: 157kB
                          Buffers: shared hit=223
                          ->  Nested Loop  (cost=228.58..445.34 rows=978 width=293) (actual time=0.319..1.545 rows=476 loops=1)
                                Join Filter: (users_customuser.id = questions_question.author_id)
                                Buffers: shared hit=223
                                ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.004..0.005 rows=1 loops=1)
                                      Buffers: shared hit=1
                                ->  Hash Join  (cost=228.58..432.11 rows=978 width=168) (actual time=0.312..1.465 rows=476 loops=1)
                                      Hash Cond: (questions_question.id = t4.question_id)
                                      Buffers: shared hit=222
                                      ->  Seq Scan on questions_question  (cost=0.00..175.00 rows=5000 width=168) (actual time=0.004..0.645 rows=5000 loops=1)
                                            Filter: (deleted_at IS NULL)
                                            Buffers: shared hit=125
                                      ->  Hash  (cost=216.35..216.35 rows=978 width=8) (actual time=0.303..0.304 rows=476 loops=1)
                                            Buckets: 1024  Batches: 1  Memory Usage: 27kB
                                            Buffers: shared hit=97
                                            ->  Nested Loop  (cost=8.07..216.35 rows=978 width=8) (actual time=0.047..0.245 rows=476 loops=1)
                                                  Buffers: shared hit=97
                                                  ->  Seq Scan on tags_tag t5  (cost=0.00..1.60 rows=2 width=8) (actual time=0.011..0.025 rows=1 loops=1)
                                                        Filter: ((upper((slug)::text) = 'KUBERNETES'::text) OR (upper((name)::text) = 'KUBERNETES'::text))
                                                        Rows Removed by Filter: 29
                                                        Buffers: shared hit=1
                                                  ->  Bitmap Heap Scan on questions_question_tag t4  (cost=8.07..102.49 rows=489 width=16) (actual time=0.032..0.174 rows=476 loops=1)
                                                        Recheck Cond: (tag_id = t5.id)
                                                        Heap Blocks: exact=94
                                                        Buffers: shared hit=96
                                                        ->  Bitmap Index Scan on questions_question_tag_tag_id_438f51e8  (cost=0.00..7.95 rows=489 width=0) (actual time=0.019..0.019 rows=476 loops=1)
                                                              Index Cond: (tag_id = t5.id)
                                                              Buffers: shared hit=2
Planning:
  Buffers: shared hit=40
Planning Time: 0.918 ms
Execution Time: 5.945 ms
```
### q=deadlock (legacy search box, LIMIT 50)
rows returned: 12; execution time: 35.953 ms
```
Limit  (cost=583.12..586.24 rows=50 width=301) (actual time=35.874..35.891 rows=12 loops=1)
  Buffers: shared hit=411
  ->  Unique  (cost=583.12..588.12 rows=80 width=301) (actual time=35.873..35.889 rows=12 loops=1)
        Buffers: shared hit=411
        ->  Sort  (cost=583.12..583.32 rows=80 width=301) (actual time=35.872..35.876 rows=12 loops=1)
              Sort Key: questions_question.created_at DESC, questions_question.id DESC, questions_question.updated_at, questions_question.deleted_at, questions_question.title, questions_question.description, questions_question.slug, questions_question.is_active, questions_question.author_id, (count(questions_question_tag.tag_id)), users_customuser.last_login, users_customuser.is_superuser, users_customuser.email, users_customuser.first_name, users_customuser.last_name, users_customuser.password, users_customuser.is_active, users_customuser.is_staff, users_customuser.avatar, users_customuser.preffered_language, users_customuser.timezone, users_customuser.created_at, users_customuser.updated_at, users_customuser.deleted_at
              Sort Method: quicksort  Memory: 29kB
              Buffers: shared hit=411
              ->  GroupAggregate  (cost=578.99..580.59 rows=80 width=301) (actual time=35.828..35.862 rows=12 loops=1)
                    Group Key: questions_question.id, users_customuser.id
                    Buffers: shared hit=411
                    ->  Sort  (cost=578.99..579.19 rows=80 width=301) (actual time=35.818..35.826 rows=119 loops=1)
                          Sort Key: questions_question.id DESC, users_customuser.id
                          Sort Method: quicksort  Memory: 65kB
                          Buffers: shared hit=411
                          ->  Nested Loop Left Join  (cost=239.46..576.46 rows=80 width=301) (actual time=2.117..35.732 rows=119 loops=1)
                                Buffers: shared hit=411
                                ->  Nested Loop  (cost=239.18..563.67 rows=27 width=293) (actual time=2.099..35.565 rows=37 loops=1)
                                      Join Filter: (users_customuser.id = questions_question.author_id)
                                      Buffers: shared hit=221
                                      ->  Seq Scan on users_customuser  (cost=0.00..1.01 rows=1 width=125) (actual time=0.005..0.006 rows=1 loops=1)
                                            Buffers: shared hit=1
                                      ->  Hash Right Join  (cost=239.18..562.32 rows=27 width=168) (actual time=2.091..35.546 rows=37 loops=1)
                                            Hash Cond: (t4.question_id = questions_question.id)
                                            Filter: ((upper((questions_question.title)::text) ~~ '%DEADLOCK%'::text) OR (upper(questions_question.description) ~~ '%DEADLOCK%'::text) OR (upper((t5.name)::text) ~~ '%DEADLOCK%'::text))
                                            Rows Removed by Filter: 14627
                                            Buffers: shared hit=220
                                            ->  Hash Left Join  (cost=1.68..286.25 rows=14664 width=14) (actual time=0.032..3.839 rows=14664 loops=1)
                                                  Hash Cond: (t4.tag_id = t5.id)
                                                  Buffers: shared hit=95
                                                  ->  Seq Scan on questions_question_tag t4  (cost=0.00..240.64 rows=14664 width=16) (actual time=0.005..1.102 rows=14664 loops=1)
                                                        Buffers: shared hit=94
                                                  ->  Hash  (cost=1.30..1.30 rows=30 width=14) (actual time=0.023..0.023 rows=30 loops=1)
                                                        Buckets: 1024  Batches: 1  Memory Usage: 10kB
                                                        Buffers: shared hit=1
                                                        ->  Seq Scan on tags_tag t5  (cost=0.00..1.30 rows=30 width=14) (actual time=0.004..0.007 rows=30 loops=1)
                                                              Buffers: shared hit=1
                                            ->  Hash  (cost=175.00..175.00 rows=5000 width=168) (actual time=1.139..1.139 rows=5000 loops=1)
                                                  Buckets: 8192  Batches: 1  Memory Usage: 1063kB
                                                  Buffers: shared hit=125
                                                  ->  Seq Scan on questions_question  (cost=0.00..175.00 rows=5000 width=168) (actual time=0.004..0.673 rows=5000 loops=1)
                                                        Filter: (deleted_at IS NULL)
                                                        Buffers: shared hit=125
                                ->  Index Scan using questions_question_tag_question_id_4dda0a92 on questions_question_tag  (cost=0.29..0.44 rows=3 width=16) (actual time=0.002..0.004 rows=3 loops=37)
                                      Index Cond: (question_id = questions_question.id)
                                      Buffers: shared hit=190
Planning:
  Buffers: shared hit=72
Planning Time: 1.264 ms
Execution Time: 35.953 ms
```
