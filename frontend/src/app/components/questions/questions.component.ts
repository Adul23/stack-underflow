import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subject, of, timer } from 'rxjs';
import { catchError, switchMap, takeUntil } from 'rxjs/operators';
import { Questions, Tags } from 'src/app/models';
import { QuestionsService } from 'src/app/services/questions.service';
import { ServiceService } from 'src/app/services/service.service';

@Component({
  selector: 'app-questions',
  templateUrl: './questions.component.html',
  styleUrls: ['./questions.component.css'],
})
export class QuestionsComponent implements OnInit, OnDestroy {
  query = '';
  loading = false;
  error = '';
  filteredQuestions: Questions[] = [];
  suggestions: Questions[] = [];
  tags: Tags[] = [];
  private input = new Subject<string>();
  private destroyed = new Subject<void>();

  constructor(private service: QuestionsService, private tagService: ServiceService) {}

  ngOnInit(): void {
    this.tagService.getTags().pipe(takeUntil(this.destroyed)).subscribe(tags => this.tags = tags);
    // Cancel the previous timer/request as soon as the input changes.
    this.input.pipe(
      switchMap(query => query.trim() ? timer(300).pipe(
        switchMap(() => this.service.getQuestions(query.trim(), true)),
        catchError(() => of([]))
      ) : of([])),
      takeUntil(this.destroyed)
    ).subscribe(questions => this.suggestions = questions);
    this.search();
  }

  onQueryChange(value: string) {
    this.suggestions = [];
    this.input.next(value);
  }

  search() {
    this.input.next('');
    this.loading = true;
    this.error = '';
    this.service.getQuestions(this.query.trim()).pipe(takeUntil(this.destroyed)).subscribe({
      next: questions => {
        this.filteredQuestions = questions;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load questions. Please try again.';
        this.loading = false;
      }
    });
  }

  getTagName(tagId: number): string {
    return this.tags.find(t => t.id === tagId)?.name ?? '';
  }

  ngOnDestroy() {
    this.destroyed.next();
    this.destroyed.complete();
  }
}
