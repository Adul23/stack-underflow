import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Questions, Tags, Users, Comments, QuestionDetailResponse } from 'src/app/models';
import { QuestionsService } from 'src/app/services/questions.service';
import { ServiceService } from 'src/app/services/service.service';
import { JwtHelperService } from "@auth0/angular-jwt";


@Component({
  selector: 'app-question-detail',
  templateUrl: './question-detail.component.html',
  styleUrls: ['./question-detail.component.css']
})

export class QuestionDetailComponent implements OnInit {

  question?: Questions;
  comments: Comments[] = [];
  tags: Tags[] = [];
  tagsForQuestion: Tags[] = [];
  user?: Users;
  isAuthor: boolean = false;

  commentText: string = "";
  isAuthenticated: boolean = false;

  
  tokenPayload: any;
  usernameFromToken?: number;

  editingCommentId: number | null = null;
  editedCommentText: string = ""; 

  constructor(
    private route: ActivatedRoute,
    private questionService: QuestionsService,
    private tagService: ServiceService,
    private jwtHelper: JwtHelperService
  ) {}

  ngOnInit(): void {
    this.getUsernameFromTokenDecoded();

    const token = localStorage.getItem("access");
    if (token) {
      const helper = new JwtHelperService();
      this.isAuthenticated = !helper.isTokenExpired(token);
    }

    const slug = this.route.snapshot.paramMap.get('slug');
    if (!slug) return;

    this.questionService.getQuestion(slug).subscribe((response: QuestionDetailResponse) => {
      const q = response.question;
      this.question = q;
      this.comments = response.comments;

      this.tagService.getTags().subscribe(tags => {
        this.tags = tags;
        this.tagsForQuestion = tags.filter(tag => q.tag.includes(tag.id));
      });


      if (Number(this.usernameFromToken) === q.author) {
        this.isAuthor = true;
      }
    });
  }

  

  postComment() {
    if (!this.commentText.trim()) return;

    const slug = this.route.snapshot.paramMap.get('slug');

    const data = {
      text: this.commentText,
      author: Number(this.usernameFromToken),
      question: this.question?.id
    };

    this.tagService.addComment(slug!, data).subscribe(res => {
      this.comments.push(res);
      this.commentText = "";
    });
  }

  getUsernameFromTokenDecoded() {

    const token = localStorage.getItem('access');

    if (!token) return;

    const decoded = this.jwtHelper.decodeToken(token);


    this.usernameFromToken = decoded.user_id;


  }

  startEditComment(comment: Comments) {
    if (Number(this.usernameFromToken) !== Number(comment.author)) return;
    this.editingCommentId = comment.id;
    this.editedCommentText = comment.text;
  }

saveEditComment(comment: Comments) {
  if (!this.editedCommentText.trim()) return;

  const data = { text: this.editedCommentText };

  this.questionService.editComment(comment.id, data).subscribe({
    next: (updated) => {
      const index = this.comments.findIndex(c => c.id === comment.id);
      if (index !== -1) this.comments[index].text = this.editedCommentText;

      this.editingCommentId = null;
      this.editedCommentText = "";
    },
    error: (err) => console.error(err)
  });
}

cancelEditComment() {
  this.editingCommentId = null;
  this.editedCommentText = "";
}
getTagName(tagId: number): string {
  return this.tags.find(t => t.id === tagId)?.name ?? '';
}
}