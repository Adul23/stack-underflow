import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AuthInterceptor } from './AuthInterceptor';

import {JWT_OPTIONS, JwtHelperService} from "@auth0/angular-jwt";
import { AuthGuardService } from "./services/auth-guard.service";

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { QuestionsComponent } from './components/questions/questions.component';
import { QuestionDetailComponent } from './components/question-detail/question-detail.component';
import { UserPageComponent } from './components/user-page/user-page.component';
import { NotFoundPageComponent } from './components/not-found-page/not-found-page.component';
import { AboutComponent } from './components/about/about.component';
import { TagsComponent } from './components/tags/tags.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { TagDetailComponent } from './components/tag-detail/tag-detail.component';
import { BackButtonDirective } from './directives/back-button.directive';
import { UsersComponent } from './components/users/users.component';
import { NewQuestionComponent } from './components/new-question/new-question.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { EditQuestionComponent } from './components/edit-question/edit-question.component';
import { PasswordChangeComponent } from './components/password-change/password-change.component';
import { ProfileComponent } from './components/profile/profile.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    QuestionsComponent,
    QuestionDetailComponent,
    UserPageComponent,
    NotFoundPageComponent,
    AboutComponent,
    TagsComponent,
    LoginPageComponent,
    TagDetailComponent,
    BackButtonDirective,
    UsersComponent,
    NewQuestionComponent,
    UsersComponent,
    SignUpComponent,
    EditQuestionComponent,
    PasswordChangeComponent,
    ProfileComponent,
  ],
  imports: [BrowserModule, AppRoutingModule, FormsModule, HttpClientModule, ReactiveFormsModule],
  providers: [
    {
      provide:HTTP_INTERCEPTORS,
      useClass:AuthInterceptor,
      multi:true
    },
    { provide: JWT_OPTIONS, useValue: JWT_OPTIONS }, JwtHelperService
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
