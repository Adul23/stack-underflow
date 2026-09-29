import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { QuestionsComponent } from './questions.component';
import { QuestionsService } from '../../services/questions.service';
import { ServiceService } from '../../services/service.service';

describe('Questions search', () => {
  let component: QuestionsComponent;
  let service: jasmine.SpyObj<QuestionsService>;

  beforeEach(() => {
    service = jasmine.createSpyObj('QuestionsService', ['getQuestions']);
    service.getQuestions.and.returnValue(of([]));
    const tags = jasmine.createSpyObj('ServiceService', ['getTags']);
    tags.getTags.and.returnValue(of([]));
    component = new QuestionsComponent(service, tags as ServiceService);
    component.ngOnInit();
    service.getQuestions.calls.reset();
  });

  afterEach(() => component.ngOnDestroy());

  it('waits 300 ms and requests only the latest typed query', fakeAsync(() => {
    component.onQueryChange('d');
    tick(200);
    component.onQueryChange('django');
    tick(299);
    expect(service.getQuestions).not.toHaveBeenCalled();
    tick(1);
    expect(service.getQuestions).toHaveBeenCalledOnceWith('django', true);
  }));

  it('ignores a stale response after clearing the input', fakeAsync(() => {
    const pending = new Subject<any[]>();
    service.getQuestions.and.returnValue(pending);
    component.onQueryChange('python');
    tick(300);
    component.onQueryChange('');
    pending.next([{ title: 'Old result' }]);
    expect(component.suggestions).toEqual([]);
  }));

  it('submits the full search without also sending a pending suggestion', fakeAsync(() => {
    component.query = ' python ';
    component.onQueryChange(component.query);
    component.search();
    tick(500);
    expect(service.getQuestions).toHaveBeenCalledOnceWith('python');
  }));
});
