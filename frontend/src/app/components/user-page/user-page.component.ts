import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Users, Comments, Questions } from 'src/app/models';
import { JwtHelperService } from "@auth0/angular-jwt";
import { ServiceService } from 'src/app/services/service.service';
import { QuestionsService } from 'src/app/services/questions.service';

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.css'],
})

export class UserPageComponent implements OnInit {
  user: Users | undefined;
  userQuestions: Questions[] = [];
  userComments: Comments[] = [];
  activeTab: 'questions' | 'comments' = 'questions';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: ServiceService,
    private questionService: QuestionsService,
    private jwtHelper: JwtHelperService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));

    this.service.getUser(id).subscribe(user => {
      this.user = user;
    });

    this.questionService.getQuestionsByAuthor(id).subscribe(questions => {
      this.userQuestions = questions;
    });

    this.questionService.getCommentsByAuthor(id).subscribe(comments => {
      this.userComments = comments;
    });
  }

  setTab(tab: 'questions' | 'comments') {
    this.activeTab = tab;
  }

  back() {
    this.router.navigateByUrl('users');
  }
}