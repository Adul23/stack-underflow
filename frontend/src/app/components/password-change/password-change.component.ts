import { Component, OnInit } from '@angular/core';
import { ServiceService } from 'src/app/services/service.service';
import { Location } from "@angular/common";

@Component({
  selector: 'app-password-change',
  templateUrl: './password-change.component.html',
  styleUrls: ['./password-change.component.css']
})
export class PasswordChangeComponent implements OnInit {

  old_password = '';
  password = '';
  password2 = '';

  isCompleted = false;
  oldEmpty = false;
  new1Empty = false;
  new2Empty = false;
  same = true;

  constructor(
    private _service: ServiceService,
    public _location: Location
  ) { }

  ngOnInit(): void {
    // Stripped out the broken URL parameter checks that were crashing the page.
  }

  check() {
    this.oldEmpty = this.old_password === '';
    this.new1Empty = this.password === '';
    this.new2Empty = this.password2 === '';
    this.same = this.password === this.password2;

    if (!this.oldEmpty && !this.new1Empty && !this.new2Empty && this.same) {
      this.isCompleted = true;
    }
  }

  recheck() {
    this.isCompleted = false;
  }

  changePassword() {
    const data = {
      old_password: this.old_password,
      new_password: this.password // Matches Django backend
    };

    this._service.changePassword(data).subscribe({
      next: () => {
        alert('Password changed successfully!');
        this._location.back();
      },
      error: (err) => {
        alert(err.error?.old_password || 'Failed to change password. Check your old password.');
        this.isCompleted = false;
      }
    });
  }
}