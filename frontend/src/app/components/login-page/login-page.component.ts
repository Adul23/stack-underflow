import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/services/service.service';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit {

  email='';
  password='';
  logged=false;
  error=false;

  constructor(private _service:ServiceService,
              private location:Location,
              private router: Router) { }

  ngOnInit(): void {
  const access = localStorage.getItem('access');
  if (access) {
    this.logged = true;
    this.router.navigateByUrl('/questions');  // <-- слэш
  }
}

login() {
  this.error = false;

  this._service.login(this.email, this.password).subscribe(
    (data: any) => {
      localStorage.setItem('access', data.access);
      if (data.refresh) localStorage.setItem('refresh', data.refresh);

      this.logged = true;
      this.router.navigateByUrl('/questions'); // <-- слэш

      this.email = '';
      this.password = '';
    },
    (err) => {
      this.error = true;
      console.log(err);
    }
  );
}

}