import { Component, OnInit } from '@angular/core';
import { Users } from 'src/app/models';
import { ServiceService } from 'src/app/services/service.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css'],
})
export class UsersComponent implements OnInit {
  users: Users[] = [];
  constructor(private service: ServiceService) {}

  ngOnInit(): void {
    this.service.getUsers().subscribe((users) => (this.users = users));
  }
}
