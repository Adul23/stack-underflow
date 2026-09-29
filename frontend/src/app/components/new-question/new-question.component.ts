import { Component, OnInit } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { QuestionsService } from 'src/app/services/questions.service';
import { ServiceService } from 'src/app/services/service.service';
import { Router } from "@angular/router";
import { Tags, Questions } from 'src/app/models';
import { JwtHelperService } from "@auth0/angular-jwt";

@Component({
  selector: 'app-new-question',
  templateUrl: './new-question.component.html',
  styleUrls: ['./new-question.component.css'],
})
export class NewQuestionComponent implements OnInit {

  tagInputs: string[] = [''];
  tagIds: number[] = [];

  question?: Questions;

  tags: Tags[] = [];

  saving = false;
  error = '';
  title = '';
  description = '';
  slug = '';

  tag!: number;
  newTagName = '';

  author!: number;

  title_empty = false;
  description_empty = false;
  tag_empty = false;

  isCompleted = false;

  tokenPayload: any;
  usernameFromToken?: number;

  constructor(
    private service: QuestionsService,
    private tagService: ServiceService,
    private router: Router,
    private jwtHelper: JwtHelperService
  ) {}

  ngOnInit(): void {

    this.getUsernameFromTokenDecoded();

    this.loadTags();

    if (this.usernameFromToken == undefined) {
      this.router.navigateByUrl('questions');
    }

  }

  loadTags(){
    this.tagService.getTags().subscribe((tags)=>{
      this.tags = tags;
    });
  }

  check() {

    this.title_empty = this.title.trim() === '';
    this.description_empty = this.description.trim() === '';

    this.tag_empty = this.tagInputs.length === 0;

    if (!this.title_empty && !this.description_empty) {
      this.isCompleted = true;
    }

  }

  recheck() {
    this.isCompleted = false;
  }

  async newquestion() {
    this.check();
    if (this.title_empty || this.description_empty || this.saving) return;
    this.saving = true;
    this.error = '';
    try {
      this.tagIds = [];
      const names = [...new Set(this.tagInputs.map(name => name.replace('#', '').trim().toLowerCase()).filter(Boolean))];
      for (const name of names) {
        let tag = this.tags.find(t => t.name.toLowerCase() === name);
        if (!tag) {
          tag = await firstValueFrom(this.tagService.createTag(name));
          this.tags.push(tag);
        }
        this.tagIds.push(tag.id);
      }
      this.question = {
        id: 0, title: this.title.trim(), description: this.description.trim(),
        slug: this.title, author: Number(this.usernameFromToken), tag: this.tagIds,
        created_at: new Date(), updated_at: new Date(), is_active: true
      };
      const created = await firstValueFrom(this.service.addQuestion(this.question));
      this.router.navigate(['/questions', created.slug]);
    } catch (error) {
      this.error = 'Could not save the question. Check your login and try again.';
    } finally {
      this.saving = false;
    }
  }

  addTag() {
  this.tagInputs.push('');
  }

  createTag() {

    if (!this.newTagName) return;

    this.tagService.createTag(this.newTagName).subscribe(tag => {

      console.log("Tag created:", tag);

      this.tags.push(tag);

      this.tag = tag.id;

      this.newTagName = '';

    });

  }

  trackByIndex(index: number): number {
  return index;
}

  getUsernameFromTokenDecoded() {

    const token = localStorage.getItem('access');

    if (!token) return;

    const decoded = this.jwtHelper.decodeToken(token);



    this.usernameFromToken = decoded.user_id;

  }

}