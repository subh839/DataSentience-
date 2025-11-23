import { Component } from '@angular/core';
import { AnalyzerComponent } from './components/analyzer/analyzer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [AnalyzerComponent],
  template: `
    <app-analyzer></app-analyzer>
  `,
  styles: []
})
export class AppComponent {
  title = 'datasentience-frontend';
}