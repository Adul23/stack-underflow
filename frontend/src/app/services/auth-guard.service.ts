import { Injectable } from '@angular/core';
import {
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
} from '@angular/router';
import { ServiceService } from 'src/app/services/service.service';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class AuthGuardService {

  constructor(private router: Router, private service: ServiceService) { }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> | Promise<boolean> | boolean {
    if (!this.service.isExpiredToken(null)) {
      return true;
    } else {
      localStorage.removeItem('access');
      alert('you must log in to view this page');

      // location.reload();
    }

    this.router.navigate(['/login']).then();
    return true;
  }

}
