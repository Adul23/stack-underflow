import { environment } from '../environments/environment';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable, throwError } from "rxjs";
import { catchError, switchMap } from "rxjs/operators";
import { HttpClient } from "@angular/common/http";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private http: HttpClient) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!req.url.startsWith(environment.apiUrl + '/')) return next.handle(req);
    let sessionId = sessionStorage.getItem('analytics_session');
    if (!sessionId) {
      sessionId = crypto.randomUUID();
      sessionStorage.setItem('analytics_session', sessionId);
    }
    req = req.clone({ setHeaders: { 'X-Session-ID': sessionId } });
    if (req.url.endsWith('/users/login') || req.url.endsWith('/users/register') || req.url.endsWith('/users/token/refresh')) {
      return next.handle(req);
    }
    const access = localStorage.getItem('access');

    const authReq = access
      ? req.clone({ headers: req.headers.set('Authorization', `Bearer ${access}`) })
      : req;

    return next.handle(authReq).pipe(
      catchError(err => {
        if (err.status === 401) {
          const refresh = localStorage.getItem('refresh');
          if (!refresh) return throwError(() => err);

          return this.http.post<any>(`${environment.apiUrl}/users/token/refresh`, { refresh }).pipe(
            switchMap(tokens => {
              localStorage.setItem('access', tokens.access);

              const retryReq = req.clone({
                headers: req.headers.set('Authorization', `Bearer ${tokens.access}`)
              });
              return next.handle(retryReq);
            }),
            catchError(() => {
              localStorage.removeItem('access');
              localStorage.removeItem('refresh');
              return throwError(() => err);
            })
          );
        }
        return throwError(() => err);
      })
    );
  }
}