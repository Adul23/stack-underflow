import { Injectable } from '@angular/core';
import { QuestionDetailResponse, Questions, Comments } from '../models';
import { Observable, of } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { JwtHelperService } from "@auth0/angular-jwt";
import { Router } from "@angular/router";

let helper = new JwtHelperService()

@Injectable({
  providedIn: 'root',
})
export class QuestionsService {
  private base_url='http://127.0.0.1:8000/api/questions';

  constructor(private http: HttpClient, private router: Router) {
  }

  getQuestions(query = ''): Observable<Questions[]> {
    return this.http.get<Questions[]>(`${this.base_url}/list`, { params: { q: query } });
  }

  getQuestion(slug: string): Observable<QuestionDetailResponse> {
    return this.http.get<QuestionDetailResponse>(`${this.base_url}/${slug}/retrieve`);
  }

  deleteQuestion(slug: string): Observable<any> {
    return this.http.delete(`${this.base_url}/${slug}/delete`);
  }

  updateQuestion(slug: string, data: any) {
    return this.http.patch<Questions>(
      `http://127.0.0.1:8000/api/questions/${slug}/update`,
      data
    );
  }

  addQuestion(question: Questions): Observable<Questions> {
    return this.http.post<Questions>(`${this.base_url}/create`, question);
  }

  editComment(id : number, data : any) {
    return this.http.patch<Comment>(
      `http://127.0.0.1:8000/api/comments/${id}/update`,
      data
    )
  }

  getQuestionsByAuthor(userId: number): Observable<Questions[]> {
    return this.http.get<Questions[]>(
      `http://127.0.0.1:8000/api/questions/list_by_author?author=${userId}`
    );
  }

  getCommentsByAuthor(userId: number): Observable<Comments[]> {
    return this.http.get<Comments[]>(`http://127.0.0.1:8000/api/comments/list_by_author?author=${userId}`);
  }
}
