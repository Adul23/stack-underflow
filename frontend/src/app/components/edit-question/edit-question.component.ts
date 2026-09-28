import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { QuestionsService } from 'src/app/services/questions.service';
import { ServiceService } from 'src/app/services/service.service';
import { Users, Questions, Tags } from 'src/app/models';
import { JwtHelperService } from "@auth0/angular-jwt";

@Component({
  selector: 'app-edit-question',
  templateUrl: './edit-question.component.html',
  styleUrls: ['./edit-question.component.css']
})
export class EditQuestionComponent implements OnInit {

  question?: Questions;
  id = 0;
  title = '';
  description = '';
  isActive: boolean = true;
  isCompleted = false;

  tagInputs: string[] = [''];  // ✅ как в new-question

  title_empty = false;
  description_empty = false;
  tag_empty = false;

  usernameFromToken?: string;

  constructor(
    private route: ActivatedRoute,
    private service: QuestionsService,
    private tagService: ServiceService,
    private router: Router,
    private jwtHelper: JwtHelperService
  ) {}

  ngOnInit(): void {
    const slug = this.route.snapshot.paramMap.get('slug');
    if (!slug) {
      this.router.navigateByUrl('/questions');
      return;
    }

    this.getTokenDecoded();

    this.service.getQuestion(slug).subscribe((response) => {
      const question = response.question;
      this.question = question;
      this.id = question.id;
      this.title = question.title;
      this.description = question.description;
      this.isActive = question.is_active;

      // ✅ загружаем существующие теги как строки
      this.tagService.getTags().subscribe((tags) => {
        const questionTags = tags
          .filter(t => question.tag.includes(t.id))
          .map(t => t.name);

        this.tagInputs = questionTags.length > 0 ? questionTags : [''];
      });
    });
  }

  addTag() {
    this.tagInputs.push('');
  }

  trackByIndex(index: number) {
    return index;
  }

  check() {
    this.title_empty = this.title.trim() === '';
    this.description_empty = this.description.trim() === '';
    this.tag_empty = this.tagInputs.every(t => t.trim() === '');

    this.isCompleted =
      !this.title_empty &&
      !this.description_empty &&
      !this.tag_empty;
  }

  recheck() {
    this.isCompleted = false;
  }

  editquestion() {
    if (!this.question) return;

    const oldSlug = this.question.slug;

    // ✅ создаём/находим теги как в new-question
    const tagNames = this.tagInputs
      .map(t => t.replace('#', '').trim())
      .filter(t => t !== '');

    const tagRequests = tagNames.map(name =>
      this.tagService.createTag(name).toPromise()
    );

    Promise.all(tagRequests).then(createdTags => {
      const tagIds = createdTags
        .filter(t => t !== undefined)
        .map(t => t!.id);

      const updatedQuestion: Partial<Questions> = {
        title: this.title,
        description: this.description,
        tag: tagIds,
        is_active: this.isActive
      };

      this.service.updateQuestion(oldSlug, updatedQuestion).subscribe(
        () => this.router.navigateByUrl('/questions'),
        (err) => console.error(err)
      );
    });
  }

  getTokenDecoded() {
    const token = localStorage.getItem('access');
    if (token) {
      const payload = this.jwtHelper.decodeToken(token);
      this.usernameFromToken = payload.user;
    }
  }
}