import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'STACK UNDERFLOW';
  logged = false;

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.logged = !!localStorage.getItem('access');
      }
    });
  }

  goToPage(page: string) {
    this.router.navigate([`${page}`]);
  }

  logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    this.logged = false;
    this.router.navigateByUrl('questions');
  }
}