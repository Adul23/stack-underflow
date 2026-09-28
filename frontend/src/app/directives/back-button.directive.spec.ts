import { BackButtonDirective } from './back-button.directive';

describe('BackButtonDirective', () => {
  it('should create an instance', () => {
    const directive = new BackButtonDirective(jasmine.createSpyObj('NavigationService', ['back']));
    expect(directive).toBeTruthy();
  });
});
