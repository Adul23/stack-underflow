import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ServiceService } from '../../services/service.service';

@Component({
  selector: 'app-register',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  form!: FormGroup;  
  submitted = false;
  error: string = '';

  constructor(private fb: FormBuilder, private authService: ServiceService, private router: Router) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      firstname: ['', Validators.required],
      lastname: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8), Validators.maxLength(40)]],
      confirmPassword: ['', Validators.required]
    }, {
      validators: this.passwordsMatchValidator
    });
  }

  // Валидатор для проверки совпадения паролей
  passwordsMatchValidator(form: FormGroup) {
    const password = form.get('password')?.value;
    const confirm = form.get('confirmPassword')?.value;
    return password === confirm ? null : { matching: true };
  }

  // Удобный getter для шаблона
  get f() { return this.form.controls; }

  onSubmit() {
    this.submitted = true;

    if (this.form.invalid) {
      return;
    }

    const userData = {
      first_name: this.f['firstname'].value,
      last_name: this.f['lastname'].value,
      email: this.f['email'].value,
      password: this.f['password'].value
    };

    this.authService.register(userData).subscribe({
      next: (res) => {
        // регистрация успешна, редирект
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.error = err.error?.detail || JSON.stringify(err.error) || 'Registration failed';
      }
    });
  }

  onReset() {
    this.submitted = false;
    this.form.reset();
  }
}