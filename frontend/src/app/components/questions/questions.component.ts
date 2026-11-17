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
  selectedTag = '';  // tag slug, '' = all tags
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

  get hasFilters(): boolean {
    return !!(this.query.trim() || this.selectedTag);
  }

  search() {
    this.input.next('');
    this.loading = true;
    this.error = '';
    // With a keyword or tag use the US-03 search API; otherwise load the full list.
    const request = this.hasFilters
      ? this.service.searchQuestions(this.query, this.selectedTag)
      : this.service.getQuestions();
    request.pipe(takeUntil(this.destroyed)).subscribe({
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

  filterByTag(tagId: number) {
    const slug = this.tags.find(t => t.id === tagId)?.slug;
    if (!slug) return;
    this.selectedTag = slug;
    this.search();
  }

  clearFilters() {
    this.query = '';
    this.selectedTag = '';
    this.search();
  }

  getTagName(tagId: number): string {
    return this.tags.find(t => t.id === tagId)?.name ?? '';
  }

  ngOnDestroy() {
    this.destroyed.next();
    this.destroyed.complete();
  }
}
