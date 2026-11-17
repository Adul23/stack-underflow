import { fakeAsync, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { QuestionsComponent } from './questions.component';
import { QuestionsService } from '../../services/questions.service';
import { ServiceService } from '../../services/service.service';

describe('Questions search', () => {
  let component: QuestionsComponent;
  let service: jasmine.SpyObj<QuestionsService>;

  beforeEach(() => {
    service = jasmine.createSpyObj('QuestionsService', ['getQuestions', 'searchQuestions']);
    service.getQuestions.and.returnValue(of([]));
    service.searchQuestions.and.returnValue(of([]));
    const tags = jasmine.createSpyObj('ServiceService', ['getTags']);
    tags.getTags.and.returnValue(of([{ id: 7, name: 'Python', slug: 'python' }]));
    component = new QuestionsComponent(service, tags as ServiceService);
    component.ngOnInit();
    service.getQuestions.calls.reset();
    service.searchQuestions.calls.reset();
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
    expect(service.searchQuestions).toHaveBeenCalledOnceWith(' python ', '');
    expect(service.getQuestions).not.toHaveBeenCalled();
  }));

  it('loads the full list when there is no keyword or tag', () => {
    component.search();
    expect(service.getQuestions).toHaveBeenCalledOnceWith();
    expect(service.searchQuestions).not.toHaveBeenCalled();
  });

  it('combines keyword and selected tag in one search request', () => {
    const results = [{ id: 1, title: 'Django serializers', tag: [7] } as any];
    service.searchQuestions.and.returnValue(of(results));
    component.query = 'django';
    component.selectedTag = 'python';
    component.search();
    expect(service.searchQuestions).toHaveBeenCalledOnceWith('django', 'python');
    expect(component.filteredQuestions).toEqual(results);
  });

  it('filters by a tag chip using the tag slug', () => {
    component.filterByTag(7);
    expect(component.selectedTag).toBe('python');
    expect(service.searchQuestions).toHaveBeenCalledOnceWith('', 'python');
  });

  it('clear resets keyword and tag and reloads the full list', () => {
    component.query = 'django';
    component.selectedTag = 'python';
    component.clearFilters();
    expect(component.query).toBe('');
    expect(component.selectedTag).toBe('');
    expect(service.getQuestions).toHaveBeenCalledOnceWith();
  });
});
