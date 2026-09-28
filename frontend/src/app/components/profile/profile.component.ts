import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServiceService } from 'src/app/services/service.service';
import { JwtHelperService } from '@auth0/angular-jwt';
import { Users } from 'src/app/models';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  user?: Users;
  isOwner: boolean = true;

  constructor(
    private service: ServiceService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.service.myProfile().subscribe(user => {
      this.user = user;
    });
  }

  editProfile() {
    this.router.navigate(['/profile/edit']);
  }

  logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    this.router.navigate(['/login']);
  }
}