import { environment } from '../../environments/environment';
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
  private base_url = `${environment.apiUrl}/questions`;

  constructor(private http: HttpClient, private router: Router) {
  }

  getQuestions(query = '', suggest = false): Observable<Questions[]> {
    return this.http.get<Questions[]>(`${this.base_url}/list`, { params: { q: query, suggest: suggest ? '1' : '0' } });
  }

  getQuestion(slug: string): Observable<QuestionDetailResponse> {
    return this.http.get<QuestionDetailResponse>(`${this.base_url}/${slug}/retrieve`);
  }

  deleteQuestion(slug: string): Observable<any> {
    return this.http.delete(`${this.base_url}/${slug}/destroy`);
  }

  updateQuestion(slug: string, data: any) {
    return this.http.patch<Questions>(
      `${this.base_url}/${slug}/update`,
      data
    );
  }

  addQuestion(question: Questions): Observable<Questions> {
    return this.http.post<Questions>(`${this.base_url}/create`, question);
  }

  editComment(id : number, data : any) {
    return this.http.patch<Comment>(
      `${environment.apiUrl}/comments/${id}/update`,
      data
    )
  }

  getQuestionsByAuthor(userId: number): Observable<Questions[]> {
    return this.http.get<Questions[]>(
      `${environment.apiUrl}/questions/list_by_author?author=${userId}`
    );
  }

  getCommentsByAuthor(userId: number): Observable<Comments[]> {
    return this.http.get<Comments[]>(`${environment.apiUrl}/comments/list_by_author?author=${userId}`);
  }
}
