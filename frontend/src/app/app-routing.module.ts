import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuardService } from "./services/auth-guard.service";

import { HomeComponent } from './components/home/home.component';
import { QuestionsComponent } from './components/questions/questions.component';
import { QuestionDetailComponent } from './components/question-detail/question-detail.component';
import { NotFoundPageComponent } from './components/not-found-page/not-found-page.component';
import { UserPageComponent } from './components/user-page/user-page.component';
import { AboutComponent } from './components/about/about.component';
import { TagsComponent } from './components/tags/tags.component';
import { LoginPageComponent } from './components/login-page/login-page.component';
import { TagDetailComponent } from './components/tag-detail/tag-detail.component';
import { UsersComponent } from './components/users/users.component';
import { NewQuestionComponent } from './components/new-question/new-question.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { EditQuestionComponent } from './components/edit-question/edit-question.component';
import { PasswordChangeComponent } from './components/password-change/password-change.component';
import { ProfileComponent } from './components/profile/profile.component';

const routes: Routes = [
  { path: 'home', component: HomeComponent },
  { path: 'questions', component: QuestionsComponent },
  { path: 'questions/:slug', component: QuestionDetailComponent },
  { path: 'questions/edit/:slug', component: EditQuestionComponent, canActivate: [AuthGuardService], },
  { path: 'tags', component: TagsComponent },
  { path: 'tags/:slug', component: TagDetailComponent },
  { path: 'login', component: LoginPageComponent },
  { path: 'signup', component: SignUpComponent },
  { path: 'users/:id', component: UserPageComponent, },
  { path: 'users/:username/change_password', component: PasswordChangeComponent, canActivate: [AuthGuardService], },
  { path: 'users', component: UsersComponent },
   {path: 'profile', component : ProfileComponent, canActivate : [AuthGuardService]},
  { path: 'about', component: AboutComponent },
  { path: 'newquestion', component: NewQuestionComponent, canActivate: [AuthGuardService], },
  { path: 'profile/edit', component: PasswordChangeComponent, canActivate: [AuthGuardService] },
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', component: NotFoundPageComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
