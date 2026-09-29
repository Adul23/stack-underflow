import { environment } from '../../environments/environment';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { JwtHelperService } from "@auth0/angular-jwt";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthToken } from '../models';
import { Router } from "@angular/router";
import { Tags, TagDetailResponse,Comments, Users, } from '../models';

const helper = new JwtHelperService();

@Injectable({
  providedIn: 'root',
})

export class ServiceService {
  private base_url = `${environment.apiUrl}/`;

  constructor(private http: HttpClient, private router: Router) {
  }

  getTags(): Observable<Tags[]> {
    return this.http.get<Tags[]>(`${this.base_url}tags/list`);
  }

  // getTag(id: number): Observable<Tags> {
  //   return this.http.get<Tags>(`${this.base_url}/tags/${id}/`);
  // }

  getTag(name: string): Observable<TagDetailResponse> {
    return this.http.get<TagDetailResponse>(`${this.base_url}tags/${name}/retrieve`);
  }

  createTag(name: string): Observable<Tags> {
    return this.http.post<Tags>(`${this.base_url}tags/create`, {
      name: name
    });
  }


  addComment(slug : string, data: any): Observable<Comments> {
    return this.http.post<Comments>(`${this.base_url}questions/${slug}/create_comment`, data)
  }

  // Legacy screens are not routed in the MVP; their backend APIs never existed.
  getUsers(): Observable<Users[]> {
    return throwError(() => new Error('User directory is outside the MVP.'));
  }

  getUser(id: number): Observable<Users> {
    return throwError(() => new Error('User profiles are outside the MVP.'));
  }

  login(email: string, password: string) {
    return this.http.post<any>(`${this.base_url}users/login`, {
      email: email,
      password: password
    });
  }

  register(data: any): Observable<Users> {
    return this.http.post<Users>(`${this.base_url}users/register`, data)
  }

  changePassword(data: any): Observable<null> {
    return throwError(() => new Error('Password management is outside the MVP.'));
  }

  myProfile(): Observable<Users> {
    return throwError(() => new Error('User profiles are outside the MVP.'));
  }

  isExpiredToken(token: string | null): boolean {
    if (!token) {
      token = localStorage.getItem('access');
    }
    if (!token) {
      return true;
    }

    const date = helper.getTokenExpirationDate(token);

    if (date === undefined) return false;
    if (date) {
      return !(date.valueOf() > new Date().valueOf());
    }
    return true;
  }

}
