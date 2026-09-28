import { Component, OnInit } from '@angular/core';
import { Tags } from 'src/app/models';
import { ServiceService } from 'src/app/services/service.service';

@Component({
  selector: 'app-tags',
  templateUrl: './tags.component.html',
  styleUrls: ['./tags.component.css'],
})
export class TagsComponent implements OnInit {
  tags: Tags[] | undefined;
  constructor(private service: ServiceService) {}

  ngOnInit(): void {
    this.service.getTags().subscribe((tags) => (this.tags = tags));
  }
}
