import { Component, OnInit } from '@angular/core';
import { Questions, Tags } from 'src/app/models';
import { QuestionsService } from 'src/app/services/questions.service';
import { ServiceService } from 'src/app/services/service.service';

@Component({
  selector: 'app-questions',
  templateUrl: './questions.component.html',
  styleUrls: ['./questions.component.css'],
})
export class QuestionsComponent implements OnInit {
  query = '';
  loading = false;
  error = '';
  logged=false;
  alertF=false;
  activeTab: 'active' | 'archive' = 'active';
  filteredQuestions: Questions[] = [];
  questions: Questions[] = [];
  tags: Tags[] = [];

  constructor(private service: QuestionsService,
    private tagService: ServiceService
  ) {}

  ngOnInit(): void {

    this.tagService.getTags().subscribe(tags => {
    this.tags = tags;
  });

    const access=localStorage.getItem('access');
    if (access) this.logged=true;

    this.search();
  }

  search() {
    this.loading = true;
    this.error = '';
    this.service.getQuestions(this.query.trim()).subscribe({
      next: questions => {
        this.questions = questions.sort((a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        this.filteredQuestions = this.questions;
        this.loading = false;
      },
      error: () => {
        this.error = 'Could not load questions. Please try again.';
        this.loading = false;
      }
    });
  }

  alert(){
    this.alertF=true;
  }



  setTab(tab: 'active' | 'archive') {
  this.activeTab = tab;
  this.applyFilter();
  }

  applyFilter() {
    this.filteredQuestions = this.activeTab === 'active'
      ? this.questions.filter(q => q.is_active)
      : this.questions.filter(q => !q.is_active);
  }

getTagName(tagId: number): string {
  return this.tags.find(t => t.id === tagId)?.name ?? '';
}
}

