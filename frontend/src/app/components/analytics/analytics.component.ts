import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

interface Summary {
  totals: { question_view: number; question_create: number; search: number };
  top_questions: { question_id: number; title: string; slug: string; views: number }[];
}

@Component({
  selector: 'app-analytics',
  template: `
    <section class="py-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div><h1>Activity dashboard</h1><p class="text-muted">All-time activity · Administrators only</p></div>
        <button class="btn btn-outline-primary" (click)="load()" [disabled]="loading">Refresh</button>
      </div>
      <p *ngIf="loading" role="status">Loading analytics…</p>
      <p *ngIf="error" class="alert alert-warning" role="alert">{{ error }}</p>
      <ng-container *ngIf="summary as data">
        <div class="row g-3 mb-4">
          <div class="col-md-4" *ngFor="let metric of metrics">
            <div class="card h-100"><div class="card-body">
              <h2 class="h6 text-muted">{{ metric.label }}</h2>
              <strong class="display-5">{{ data.totals[metric.key] | number }}</strong>
            </div></div>
          </div>
        </div>
        <h2 class="h4">Top 5 viewed questions</h2>
        <p *ngIf="!data.top_questions.length">No question views yet. Open a question and refresh.</p>
        <div class="table-responsive" *ngIf="data.top_questions.length">
          <table class="table"><thead><tr><th>Question</th><th>Views</th><th>Relative views</th></tr></thead>
            <tbody><tr *ngFor="let question of data.top_questions">
              <td><a [routerLink]="['/questions', question.slug]">{{ question.title }}</a></td>
              <td>{{ question.views | number }}</td>
              <td><progress [value]="question.views" [max]="data.top_questions[0].views" [attr.aria-label]="question.title"></progress></td>
            </tr></tbody>
          </table>
        </div>
        <p class="text-muted small">Reloading a question counts as another view. Demo events, when seeded, are included.</p>
      </ng-container>
    </section>`
})
export class AnalyticsComponent implements OnInit {
  summary: Summary | null = null;
  loading = false;
  error = '';
  metrics: {key: keyof Summary['totals']; label: string}[] = [
    {key: 'question_view', label: 'Question views'},
    {key: 'question_create', label: 'Questions created'},
    {key: 'search', label: 'Searches'}
  ];
  constructor(private http: HttpClient) {}
  ngOnInit(): void { this.load(); }
  load(): void {
    this.loading = true;
    this.error = '';
    this.summary = null;
    this.http.get<Summary>(environment.apiUrl + '/analytics/summary/').subscribe({
      next: data => { this.summary = data; this.loading = false; },
      error: err => {
        this.loading = false;
        this.error = err.status === 401 || err.status === 403
          ? 'Sign in with an administrator account to view analytics.'
          : 'Could not load analytics. Check the API and try again.';
      }
    });
  }
}
