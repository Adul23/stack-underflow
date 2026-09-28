import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Tags,Questions } from 'src/app/models';

import { ServiceService } from 'src/app/services/service.service';
import { QuestionsService } from 'src/app/services/questions.service';

@Component({
  selector: 'app-tag-detail',
  templateUrl: './tag-detail.component.html',
  styleUrls: ['./tag-detail.component.css'],
})
export class TagDetailComponent implements OnInit {
  tag: Tags | undefined;
  questions: Questions[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: ServiceService,
    private questionService: QuestionsService
  ) {}

  ngOnInit(): void {
    const routeParams = this.route.snapshot.paramMap;
    const tagNameFromRoute = String(routeParams.get('slug'));
    this.service.getTag(tagNameFromRoute).subscribe(
      (response) => {
        this.tag = response.tag;
        this.questions = response.questions        
      },
      (error) => {
        this.router.navigateByUrl(`notagfound`);
      }
    );
  }
}
